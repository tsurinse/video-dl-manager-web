import os
import pathlib
import sys

import redis


# General
ytdl_output_format = '%(title)s [%(id)s].%(ext)s'


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
    url  = k.decode('UTF-8')
    dest = r[k].decode('UTF-8')

    if dest[-1] != '/':
        dest += '/'

    print()
    print(url, '->', dest)

    # Make directory path if it doesn't exist
    pathlib.Path(dest).mkdir(parents=True, exist_ok=True)

    os.system('youtube-dl "{}" -o "{}{}"'.format(url, dest, ytdl_output_format))
    r.delete(k)
