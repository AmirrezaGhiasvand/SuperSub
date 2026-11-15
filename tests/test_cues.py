import unittest
from app import reflow, stamp

class CueTests(unittest.TestCase):
    def test_limits_and_halfspace(self):
        words=[dict(start=i,end=i+.5,word=w) for i,w in enumerate(['من','می‌روم','خانه'])]
        cues=reflow(words,2)
        self.assertEqual([c['text'] for c in cues],['من می‌روم','خانه'])
    def test_pause(self):
        self.assertEqual(len(reflow([dict(start=0,end=1,word='سلام'),dict(start=3,end=4,word='خوبی؟')],8)),2)
    def test_stamp(self):
        self.assertEqual(stamp(3661.234),'01:01:01,234')
