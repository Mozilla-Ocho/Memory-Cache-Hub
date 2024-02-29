import os

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description="Build a Memory Cache Hub executable.")
    parser.add_argument("--executable-name", type=str, required=False, help="The name of the executable.")
    parser.add_argument("--entry-point", type=str, required=False, help="The entry point for the executable.")
    parser.add_argument("--onefile", action="store_true", required=False, help="Build a single file executable.")
    parser.add_argument("--client-path", type=str, required=False, help="The path to the client directory.")
    args = parser.parse_args()

    args.project_root = os.path.join(os.path.dirname(__file__), "..", "..")

    if args.entry_point is None:
        args.entry_point = os.path.join(args.project_root, "memory_cache_hub", "server", "main.py")

    if args.executable_name is None:
        args.executable_name = "memory_cache_hub"

    return args

def main():
    import PyInstaller.__main__
    args = parse_arguments()
    print(f"Building with args:", args)

    add_data_args = []
    add_data_args += [
        # Explicitly add the site-packages directory, because otherwise the executable will fail to find dependencies at runtime.
        f'--add-data={os.path.join(args.project_root, "venv", "lib", "python3.11", "site-packages")}{os.pathsep}.'
    ]
    llamafile_infos_json = os.path.join(args.project_root, "memory_cache_hub", "llamafile", "llamafile_infos.json")
    add_data_args += [
        f'--add-data={llamafile_infos_json}{os.pathsep}.'
    ]

    if args.client_path:
        print(f"Adding client path: {args.client_path}")
        add_data_args += [f'--add-data={args.client_path}{os.pathsep}client']
    else:
        print(f"WARN: No client path provided. The client will not be included in the executable. Pass --client-path to include the client.")

    PyInstaller.__main__.run([
       args.entry_point,
       "--onefile" if args.onefile else "--onedir",
       "--clean",
       "--noconfirm",
       "--name", args.executable_name,
       *add_data_args
    ])

if __name__ == "__main__":
    main()
