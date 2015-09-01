# coding=utf-8


def total_clean(string):
    string = string.strip('\n').strip().lstrip('[').rstrip(']')
    string = string.strip('\n').strip().lstrip('{').rstrip('}')
    return string.strip().strip('\n').replace('\n', '')


def object_clean(string):
    string = string.strip().lstrip('{').rstrip('}').strip()
    string = '['.join([i.strip() for i in string.split('[')])
    return ']'.join([i.strip() for i in string.split(']')])


# "ofr": 80
def get_numeric_attr(js_string, key):
    if key in js_string:
        left = js_string.find(key) + len(key) + 3
        right = js_string[left:].find(',') + left
        str_val = js_string[left:right]
        value = int(str_val) if str_val.isdigit() else str_val
        return key, value
    return key, -1


# "retiro": "SI"
def get_boolean_attr(js_string, key):
    if key in js_string:
        left = js_string.find(key) + len(key) + 4
        right = js_string[left:].find(',') + left - 1
        value = True if js_string[left:right] == 'SI' else False
        return key, value
    return key, None


# "curso": "Cálculo I"
def get_string_attr(js_string, key):
    if key in js_string:
        left = js_string.find(key) + len(key) + 4
        right = js_string[left:].find('"', 2) + left
        value = js_string[left:right]
        return key, value
    return key, ''


# "profesor": ['Pedro', 'Juan']
def get_list_attr(js_string, key):
    if key in js_string:
        left = js_string.find(key) + len(key) + 3
        right = js_string[left:].find(']') + left
        str_val = js_string[left:right]
        value = [i.strip().strip('"') for i in str_val.split(',')]
        return key, value
    return key, []


# "equiv": "(FIS1533 o FIZ021) y MAT1203"
def get_logical_attr(js_string, key):
    key, string = get_string_attr(js_string, key)
    return key, string


# W:4, W-V:5, L:4,5, V-W:1,2
def process_hora(string):
    dias, horas = string.split(':')
    dias = dias.split('-')
    horas = horas.split(',')
    return [(i, j) for i in dias for j in horas]


class Reader:

    def __init__(self, ruta):
        with open(ruta, 'r') as f:
            text = total_clean(f.read())
        self.objects = [object_clean(i) for i in text.split('},')]

    @property
    def parsed_strings(self):
        parsed = []
        for i in self.objects:
            numeric = [get_numeric_attr(i, j) for j in self.__class__.numeric_keys]
            boolean = [get_boolean_attr(i, j) for j in self.__class__.boolean_keys]
            string = [get_string_attr(i, j) for j in self.__class__.string_keys]
            list_ = [get_list_attr(i, j) for j in self.__class__.list_keys]
            non_empty = [k for k, l in string if l != '']
            list_ = [(i, j) for i, j in list_ if j != [''] or
                     (j == [''] and i not in non_empty)]
            logical = [get_logical_attr(i, j) for j in self.__class__.logical_keys]
            parsed.append(numeric + boolean + string + list_ + logical)
        return parsed

    @property
    def dictionaries(self):
        dicts = []
        for obj in self.parsed_strings:
            dicts.append(dict((i, j) for i, j in obj))
        return dicts


class CourseReader(Reader):

    numeric_keys = ['disp', 'ofr', 'ocu', 'cred', 'sec', 'NRC']
    boolean_keys = ['eng', 'apr', 'retiro']
    string_keys = ['curso', 'sala_lab', 'hora_cat', 'sala_cat', 'hora_ayud',
                   'hora_lab', 'sigla', 'sala_ayud', 'campus', 'profesor']
    list_keys = ['profesor']
    logical_keys = []


class PeopleReader(Reader):

    numeric_keys = []
    boolean_keys = ['alumno']
    string_keys = ['usuario', 'clave', 'nombre']
    list_keys = ['ramos_pre', 'idolos']
    logical_keys = []


class TestsReader(Reader):

    numeric_keys = ['sec']
    boolean_keys = []
    string_keys = ['sigla', 'tipo', 'fecha']
    list_keys = []
    logical_keys = []


class RequirementsReader(Reader):

    numeric_keys = []
    boolean_keys = []
    string_keys = ['sigla']
    list_keys = []
    logical_keys = ['prerreq', 'equiv']


if __name__ == '__main__':
    people = PeopleReader('personas.txt')
    people.dictionaries
    courses = CourseReader('cursos.txt')
    courses.dictionaries
    tests = TestsReader('evaluaciones.txt')
    tests.dictionaries
    req = RequirementsReader('requisitos.txt')
    req.dictionaries
    print(courses.dictionaries[1])
    # print(sl)

    # print(get_numeric_attr(sl[0], 'ofr'))
    # print(get_boolean_attr(sl[0], 'retiro'))
    # print(get_string_attr(sl[0], 'curso'))
    # print(get_list_attr(sl[0], 'profesor'))
