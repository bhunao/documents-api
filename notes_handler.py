import os
import asyncio
from api.database import add_document
from api.api_logging import logger


def read_markdown_file(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return f.read()


async def main(folder_path):
    for dirpath, dnames, fnames in os.walk(folder_path):
        for file_name in fnames:
            if file_name.endswith(".md"):
                with open(dirpath + "\\" + file_name, "r", encoding="utf-8") as f:
                    request_dict = {
                        "name": file_name[:-3], "content": f.read()}

                document = await add_document(request_dict)
                if document:
                    logger.debug(
                        f"file [{dirpath}{file_name}] named [{document['name']}] added into database]")

                logger.debug(
                    f"file [{dirpath}{file_name}] already exists in the database]")


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(argv[1]))
    elif len(argv) < 2:
        raise ValueError("You need to pass a folder path as parameter.")
    else:
        raise ValueError("Unknown error")
