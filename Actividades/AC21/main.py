import json
from collections import defaultdict

__author__ = 'ivania'
start_hour = '23:30'


def read_tweet(tweet, words_frequency, players_frequency, players_names):
    # Implementar
    # Buscar palabras frecuentes
    # Revisar si las palabras corresponden a un jugador
    return words_frequency, players_frequency


def read_tweets_window(start, end, todo, tweets, players_names):
    # Implementar
    # Revisar las palabras para cada tweet si está en la ventana de tiempo
    words_frequency = {}
    for i in tweets:
        tweet = tweets[i]['tweet']
        palabras = tweet.split()
        tiempo = transform_event_time(tweets[i]['hora'])
        for i in palabras:
            if len(i) >= 4 and start <= tiempo <= end:
                # fue pensado para que la fx entrefara los minutos y dps me
                # me di cuenta de que entregaba el string la funcion
                if i not in words_frequency:
                    words_frequency[i] = todo.count(i)
    players_frequency = {}
    # Filtrar palabras infrecuentes
    return words_frequency, players_frequency


def is_in_time_window(hour, start, end):
    # Implementar
    return True


def transform_event_time(minute):
    hour_s, min_s = start_hour.split(':')
    min_s = int(min_s)
    hour_s = int(hour_s)
    if min_s + minute > 59:
        if hour_s + (min_s + minute) / 60 > 23:
            hour_s = int((min_s + minute) / 60 - 1)
        min_s = (min_s + minute) % 60
    else:
        min_s += minute

    return hour_s, min_s


def frequent_words(tweets, events, players_words):
    event_statistics = {}

    for event in events:
        # Implementar
        # Obtener frecuencias de las palabras de la ventana del evento
        words_frequency = {}

        # Cada uno de estos archivos lo pueden utilizar en wordcloud
        with open('Evento{}.txt'.format(minute), 'w+') as file_words:
            for word, frequency in words_frequency.items():
                file_words.write('{}\t{}\n'.format(frequency, word))

    return event_statistics


def load_names_players(players):
    players_names = {}
    # Implementar
    # Crear diccionario para guardar las palabras asociadas a cada uno de los
    # jugadores

    return players_names


def obtener_frecuencias(tweets):pass


if __name__ == "__main__":

    # Crear dict de jugadores
    with open('players.json') as f:
        players = json.load(f)
    tweets = {}
    with open('tweets.csv') as f:
        l_tw = f.read().split('"\n"')
        for i in l_tw:
            linea = i.split('","')
            tweets[linea[0]] = {'hora': linea[1], 'tweet': linea[2]}
        lista = []
        for i in tweets:
            lista.append(tweets[i]['tweet'])
        todo = "-".join(lista)
        # for i in range(0, len(l_tw), 3):
        #     tweets.append({'usuario': l_tw[i],
        #                    'hora': l_tw[i + 1],
        #                    'tweet': l_tw[i + 2]})
    events = {}
    with open('events.csv') as f:
        l_ev = f.readlines()
        for i in l_ev:
            linea = i.strip().split(',', 1)
            events[linea[0]] = linea[1]
    print(events, len(events))
    print(tweets, len(tweets))
    print(read_tweets_window(90, 95, todo, tweets, players))
    # lo pense con minutos
    # players_words = load_names_players(players)
    # events_statistics = frequent_words(tweets, events, players_words)
