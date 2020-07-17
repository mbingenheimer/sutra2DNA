from flask import Flask, render_template, request

app = Flask(__name__)
transcoding = ['A', 'C', 'G', 'T']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/simple', methods=['POST', 'GET'])
def simple():
    text_string = ''
    dna_string = ''
    output_string = ''
    if request.method == 'POST':
        if 'encode' in request.form:
            input_text = request.form['text']
            dna_string = convert_unicode_to_dna(input_text, 'simple')
            return render_template('simple.html', action='/simple', text=text_string, dna=dna_string,
                                   output=output_string)
        elif 'decode' in request.form:
            output_string = convert_dna_to_unicode(request.form['dna'], 'simple')
            return render_template('simple.html', action='/simple', text=text_string, dna=dna_string,
                                   output=output_string)
        elif 'clear' in request.form:
            text_string = dna_string = output_string = ''
            return render_template('simple.html', action='/simple', text=text_string, dna=dna_string,
                                   output=output_string)
        else:
            pass
    else:
        return render_template('simple.html', action='/simple', text='', dna='', output='')


@app.route('/ternary', methods=['POST', 'GET'])
def ternary():
    text_string = ''
    dna_string = ''
    output_string = ''
    if request.method == 'POST':
        if 'encode' in request.form:
            input_text = request.form['text']
            dna_string = convert_unicode_to_dna(input_text, 'ternary')
            return render_template('ternary.html', action='/ternary', text=text_string, dna=dna_string,
                                   output=output_string)
        elif 'decode' in request.form:
            output_string = convert_dna_to_unicode(request.form['dna'], 'ternary')
            return render_template('ternary.html', action='/ternary', text=text_string, dna=dna_string,
                                   output=output_string)
        elif 'clear' in request.form:
            text_string = dna_string = output_string = ''
            return render_template('ternary.html', action='/ternary', text=text_string, dna=dna_string,
                                   output=output_string)
        else:
            pass
    else:
        return render_template('ternary.html', action='/ternary', text='', dna='', output='')


def convert_decimal_to_ternary(dec):
    if dec < 3:
        return str(dec)
    else:
        return convert_decimal_to_ternary(int(dec / 3)) + str(dec % 3)


def convert_unicode_to_dna(user_input, algorithm):
    dna_string = ''
    if algorithm == 'ternary':
        for character in user_input:
            ternary_value = convert_decimal_to_ternary(ord(character))
            dna_string += ''.join([transcoding[int(i)] for i in ternary_value])
            dna_string += transcoding[3]
    elif algorithm == 'simple':
        for character in user_input:
            binary_value = str(bin(ord(character)))[2:].zfill(18)
            dna_string += ''.join(transcoding[2 * int(binary_value[i * 2]) + int(binary_value[(i * 2) + 1])]
                                  for i in range(int(len(binary_value) / 2)))
    else:
        return
    return dna_string


def convert_dna_to_unicode(dna_input, algorithm):
    unicode_string = ''
    if algorithm == 'ternary':
        for dna_strings in dna_input.split('T')[:len(dna_input.split('T')) - 1]:
            unicode_string += chr(int(''.join([str(transcoding.index(i)) for i in dna_strings]), 3))
    elif algorithm == 'simple':
        binary_values = ''
        for character in dna_input:
            binary_values += str(bin(transcoding.index(character)))[2:].zfill(2)
        for value in range(0, len(binary_values), 9):
            unicode_string += chr(int(binary_values[value:value + 9], 2))
    else:
        return
    return unicode_string


if __name__ == '__main__':
    app.run(debug=True)
