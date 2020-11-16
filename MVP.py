from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
        # permet de creer un evenement uniquement pour moi
        nom = input('Quel est le nom de l"évènement')
        start_time = datetime.strptime(input('Entrez la date de départ en format (2000-00-00T00:00:00)'),
                                       '%Y-%m-%dT%H:%M:%S')
        duree = int(input('Combien de temps dure l"evenement en heure'))
        end_time = start_time + timedelta(hours=duree)
        timezone = 'Europe/Brussels'
        new_event = {
            'summary': nom,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        ev = service.events().insert(calendarId='primary', body=new_event).execute()
        print((ev.get('htmlLink')))

    def commu():
        # permet de creer un evenement et d'y ajouter des gens
        nom = input('Quel est le nom de l"évènement')
        start_time = datetime.strptime(input('Entrez la date de départ en format (2000-00-00T00:00:00)'),
                                       '%Y-%m-%dT%H:%M:%S')
        duree = int(input('Combien de temps dure l"evenement en heure'))
        end_time = start_time + timedelta(hours=duree)
        attend = (input('Avec qui allez vous participer?'))

        timezone = 'Europe/Brussels'
        event_commu = {
            'summary': nom,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'attendees': [
                {'email': attend}

            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
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
classe event orienté objet
utilisation simultanée
fonction de tri quand tout le monde a complété ses horaires
mise en forme visuelle du formulaire d'information
gui + console
separation en plusieurs fichiers avec héritage
automatisation des tokens + gestion de l'utilisateur
Gestion des erreurs
"""