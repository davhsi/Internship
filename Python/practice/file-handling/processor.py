import re
from functools import reduce

def clean_text(line):
    line = line.lower()
    line = re.sub(r'[^\w\s]', '', line) # w -> words(alpha-numeric, _), s-> spaces(newline,space,tab)
    line = line.strip()
    return line

def clean_lines(lines):
    return list(map(clean_text, lines))

def filter_lines(lines, keyword):
    return list(filter(lambda x: keyword in x, lines))

def word_count(lines):
    words = " ".join(lines).split()
    return len(words)

def most_common_word(lines):
    words = "".join(lines).split()
    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) +1
    
    return max(freq, key=freq.get)

def total_characters(lines):
    return reduce(lambda acc, line: acc + len(line), lines, 0)