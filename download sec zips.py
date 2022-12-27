# imports
import os
import requests
from bs4 import BeautifulSoup

# global variable declaration
URL = "https://www.sec.gov/dera/data/financial-statement-and-notes-data-set"
DOWNLOADS_FOLDER = "D:\\Programming\\Python\\pull form from SEC site\\Sec filings"

def main():

    # webscraping for the URL's since they decided to change the formating of the file name and report frequency in 2020, quarterly was fine but oh no we just had to change it and not modify the previous files to keep it consistent with the new scheme so now you cant even build the file name logically and have to create an if statement and two differnt algorithims for pre 2020 and post 2020, but that wasn't enough was it? they just had to change the way they report it in Q4 2020 so you then have to create a special arguement for 2020 becuase most of it is in Q format but the last half is in monthly.
    site = requests.get(URL)
    soup = BeautifulSoup(site.content, "html.parser")

    # generate download urls from web scaped content
    download_list = [f"https://www.sec.gov{i.a['href']}" for i in soup.table.tbody.find_all("tr")]

    download_sec_filings(download_list)

# I decided to split this up, so I have the option to use it else where later should I want to download just one file
def download_zip(from_url, file_name, path=DOWNLOADS_FOLDER):

    # create downloads folder, path declared earlier
    if not os.path.isdir(path):
        os.makedirs(path)

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

        # check if file already exists if it does then skip, else download
        if os.path.isfile(os.path.join(DOWNLOADS_FOLDER, file_name)):
            print(f"{file_name} already exists, moving to {download_list[index + 1]}\n")
            continue
        else:
            download_zip(download, file_name)


main()
