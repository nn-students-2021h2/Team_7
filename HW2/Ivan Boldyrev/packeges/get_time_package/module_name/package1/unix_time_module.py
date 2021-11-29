import requests


def get_time():
    u = 'http://worldtimeapi.org/api/timezone/Europe/Moscow'
    res = requests.get(u)
    unixtime = res.json()['unixtime']
    return unixtime


def print_time(unixtime):
    print(unixtime)


def main():
    unixtime = get_time()
    print_time(unixtime)


if __name__ == '__main__':
    main()
