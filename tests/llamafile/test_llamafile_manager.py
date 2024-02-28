import unittest
import asyncio
from memory_cache_hub.llamafile.download_handle import DownloadHandle
from memory_cache_hub.llamafile.llamafile_infos import get_default_llamafile_infos

import os
RUN_LONG_TESTS = os.environ.get('RUN_LONG_TESTS', False)

class TestLlamafileManager(unittest.IsolatedAsyncioTestCase):
    @unittest.skipUnless(RUN_LONG_TESTS, 'Long-running tests are skipped unless explicitly requested.')
    async def test_llamafile_download(self):
        llamafile_infos = get_default_llamafile_infos()
        llamafile_info = llamafile_infos[0]
        handle = DownloadHandle(
            url=llamafile_info.url,
            filename=llamafile_info.filename
        )
        # handle = DownloadHandle(
        #     url="https://releases.ubuntu.com/22.04.4/ubuntu-22.04.4-live-server-amd64.iso",
        #     filename="ubuntu-22.04.4-live-server-amd64.iso"
        # )
        await handle.task
        self.assertTrue(handle.task.done())
