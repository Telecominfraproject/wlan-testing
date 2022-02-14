def iss(text: str) -> bool:
    """

    :param text: string to test
    :return: true if text is at lease one non-whitespace character
    """
    if text is None:
        return False
    if (len(text) == 0) or (text.strip() == ""):
        return False
    return True


def nott(text: str) -> bool:
    """

    :param text:
    :return: opposite of is
    """
    return not iss(text=text)
