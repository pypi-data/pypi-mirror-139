import os
import zipfile

import requests


DATA_URL = "https://raw.githubusercontent.com/cse163/book/main/book_source/source/_static/data/"


def download(file_name: str, force_download: bool=False):
    """
    Downloads the given file from the following URL if it doesn't exist in the current directory.
    If the file is a .zip, unzips it. If force_download is True, downloads the file even if it exists.

    https://github.com/cse163/book/tree/main/book_source/source/_static/data
    """
    if force_download or not os.path.exists(file_name):
        url = os.path.join(DATA_URL, file_name)
        r = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(r.content)

        # Unzip zip files
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(file_name, 'r') as z:
                z.extractall(".")




