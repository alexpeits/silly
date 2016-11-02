"""
regex finder & colorizer
~~~~~~~~~~~~~~~~~~~~~~~~

Usage:

    cat <file> | python regexfind.py [-c color] <pattern>

"""


import re, sys, argparse

colors = {
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36
}

defaultc = 'red'


def highlight(s, color=defaultc):
    return ('\033[01;{}m{}\033[0m'
            .format(colors.get(color, colors[defaultc]), s))


def search(s, pat):
    rg = re.compile(r'{}'.format(pat), flags=re.M)
    for res in rg.finditer(s):
        yield (res.start(), res.end(), res.group())


def finder(s, pat, color):
    new_s = ''
    prev_end = 0
    for start, end, match in search(s, pat):
        new_s += s[prev_end:start] + highlight(match, color)
        prev_end = end
    new_s += s[prev_end:]
    return new_s


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--color', dest='color', action='store',
                        type=str, required=False, help='Color', default=defaultc)
    parser.add_argument('pat', metavar='<pattern>', type=str, help='Pattern')

    args = parser.parse_args()
    s = sys.stdin.read()
    print(finder(s.strip('\n'), args.pat, args.color))
