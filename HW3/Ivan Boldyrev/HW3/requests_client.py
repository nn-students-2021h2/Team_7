import time

import requests

start = time.time()
for i in range(1000):
    r = requests.get('http://127.0.0.1:5000/factorial', params={'n': 10})
    # print(r.text)
stop = time.time()
print('TIME: ', stop-start)
print('RPS: ', 1000/(stop-start))
