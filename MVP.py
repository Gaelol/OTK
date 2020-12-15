from __future__ import print_function

import os.path
import pickle
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import Event

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    creds = None

    # Vérifie la présence de token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # En cas de token invalide
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Garde en mémoire le cred
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    def affiche():
        """affiche les x futurs évènements prévus dans le google calendar

                PRE : ?
                POST : ?
                """
        # permet d'afficher les x premiers events de mon calendrier
        nbr_event = int(input("Combien d'evenements voulez-vous afficher ?"))
        now = datetime.utcnow().isoformat() + 'Z'  # Z pour le lieu UTC
        print('Voici les ', nbr_event, ' premiers éléments')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=nbr_event, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('Aucun evenement prevu')
        for event in events:
            print(event['start'].get('dateTime'), event['summary'])

    def perso():
        """Ajoute un évenement personnel au calendrier de la personne connectée

                PRE : ?
                POST : ?
                """
        # permet de creer un evenement uniquement pour moi
        nom = input('Quel est le nom de l"évènement')
        start_time = datetime.strptime(input('Entrez la date de départ en format (2000-00-00T00:00:00)'),
                                       '%Y-%m-%dT%H:%M:%S')
        duree = int(input('Combien de temps dure l"evenement en heure'))
        end_time = start_time + timedelta(hours=duree)
        timezone = 'Europe/Brussels'
        my_eve = Event.Event(nom, start_time, end_time, timezone)
        new_event = my_eve.eventPerso()
        ev = service.events().insert(calendarId='primary', body=new_event).execute()
        print((ev.get('htmlLink')))

    def commu():
        """Ajoute un évenement communautaire pouvant regrouper plusieurs personnes

                PRE : ?
                POST : ?
                """
        # permet de creer un evenement et d'y ajouter des gens
        nom = input('Quel est le nom de l"évènement')
        start_time = datetime.strptime(input('Entrez la date de départ en format (2000-00-00T00:00:00)'),
                                       '%Y-%m-%dT%H:%M:%S')
        duree = int(input('Combien de temps dure l"evenement en heure'))
        end_time = start_time + timedelta(hours=duree)
        attend = (input('Avec qui allez vous participer?'))
        timezone = 'Europe/Brussels'
        my_eve = Event.EventCommu(attend, nom, start_time, end_time, timezone)
        event_commu = my_eve.eventPerso()
        ev = service.events().insert(calendarId='primary', body=event_commu).execute()
        print((ev.get('htmlLink')))

    while 1:
        rep = input('Que voulez-vous faire ?(affiche,perso,commu,fin)')
        if rep == 'affiche':
            affiche()
        if rep == 'perso':
            perso()
        if rep == 'commu':
            commu()
        if rep == 'fin':
            break


if __name__ == '__main__':
    main()

"""
piste d'amelioration : 
classe event orienté objet OK
utilisation simultanée
fonction de tri quand tout le monde a complété ses horaires
mise en forme visuelle du formulaire d'information
gui + console
separation en plusieurs fichiers avec héritage
automatisation des tokens + gestion de l'utilisateur
Gestion des erreurs
"""
