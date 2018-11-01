# Adapted from https://stackabuse.com/python-async-await-tutorial/
import signal
import sys
import asyncio
import aiohttp
import json

loop = asyncio.get_event_loop()
conn = aiohttp.TCPConnector()
client = aiohttp.ClientSession(loop=loop, connector=conn)

asyncdict = {'python': False, 'programming': False, 'compsci': False}


async def get_json(client, url):
    async with client.get(url) as response:
        assert response.status == 200
        data = await response.read()
        return data


async def get_reddit_top(subreddit, client):
    data1 = await get_json(client, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')

    j = json.loads(data1.decode('utf-8'))
    result_strings = []
    for i in j['data']['children']:
        score = i['data']['score']
        title = i['data']['title']
        link = i['data']['url']
        result_string = str(score) + ': ' + title + ' (' + link + ')'
        result_strings.append(result_string)

    print('\nDONE:', subreddit + '\n')
    print(result_strings)

    return result_strings


task1 = asyncio.gather(get_reddit_top('python', client))
task2 = asyncio.gather(get_reddit_top('programming', client))
task3 = asyncio.gather(get_reddit_top('compsci', client))
# foo4 = asyncio.ensure_future(check_completed())

all_tasks = asyncio.gather(task1, task2, task3)

try:
    results = loop.run_until_complete(all_tasks)
finally:
    # Gracefully close connection
    loop.run_until_complete(client.close())
    conn.close()
    loop.close()
