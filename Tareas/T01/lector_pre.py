# coding=utf-8


def total_cleaner(string):
    string = string.strip('\n').strip().lstrip('[').rstrip(']')
    string = string.strip('\n').strip().lstrip('{').rstrip('}')
    return string.strip().strip('\n').replace('\n', '')


def object_cleaner(string):
    return string.strip().lstrip('{').rstrip('}').strip()


def attr_cleaner(string):
    string = ','.join([i.strip() for i in string.strip().split(',')])
    string = '['.join([i.strip() for i in string.split('[')])
    string = ']'.join([i.strip() for i in string.split(']')])
    return [i.strip() for i in string.split(':')]


class Reader:

    def __init__(self, ruta):
        with open(ruta, 'r') as f:
            text = total_cleaner(f.read())
        self.lines = [attr_cleaner(object_cleaner(i)) for i in text.split('},')]


# r = Reader('cursos.txt').lines[:3]
# for i in r:
# print(i, '\n\n')

# print(r)

# print()

# for i in r[0]:
#     print(i)
# print([i.strip() for i in r[0].split(',')])
# f = open('curs.txt', 'r').read()
# print([cleaner(f)])
# print(cleaner(f))
def splitter(string):
    return string


def descomador(string):
    new_string = string
    for i in range(len(string)):
        if string[i] == '[':
            str_list = string[i + 1:i + string[i:].find(']')]
            new_str_list = ';'.join(i.strip() for i in str_list.strip().split(','))
            new_string = string.replace(str_list, new_str_list)
    for i in range(1, len(string) - 1):
        if (string[i - 1] == ':' and string[i].isdigit()
                and string[i + 1] == ','):
            str_nums = string[i:i + string[i:].find('"')]
            new_str_nums = ';'.join(str_nums.split(','))
            new_string = string.replace(str_nums, new_str_nums)
    return new_string


def descomador_n(string):
    if 'curso' in None: # la idea es si esta curso, ir a lo de dps y sacar la coma
        return string

'a'[1:1]
with open('cursos.txt', 'r') as f:
    text = total_cleaner(f.read())
lines = [descomador_n(object_cleaner(i)) for i in text.split('},')]
print(lines[507])
print(lines[0])
print(lines[229])

# for i in lines:
#     if 'Innovación y' in i:
#         print(lines.index(i))