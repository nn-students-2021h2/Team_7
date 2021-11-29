from datetime import datetime

from get_time_package.module_name.package1.unix_time_module import get_time


def print_time(unixtime):
    for_t = datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    print(for_t)


def main():
    unixtime = get_time()
    print_time(unixtime)


if __name__ == '__main__':
    main()
