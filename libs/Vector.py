from typing import Optional, List
from datetime import datetime
from src.misc import datetime_to_seconds
import math

from libs.models.EventPlayTimes import EventPlayTimes
from libs.models.Group import Group
from libs.models.PlayTime import PlayTime
from libs.models.User import User


# Need:
#       User to Event
#       Event to User

class UserVector:

    def __init__(self,
                 age: Optional[int] = None,
                 gender: Optional[str] = None,
                 sport: Optional[int] = None,
                 city: Optional[str] = None,
                 last_login: Optional[datetime] = None,
                 include_play_times: bool = True,
                 play_times: Optional[List[PlayTime]] = None,
                 user: Optional[User] = None
                 ):
        self.age = age
        self.gender = gender
        self.sport = sport
        self.city = city.lower().strip() if city else city
        self.last_login = last_login
        self.include_play_times = include_play_times
        self.play_times = play_times
        self.user = user

    def calculate_diff(self, other) -> float:
        result: float = 0
        if self.age and other.age:
            result += 100 * (10 - math.fabs(other.age - self.age))
        if self.gender and other.gender:
            result += 100 * int(self.gender == other.gender)
        if self.sport and other.sport:
            result += 100 * int(self.sport == other.sport)
        if self.city and other.city:
            result += 100 * int(self.city != other.city)
        if self.last_login and other.last_login:
            result += 100 * (604800 / math.fabs(
                datetime_to_seconds(self.last_login) - datetime_to_seconds(other.last_login)
            ))
        if self.include_play_times and self.play_times \
                and other.include_play_times and other.play_times:
            result += UserVector.calculate_play_times_diff(self.play_times, other.play_times)
        return result

    @staticmethod
    def calculate_play_times_diff(my_pt, other_pt) -> float:
        return 0


class EventVector:

    def __init__(self,
                 sport: Optional[int],
                 group: Optional[Group],
                 closed: Optional[bool],
                 recurring: Optional[bool],
                 play_times: Optional[List[EventPlayTimes]]
                 ):
        self.sport = sport
        self.group = group,
        self.closed = closed,
        self.recurring = recurring,
        self.play_time = play_times
