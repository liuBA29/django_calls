import redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)
print(client.ping())  # Это проверит соединение с Redis

