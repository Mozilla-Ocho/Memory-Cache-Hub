import asyncio
import aiohttp
import aiofiles
import os

class RunHandle:
    def __init__(self, llamafile_info, llamafile_store_path):
        self.llamafile_info = llamafile_info
        self.llamafile_store_path = llamafile_store_path
        self.process = None
        self.task = None

    def is_running(self):
        return self.process is not None and self.process.returncode is None

    def start(self):
        self.task = asyncio.create_task(self._run())

    async def stop(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()  # Await the process to properly terminate
            self.process = None
            if self.task:
                self.task.cancel()
                try:
                    await self.task  # This ensures any exceptions are raised and handled
                except asyncio.CancelledError:
                    print("Task was cancelled")
                self.task = None

    # Don't call this. Use start() instead.
    async def _run(self):
        await self.stop()
        try:
            full_file_path = os.path.join(self.llamafile_store_path, self.llamafile_info.filename)
            if not os.path.isfile(full_file_path):
                print("_run: File not found", flush=True)
                raise FileNotFoundError(f"{full_file_path} not found in {self.llamafile_store_path}")

            if os.name == 'posix' or os.name == 'darwin':
                if not os.access(full_file_path, os.X_OK):
                    print(f"Making {self.llamafile_info.filename} executable")
                    os.chmod(full_file_path, 0o755)

            args = ["--host", "0.0.0.0", "--port", "8888", "--nobrowser"]
            enable_gpu = False
            if enable_gpu:
                args += ["--ngl", "999"]
            print("STARTING llamafile with args: ", args, flush=True)
            self.process = await asyncio.create_subprocess_exec(full_file_path,
                                                                *args,
                                                                stdout=asyncio.subprocess.PIPE,
                                                                stderr=asyncio.subprocess.PIPE)

        except Exception as e:
            print(f"_run Error: {e}")
