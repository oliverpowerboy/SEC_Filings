# SEC_Filings

Created by Oliver De Fusco

# Download all sec filings

requirements : beautifulsoup4

This downloads all the zip files to a specified downloads folder, beautifulsoup is used to create the links and is optional because it is only used for that.

In Q4 2020 the SEC changed it's reporting frequency from quarterly to monthly and did not go back to amend the previous files to match
- As a result half of the zip files are named in a different format
In response I chose to webscrape the URL's as it future proofs the program and allows it to be ran automatically without changing it until they revamp the site

Verbose logging is reccomended to be set to `True` as the zip folder take time to download so it is important to check the program is still downloading and it's progress

## Downloads folder
- Can be named whatever so long as the `DOWNLOADS_FOLDER` variable points to it correctly same for the `path` variable for the function `download_zip`
- Should only contain relevant `zip` files should you want it to interact with the other programs in the repository properly as no error handling for that is in place for now
- DO NOT RENAME SEC `zip` FILES OR REMOVE FROM DOWNLOADS FOLDER IF YOU REGULARLY RUN THIS PROGRAM
    - `os.path.isfile(os.path.join(DOWNLOADS_FOLDER, file_name))` will re-download the same zip files should the names not match
    
# Read Data

Reads through all the sec zip files and pulls out requested data
