from easy_lang import easy_lang
import sys

if len(sys.argv) != 2:
    sys.exit(1)

filename = sys.argv[1]
if filename.split('.')[1] != 'gks':
    sys.exit(1)

r = open(filename, 'r', encoding='UTF8')
code = r.read()
r.close()

interpreter = easy_lang()
interpreter.interprete(code)