import unireedsolomon


def convert_unicode_to_binary(unicode_input):
    """
    converts unicode string input into binary integer

    :param unicode_input: String
    :return: int
    """
    binary_output = ''
    for character in unicode_input:
        binary_output += str(bin(ord(character)))[2:].zfill(18)
    return binary_output


def convert_binary_to_reed_solomon(binary_input, errors):
    """
    converts binary string input, using errors, to DNA using reed solomon algorithm

    :param binary_input: String
    :param errors: int
    :return: String
    """
    rsc = unireedsolomon.RSCoder(len(binary_input) + (2 * errors), len(binary_input))
    return rsc.encode(binary_input)


def convert_reed_solomon_to_binary(encoded_input, message_length, errors):
    """
    converts encoded string input of specified length with predetermined number of possible errors to unicode

    :param encoded_input: String
    :param message_length: int
    :param errors: int
    :return: String
    """
    rsc = unireedsolomon.RSCoder(message_length + (2 * errors), message_length)
    return rsc.decode(encoded_input)[0]


def convert_binary_to_unicode(binary_input):
    """
    converts binary string of length 18 input to unicode

    :param binary_input: String
    :return: String
    """
    unicode_output = ''
    for starting_position in range(0, len(binary_input), 18):
        unicode_output += chr(int(binary_input[starting_position:starting_position + 18], 2))
    return unicode_output


def convert_encoded_to_dna(encoded, transcoding):
    """
    converts encoded string to DNA string using transcoding list

    :param encoded: String
    :param transcoding: List[char]
    :return: String
    """
    dna_binary = ''
    for character in encoded:
        dna_binary += str(bin(ord(character)))[2:].zfill(8)
    return ''.join([transcoding[2*int(dna_binary[i]) + int(dna_binary[i+1])] for i in range(0, len(dna_binary) - 2, 2)])


def convert_dna_to_encoded(dna_string, transcoding):
    """
    converts DNA string to encoded string using transcoding list and reed solomon algorithm

    :param dna_string: String
    :param transcoding: List[char]
    :return: String
    """
    encoded_string = ''
    binary_stage = ''
    for character in dna_string:
        binary_stage += str(int(transcoding.index(character) / 2))
        binary_stage += str(int(transcoding.index(character) % 2))
    for i in range(0, len(binary_stage), 8):
        encoded_string += chr(int(binary_stage[i:i + 8], 2))
    return encoded_string


def convert_unicode_to_dna(unicode_string, errors, transcoding):
    """
    converts unicode string input to dna string output using predetermined number of errors and transcoding list

    :param unicode_string: String
    :param errors: int
    :param transcoding: List[char]
    :return: String
    """
    return convert_encoded_to_dna(convert_binary_to_reed_solomon(convert_unicode_to_binary(unicode_string), errors),
                                  transcoding)


def convert_dna_to_unicode(dna_string, message_length, errors, transcoding):
    """
    converts dna string of set message length, predetermined number of errors, and transcoding list

    :param dna_string: String
    :param message_length: int
    :param errors: int
    :param transcoding: List[char]
    :return: String
    """
    return convert_binary_to_unicode(convert_reed_solomon_to_binary(convert_dna_to_encoded(dna_string, transcoding),
                                                                    message_length, errors))
