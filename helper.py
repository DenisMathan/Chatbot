

def splitkeep(s, delimiter):
    split = s.split(delimiter)
    return [split[0]] + [delimiter + substr for substr in split[1:]]

def filterMinlenght(stringArr, minlenght):
    result = []
    longest = 0
    for string in stringArr:
        if "?" in string:
            continue
        if len(string) > minlenght:
            result.append(string)
        if len(string) > longest:
            longest = len(string)
    print(longest)
    return result
