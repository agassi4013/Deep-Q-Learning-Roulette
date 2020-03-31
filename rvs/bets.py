
from .numbers import *

bets = (
    {
        'name': '0',
        'winningSpaces': [0],
        'payout': (35, 1),
        'type': 'any'
    },
    {
        'name': '00',
        'winningSpaces': ['00'],
        'payout': (35, 1),
        'type': 'any'
    },
    {
        'name': 'Straight up',
        'winningSpaces': list(range(0, 37)),
        'payout': (35, 1),
        'type': 'pickone'
    },
    {
        'name': 'Row',
        'winningSpaces': [0, '00'],
        'payout': (17, 1),
        'type': 'any'
    },
    {
        'name': 'Top line or Basket',
        'winningSpaces': [0, '00', 1, 2, 3],
        'payout': (5, 1),
        'type': 'any'
    },
    {
        'name': '1st column',
        'winningSpaces': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
        'payout': (2, 1),
        'type': 'any'
    },
    {
        'name': '2nd column',
        'winningSpaces': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        'payout': (2, 1),
        'type': 'any'
    },
    {
        'name': '3rd column',
        'winningSpaces': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        'payout': (2, 1),
        'type': 'any'
    },
    {
        'name': '1st dozen',
        'winningSpaces': list(range(1, 13)),
        'payout': (2, 1),
        'type': 'any'
    },
    {
        'name': '2nd dozen',
        'winningSpaces': list(range(13, 25)),
        'payout': (2, 1),
        'type': 'any'
    },
    {
        'name': '3rd dozen',
        'winningSpaces': list(range(25, 37)),
        'payout': (2, 1),
        'type': 'any'
    },
    {
        'name': 'Odd',
        'winningSpaces': [item for item in range(1, 37) if item % 2],
        'payout': (1, 1),
        'type': 'any'
    },
    {
        'name': 'Even',
        'winningSpaces': [item for item in range(1, 37) if not item % 2],
        'payout': (1, 1),
        'type': 'any'
    },
    {
        'name': 'Red',
        'winningSpaces': list(red),
        'payout': (1, 1),
        'type': 'any'
    },
    {
        'name': 'Black',
        'winningSpaces': list(black),
        'payout': (1, 1),
        'type': 'any'
    },
    {
        'name': '1 to 18',
        'winningSpaces': list(range(1, 19)),
        'payout': (1, 1),
        'type': 'any'
    },
    {
        'name': '19 to 36',
        'winningSpaces': list(range(19, 37)),
        'payout': (1, 1),
        'type': 'any'
    },
	{
		'name': 'Exit',
		'winningSpaces': [37],
		'payout': (1, 1),
		'type': 'any'
	},
)
