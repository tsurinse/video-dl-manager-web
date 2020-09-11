import os
import sys

import redis


# Redis init
redis_url = ''

if len(sys.argv) > 1:
    redis_url = sys.argv[1]
elif 'REDIS_URL' in os.environ:
    redis_url = os.environ['REDIS_URL']

r = redis.Redis.from_url(redis_url)


# Download videos
print('{} in queue'.format(len(r.keys())))

for k in r.keys('*'):
    print()
    print(k.decode('UTF-8'), '->', r[k].decode('UTF-8'))

    os.system('youtube-dl "{}" -o "{}"'.format(k.decode('UTF-8'), r[k].decode('UTF-8')))
    r.delete(k)
