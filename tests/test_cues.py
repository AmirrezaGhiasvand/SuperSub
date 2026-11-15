import unittest
from app import reflow, stamp

class CueTests(unittest.TestCase):
    def test_limits_and_halfspace(self):
        words=[dict(start=i,end=i+.9,word=w) for i,w in enumerate(['من','می‌روم','خانه'])]
        cues=reflow(words,2)
        self.assertEqual([c['text'] for c in cues],['من می‌روم','خانه'])
    def test_pause(self):
        self.assertEqual(len(reflow([dict(start=0,end=1,word='سلام'),dict(start=3,end=4,word='خوبی؟')],8)),2)
    def test_stamp(self):
        self.assertEqual(stamp(3661.234),'01:01:01,234')
    def test_pause_threshold_and_no_subtitle_during_silence(self):
        words=[dict(start=0,end=.3,word='سلام'),dict(start=.9,end=1.2,word='خوبی')]
        cues=reflow(words,8)
        self.assertEqual(len(cues),2)
        self.assertEqual(cues[0]['end'],.3)
        self.assertEqual(len(reflow(words,8,pause=1)),1)
    def test_long_continuous_speech_still_splits(self):
        words=[dict(start=i,end=i+.9,word='word') for i in range(15)]
        cues=reflow(words,30)
        self.assertTrue(all(c['end']-c['start']<=6 for c in cues))
