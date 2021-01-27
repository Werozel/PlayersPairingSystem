from typing import Optional, List
from datetime import datetime
from src.misc import datetime_to_seconds, time_to_seconds
import math

from libs.models.EventPlayTimes import EventPlayTimes
from libs.models.Group import Group
from libs.models.PlayTime import PlayTime
from libs.models.User import User
from libs.models.Event import Event


# Need:
#       User to Event
#       Event to User

class UserVector:

    def __init__(self,
                 age: Optional[int] = None,
                 gender: Optional[str] = None,
                 sport: Optional[List[int]] = None,
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

    def calculate_diff_with_user(self, other) -> float:
        result: float = 0
        if self.age and other.age:
            result += 100 * (10 - math.fabs(other.age - self.age))
        if self.gender and other.gender:
            result += 100 * int(self.gender == other.gender)
        if self.sport and other.sport:
            my_sport_set = set(self.sport)
            other_sport_set = set(other.sport)
            result += 10000 * len(my_sport_set.intersection(other_sport_set))
        if self.city and other.city:
            result += 10000 * int(self.city != other.city)
        if self.last_login and other.last_login:
            divider = math.fabs(
                datetime_to_seconds(self.last_login) - datetime_to_seconds(other.last_login)
            )
            result += 100 * (604800 / divider) if divider else 0
        if self.include_play_times and self.play_times and other.play_times:
            result -= 100 * UserVector.calculate_play_times_diff(self.play_times, other.play_times)
        return result

    def calculate_diff_with_event(self, event) -> float:
        result: float = 0
        if self.sport and event.sport:
            my_sport_set = set(self.sport)
            other_sport_set = set(event.sport)
            result += 10000 * len(my_sport_set.intersection(other_sport_set))
        if self.city and event.city:
            result += 10000 * int(self.city != event.city)
        if self.last_login and event.last_login:
            divider = math.fabs(
                datetime_to_seconds(self.last_login) - datetime_to_seconds(event.last_login)
            )
            result += 100 * (604800 / divider) if divider else 0
        if self.include_play_times and self.play_times:
            result -= 100 * UserVector.calculate_play_times_diff(self.play_times, event.play_times) \
                if event.play_times \
                else 10000000000
        return result

    @staticmethod
    def calculate_play_times_diff(my_pts: list, other_pts: list) -> float:
        res_list = []

        for my_pt in my_pts:
            res = 100000000000
            for other_pt in other_pts:
                res = min(
                    10 * abs(my_pt.day_of_week - other_pt.day_of_week) + abs(time_to_seconds(my_pt.start_time) - time_to_seconds(other_pt.start_time)),
                    res
                )
            res_list.append(res)

        return sum(res_list) / len(res_list)


class EventVector:

    def __init__(self,
                 sport: Optional[List[int]],
                 city: Optional[str],
                 group: Optional[Group],
                 closed: Optional[bool],
                 last_login: Optional[datetime],
                 play_times: Optional[List[EventPlayTimes]],
                 event: Optional[Event]
                 ):
        self.sport = sport
        self.city = city
        self.group = group
        self.closed = closed
        self.last_login = last_login
        self.play_times = play_times
        self.event = event
