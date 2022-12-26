import zipfile
import os
import pandas as pd



def extract_tsv(file_path, file_name):
    try:

        with zipfile.ZipFile(file_path, "r") as zip:

            if "sub.tsv" in zip.namelist():
                with zip.open(file_name, "r") as tsv:
                    return pd.read_csv(tsv, sep="\t", low_memory=False)

    except zipfile.BadZipFile:
        print(f"{file_path} bad zip")
        return None


#submissions_data = extract_tsv("Sec filings\\2022_05_notes.zip", "sub.tsv")
#numeric_data = extract_tsv()

company = "APPLE INC"

notes = [root + "\\" + file for root, dirs, files in os.walk("Sec filings") for file in files if file[-3:] == "zip"]

sub_frames = [extract_tsv(i, "sub.tsv") for i in notes]
#num_frames = [extract_tsv(i, "num.tsv") for i in notes]

submissions_data = pd.concat(sub_frames)
#numeric_data = pd.concat(num_frames)

print(submissions_data["name"].unique().shape[0])
#print(numeric_data["name"].unique().shape[0])

filt = (submissions_data["name"] == company) & ((submissions_data["form"] == "10-K") | (submissions_data["form"] == "10-Q"))
information_display = ["name", "adsh", "cik", "form"]

# print(data.loc[filt].T.dropna().squeeze())

company_submissions = submissions_data.loc[filt]

print(company_submissions[information_display])
