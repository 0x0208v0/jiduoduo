import redis

if __name__ == '__main__':
    host = f'redis'
    password = None
    client = redis.Redis(host=host, port=6379, db=0, password=password)
    print(client.info())
