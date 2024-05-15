import asyncio

from TonTools import *

def parse_response(response):
    return [
        {
            "address": item[0],
            **item[1]
        }
        for item in response['data']['response']
    ]

