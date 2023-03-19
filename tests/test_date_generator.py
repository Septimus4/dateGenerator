import io
import unittest
from unittest.mock import patch
from date_generator import DateGenerator


class TestDateGenerator(unittest.TestCase):
    def test_generate_date(self):
        start_year = 2022
        end_year = 2023
        display_format = "0"
        separator = "-"
        date_gen = DateGenerator(start_year, end_year, display_format, separator)

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            date_gen.generate_date()
            result = fake_stdout.getvalue()
        with open("values/generate.txt", "r") as f:
            exp_output = f.read()
        self.assertEqual(result, exp_output)

    def test_ymd(self):
        # Given
        year = 2010
        month = 6
        day = 15
        separator = "-"
        exp_output = "2010-06-15\n"
        date_gen = DateGenerator(year, year, "0", separator)

        # When
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            date_gen.ymd(year, month, day)
            result = fake_stdout.getvalue()

        # Then
        self.assertEqual(result, exp_output)

    def test_dmy(self):
        # Given
        year = 2010
        month = 6
        day = 15
        separator = "-"
        exp_output = "15-06-2010\n"
        date_gen = DateGenerator(year, year, "1", separator)

        # When
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            date_gen.dmy(year, month, day)
            result = fake_stdout.getvalue()

        # Then
        self.assertEqual(result, exp_output)

    def test_mdy(self):
        # Given
        year = 2010
        month = 6
        day = 15
        separator = "/"
        exp_output = "06/15/2010\n"
        date_gen = DateGenerator(year, year, "2", separator)

        # When
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            date_gen.mdy(year, month, day)
            result = fake_stdout.getvalue()

        # Then
        self.assertEqual(result, exp_output)

    def test_dmys(self):
        # Given
        year = 2010
        month = 6
        day = 15
        separator = "/"
        exp_output = "15/06/10\n"
        date_gen = DateGenerator(year, year, "3", separator)

        # When
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            date_gen.dmys(year, month, day)
            result = fake_stdout.getvalue()

        # Then
        self.assertEqual(result, exp_output)


if __name__ == '__main__':
    unittest.main()
