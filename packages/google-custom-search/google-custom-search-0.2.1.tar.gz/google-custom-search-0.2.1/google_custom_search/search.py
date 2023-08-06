import requests
try:
    import aiohttp
except:
    no_async = True
else:
    no_async = False
    
from .object import result
from typing import Optional

class ApiError(Exception):
    pass

class AsyncError(Exception):
    pass

class custom_search(object):
    APIURL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self,
                 apikey: str,
                 engine_id: str,
                 image: Optional[bool]=False):
        self.token = apikey
        self.engine_id = engine_id
        self.image = image

    def search(self, keyword:str) -> result:
        params={
            "key": self.token,
            "cx": self.engine_id,
            "q": keyword
        }
        res = requests.get(self.APIURL,params=params)
        return result(res.json())
      
    async def search_async(self, keyword:str) -> result:
        if no_async:
            raise AsyncError("This library can't use aiohttp. Please install aiohttp")
        params={
            "key": self.token,
            "cx": self.engine_id,
            "q": keyword
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.APIURL, params=params) as res:
                return result(await res.json())
