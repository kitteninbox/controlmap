import os
import pandas as pd
import numpy as np
import math
import base64
import streamlit as st

css = """
<style>
[data-testid="stToolbar"] {
    visibility: hidden;
}
</style>
"""

st.markdown(
    css,
    unsafe_allow_html=True
)

# ### Extract each individual sheet from the Excel, and convert them into csv files

# Create a function that faciitate file download
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


def main():

    st.title('Control Maps Converter for ASM PNP Machines')
    st.title('Created by Yue Hang')

    xlsx_file = st.file_uploader("Upload the Control Map (Bond Map) from Chen Kang as is (in .xlsx format)", type=['xlsx'], accept_multiple_files=True)

    if xlsx_file:
        csv_files = []
        txt_files = []
        
        # Read the input xlsx file as a whole
        for file in xlsx_file:
            xls = pd.ExcelFile(file)

            # Loop through the sheets and export each of them into individual csv file
            for sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet, header=None)


                ## CLEANING
                # Identify the columns which contain any NaN value(s)
                nan_cols = df.columns[df.isna().any()].to_list()

                # Drop all the columns with NaN value(s)
                df.drop(nan_cols, axis=1, inplace=True)

                # Export and replace the original CSV files with the cleaned Dataframe
                csv_filename = f"{sheet}.csv"
                df.to_csv(csv_filename, header=None, index=False)
                csv_files.append(csv_filename)

                
                # Read the CSV file
                with open(csv_filename, 'r') as file:
                    data = file.read()

                # Replace the tab characters with nothing
                data_no_spaces = data.replace('\t', '')

                # Remove the commas
                data_no_spaces = data_no_spaces.replace(',', '')

                txt_filename = f"{sheet}.txt"

                with open(txt_filename, 'w') as file:
                    file.write(data_no_spaces)

                txt_files.append(txt_filename)
                

            # Download buttons
            if st.button('Download All CSV Files'):
                for i, csv_file in enumerate(csv_files):
                    tmp_download_link = download_link(pd.read_csv(csv_file), csv_file, f'Click here to download {csv_file}!')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)

            if st.button('Download All TXT Files'):
                for i, txt_file in enumerate(txt_files):
                    with open(txt_file, 'r') as file:
                        tmp_download_link = download_link(file.read(), txt_file, f'Click here to download {txt_file}!')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
