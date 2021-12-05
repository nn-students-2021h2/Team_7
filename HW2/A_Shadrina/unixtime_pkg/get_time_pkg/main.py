import requests

URL = 'http://worldtimeapi.org/api/timezone/Europe/Moscow'


def get_time() -> int:
    response = requests.get(URL)
    unixtime = response.json()['unixtime']
    return unixtime


def main():
    unixtime = get_time()
    print(unixtime)


if __name__ == '__main__':
    main()
