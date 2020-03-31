import unittest
from unittest.mock import patch
import sys

from .. import play
from ..utils import config


class Test(unittest.TestCase):

    def setUp(self):
        # Get config
        play.conf = config.getConfig()

    def test_showBank(self):
        play.currentBank = 10
        self.assertIsNone(play.showBank())

    def test_updateBank(self):
        play.currentBank = 10
        play.updateBank(10)
        self.assertEqual(play.currentBank, 20)

    def test_checkBankStatus(self):
        play.currentBank = 10
        self.assertIsNone(play.checkBankStatus())

    def test_checkBankStatus_2(self):
        play.currentBank = -10
        self.assertRaises(SystemExit, play.checkBankStatus)

    def test_amountToCurrency(self):
        self.assertEqual(play.amountToCurrency(10), '$10.00')

    def test_getMaxPossibleBet(self):
        play.currentBank = 10
        self.assertEqual(play.getMaxPossibleBet(10000), 10)
        play.currentBank = 999999
        self.assertEqual(play.getMaxPossibleBet(10000), 10000)

    def test_wheel(self):
        from ..vars.numbers import french
        from ..vars.bets import addColors

        play.withColors = addColors(french)
        self.assertIsInstance(play.wheel(), list)

    def test_game(self):
        from ..vars.numbers import french
        from ..vars.bets import addColors

        play.withColors = addColors(french)
        play.currentBank = 10
        self.assertIsInstance(play.game(), tuple)

    def test_getOutcome(self):
        self.assertIsNone(play.getOutcome(10, {'name': '19 to 36', 'winningSpaces': [
            1, 3], 'payout': (1, 1), 'type': 'any'}))

    def test_getOutcome_2(self):
        self.assertIsNone(play.getOutcome(10, {'name': '19 to 36', 'winningSpaces': [
            1, 3], 'payout': (1, 1), 'type': 'any'},
            specificChoice=5))

    def test_getColorIcon(self):
        if play.isUnicodeSupported():
            self.assertEqual(play.getColorIcon('red'), u"\U0001F534")
            self.assertEqual(play.getColorIcon('black'), u"\u2B24")
            self.assertEqual(play.getColorIcon('green'), u"\U0001F49A")
        else:
            self.assertEqual(play.getColorIcon('red'), 'R')
            self.assertEqual(play.getColorIcon('black'), 'B')
            self.assertEqual(play.getColorIcon('green'), 'G')

    def test_sleep(self):
        self.assertIsNone(play.sleep(1, 100))

    def test_isUnicodeSupported(self):
        self.assertIsInstance(play.isUnicodeSupported(), bool)

    def test_betsTable(self):
        self.assertIsNone(play.betsTable())

    def test_isBetTypeValid(self):
        from ..vars.bets import bets

        play.bets = bets
        self.assertTrue(play.isBetTypeValid(2))
        self.assertFalse(play.isBetTypeValid(44))
        self.assertFalse(play.isBetTypeValid('abc'))

    def test_getBet(self):
        from ..vars.bets import bets

        play.bets = bets
        self.assertIsInstance(play.getBet(2), dict)

    def test_isBetAmountValid(self):
        self.assertTrue(play.isBetAmountValid(10, 5, 100))
        self.assertFalse(play.isBetAmountValid(1, 5, 100))

    def test_isSpecificChoiceValid(self):
        self.assertFalse(play.isSpecificChoiceValid('00', 'french'))
        self.assertTrue(play.isSpecificChoiceValid('00', 'american'))
        self.assertTrue(play.isSpecificChoiceValid(5, 'french'))
        self.assertTrue(play.isSpecificChoiceValid(5, 'american'))
        self.assertFalse(play.isSpecificChoiceValid(55, 'french'))
        self.assertFalse(play.isSpecificChoiceValid(55, 'american'))

    def test_play(self):
        with unittest.mock.patch('builtins.input', return_value='17'):
            play.currentBank = 20
            play.play(break_=True)

    def test_firstPlay(self):
        with unittest.mock.patch('builtins.input', return_value='17'):
            play.firstPlay(bank=20, break_=True)
