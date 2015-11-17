# coding=utf-8
import requests
from argparse import ArgumentParser


# Debe tener los atributos:
# * _id (string)
# * name (string)
# * votes (diccionario string: int)


class Table:

    def __init__(self, json_dict):
        self._id = json_dict['_id']
        self.name = json_dict['name']
        self.votes = json_dict['votes']

    def __repr__(self):
        return '%s, %s, %s' % (self._id, self.name, self.votes)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('obtener_votos', help='Obtener ganador de votos')
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        required=True,
        help="Username for API",
    )
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        help="Password for API",
    )
    args = parser.parse_args()
    if args.obtener_votos:
        url = 'http://votaciometro.cloudapp.net/api/v1/'
        auth = requests.auth.HTTPBasicAuth(args.user, args.password)
        tables_response = requests.get(url + 'tables', auth=auth)
        lists = requests.get(url + 'lists', auth=auth)
        dict_listas = {}
        for i in lists.json():
            dict_listas[i] = 0
        tables_dicts = tables_response.json()
        tables = []
        for json_dict in tables_dicts:
            n_url = '%stables/%s' % (url, json_dict['_id'])
            table_with_votes = requests.get(n_url, auth=auth)
            t = Table(table_with_votes.json())
            tables.append(t)
        for table in tables:
            for k in table.votes:
                if k in dict_listas:
                    dict_listas[k] += table.votes[k]
        maximo_name = max(dict_listas)
        maximo = (maximo_name, dict_listas[maximo_name])
        print('Los votos totales son:')
        for k in dict_listas:
            print('', k + ':', dict_listas[k])
        print('El que obtuvo el máximo fue: %s con %d votos.' %
              (maximo[0], maximo[1]))
