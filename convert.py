import sys
import converters

converters.update_dict_from_file()
'''
if sys.argv[0] != '':
    infile = sys.argv[0]
else:
    infile = "input.md"'''
# infile = 'input.md'
# infile = open(infile, 'r')
infile = open('input.md', 'r', encoding='utf8')
outfile = open('output.md', 'w', encoding='utf8')
try:
    for i in infile.readlines():
        j = converters.eng_to_kerct(i)
        #j=converters.eng_to_ipa(i)
        print(j)
        outfile.write(j + "\n")
        converters.update_dict_to_file()
finally:
    print('finally')
    converters.update_dict_to_file()
