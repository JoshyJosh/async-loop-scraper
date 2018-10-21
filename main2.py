# Taken from https://stackabuse.com/python-async-await-tutorial/
import signal
import sys
import asyncio
import aiohttp
import json

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)

asyncdict = {'python': False, 'programming': False, 'compsci': False}

async def get_json(client, url):
    async with client.get(url) as response:
        assert response.status == 200
        data = response.read()
        # response.close()
        return await data

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

    print('DONE:', subreddit + '\n')

    asyncdict[subreddit] = True
    return result_strings

async def check_completed():
    print("made it here")
    if asyncdict.count(True) == 3:
        import pdb; pdb.set_trace()

task1 = asyncio.gather(get_reddit_top('python', client))
task2 = asyncio.gather(get_reddit_top('programming', client))
task3 = asyncio.gather(get_reddit_top('compsci', client))
# foo4 = asyncio.ensure_future(check_completed())

all_tasks = asyncio.gather(task1, task2, task3)

results = loop.run_until_complete(all_tasks)

client.close()

loop.close()

print(results)

#
# async def get_reddit_top(subreddit, client):
#     data1 = await get_json(client, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')
#
#     j = json.loads(data1.decode('utf-8'))
#     for i in j['data']['children']:
#         score = i['data']['score']
#         title = i['data']['title']
#         link = i['data']['url']
#         print(str(score) + ': ' + title + ' (' + link + ')')
#
#     print('DONE:', subreddit + '\n')
#
# # Takes keyboard signal and runs the following method
# def signal_handler(signal, frame):
#     loop.stop()
#     client.close()
#     sys.exit(0)
#
# # overrides SIGINT (KeyboardInterrupt)
# signal.signal(signal.SIGINT, signal_handler)
#
#
# # TODO make this async
# async def all_of_my_asyncs():
#     task1 = get_reddit_top('python', client)
#     task2 = get_reddit_top('programming', client)
#     task3 = get_reddit_top('compsci', client)
#
#
# loop.run_forever()
