from unittest import TestCase
from mars_planner import *


class TestRoverState(TestCase):
    pass


class Test(TestCase):
    def  test_move_to_sample(self):
        s = RoverState(loc="battery")
        s2 = move_to_sample(s)
        self.assertEqual(s2.loc, "sample")

    def test_eq(self):
        s = RoverState(loc="battery")
        s2 = RoverState(loc="battery")
        self.assertEqual(s,s2)
        s3 = RoverState(loc="station")
        self.assertNotEqual(s, s3)


class TestRoverState(TestCase):
    def test_successors(self):
        s=RoverState()
        slist = s.successors(action_list)
        print(slist)
