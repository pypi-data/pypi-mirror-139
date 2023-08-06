# Process all the tokens about temporal information

from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Optional, Dict, Union

class TimeGranularity(Enum):
    Second = 1
    Minute = 2
    Hour = 3
    Day = 4
    Week = 5
    WeekDay = 5.1
    Month = 6
    Quarter = 7
    Year = 8
    Decade = 9
    Century = 10
    Era = 11    # Dynamic time granularity


class BaseTimePoint(Enum):
    Now = 1
    Today = 2
    Monday = 3
    # FIRST_DAY = 4
    # SPRING = 6


class TimeFunction(Enum):
    Every = 1
    This = 2
    Last = 3
    Next = 4


class Tense(Enum):
    Future = 1
    Past = 2
    Now = 3


class TimePoint:

    def __init__(self, time_dict: Dict[TimeGranularity, Union[int]], tense: Tense = Tense.Now):
        self.time_dict = time_dict
        self.tense = tense

    def __str__(self) -> str:
        pass

    def __add__(self, other: TimePoint):
        time_dict = {}
        for gran in self.time_dict.keys() + other.time_dict.keys():
            pass

        self.time_dict
        return TimePoint()

    def __sub__(self, other: TimePoint):
        pass

    @property
    def is_monday(self):
        return self.time_dict.get(TimeGranularity.WeekDay) == 1


class SomeTime(TimePoint):

    def __init__(self):
        self.time_point = TimePoint({})

    def __add__(self, other: TimePoint):
        self.time_dict = self.time_dict + other


Now = SomeTime()


class TimeInterval:

    def __init__(self, interval: TimePoint) -> None:
        self.interval = interval


class TimeListInterval(TimeInterval):

    def __init__(self, times: List[TimePoint]):
        pass

    def __add__(self, other: TimePoint):
        pass

    def __sub__(self, other: TimePoint):
        pass


class StartEndInterval(TimeInterval):

    def __init__(self, start: TimePoint, end: TimePoint):
        self.start = start
        self.end = end

    @property
    def lasting_time(self):
        pass


AD = TimePoint({TimeGranularity.YEAR: 0})

# On monday, 指的是这周周一，还是普遍意义的周一？也许两者都有，取决于具体的语境
# 根据上一句中的时间可以推断出这句的on Monday含义
Monday = TimePoint({
    # TimeGranularity.Week: TimeFunction.Every,
    TimeGranularity.WeekDay: 1,
})
Tuesday = Monday + TimePoint({TimeGranularity.WeekDay: 1})
Wednesday = Tuesday + TimePoint({TimeGranularity.WeekDay: 1})
Thursday = Wednesday + TimePoint({TimeGranularity.WeekDay: 1})
Friday = Thursday + TimePoint({TimeGranularity.WeekDay: 1})
Saturday = Friday + TimePoint({TimeGranularity.WeekDay: 1})
Sunday = Saturday + TimePoint({TimeGranularity.WeekDay: 1})

January = TimePoint({
    TimeGranularity.Month: 1,
})
February = January + TimePoint({TimeGranularity.Month: 1})
March = February + TimePoint({TimeGranularity.Month: 1})
April = March + TimePoint({TimeGranularity.Month: 1})
May = April + TimePoint({TimeGranularity.Month: 1})
June = May + TimePoint({TimeGranularity.Month: 1})
July = June + TimePoint({TimeGranularity.Month: 1})
August = July + TimePoint({TimeGranularity.Month: 1})
September = August + TimePoint({TimeGranularity.Month: 1})
October = September + TimePoint({TimeGranularity.Month: 1})
November = October + TimePoint({TimeGranularity.Month: 1})
December = November + TimePoint({TimeGranularity.Month: 1})

Spring = TimeListInterval([February, March, April])
Summer = TimeListInterval([May, June, July])
Autumn = TimeListInterval([August, September, October])
Winter = TimeListInterval([November, December, January])

# 需要模糊的概念，正态分布函数
Morning = TimePoint({TimeGranularity.Day: TimeFunction.Every, TimeGranularity.Hour: [6, 7, 8, 9, 10, 11]})
Noon = TimePoint({TimeGranularity.Day: TimeFunction.Every, TimeGranularity.Hour: 12}),
Afternoon = TimeListInterval([
    TimePoint({TimeGranularity.Day: TimeFunction.Every, TimeGranularity.Hour: [13, 14, 15, 16, 17]}),
])
Evening = TimePoint({
    TimeGranularity.Day: TimeFunction.Every, TimeGranularity.Hour: [18, 19, 20],
})
Night = TimePoint({
    TimeGranularity.Day: TimeFunction.Every, TimeGranularity.Hour: [21, 22, 23],
})


def resolve_time(text_object):
    pass





# 时间的表达
# 1、今天
# 2、明天 = （今天，）
# 3、2000 = 元年 + （2000， 年） + （5，月） + （1，日）

# 时间是否重复，取决于起始时间是否是周期性的
# 3、一月份，重复性的时间，[StartYear, StartYear + （30，日）]
# 4、二月份 = 一月份 + （30, 日）
# 5、2000年一月份 = 元年 + （2000, 年） + [Start(Year), Start(Year) + （30，日）]