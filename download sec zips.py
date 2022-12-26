import os

import requests
from bs4 import BeautifulSoup

URL = "https://www.sec.gov/dera/data/financial-statement-and-notes-data-set"

downloads_folder = "D:\\Programming\\Python\\pull form from SEC site\\Sec filings"

site = requests.get(URL)

soup = BeautifulSoup(site.content, "html.parser")

download_list = [f"https://www.sec.gov{i.a['href']}" for i in soup.table.tbody.find_all("tr")]


def main():
    download_sec_filings(download_list)


def download_zip(from_url, file_name, path=downloads_folder):
    if not os.path.isdir(downloads_folder):
        os.makedirs(downloads_folder)

    print(f"Downloading : {from_url}")

    r = requests.get(from_url)

    with open(os.path.join(os.getcwd(), path, file_name), "wb") as f:
        f.write(r.content)

    print("Download Complete\n")


def download_sec_filings(download_list):
    for index, download in enumerate(download_list):

        print(f"{index + 1} of {len(download_list)} downloads")

        file_name = download[download.rfind("/") + 1:]
        # print(download[download.rfind("/")+1:])

        # print(os.path.isfile(os.path.join(downloads_folder, file_name)))
        if os.path.isfile(os.path.join(downloads_folder, file_name)):
            print(f"{file_name} already exists, moving to {download_list[index + 1]}\n")
            continue
        else:
            download_zip(download, file_name)


main()
