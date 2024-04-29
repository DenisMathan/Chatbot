

def splitkeep(s, delimiter, beginning = True):
    split = s.split(delimiter)
    if beginning:
        return [split[0]] + [delimiter + substr for substr in split[1:]]
    else:
        return [substr + delimiter for substr in split[0:len(split)-1]] +[split[len(split)-1]]

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
    return result
