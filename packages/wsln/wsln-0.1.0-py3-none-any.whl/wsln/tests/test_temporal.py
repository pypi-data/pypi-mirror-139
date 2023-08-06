from wsln.temporal import (
    January, Saturday, TimeFunction, TimeInterval, TimePoint, Today, TimeGranularity, TimeListInterval
    Today,
    Monday, Tuesday, Wednesday, Week
    Weekday, Weekend
)

def test_resolve_atomic_time():
    cases = [
        ("today", Today),
        ("last week", Today - TimePoint({TimeGranularity.Week: -1})),
        ("every week", TimePoint({TimeGranularity.Week: TimeFunction.Every})),
        ("weekend", WeekEnd),
        ("weekday", WeekDay),
        ("the first month", January),
        ("January", January),
        ("9 am", TimePoint({TimeGranularity.Hour: 9})),
        ("9 pm", TimePoint({TimeGranularity.Hour: 21})),
        ("nine ten", TimePoint({TimeGranularity.Hour: 9, TimeGranularity.Mintue: 10})),
        ("nine ten", TimePoint({TimeGranularity.Hour: 9, TimeGranularity.Mintue: 10})),
        ("for two days", TimeInterval(Today, Today + {TimeGranularity.Day: 2})),
    ]

    for case in cases:
        pass




# def test_resolve_period_time():
#         (
#             Phrase([
#                 Token("good", TokenTag.ADJ),
#                 Token("morning", TokenTag.NOUN),
#             ], TokenTag.NOUN),
#             TimeInterval(BaseTime.TODAY, ),
#         ),

# def test_resolve_specific_time():
#     (
#         Phrase([
#             Token("good", TokenTag.ADJ),
#             Token("morning", TokenTag.NOUN),
#         ], TokenTag.NOUN),
#         TimeInterval(BaseTime.TODAY, ),
#     ),


# def test_resolve_compound_time():
#     cases = [
#         (
#             [
#                 Phrase([
#                     Token("two", TokenTag.ADJ),
#                     Token("weeks", TokenTag.NOUN),
#                 ]),
#                 Token("ago", TokenTag.ADV),
#             ],
#             TimePoint()
#         ),
#         (
#             Phrase()
#         )
#     ]