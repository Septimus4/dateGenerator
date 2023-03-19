import sys
import calendar

class DateGenerator:
    def __init__(self, starting, ending, display, separator):
        self.year_range = [int(start) for start in [starting, ending]]
        self.display = display
        self.separator = separator
        self.display_array = {
            '0': self.ymd,
            '1': self.dmy,
            '2': self.mdy,
            '3': self.dmys
        }

    def generate_date(self):
        dispatch = self.display_array[self.display]
        for year in range(*self.year_range):
            for month in range(1, 13):
                _, last_day = calendar.monthrange(year, month)
                for day in range(1, last_day + 1):
                    dispatch(year, month, day)

    def ymd(self, year, month, day):
        print(f"{year}{self.separator}{month:02d}{self.separator}{day:02d}")

    def dmy(self, year, month, day):
        print(f"{day:02d}{self.separator}{month:02d}{self.separator}{year}")

    def mdy(self, year, month, day):
        print(f"{month:02d}{self.separator}{day:02d}{self.separator}{year}")

    def dmys(self, year, month, day):
        print(f"{day:02d}{self.separator}{month:02d}{self.separator}{str(year)[-2:]}")

def main():
    if len(sys.argv) == 4:
        DateGenerator(sys.argv[1], sys.argv[2], sys.argv[3], "").generate_date()
    elif len(sys.argv) == 5:
        DateGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).generate_date()
    else:
        print("args:\n\t1: starting year\n\t2: ending year\n\t3: display format\n\t\t0 = yyyymmdd\n\t\t1 = ddmmyyyy\n\t\t2 = mmddyyyy\n\t\t3 = ddmmyy\n\t3: optional separator added in between")

if __name__ == '__main__':
    main()
