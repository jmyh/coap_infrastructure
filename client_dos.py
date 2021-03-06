import asyncio
import logging
import time
from random import randrange

from aiocoap import *

logging.basicConfig(level=logging.INFO)
SERVER_URI = "coap://localhost/temperature";


async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    payload = b"The quick brown fox jumps over the lazy dog.\n" * 30
    # payload = str.encode(str(randrange(1500, 1900, 2)))
    request = Message(code=PUT, payload=payload, uri=SERVER_URI)

    response = await context.request(request).response

    print('Result: %s\n%r' % (response.code, response.payload))

if __name__ == "__main__":
    while True:
        asyncio.get_event_loop().run_until_complete(main())
