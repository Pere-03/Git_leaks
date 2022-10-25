#!user/bin/python3
from git import Repo
from time import sleep as delay
from json import dump

import os
import re
import sys
import signal


DANGEROUS_WORDS = [
                'credentials', 'credenciales', 'claves', 'seguridad',
                'password', 'key', 'keys', 'security', 'issue', 'secret'
                ]


REPO_DIR = "./skale/skale-manager"


def handler_signal(signal, frame):
    print('\n\n [!] Out ........\n')
    sys.exit(1)


signal.signal(signal.SIGINT, handler_signal)


def limpiar_pantalla():

    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')


def extract(url: str):
    '''
    Extraemos el repositorio de nuestro directorio
    '''
    repo = Repo(url)
    return repo


# En la funcion, buscaremos cada palabra clave en cada commit.
# Si encontramos la palabra, guardamos la version del comit como
# clave de un diccionario, y el commit junto con el autor en el contenido.
def transform(repo: Repo):
    '''
    Sacamos los commits peligrosos a un diccionario
    '''
    commits_dictionary = {}
    commits = list(repo.iter_commits())
    total_process = len(commits) * len(DANGEROUS_WORDS)
    process = 0
    loading_bar = '|'
    porcentage = 0
    igual = 1

    for commit in commits:
        for word in DANGEROUS_WORDS:
            process += 1
            if re.findall(word, commit.summary, re.I):
                message = commit.summary + ' by ' + commit.author.name
                message2 = str(word)
                commits_dictionary[commit.hexsha] = [message, message2]

            porcentage = process*100/total_process
            if porcentage >= 5*igual:
                igual += 1
                loading_bar += '='
                limpiar_pantalla()
                print(loading_bar + ' '*(21 - igual) + '>|', end='')
                print(f'{porcentage}%')
                print(f'Potential leaks found: {len(commits_dictionary)}')
                delay(0.1)

            elif process % 500 == 0:
                limpiar_pantalla()
                print(loading_bar + ' '*(21 - igual) + '>|', end='')
                print(f'{porcentage}%')
                print(f'Potential leaks found: {len(commits_dictionary)}')

    limpiar_pantalla()
    loading_bar += '>|'
    print(loading_bar, end='')
    print('100% loaded')
    delay(1)
    return commits_dictionary


def load(dictionary: dict):
    '''
    Imprimimos por pantalla, a la vez que guardamos el diccionario en un JSON
    '''
    dicc = {}

    number = 1
    for k in dictionary:
        dicc['Leak ' + str(number)] = {
                                'Commit id': k, 'mensaje': dictionary[k][0],
                                'Dangerous word': dictionary[k][1]
                                }
        mensaje = 'Possible leak nº ' + str(number) + ' at commit ' + str(k)
        mensaje += 'Commit message: ' + dictionary[k][0]
        mensaje += 'Word that alerted the system: ' + dictionary[k][1]
        print(mensaje)
        number += 1

    archivo = open('leaks.json', 'w')
    dump(dicc, archivo)
    archivo.close()

    return


if __name__ == '__main__':
    entrada = input('Presione cualquier tecla para continuar: ')
    repo = extract(REPO_DIR)
    conflictive_comments = transform(repo)
    load(conflictive_comments)
