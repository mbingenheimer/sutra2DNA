from flask import Flask, render_template, request

app = Flask(__name__)
transcoding = [chr(i + 97) for i in range(11)]
master_page_selection = ['Home', 'Simple Transform', 'Some Other Page']


@app.route('/')
def home():
    return render_template('index.html', header_elements=['Home', 'simple', 'Simple Transform', '',
                                                          'Some Other Algorithm'])


@app.route('/simple', methods=['POST', 'GET'])
def simple_transform():
    text_string = ''
    dna_string = ''
    output_string = ''
    if request.method == 'POST':
        if 'encode' in request.form:
            input_text = request.form['text']
            range_value = int(request.form['range'])
            dna_string = convert_unicode_to_dna(input_text, range_value)
            return render_template('simple_transform.html', action='/simple', text=text_string, dna=dna_string,
                                   output=output_string, range_value=range_value, error_message='',
                                   header_elements=['Simple Transform', '', 'Home', '', 'Some Other Algorithm'])
        elif 'decode' in request.form:
            range_value = int(request.form['range'])
            try:
                output_string = convert_dna_to_unicode(request.form['dna'], range_value)
                return render_template('simple_transform.html', action='/simple', text=text_string, dna=dna_string,
                                       header_elements=['Simple Transform', '', 'Home', '', 'Some Other Algorithm'])
            except OverflowError:
                return render_template('simple_transform.html', action='/simple', text=text_string, dna=dna_string,
                                       output=output_string, range_value=range_value,
                                       error_message='Decoded Unicode value was too large.',
                                       header_elements=['Simple Transform', '', 'Home', '', 'Some Other Algorithm'])
        elif 'clear' in request.form:
            text_string = dna_string = output_string = ''
            return render_template('simple_transform.html', action='/simple', text=text_string, dna=dna_string,
                                   output=output_string, range_value=request.form['range'], error_message='',
                                   header_elements=['Simple Transform', '', 'Home', '', 'Some Other Algorithm'])
        else:
            pass
    else:
        return render_template('simple_transform.html', action='/simple', text='', dna='', output='', range_value='2',
                               error_message='', header_elements=['Simple Transform', '', 'Home', '',
                                                                  'Some Other Algorithm'])


def convert_decimal_to_base(dec, base):
    if dec < base:
        return str(dec)
    else:
        return convert_decimal_to_base(int(dec / base), base) + str(dec % base)


def convert_unicode_to_dna(user_input, base):
    dna_string = ''
    for character in user_input:
        ternary_value = convert_decimal_to_base(ord(character), base)
        dna_string += ''.join([transcoding[int(i)] for i in ternary_value])
        dna_string += transcoding[base]
    return dna_string


def convert_dna_to_unicode(dna_input, base):
    unicode_string = ''
    for dna_strings in dna_input.split(transcoding[base]):
        if len(dna_strings) == 0:
            continue
        unicode_string += chr(int(''.join([str(transcoding.index(i)) for i in dna_strings]), base))
    return unicode_string


if __name__ == '__main__':
    app.run(debug=True)
