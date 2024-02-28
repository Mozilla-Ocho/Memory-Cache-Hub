import asyncio
import aiohttp
import aiofiles
import os

class DownloadHandle:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
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
                async with aiofiles.open(self.filename, 'wb') as file:
                    async for data in response.content.iter_chunked(1024):
                        await file.write(data)
                        self.written += len(data)

    def progress(self):
        return int(100 * self.written / self.content_length) if self.content_length > 0 else 0

    def is_complete(self):
        return self.task.done()

    def get_result(self):
        return self.task.result() if self.task.done() else None


if __name__ == '__main__':
    async def main():
        url = 'https://www.python.org/static/img/python-logo.png'
        filename = 'python-logo.png'
        download = DownloadHandle(url, filename)
        while not download.is_complete():
            print(f'{download.progress()}%')
            await asyncio.sleep(1)
        print(f'Download complete: {download.get_result()}')

    asyncio.run(main())
