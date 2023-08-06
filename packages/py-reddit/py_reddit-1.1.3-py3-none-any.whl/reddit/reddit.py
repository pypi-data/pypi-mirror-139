import requests
import string
import random
import aiohttp
import asyncio


class Client():
    """
    Represents a synchronous Client for fetching reddit posts 
    """

    def __init__(self, agent, key):
        self.agent = agent
        self.key = key

    class Subreddit():
        r"""
        Gets the raw data on a subreddit, which can be fetched via the various methods here
        """

        def __init__(self, type, name):
            self.name = name
            self.type = type
            self.agent = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8))
            if type == 'top':
                self.json = requests.get(
                    'https://www.reddit.com/r/{}/top/.json'.format(name), headers={'User-Agent': self.agent}).json()
            elif type == 'hot':
                self.json = requests.get(
                    'https://www.reddit.com/r/{}/hot/.json'.format(name), headers={'User-Agent': self.agent}).json()
            elif type == 'new':
                self.json = requests.get(
                    'https://www.reddit.com/r/{}/new/.json'.format(name), headers={'User-Agent': self.agent}).json()

        def selftext(self, index: int):
            r"""Returns the selftext of the post at the specified index
                Example: reddit.Subreddit('top', 'python').selftext(0)"""
            return self.json['data']['children'][index]['data']['selftext']

        def title(self, index: int):
            r"""Returns the title of the post at the specified index
                Example: reddit.Subreddit('top', 'python').title(0)"""
            return self.json['data']['children'][index]['data']['title']

        def post_url(self, index: int):
            r"""Returns the url of the post at the specified index
                  Example: reddit.Subreddit('top', 'python').url(0)"""
            # return the reddit link of the post
            return 'https://reddit.com' + self.json['data']['children'][index]['data']['permalink']

        def author(self, index: int):
            r"""Returns the author of the post at the specified index
                Example: reddit.Subreddit('top', 'python').author(0)"""
            return self.json['data']['children'][index]['data']['author']

        def image(self, index: int):
            r"""Returns any image in the post at the specified index
                Example: reddit.Subreddit('top', 'python').image(0)
                Possible exceptions: KeyError, IndexError"""

            try:
                return self.json['data']['children'][index]['data']['url_overridden_by_dest']
            except KeyError:
                raise KeyError('No image found')

        def num_comments(self, index: int):
            r"""Returns the number of comments of the post at the specified index
                Example: reddit.Subreddit('top', 'python').num_comments(0)"""
            return self.json['data']['children'][index]['data']['num_comments']

        def upvotes(self, index: int):
            r"""Returns the number of upvotes of the post at the specified index
                Example: reddit.Subreddit('top', 'python').upvotes(0)"""
            return self.json['data']['children'][index]['data']['ups']

        def downvotes(self, index: int):
            r"""Returns the number of downvotes of the post at the specified index
                Example: reddit.Subreddit('top', 'python').downvotes(0)"""
            return self.json['data']['children'][index]['data']['downs']

        def score(self, index: int):
            r"""Returns the score of the post at the specified index
                Example: reddit.Subreddit('top', 'python').score(0)"""
            return self.json['data']['children'][index]['data']['score']

        def permalink(self, index: int):
            r"""Returns the permalink of the post at the specified index
                Example: reddit.Subreddit('top', 'python').permalink(0)"""
            return self.json['data']['children'][index]['data']['permalink']


class AsyncClient():
    """
    Represents an asynchronous Client for fetching reddit posts
    """

    def __init__(self, agent, key):
        self.agent = agent
        self.key = key

    class Subreddit():
        r"""
        Gets the raw data on a subreddit, which can be fetched via the various methods here
        """
        async def subreddit_main(self, type, name):
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.reddit.com/r/{}/{}.json".format(name, type)) as resp:
                    return await resp.json()

        def __init__(self, type, name):
            self.name = name
            self.type = type
            self.agent = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8))
            self.json = asyncio.run(self.subreddit_main(self.type, self.name))

        async def selftext(self, index: int):
            r"""Returns the selftext of the post at the specified index
                Example: reddit.Subreddit('top', 'python').selftext(0)"""
            return self.json['data']['children'][index]['data']['selftext']

        async def title(self, index: int):
            r"""Returns the title of the post at the specified index
                Example: reddit.Subreddit('top', 'python').title(0)"""
            return self.json['data']['children'][index]['data']['title']

        async def post_url(self, index: int):
            r"""Returns the url of the post at the specified index
                  Example: reddit.Subreddit('top', 'python').url(0)"""
            # return the reddit link of the post
            return 'https://reddit.com' + self.json['data']['children'][index]['data']['permalink']

        async def author(self, index: int):
            r"""Returns the author of the post at the specified index
                Example: reddit.Subreddit('top', 'python').author(0)"""
            return self.json['data']['children'][index]['data']['author']

        async def image(self, index: int):
            r"""Returns any image in the post at the specified index
                Example: reddit.Subreddit('top', 'python').image(0)
                Possible exceptions: KeyError, IndexError"""

            try:
                return self.json['data']['children'][index]['data']['url_overridden_by_dest']
            except KeyError:
                raise KeyError('No image found')

        async def num_comments(self, index: int):
            r"""Returns the number of comments of the post at the specified index
                Example: reddit.Subreddit('top', 'python').num_comments(0)"""
            return self.json['data']['children'][index]['data']['num_comments']

        async def upvotes(self, index: int):
            r"""Returns the number of upvotes of the post at the specified index
                Example: reddit.Subreddit('top', 'python').upvotes(0)"""
            return self.json['data']['children'][index]['data']['ups']

        async def downvotes(self, index: int):
            r"""Returns the number of downvotes of the post at the specified index
                Example: reddit.Subreddit('top', 'python').downvotes(0)"""
            return self.json['data']['children'][index]['data']['downs']

        async def score(self, index: int):
            r"""Returns the score of the post at the specified index
                Example: reddit.Subreddit('top', 'python').score(0)"""
            return self.json['data']['children'][index]['data']['score']

        async def permalink(self, index: int):
            r"""Returns the permalink of the post at the specified index
                Example: reddit.Subreddit('top', 'python').permalink(0)"""
            return self.json['data']['children'][index]['data']['permalink']
