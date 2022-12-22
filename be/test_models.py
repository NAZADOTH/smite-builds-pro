import copy
import logging
import unittest.mock

import be.models
from be.models import MyError

be.models.auto_fixes_logger.setLevel(logging.ERROR)


class TestFixRoles(unittest.TestCase):
    BUILDS = [
        {
            "role": "ADC",
            "team1": "A",
            "god1": "A1",
            "player1": "A1",
            "god2": "B1",
            "player2": "B1",
        },
        {
            "role": "Jungle",
            "team1": "A",
            "god1": "A2",
            "player1": "A2",
            "god2": "B2",
            "player2": "B2",
        },
        {
            "role": "Mid",
            "team1": "A",
            "god1": "A3",
            "player1": "A3",
            "god2": "B3",
            "player2": "B3",
        },
        {
            "role": "Solo",
            "team1": "A",
            "god1": "A4",
            "player1": "A4",
            "god2": "B4",
            "player2": "B4",
        },
        {
            "role": "Support",
            "team1": "A",
            "god1": "A5",
            "player1": "A5",
            "god2": "B5",
            "player2": "B5",
        },
        {
            "role": "ADC",
            "team1": "B",
            "god1": "B1",
            "player1": "B1",
            "god2": "A1",
            "player2": "A1",
        },
        {
            "role": "Jungle",
            "team1": "B",
            "god1": "B2",
            "player1": "B2",
            "god2": "A2",
            "player2": "A2",
        },
        {
            "role": "Mid",
            "team1": "B",
            "god1": "B3",
            "player1": "B3",
            "god2": "A3",
            "player2": "A3",
        },
        {
            "role": "Solo",
            "team1": "B",
            "god1": "B4",
            "player1": "B4",
            "god2": "A4",
            "player2": "A4",
        },
        {
            "role": "Support",
            "team1": "B",
            "god1": "B5",
            "player1": "B5",
            "god2": "A5",
            "player2": "A5",
        },
    ]

    def test_happy(self):
        builds = copy.deepcopy(self.BUILDS)
        be.models.fix_roles_in_single_game(builds)
        self.assertEqual(builds, self.BUILDS)

    def test_illegal(self):
        # Three teams.
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["team1"] = "C"
        with self.assertRaises(MyError):
            be.models.fix_roles_in_single_game(builds)

        # One team.
        builds = copy.deepcopy(self.BUILDS)
        for build in builds:
            build["team1"] = "A"
        with self.assertRaises(MyError):
            be.models.fix_roles_in_single_game(builds)

        # Six player vs four players.
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["team1"] = "B"
        with self.assertRaises(MyError):
            be.models.fix_roles_in_single_game(builds)

    @unittest.mock.patch("be.models.get_player_count_with_team")
    def test_fixable_2a(self, mock):
        # Situation 2a.
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["role"] = "Coach"
        be.models.fix_roles_in_single_game(builds)
        self.assertEqual(builds, self.BUILDS)

        # Situation 2b.
        mock.side_effect = [0, 1]
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["role"] = "Mid"
        be.models.fix_roles_in_single_game(builds)
        self.assertEqual(builds, self.BUILDS)

        # 2a + 2b.
        mock.side_effect = [0, 1]
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["role"] = "Coach"
        builds[5]["role"] = "Mid"
        be.models.fix_roles_in_single_game(builds)
        self.assertEqual(builds, self.BUILDS)

    @unittest.mock.patch("be.models.get_player_count_with_team")
    def test_unfixable(self, mock):
        # Coach + Sub.
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["role"] = "Coach"
        builds[1]["role"] = "Sub"
        be.models.fix_roles_in_single_game(builds)
        self.assertNotEqual(builds, self.BUILDS)

        # Sub + Sub.
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["role"] = "Sub"
        builds[1]["role"] = "Sub"
        be.models.fix_roles_in_single_game(builds)
        self.assertNotEqual(builds, self.BUILDS)

        # Mid + Mid + Mid.
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["role"] = "Mid"
        builds[1]["role"] = "Mid"
        be.models.fix_roles_in_single_game(builds)
        self.assertNotEqual(builds, self.BUILDS)

        # Missing build.
        builds = copy.deepcopy(self.BUILDS)
        del builds[0]
        be.models.fix_roles_in_single_game(builds)
        self.assertNotEqual(builds, self.BUILDS)

        # Mid + Mid (same count).
        mock.side_effect = [1, 1]
        builds = copy.deepcopy(self.BUILDS)
        builds[0]["role"] = "Mid"
        be.models.fix_roles_in_single_game(builds)
        self.assertNotEqual(builds, self.BUILDS)


if __name__ == "__main__":
    unittest.main()