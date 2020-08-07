import unireedsolomon
from random import random

transcoding = ['A', 'C', 'G', 'T']
message = chr(131074) + chr(131074) + chr(131074) + chr(131074) + chr(131074) + chr(131074) + chr(131074)


def convert_unicode_to_binary(unicode_input):
    binary_output = ''
    for character in unicode_input:
        binary_output += str(bin(ord(character)))[2:].zfill(18)
    return binary_output


def convert_binary_to_reed_solomon(binary_input, errors):
    rsc = unireedsolomon.RSCoder(len(binary_input) + (2 * errors), len(binary_input))
    return rsc.encode(binary_input)


def convert_reed_solomon_to_binary(encoded_input, message_length, errors):
    rsc = unireedsolomon.RSCoder(message_length + (2 * errors), message_length)
    return rsc.decode(encoded_input)[0]


def convert_binary_to_unicode(binary_input):
    unicode_output = ''
    for starting_position in range(0, len(binary_input), 18):
        unicode_output += chr(int(binary_input[starting_position:starting_position + 18], 2))
    return unicode_output


def generate_errors(dna_string, errors):
    return_string = [i for i in dna_string]
    for i in range(errors):
        return_string[int(random() * len(dna_string))] = transcoding[int(random() * 4)]
    return ''.join(return_string)


def convert_encoded_to_dna(encoded):
    dna_binary = ''
    for character in encoded:
        dna_binary += str(bin(ord(character)))[2:].zfill(8)
    return ''.join([transcoding[2*int(dna_binary[i]) + int(dna_binary[i+1])] for i in range(0, len(dna_binary) - 2, 2)])


def convert_dna_to_encoded(dna_string):
    encoded_string = ''
    binary_stage = ''
    for character in dna_string:
        binary_stage += str(int(transcoding.index(character) / 2))
        binary_stage += str(int(transcoding.index(character) % 2))
    for i in range(0, len(binary_stage), 8):
        encoded_string += chr(int(binary_stage[i:i + 8], 2))
    return encoded_string


binary = convert_unicode_to_binary(message)
reed_solomon = convert_binary_to_reed_solomon(binary, 4)
original_dna = convert_encoded_to_dna(reed_solomon)
errors_dna = generate_errors(original_dna, 4)
decoded = convert_dna_to_encoded(errors_dna)
binary_converted = convert_reed_solomon_to_binary(decoded, len(binary), 4)
unicode = convert_binary_to_unicode(binary_converted)

print(message + '\n' + binary + '\n' + reed_solomon + '\n' + original_dna + '\n' + errors_dna + '\n' + decoded + '\n' +
      binary_converted + '\n' + unicode)
