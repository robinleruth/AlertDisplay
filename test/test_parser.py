import datetime as dt
import unittest

from app.domain.services.parser.absolute_parser import AbsoluteParser
from app.domain.services.parser.cron_parser import CronParser
from app.domain.services.parser.relative_parser import RelativeParser


class TestParser(unittest.TestCase):
    def test_absolute(self):
        time = "2021-03-30 15:20"
        p = AbsoluteParser()
        d = p.parse(time)
        datetime = dt.datetime(2021, 3, 30, 15, 20)
        self.assertEqual(datetime, d)

    def test_cron(self):
        cron = '15 * * * *'
        p = CronParser()
        d = p.parse(cron, now=dt.datetime(2021, 3, 30, 15, 20))
        datetime = dt.datetime(2021, 3, 30, 16, 15)
        self.assertEqual(datetime, d)
        time = '+15m'
        self.assertRaises(Exception, p.parse, time)
        time = '2021-03-30 15:20'
        self.assertRaises(Exception, p.parse, time)

    def test_relative(self):
        time = "+15m"
        p = RelativeParser()
        d = p.parse(time, now=dt.datetime(2021, 3, 30, 15, 20))
        datetime = dt.datetime(2021, 3, 30, 15, 35)
        self.assertEqual(datetime, d)
        time = "+15s"
        d = p.parse(time, now=dt.datetime(2021, 3, 30, 15, 20))
        datetime = dt.datetime(2021, 3, 30, 15, 20, 15)
        self.assertEqual(datetime, d)
        time = "+1h15m"
        d = p.parse(time, now=dt.datetime(2021, 3, 30, 15, 20))
        datetime = dt.datetime(2021, 3, 30, 16, 35)
        self.assertEqual(datetime, d)

    def test_relative_parse(self):
        p = RelativeParser()
        time = "+15m"
        r = p._parse(time)
        self.assertEqual(0, r.hours)
        self.assertEqual(15, r.minutes)
        self.assertEqual(0, r.seconds)
        time = "+15s"
        r = p._parse(time)
        self.assertEqual(0, r.hours)
        self.assertEqual(0, r.minutes)
        self.assertEqual(15, r.seconds)
        time = "+2h"
        r = p._parse(time)
        self.assertEqual(2, r.hours)
        self.assertEqual(0, r.minutes)
        self.assertEqual(0, r.seconds)
        time = "+1h15m"
        r = p._parse(time)
        self.assertEqual(1, r.hours)
        self.assertEqual(15, r.minutes)
        self.assertEqual(0, r.seconds)
        time = "+1h10s"
        r = p._parse(time)
        self.assertEqual(1, r.hours)
        self.assertEqual(0, r.minutes)
        self.assertEqual(10, r.seconds)
        time = "1h10s"
        r = p._parse(time)
        self.assertEqual(1, r.hours)
        self.assertEqual(0, r.minutes)
        self.assertEqual(10, r.seconds)
