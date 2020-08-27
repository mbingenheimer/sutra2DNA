from flask import Flask, render_template, request
import reed_solomon as rsf
import unireedsolomon as rs

app = Flask(__name__)
transcoding = [chr(i + 97) for i in range(11)]
num_errors = 0
msg_length = 0


@app.route('/')
def home():
    """
    returns home page render template
    """
    return render_template('index.html')


@app.route('/simple', methods=['POST', 'GET'])
def simple_transform():
    """
    handles the simple transcoding/transform page
    """
    input_string = ''
    dna_string = ''
    output_string = ''
    # program may or may not be using the above variables
    if request.method == 'POST':
        # if server receives a POST http request
        if 'encode' in request.form:
            # steps taken when the POST is received from element named encode
            input_text = request.form['input_text']
            range_value = int(request.form['base'])
            checked_value = ['', '', '']
            checked_value[range_value - 2] = 'checked'
            dna_string = convert_unicode_to_dna(input_text, range_value)
            input_string = input_text
            output_string = request.form['output_text']
            # returns template for simple transform page; variables relate to encode action
            return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                   checked=checked_value, dna_text=dna_string,
                                   output_text=output_string)
        elif 'decode' in request.form:
            # steps taken from when the POST is received from element named decode
            range_value = int(request.form['base'])
            checked_value = ['', '', '']
            checked_value[range_value - 2] = 'checked'
            input_string = request.form['input_text']
            dna_string = request.form['dna_text']
            output_string = request.form['output_text']
            try:
                # TODO: simplify error handling section, maybe should make render_template() more efficient
                output_string = convert_dna_to_unicode(request.form['dna_text'], range_value)
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=checked_value, dna_text=dna_string,
                                       output_text=output_string)
            except OverflowError:
                # for when the conversion results in a character value too large for Unicode to handle
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=['checked', '', ''], dna_text=dna_string,
                                       dna_right='One or more of the values that you tried to decode fell outside of'
                                                 ' the Unicode bounds. Try using a shorter DNA value or encoding a'
                                                 ' different set of data.', output_text=output_string)
            except ValueError:
                # error received when user decodes DNA not within the transcoding list
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=['checked', '', ''], dna_text=dna_string,
                                       dna_right='One or more of the values that you tried to decode were not '
                                                 'accounted for based on your selected encoding method. Please try '
                                                 'again with a different set of data.', output_text=output_string)
            except Exception as e:
                # TODO: all other errors, doesn't give any useful informtion as of now, more testing is needed
                print(e)
                return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                       checked=['checked', '', ''], dna_text=dna_string,
                                       dna_right='There was an unknown error while decoding your DNA data. Please '
                                                 'try again with a different input.', output_text=output_string)
        elif 'clear' in request.form:
            # when the POST is sent from the element named clear
            input_string = dna_string = output_string = ''
            return render_template('simple_transform.html', action='/simple', input_text=input_string,
                                   checked=['checked', '', ''], dna_text=dna_string, input_right='', dna_right='',
                                   output_text=output_string, output_right='')
        else:
            # not entirely sure what to have here, not sure when this code would even run
            pass
    else:
        # this runs when we receive a GET http request from the program, returns an 'empty' simple transcoding page
        return render_template('simple_transform.html', action='/simple', input_text=input_string,
                               checked=['checked', '', ''], dna_text=dna_string, input_right='', dna_right='',
                               output_text=output_string, output_right='')


@app.route('/solomon', methods=['POST', 'GET'])
def reed_solomon_transform():
    """
    handles the reed solomon page
    """
    global num_errors
    # entire use of num_errors seems nonsense, variable is being used to help complete this pseudo-reed solomon process
    if request.method == 'POST':
        # when we receive a POST request
        if 'encode' in request.form:
            user_message = ''
            input_text = request.form['input_text']
            try:
                # we need to make sure that there is a user entered value for expected errors for solomon algorithm
                # sets the value to 1 if there is nothing entered from the user
                number_of_errors = int(request.form['error_choice'])
                if number_of_errors == 0:
                    user_message = 'The entered number of possible errors must be at least \'1\'.'
                    number_of_errors = 1
            except ValueError:
                user_message = 'The entered number of possible errors must be at least \'1\'.'
                number_of_errors = 1
            num_errors = number_of_errors * 2
            dna_string = request.form['dna_text']
            input_string = request.form['input_text']
            encode_string = rsf.convert_binary_to_reed_solomon(rsf.convert_unicode_to_binary(input_text), num_errors)
            # using the reed solomon functions to convert
            # simple transcoding/transform Python file should hold simple tran. functions for organization
            # I guess not completely necessary
            format_encode = encode_string[:len(encode_string) - (2 * num_errors)] + ' + ' + \
                            encode_string[len(encode_string) - (2 * num_errors):]
            output_string = request.form['output_text']
            # returns first encode of the reed solomon algorithm
            return render_template('solomon.html', action='/solomon', input_text=input_string,
                                   error_text=number_of_errors, encode_text=format_encode, dna_text=dna_string,
                                   user_message=user_message, output_text=output_string,
                                   encode_right='Encode right text...')
        elif 'continue' in request.form:
            # handles the second encode request from the user
            # the two-part encoding idea is new and is probably implemented very inefficiently
            input_string = request.form['input_text']
            dna_string = rsf.convert_encoded_to_dna(''.join(request.form['encode_text'].split(' + ')), transcoding)
            encode_string = request.form['encode_text']
            output_string = request.form['output_text']
            # returns the DNA to the user on the solomon webpage
            return render_template('solomon.html', action='/solomon', input_text=input_string,
                                   error_text=int(num_errors / 2), encode_text=encode_string, dna_text=dna_string,
                                   output_text=output_string)
        elif 'decode' in request.form:
            # decodes DNA, there is no error handling and must be added
            encoded_text = request.form['dna_text']
            decoded_text = rsf.convert_dna_to_unicode(encoded_text, msg_length, num_errors, transcoding)
            input_string = request.form['input_text']
            encode_string = request.form['encode_text']
            dna_string = encoded_text
            return render_template('solomon.html', action='/solomon', input_text=input_string,
                                   error_text=int(num_errors / 2), encode_text=encode_string, dna_text=dna_string,
                                   output_text=decoded_text)
        elif 'clear' in request.form:
            # clears input fields
            return render_template('solomon.html', action='/solomon', input_text='', error_text='', dna_text='',
                                   output_text='')
        else:
            # returns the 'empty' reed solomon page
            return render_template('solomon.html', action='/solomon', input_text='', error_text='', dna_text='',
                                   output_text='')
    else:
        # returns the 'empty' reed solomon page
        return render_template('solomon.html', action='/solomon', input_text='', error_text='', dna_text='',
                               output_text='')


def convert_decimal_to_base(dec, base):
    """
    converts integer base 10 into integer base 'base'

    :param dec: int
    :param base: int
    :return: int
    """
    if dec < base:
        return str(dec)
    else:
        return convert_decimal_to_base(int(dec / base), base) + str(dec % base)


def convert_unicode_to_dna(user_input, base):
    """
    converts unicode into dna

    :param user_input: String
    :param base: int
    :return: String
    """
    dna_string = ''
    for character in user_input:
        converted_value = convert_decimal_to_base(ord(character), base)
        dna_string += ''.join([transcoding[int(i)] for i in converted_value])
        dna_string += transcoding[base]
    return dna_string


def convert_dna_to_unicode(dna_input, base):
    """
    converts dna string input into unicode string

    :param dna_input: String
    :param base: int
    :return: String
    """
    unicode_string = ''
    for dna_strings in dna_input.split(transcoding[base]):
        if len(dna_strings) == 0:
            continue
        unicode_string += chr(int(''.join([str(transcoding.index(i)) for i in dna_strings]), base))
    return unicode_string


def convert_unicode_to_dna_simple(text_input):
    """
    converts unicode string input to DNA string, only uses base-2

    :param text_input: String
    :return: String
    """
    dna_string = ''
    for character in text_input:
        binary_value = str(bin(ord(character)))[2:].zfill(20)
        print(binary_value)
        for c in range(0, len(binary_value), 2):
            dna_string += transcoding[int(binary_value[c]) * 2 + int(binary_value[c + 1])]
    return dna_string


def convert_dna_to_unicode_simple(dna_string):
    """
    converts DNA string input to unicode output, only uses base-2

    :param dna_string: String
    :return: String
    """
    return_string = ''
    for character in range(0, len(dna_string), 10):
        numerical_dna_string = ''
        for x in dna_string[character:character + 10]:
            numerical_dna_string += str(int(transcoding.index(x) / 2))
            numerical_dna_string += str(int(transcoding.index(x) % 2))
        return_string += chr(int(numerical_dna_string, 2))
    return return_string


def unicode_to_reed_solomon(message, number_of_errors):
    """
    converts unicode to dna using reed solomon algorithm

    :param message: String
    :param number_of_errors: int
    :return: String
    """
    encoder = rs.RSCoder(len(message) + (2 * number_of_errors), len(message))
    encoded_unicode = encoder.encode(message)
    return convert_unicode_to_dna(encoded_unicode, 4)


def reed_solomon_to_unicode(dna, message_length, number_of_errors):
    """
    converts DNA string, encoded using reed solomon, into unicode string

    :param dna: String
    :param message_length: int
    :param number_of_errors: int
    :return: String
    """
    decoder = rs.RSCoder(message_length + (2 * number_of_errors), message_length)
    dna_string = convert_dna_to_unicode(dna, 4)
    return decoder.decode(dna_string)[0]


if __name__ == '__main__':
    # runs the program if you are running this file directly
    app.run(debug=True)
