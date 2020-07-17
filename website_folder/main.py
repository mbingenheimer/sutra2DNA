from flask import Flask, render_template, request

app = Flask(__name__)
transcoding = ['A', 'C', 'G', 'T']


@app.route('/', methods=['POST', 'GET'])
def home():
    text_string = ''
    dna_string = ''
    output_string = ''
    if request.method == 'POST':
        if 'encode' in request.form:
            input_text = request.form['text']
            dna_string = convert_unicode_to_dna(input_text)
            return render_template('index.html', text=text_string, dna=dna_string, output=output_string)
        elif 'decode' in request.form:
            output_string = convert_dna_to_unicode(request.form['dna'])
            return render_template('index.html', text=text_string, dna=dna_string, output=output_string)
        elif 'clear' in request.form:
            text_string = dna_string = output_string = ''
            return render_template('index.html', text=text_string, dna=dna_string, output=output_string)
        else:
            pass
    else:
        return render_template('index.html', text='', dna='', output='')


def convert_decimal_to_ternary(dec):
    if dec < 3:
        return str(dec)
    else:
        return convert_decimal_to_ternary(int(dec / 3)) + str(dec % 3)


def convert_unicode_to_dna(user_input):
    dna_string = ''
    for character in user_input:
        ternary = convert_decimal_to_ternary(ord(character))
        dna_string += ''.join([transcoding[int(i)] for i in ternary])
        dna_string += transcoding[3]
    return dna_string


def convert_dna_to_unicode(dna_input):
    unicode_string = ''
    for dna_strings in dna_input.split('T')[:len(dna_input.split('T')) - 1]:
        unicode_string += chr(int(''.join([str(transcoding.index(i)) for i in dna_strings]), 3))
    return unicode_string


if __name__ == '__main__':
    app.run(debug=True)
