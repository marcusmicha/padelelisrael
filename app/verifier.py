from datetime import datetime

class Verifier:
    def __init__(self,
                 occupancies:dict,
                 playing_time:int = 90,
                 start_play_from:str = '19:00',
                 start_play_to:str = '21:30',
                 previous_availabilities:dict = {}) -> None:
        self.playing_time = playing_time
        self.availabilities = self.get_availabilities(occupancies)
        self.start_play_from = datetime.strptime(start_play_from, '%H:%M')
        self.start_play_to = datetime.strptime(start_play_to, '%H:%M')
        self.previous_availabilities = previous_availabilities
        self.notification_to_send = ''
        self.valid_availabilities = False

    def get_availabilities(self, occupancies) -> dict:
        availablities = {}
        for date in occupancies:
            availablities[date] = {}
            for club in occupancies[date]:
                availablities[date][club] = {}
                for field in occupancies[date][club]:
                    field_occupancies  = occupancies[date][club][field]['Ocupaciones']
                    available_hours = self.convert_occupancy(field_occupancies)
                    availablities[date][club][field] = available_hours
                availablities[date][club] = self.get_club_availabilities(availablities[date][club])
        return availablities
    
    def convert_occupancy(self, field_occupancies) -> dict:
        parsed_occupancies = self.parse_occupancy(field_occupancies)
        prev_end = datetime.strptime('06:00', '%H:%M') # First hour of the day
        available_hours = []
        for occupancy in parsed_occupancies:
            diff = (occupancy['start'] - prev_end).seconds / 60
            if diff >= self.playing_time:
               availability = {
                    'av_start' : prev_end,
                    'av_end' : occupancy['start']
               }
               available_hours.append(availability)
            prev_end = occupancy['end']
        return available_hours

    def parse_occupancy(self, field_occupancies) -> dict:
        parsed_occupancies = []
        for occupancy in field_occupancies:
            parsed_occupancy = {
                'start': datetime.strptime(occupancy['StrHoraInicio'], '%H:%M'),
                'end': datetime.strptime(occupancy['StrHoraFin'], '%H:%M'),
                'length': int(occupancy['Minutos'])
            }
            parsed_occupancies.append(parsed_occupancy)

        fake_parsed_occupancy = {
                'start': datetime.strptime('23:59', '%H:%M'),
                'end': datetime.strptime('23:59', '%H:%M'),
                'length': 0
            }
        parsed_occupancies = sorted(parsed_occupancies, key=lambda d: d['start'])
        parsed_occupancies.append(fake_parsed_occupancy)
        return parsed_occupancies

    def get_club_availabilities(self, club_availabilities:dict) -> str:
        times = [club_availabilities[field] for field in club_availabilities]
        intervals = [[item['av_start'], item['av_end']] for items in times for item in items]
        intervals.sort()
        stack = []
        stack.append(intervals[0])
        for i in intervals[1:]:
            # Check for overlapping interval,
            # if interval overlap
            if stack[-1][0] <= i[0] <= stack[-1][-1]:
                stack[-1][-1] = max(stack[-1][-1], i[-1])
            else:
                stack.append(i)
        # to avoid duplicates, needs to be improved
        stack = set([tuple(time) for time in stack])
        stack = [list(time) for time in stack]
        return sorted(stack)
        
    def verify(self) -> bool:
        time_compatibility = False
        different_slots = False
        for date in self.availabilities:
            for club in self.availabilities[date]:         
                for slot in self.availabilities[date][club]:
                    if slot[0] >= self.start_play_from and slot[0] <= self.start_play_to:
                        time_compatibility = True
        if self.previous_availabilities != self.availabilities:
            different_slots = True
        # if time_compatibility and different_slots:
        self.notification_to_send = self.generate_tg_notification()
        self.valid_availabilities = True
        return self.valid_availabilities, self.availabilities, self.notification_to_send

    def generate_tg_notification(self) -> str:
        notif = ''
        for date in self.availabilities:
            notif += f'__{date}__\n'
            for club in self.availabilities[date]:
                notif += f'\t\t_{club}_\n'
                notif += f'\t\t\t\tAvailabilities between\n'
                for club_availability in self.availabilities[date][club]:
                    parsed_club_availability = self.date_to_str(club_availability)
                    notif += f'\t\t\t\t\t\t{parsed_club_availability[0]} and {parsed_club_availability[1]}\n'
        notif = notif.replace('-',' ')
        return notif

    def date_to_str(self, start_end:list) -> str:
        start_end[0] = start_end[0].strftime('%HH%M')
        start_end[1] = start_end[1].strftime('%HH%M')
        return start_end