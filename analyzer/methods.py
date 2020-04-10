import re


def leet_transform(word: str, indices: list) -> str:
    comparison = {
        '$': 's',
        '1': 'i',
        '0': 'o',
        '3': 'e',
        '@': 'a'
    }

    for index in indices:
        symbol = comparison.get(word[index])

        if not symbol:
            continue

        word = word[:index] + symbol + word[index + 1:]

    return re.sub(r'[\W\d\s_]+', r'', word)
