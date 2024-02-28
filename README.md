# Memory Cache Hub

Memory Cache Hub (`hub`) is a backend system for [Memory Cache](https://github.com/Mozilla-Ocho/Memory-Cache).

## Overview

Memory Cache Hub is a central component of Memory Cache:

- It exposes APIs used by the browser extension, browser client, and plugins.
- It serves static files including the browser client and various project artifacts.
- It downloads and runs `llamafiles` as subprocesses.
- It ingests and retrieves document fragments with the help of a vector database.
- It generates various artifacts using prompt templates and large language models.

Memory Cache Hub runs as a standalone application and is designed to run on your own machine. All of your data is stored locally and is never uploaded to any server.

## Installation

To use Memory Cache:

- Download the latest release executable for your platform (Windows, MacOS, or GNU/Linux)
- Run the executable. It will open a new tab in your browser showing the Memory Cache GUI.
- If the GUI does not open automatically, you can navigate to [http://localhost:4444](http://localhost:444) in your browser.

Each release build of Memory Cache Hub is a standalone executable that includes the browser client and all necessary assets. You do not need to install any additional software to use Memory Cache. 

A Firefox browser extension for Memory Cache that extends its functionality is also available. More information can be found in the main [Memory Cache repository](https://github.com/Mozilla-Ocho/Memory-Cache).

If you want to build `memory-cache-hub` from source, you can follow the instructions in the sections below.

