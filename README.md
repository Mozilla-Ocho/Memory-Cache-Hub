# Memory Cache Hub

A backend server for [Memory Cache](https://github.com/Mozilla-Ocho/Memory-Cache).

## Overview

Memory Cache Hub is a core component of Memory Cache:

- It exposes APIs used by the browser extension, browser client, and plugins.
- It serves static files including the browser client and various project artifacts.
- It downloads and runs `llamafiles` as subprocesses.
- It ingests and retrieves document fragments with the help of a vector database.
- It generates various artifacts using prompt templates and large language models.

Memory Cache Hub is designed to run on your own machine. All of your data is stored locally and is never uploaded to any server. 

## Installation

To use Memory Cache Hub:

- Find the latest release for your platform (Windows, MacOS, or GNU/Linux).
- Download the single-file executable or directory from the `Artifacts` section.
- Run the executable. If you want to see streaming debug output, run the executable on the command line.
- A new tab should open in your browser showing the Memory Cache Browser Client GUI.
- If the GUI does not open automatically, you can navigate to [http://localhost:4444](http://localhost:444) in your browser.

Each release build of Memory Cache Hub is a standalone executable that includes the browser client and all necessary assets. By "standalone", we mean that you do not need to install any additional software to use Memory Cache Hub. 

### Release Builds

Release builds can be downloaded from the `Artifacts` section of the following pages:

- [Memory Cache Hub (Ubuntu)](https://github.com/Mozilla-Ocho/Memory-Cache-Hub/actions/runs/8723898292)
- [Memory Cache Hub (Windows)](https://github.com/Mozilla-Ocho/Memory-Cache-Hub/actions/runs/8723898288)
- [Memory Cache Hub (MacOS)](https://github.com/Mozilla-Ocho/Memory-Cache-Hub/actions/runs/8723898296)

Release builds are available in two formats:

- A single file executable, which is compact and easy to use but takes ~30 seconds to boot (because it unpacks supporting files at runtime).
- A directory that includes an executable and supporting files. The executable included in this format boots instantly.

On MacOS and Windows, you may need to enable settings to allow unsigned/unverified packages. On Linux, you may need to `chmod +x`.

### Firefox Browser Extension

A Firefox browser extension for Memory Cache that extends its functionality is also available. More information can be found in the main [Memory Cache repository](https://github.com/Mozilla-Ocho/Memory-Cache).

### Installing from source

If you want to build `memory-cache-hub` from source, you can follow the instructions in the sections below.

## Development

Memory Cache consists of three separate components:

- [Memory Cache Hub](https://github.com/Mozilla-Ocho/Memory-Cache-Hub?tab=readme-ov-file#memory-cache-hub) (this repo)
- [Memory Cache Browser Client](https://github.com/Mozilla-Ocho/Memory-Cache-Browser-Client)
- [Memory Cache Firefox Extension](https://github.com/Mozilla-Ocho/Memory-Cache)

Release builds of Memory Cache Hub include the (pre-built) browser client assets so that the entire application can be run as a standalone executable. While developing Memory Cache Hub, you build and run the browser client separately (or not at all).

Memory Cache Hub is built with `Python 3.11`. Other versions of `Python 3` may work, but they are not officially supported.

During development, Memory Cache Hub runs as a regular Python application. Release builds package the application and its dependencies into a standalone executable using `PyInstaller`. More information about packaging and building Memory Cache Hub for release can be found in a later section.

To set up your development environment, navigate to the root of the repository and run the following commands:

```bash
# Create a virtual environment
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

Then, run the application:

```bash
python -m memory_cache_hub.server.main
```

If you specify a `--client-path` on the command line, Memory Cache Hub will serve the static client assets from its root path, and you can navigate to [http://localhost:4444](http://localhost:4444) in your browser to access the GUI.

Memory Cache Hub also has a SwaggerUI interface that you can access at [http://localhost:4444/docs](http://localhost:4444/docs).

Memory Cache Hub accepts several command-line arguments to customize its behavior. You can see a list of available arguments by running:

``` sh
python -m memory_cache_hub.server.main --help
```

## Building for Release

Memory Cache Hub is packaged into a standalone executable using `PyInstaller`. The build process has not been automated, which means that building a release requires running scripts manually. 

`PyInstaller` does not support cross-compilation, so you must build the application on the platform for which you are building the release. 

To build a release, follow the instructions above to set up your development environment. Then install the additional requirements for building the release:

```bash
pip install -r requirements.build.txt
```

Then run the appropriate build script:

``` sh
python -m memory_cache_hub.build.build_memory_cache_hub
```

The build script will output a standalone executable in the `dist` directory.

Pass `--help` as an argument to see additional arguments for the build script, such as where the browser client assets will be loaded from.

## Running Tests

To run the tests, set up your development environment following the instructions above. Then run the following command from the root of the repository:

```bash
python -m unittest discover -s tests
```

To run a particular test, you can specify a module name or file:

```bash
# Test a module
python -m unittest tests.llamafile.test_llamafile_manager

# Test a file
python -m unittest tests/llamafile/test_llamafile_manager.py
```

By default, long-running tests (such as those that test file downloads) are skipped. To run these tests, set the `RUN_LONG_TESTS` environment variable to `1`:

```bash 
RUN_LONG_TESTS=1 python -m unittest discover -s tests
```

## Troubleshooting

### GLIBC Error

You may encounter an error similar to the following when running the release build:

```
[76074] Error loading Python lib '/home/john/downloads/memory_cache_hub/_internal/libpython3.11.so.1.0': dlopen: /lib/x86_64-linux-gnu/libm.so.6: version `GLIBC_2.38' not found (required by /home/john/downloads/memory_cache_hub/_internal/libpython3.11.so.1.0)
```

This error occurs when the build was made on a system with a newer version of `glibc` than the one on your system. Let us know if this happens to you because it means we need to build releases on an older system.

### Memory Cache fails to start the Llamafile Server

When you select an LLM from the models tab, Memory Cache should automatically download and run a `llamafile` (in server mode). If the `llamafile` server fails to start:

- Check the server logs by running `Memory Cache Hub` from the command line.
- Try to download and run a `llamafile` following the instructions in the [`llamafile README`](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#llamafile). If you are still having trouble, check the ["Gotchas" section of `llamafile README`](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#gotchas) for platform-specific troubleshooting tips. 
