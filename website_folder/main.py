from flask import Flask, render_template, request
import reed_solomon as rsf
import unireedsolomon as rs

app = Flask(__name__)
transcoding = [chr(i + 97) for i in range(11)]
num_errors = 0
msg_length = 0


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/simple', methods=['POST', 'GET'])
def simple_transform():
    input_string = ''
    dna_string = ''
    output_string = ''
    if request.method == 'POST':
        if 'encode' in request.form:
            input_text = request.form['input_text']
            if len(input_text) > 200:
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=['checked', '', ''], dna_text=dna_string, user_message='Your message '
                                       'cannot be longer than 200 characters.', output_text=output_string)
            range_value = int(request.form['base'])
            checked_value = ['', '', '']
            checked_value[range_value - 2] = 'checked'
            dna_string = convert_unicode_to_dna(input_text, range_value)
            return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                   checked=checked_value, dna_text=dna_string, user_message='',
                                   output_text=output_string)
        elif 'decode' in request.form:
            range_value = int(request.form['base'])
            checked_value = ['', '', '']
            checked_value[range_value - 2] = 'checked'
            try:
                output_string = convert_dna_to_unicode(request.form['dna_text'], range_value)
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=checked_value, dna_text=dna_string, user_message='',
                                       output_text=output_string)
            except OverflowError:
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=['checked', '', ''], dna_text=dna_string,
                                       user_message='One or more of the values that you tried to decode fell outside of'
                                                    ' the Unicode bounds. Try using a shorter DNA value or encoding a'
                                                    ' different set of data.', output_text=output_string)
            except ValueError:
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=['checked', '', ''], dna_text=dna_string,
                                       user_message='One or more of the values that you tried to decode were not '
                                                    'accounted for based on your selected encoding method. Please try '
                                                    'again with a different set of data.', output_text=output_string)
            except Exception as e:
                print(e)
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=['checked', '', ''], dna_text=dna_string,
                                       user_message='There was an unknown error while decoding your DNA data. Please '
                                                    'try again with a different input.', output_text=output_string)
        elif 'clear' in request.form:
            input_string = dna_string = output_string = ''
            return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                   checked=['checked', '', ''], dna_text=dna_string, user_message='',
                                   output_text=output_string)
        else:
            pass
    else:
        return render_template('simple_transform.html', action='/simple', input_text=input_string,
                               checked=['checked', '', ''], dna_text=dna_string, user_message='',
                               output_text=output_string)


@app.route('/solomon', methods=['POST', 'GET'])
def reed_solomon_transform():
    global num_errors
    global msg_length
    if request.method == 'POST':
        if 'encode' in request.form:
            user_message = ''
            input_text = request.form['input_text']
            msg_length = len(input_text)
            if msg_length > 200:
                return render_template('solomon.html', action='/solomon', input_text='', error_text='', dna_text='',
                                       user_message='Your message cannot be longer than 200 characters.',
                                       output_text='')
            try:
                number_of_errors = int(request.form['error_choice'])
                if number_of_errors == 0:
                    user_message = 'The entered number of possible errors must be at least \'1\'.'
                    number_of_errors = 1
            except ValueError:
                user_message = 'The entered number of possible errors must be at least \'1\'.'
                number_of_errors = 1
            num_errors = number_of_errors * 2
            dna_string = rsf.convert_unicode_to_dna(input_text, num_errors, transcoding)
            return render_template('solomon.html', action='/solomon', input_text='', error_text=number_of_errors,
                                   dna_text=dna_string, user_message=user_message, output_text='',
                                   input_left='Input left text...', encode_right='Encode right text...',
                                   decode_left='Decode left text...', encoding_information='Binary: ' +
                                   rsf.convert_unicode_to_binary(input_text) + '\nEncoded: ' +
                                   rsf.convert_binary_to_reed_solomon(rsf.convert_unicode_to_binary(input_text),
                                                                      num_errors))
        elif 'decode' in request.form:
            encoded_text = request.form['dna_text']
            decoded_text = rsf.convert_dna_to_unicode(encoded_text, msg_length, num_errors, transcoding)
            return render_template('solomon.html', action='/solomon', input_text='', error_text=num_errors,
                                   dna_text='', user_message='', output_text=decoded_text)
        elif 'clear' in request.form:
            return render_template('solomon.html', action='/solomon', input_text='', error_text='', dna_text='',
                                   user_message='', output_text='')
        else:
            return render_template('solomon.html', action='/solomon', input_text='', error_text='', dna_text='',
                                   user_message='', output_text='')
    else:
        return render_template('solomon.html', action='/solomon', input_text='', error_text='', dna_text='',
                               user_message='', output_text='')


def convert_decimal_to_base(dec, base):
    if dec < base:
        return str(dec)
    else:
        return convert_decimal_to_base(int(dec / base), base) + str(dec % base)


def convert_unicode_to_dna(user_input, base):
    dna_string = ''
    for character in user_input:
        converted_value = convert_decimal_to_base(ord(character), base)
        dna_string += ''.join([transcoding[int(i)] for i in converted_value])
        dna_string += transcoding[base]
    return dna_string


def convert_dna_to_unicode(dna_input, base):
    unicode_string = ''
    for dna_strings in dna_input.split(transcoding[base]):
        if len(dna_strings) == 0:
            continue
        unicode_string += chr(int(''.join([str(transcoding.index(i)) for i in dna_strings]), base))
    return unicode_string


def convert_unicode_to_dna_simple(text_input):
    dna_string = ''
    for character in text_input:
        binary_value = str(bin(ord(character)))[2:].zfill(20)
        print(binary_value)
        for c in range(0, len(binary_value), 2):
            dna_string += transcoding[int(binary_value[c]) * 2 + int(binary_value[c+1])]
    return dna_string


def convert_dna_to_unicode_simple(dna_string):
    return_string = ''
    for character in range(0, len(dna_string), 10):
        numerical_dna_string = ''
        for x in dna_string[character:character+10]:
            numerical_dna_string += str(int(transcoding.index(x) / 2))
            numerical_dna_string += str(int(transcoding.index(x) % 2))
        return_string += chr(int(numerical_dna_string, 2))
    return return_string


def unicode_to_reed_solomon(message, number_of_errors):
    encoder = rs.RSCoder(len(message) + (2 * number_of_errors), len(message))
    encoded_unicode = encoder.encode(message)
    return convert_unicode_to_dna(encoded_unicode, 4)


def reed_solomon_to_unicode(dna, message_length, number_of_errors):
    decoder = rs.RSCoder(message_length + (2 * number_of_errors), message_length)
    dna_string = convert_dna_to_unicode(dna, 4)
    return decoder.decode(dna_string)[0]


if __name__ == '__main__':
    app.run(debug=True)
