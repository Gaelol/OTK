class Event:

    def __init__(self, summary, start, end, timezone):
        self.summary = summary
        self.start = start
        self.end = end
        self.timezone = timezone

    def eventPerso(self):
        new_event = {
            'summary': self.summary,
            'start': {
                'dateTime': self.start.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': self.timezone,
            },
            'end': {
                'dateTime': self.end.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': self.timezone,
            }
        }
        return new_event


class EventCommu(Event):

    def __init__(self, attendees, summary, start, end, timezone):
        super().__init__(summary, start, end, timezone)
        self.attendees = attendees

    def eventCommu(self):
        new_event = {
            'summary': self.summary,
            'start': {
                'dateTime': self.start.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': self.timezone,
            },
            'end': {
                'dateTime': self.end.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': self.timezone,
            },
            'attendees': [
                {'email': self.attendees}
            ]
        }
        return new_event
