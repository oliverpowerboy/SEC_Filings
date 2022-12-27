# imports
import zipfile
import os
import pandas as pd
import warnings

# gives an idea of progress
matches = 0
scanned_lines = 0


def main():
    # submissions_data = extract_tsv("Sec filings\\2022_05_notes.zip", "sub.tsv")
    # numeric_data = extract_tsv()

    company = "APPLE INC"

    zip_files = [{"path": os.path.join(root, file), "name": file} for root, dirs, files in os.walk("Sec filings") for
                 file in files]

    sub_data = pd.concat([process_submissions(zip["path"]) for zip in zip_files])

    filt_form_type_and_company = (
                (sub_data["name"] == "APPLE INC") & ((sub_data["form"] == "10-K") | (sub_data["form"] == "10-Q")))

    sub_data = sub_data.loc[filt_form_type_and_company]
    sub_data.reset_index(inplace=True)

    num_data = [process_numbers(zip["path"], sub_data["adsh"]) for zip in zip_files]

    try:
        pd.concat(num_data).to_csv("AccountsReceivableNetCurrent APPL.csv")
    except:
        print(num_data, "\n", type(num_data))

    # print(num_data.shape)

    # num_data["sub adsh"]

    # print(num_data[num_data["adsh"].isin(sub_data["adsh"])])


def process_submissions(path):
    try:

        with zipfile.ZipFile(path, "r") as working_directory:
            with working_directory.open("sub.tsv") as sub:
                return pd.read_csv(sub, sep="\t")


    except zipfile.BadZipfile:
        warnings.warn(f"bad zip : {path} ")


def process_numbers(path, adsh, cunksize=1_000_000):
    global matches
    global scanned_lines

    try:

        with zipfile.ZipFile(path, "r") as working_directory:
            with working_directory.open("num.tsv") as sub:
                use_cols = ["adsh", "tag", "value", "ddate", "qtrs"]

                for chunk in pd.read_csv(sub, sep="\t", chunksize=cunksize, usecols=use_cols):
                    scanned_lines += chunk.shape[0]

                    adsh_filter = chunk["adsh"].isin(adsh)

                    chunk = chunk[adsh_filter]

                    tag_filter = chunk["tag"] == "AccountsReceivableNetCurrent"

                    matches += chunk[tag_filter].shape[0]

                    print(f"found : {matches:,}\n{str(round((scanned_lines / 281_165_204) * 100, 2))}%")

                    chunk['ddate'] = pd.to_datetime(chunk['ddate'], format="%Y%m%d")

                    return chunk[tag_filter]


    except zipfile.BadZipfile:
        warnings.warn(f"bad zip : {path} ")


main()
