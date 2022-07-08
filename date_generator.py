import sys
from datetime import datetime


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
		self.generate_date()

	def generate_date(self):
		m = range(1, 13)
		d = range(1, 32)
		for year in self.__year_range:
			for month in m:
				for day in d:
					self.__display_array[self.__display](year, month, day)

	def ymd(self, year, month, day):
		print(str(year) + self.__separator + "{:02d}".format(month) + self.__separator + "{:02d}".format(day))

	def dmy(self, year, month, day):
		print("{:02d}".format(day) + self.__separator + "{:02d}".format(month) + self.__separator + str(year))

	def mdy(self, year, month, day):
		print("{:02d}".format(month) + self.__separator + "{:02d}".format(day) + self.__separator + str(year))

	def dmys(self, year, month, day):
		print("{:02d}".format(day) + self.__separator + "{:02d}".format(month) + self.__separator + str(year)[-2:])



def main():
	if len(sys.argv) == 4:
		DateGenerator(sys.argv[1], sys.argv[2], sys.argv[3], "")
	elif len(sys.argv) == 5:
		DateGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print(
			"args:\n\t1: starting year\n\t2: ending year\n\t3: display format\n\t\t0 = yyyymmdd\n\t\t1 = ddmmyyyy\n\t\t2 = mmddyyyy\n\t\t3 = ddmmyy\n\t3: optional separator added in between")


if __name__ == '__main__':
	main()
