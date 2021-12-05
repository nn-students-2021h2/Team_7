from datetime import datetime

from unixtime_pkg.get_time_pkg.main import get_time


def print_time(unixtime: int):
    pretty_time = datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    print(pretty_time)


def main():
    unixtime = get_time()
    print_time(unixtime)


if __name__ == '__main__':
    main()
