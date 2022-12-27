# imports
import zipfile
import os
import pandas as pd
import warnings

# gives an idea of progress
matches = 0
scanned_lines = 0

# Main function
def main():


    # only used in filt_form_type_and_company but here for clairty
    company = "APPLE INC"

    # generate list of paths for the zip files
    zip_files = [{"path": os.path.join(root, file), "name": file} for root, dirs, files in os.walk("Sec filings") for
                 file in files]

    # submissions pandas data frame
    # process_submissions() returns a data frame each time so contact is used to combine the data frames
    sub_data = pd.concat([process_submissions(zip["path"]) for zip in zip_files])

    filt_form_type_and_company = (
                (sub_data["name"] == company) & ((sub_data["form"] == "10-K") | (sub_data["form"] == "10-Q")))

    # remove all none related entries and reset the index
    sub_data = sub_data.loc[filt_form_type_and_company]
    sub_data.reset_index(inplace=True)

    # Numeric data is a massive data frame so process_numbers() handles all of the work
    num_data = [process_numbers(zip["path"], sub_data["adsh"]) for zip in zip_files]

    # create data frame and save the data as it takes a while to process the data
    try:
        pd.concat(num_data).to_csv("AccountsReceivableNetCurrent APPL.csv")
    except:
        print(num_data, "\n", type(num_data))

    # print(num_data.shape)

    # num_data["sub adsh"]

    # print(num_data[num_data["adsh"].isin(sub_data["adsh"])])


def process_submissions(path):
    try:
        # Open and read each sub.tsv file as a data frame
        with zipfile.ZipFile(path, "r") as working_directory:
            with working_directory.open("sub.tsv") as sub:
                return pd.read_csv(sub, sep="\t")

    #Zip file failed does nothing and gives a warning
    except zipfile.BadZipfile:
        warnings.warn(f"bad zip : {path} ")


def process_numbers(path, adsh, cunksize=1_000_000):
    global matches
    global scanned_lines

    try:

        #Open and read num.tsv in chunks
        with zipfile.ZipFile(path, "r") as working_directory:
            with working_directory.open("num.tsv") as sub:
                use_cols = ["adsh", "tag", "value", "ddate", "qtrs"]

                # chunk processing
                # Helps save on current memory used, doesn't do much for speed performance

                for chunk in pd.read_csv(sub, sep="\t", chunksize=cunksize, usecols=use_cols):

                    # Tracks how many lines have been scanned so far
                    scanned_lines += chunk.shape[0]

                    # adsh is passed in from when it is called
                    # adsh is a filter for documents, since we filtered the submissions earlier for the company it effectively filters for company
                    adsh_filter = chunk["adsh"].isin(adsh)
                    chunk = chunk[adsh_filter]

                    # Now we filter by tag
                    tag_filter = chunk["tag"] == "AccountsReceivableNetCurrent"
                    chunk = chunk[tag_filter]

                    # tracks how many matches and print progress
                    matches += chunk.shape[0]
                    print(f"found : {matches:,}\n{str(round((scanned_lines / 281_165_204) * 100, 2))}%")

                    # convert ddate column to datetime object
                    chunk['ddate'] = pd.to_datetime(chunk['ddate'], format="%Y%m%d")

                    return chunk


    except zipfile.BadZipfile:
        warnings.warn(f"bad zip : {path} ")


main()
