import uuid as UUID
import base64

CHAR_SET = ("a", "b", "c", "d", "e", "f",
            "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
            "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
            "W", "X", "Y", "Z")


def uuid():
    """
    :return:
    """
    return UUID.uuid4()


def uuid_36():
    """
    :return:
    """
    return str(UUID.uuid4())


def uuid_32():
    """
    :return:
    """
    return uuid_36().replace('-', '')


def uuid_8():
    """
    :return:
    """
    s = uuid_32()
    result = ''
    for i in range(0, 8):
        sub = s[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += CHAR_SET[x % 0x3E]
    return result


def uuid_16():
    """
    :return:
    """
    return uuid_8() + uuid_8()


def bas64_encode_text(text):
    """
    :param text:
    :return:
    """
    if isinstance(text, str):
        return str(base64.b64encode(text.encode('utf-8')), 'utf-8')
    return text


def bas64_decode_text(text):
    """
    :param text:
    :return:
    """
    if isinstance(text, str):
        return str(base64.decodebytes(bytes(text, encoding="utf8")), 'utf-8')
    return text


def decode_text(text, crypto=""):

    if crypto:
        if crypto.lower() == 'base64':
            text = bas64_decode_text(text)
        else:
            text = text
    return text


def encode_text(text, crypto=""):

    if crypto:
        if crypto.lower() == 'base64':
            text = bas64_encode_text(text)
        else:
            text = text
    return text
