import sys

class DateGenerator:
    def __init__(self, starting, ending, display, separator):
        self.__year_range = range(int(starting), int(ending))
        self.__display = display
        self.__separator = separator
        self.__display_array = {
            '0': self.ymd,
            '1': self.dmy,
            '2': self.mdy,
            '3': self.dmys
        }

    def generate_date(self):
        for year in self.__year_range:
            for month in range(1, 13):
                for day in range(1, 32):
                    self.__display_array[self.__display](year, month, day)

    def ymd(self, year, month, day):
        print(f"{year}{self.__separator}{month:02d}{self.__separator}{day:02d}")

    def dmy(self, year, month, day):
        print(f"{day:02d}{self.__separator}{month:02d}{self.__separator}{year}")

    def mdy(self, year, month, day):
        print(f"{month:02d}{self.__separator}{day:02d}{self.__separator}{year}")

    def dmys(self, year, month, day):
        print(f"{day:02d}{self.__separator}{month:02d}{self.__separator}{str(year)[-2:]}")

def main():
    if len(sys.argv) == 4:
        DateGenerator(sys.argv[1], sys.argv[2], sys.argv[3], "").generate_date()
    elif len(sys.argv) == 5:
        DateGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).generate_date()
    else:
        print("args:\n\t1: starting year\n\t2: ending year\n\t3: display format\n\t\t0 = yyyymmdd\n\t\t1 = ddmmyyyy\n\t\t2 = mmddyyyy\n\t\t3 = ddmmyy\n\t3: optional separator added in between")

if __name__ == '__main__':
    main()
