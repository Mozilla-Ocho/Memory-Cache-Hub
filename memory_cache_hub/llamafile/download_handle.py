import asyncio
import aiohttp
import aiofiles
import os

class DownloadHandle:
    def __init__(self, url, filename, file_path):
        self.url = url
        self.filename = filename
        self.file_path = file_path
        self.content_length = 0
        self.written = 0
        self.task = asyncio.create_task(self.download())

    async def download(self):
        # BUG On MacOS, https requests failed unless I disabled ssl checking.
        # TODO Fix ssl issue on MacOS
        #      This github issue may be related:
        #      https://github.com/aio-libs/aiohttp/issues/955
        #async with aiohttp.ClientSession() as session:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.url) as response:
                self.content_length = int(response.headers.get('content-length', 0))
                # Make sure that the directory exists
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                async with aiofiles.open(self.file_path, 'wb') as file:
                    async for data in response.content.iter_chunked(1024):
                        await file.write(data)
                        self.written += len(data)

    def progress(self):
        return int(100 * self.written / self.content_length) if self.content_length > 0 else 0

    def is_complete(self):
        return self.task.done()

    def get_result(self):
        return self.task.result() if self.task.done() else None


