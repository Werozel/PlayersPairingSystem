from typing import Optional, List
from datetime import datetime

from libs.models.EventPlayTimes import EventPlayTimes
from libs.models.Group import Group
from libs.models.PlayTime import PlayTime

# Need:
#       User to Event
#       Event to User

class UserVector:

    def __init__(self,
                 age: Optional[int],
                 gender: Optional[str],
                 sport: Optional[int],
                 city: Optional[str],
                 last_login: Optional[datetime],
                 play_times: Optional[List[PlayTime]]
                 ):
        self.age = age
        self.gender = gender
        self.sport = sport
        self.city = city
        self.last_login = last_login
        self.play_times = play_times


class EventVector:

    def __init__(self,
                 sport: Optional[int],
                 group: Optional[Group],
                 closed: Optional[bool],
                 recurring: Optional[bool],
                 play_time: Optional[EventPlayTimes]
                 ):
        self.sport = sport
        self.group = group,
        self.closed = closed,
        self.recurring = recurring,
        self.play_time = play_time
