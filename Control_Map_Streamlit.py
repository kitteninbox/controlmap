import streamlit as st
import pandas as pd
import base64
import os
import zipfile

# Create a function that facilitates file download
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def main():
    st.title('Control Maps Converter for ASM PNP Machines')
    st.title('Created by Yue Hang')

    xlsx_files = st.file_uploader("Upload the Control Map (Bond Map) from Chen Kang as is (in .xlsx format)", type=['xlsx'], accept_multiple_files=True)

    if xlsx_files:
        csv_files = []
        txt_files = []

        for xlsx_file in xlsx_files:
            xls = pd.ExcelFile(xlsx_file)

            st.write(f"It's gonna take a while to convert, please wait...")

            for sheet in xls.sheet_names:
                if "pnpmap" in sheet[:6].lower():  # Ensure only relevant sheets are processed
                    df = pd.read_excel(xls, sheet_name=sheet, header=None)

                    # Debug: Check the initial data
                    ## st.write(f"Initial data from sheet {sheet}:")
                    ## st.write(df)

                    # CLEANING
                    nan_cols = df.columns[df.isna().any()].to_list()
                    df.drop(nan_cols, axis=1, inplace=True)

                    # Debug: Check the data after cleaning
                    ## st.write(f"Data after cleaning from sheet {sheet}:")
                    ## st.write(df)

                    # Convert all values to integers
                    df = df.astype(int)  # Ensure all values are integers

                    # Debug: Check the data after conversion
                    ## st.write(f"Data after conversion to integers from sheet {sheet}:")
                    ## st.write(df)

                    # Convert DataFrame to string format with integer values
                    df_str = df.applymap(str)

                    # Export to CSV
                    csv_filename = f"{sheet}.xlsx"
                    df.to_excel(csv_filename, header=None, index=False)

                    # Debug: Check the CSV content
                    ## st.write(f"CSV content for sheet {sheet}:")
                    ## st.write(pd.read_csv(csv_filename, header=None))

                    csv_files.append(csv_filename)

                    # Convert to TXT
                    with open(csv_filename, 'r') as file:
                        data = file.read()

                    data_no_spaces = data.replace('\t', '').replace(',', '')
                    txt_filename = f"{sheet}.txt"
                    with open(txt_filename, 'w') as file:
                        file.write(data_no_spaces)
                    txt_files.append(txt_filename)
        
        if st.button('Download All CSV Files'):  # Added unique button ID handling
            for i, csv_file in enumerate(csv_files):  # Added enumerate to ensure unique IDs
                if os.path.exists(csv_file):  # Check if the file exists
                    ## st.write("Check for one last time before downloading the file...")
                    ## st.write(pd.read_csv(csv_file, header=None))
                    tmp_download_link = download_link(pd.read_excel(csv_file), csv_file, f'Click here to download {csv_file}!')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                else:
                    st.error(f"File {csv_file} does not exist.")  # Error message if file doesn't exist

        if st.button('Download All TXT Files'):  # Added unique button ID handling
            for i, txt_file in enumerate(txt_files):  # Added enumerate to ensure unique IDs
                if os.path.exists(txt_file):  # Check if the file exists
                    with open(txt_file, 'r') as file:
                        tmp_download_link = download_link(file.read(), txt_file, f'Click here to download {txt_file}!')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                else:
                    st.error(f"File {txt_file} does not exist.")  # Error message if file doesn't exist

if __name__ == "__main__":
    main()
