import logging

import asyncio
from datetime import datetime

import aiocoap.resource as resource
import aiocoap


class TemperatureResource(resource.ObservableResource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()
        self.set_content(b"Three rings for the elven kings under the sky, seven rings for dwarven lords in their "
                         b"halls of stone, nine rings for mortal men doomed to die, one ring for the dark lord on his"
                         b" dark throne.")

    def set_content(self, content):
        self.content = content
        # while len(self.content) <= 1024:
        #     self.content = self.content + b"0123456789\n"

    def get_link_description(self):
        # Publish additional data in .well-known/core
        return dict(**super().get_link_description(), title="Interesting resource")

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('{} PUT payload: {}'.format(datetime.now(),request.payload))
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)


# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(['.well-known', 'core'],
                      resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['temperature'], TemperatureResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
