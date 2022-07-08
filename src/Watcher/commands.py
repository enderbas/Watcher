import os
import csv
import datetime
from watch_log import get_date
import analysis as anls
import time_operations as to

class Color:

    def GREY(text):
        return '\033[90m' + text + '\033[0m'

    def BLUE(text):
        return '\033[34m' + text + '\033[0m'

    def GREEN(text):
        return '\033[32m' + text + '\033[0m'

    def YELLOW(text):
        return '\033[33m' + text + '\033[0m'

    def RED(text):
        return '\033[31m' + text + '\033[0m'

    def PURPLE(text):
        return '\033[35m' + text + '\033[0m'

    def DARKCYAN(text):
        return '\033[36m' + text + '\033[0m'

    def BOLD(text):
        return '\033[1m' + text + '\033[0m'

    def UNDERLINE(text):
        return '\033[4m' + text + '\033[0m'


def daily_summary():
    date = get_date()
    window_opened, time_spent = anls.extract_data(date)
    Total_screen_time = "00:00:00"
    for x,y in anls.final_report(window_opened, time_spent).items():
        Total_screen_time = to.time_addition(y, Total_screen_time)

    if len(to.format_time(Total_screen_time)) == 3:
        print(Color.YELLOW("\n   Today's Screen-Time\t\t   ") + Color.BLUE(f'{to.format_time(Total_screen_time):>16}'))
    elif len(to.format_time(Total_screen_time)) == 7:
        print(Color.YELLOW("\n   Today's Screen-Time\t\t   ") + Color.BLUE(f'{to.format_time(Total_screen_time):>11}'))
    elif len(to.format_time(Total_screen_time)) == 11:
            print(Color.YELLOW("\n   Today's Screen-Time\t\t   ") + Color.BLUE(to.format_time(Total_screen_time)))

    print(" ────────────────────────────────────────────────")
    print(Color.RED(f'{" App Usages":>29}'))
    print(" ────────────────────────────────────────────────")

    for x,y in anls.final_report(window_opened, time_spent).items():
        if x == "":
            x = "Home-Screen"
        print("   " + Color.GREEN(f'{x:<22}') + '\t ',f'{to.format_time(y):>12}')

def week_summary():
    W_Y = os.popen('''date +"W%V-%Y"''').read()[0:-1]
    user = os.getlogin()
    filename = "/home/"+user+"/.cache/Watcher/Analysis/"+W_Y+".csv"
    with open(filename, 'r') as file:
        csvreader = csv.reader(file, delimiter='\t')
        week_overview = dict()
        app_usages = dict()
        for row in csvreader:
            if len(row[0]) == 3:
                week_overview.update({row[0]:row[1]}) # Weekday -- screen-time
            else:
                app_usages.update({row[1]:row[0]}) # app-name -- usage

    week_screen_time = "00:00:00"
    for x, y in week_overview.items():
        week_screen_time = to.time_addition(y, week_screen_time)

    print(Color.PURPLE("\n   Week's screen-time\t\t   ") + Color.BLUE(to.format_time(week_screen_time)))
    print(" ────────────────────────────────────────────────")

    for x, y in week_overview.items():
        print("  " + f'{Color.YELLOW(x):>21}' + "\t\t   " + Color.BLUE(to.format_time(y)))

    #anls.prints_report(window_opened, time_spent, is_week)
    print(" ────────────────────────────────────────────────")
    print(Color.RED(f'{" App Usages":>29}'))
    print(" ────────────────────────────────────────────────")
    for x,y in app_usages.items():
        if x == "":
            x = "Home-Screen"
        print("   " + Color.GREEN(f'{x:<22}') + '\t ',f'{to.format_time(y):>12}')

if __name__ == "__main__":
    week_summary()
