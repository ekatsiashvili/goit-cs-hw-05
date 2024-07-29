import os
import asyncio
import shutil
import logging
from pathlib import Path
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="Asynchronously sort files by extension")
    parser.add_argument("source", type=str, help="Path to the source folder")
    parser.add_argument("destination", type=str, help="Path to the destination folder")
    return parser.parse_args()

async def init_paths(source, destination):
    source_path = Path(source)
    destination_path = Path(destination)
    
    if not source_path.is_dir():
        raise ValueError(f"Source path {source} is not a directory")
    if not destination_path.exists():
        destination_path.mkdir(parents=True)
    
    return source_path, destination_path

async def read_folder(source_path):
    files = []
    for root, _, filenames in os.walk(source_path):
        for filename in filenames:
            files.append(Path(root) / filename)
    return files

async def copy_file(file, destination_path):
    ext = file.suffix[1:]  # get file extension without dot
    if not ext:
        ext = 'no_extension'
    target_folder = destination_path / ext
    if not target_folder.exists():
        target_folder.mkdir(parents=True)
    target_path = target_folder / file.name
    shutil.copy(file, target_path)
    logging.info(f"Copied {file} to {target_path}")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def main():
    args = parse_args()
    source_path, destination_path = await init_paths(args.source, args.destination)
    files = await read_folder(source_path)
    
    tasks = [copy_file(file, destination_path) for file in files]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Error occurred: {e}")
