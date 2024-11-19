# Wikipedia Documents


This directory contains the Wikipedia tools to extract the documents used for the RAG model.

# Steps to extract the documents:

1. Extract the zip file `categories.zip` in the same directory as the `extract_documents.py` script.

2. Run the script `extract_documents.py` to extract the documents from the Wikipedia categories. The script will create a directory `documents` with the extracted documents.

3. Use the script `filter_documents.py` to filter the documents and create a new directory `documents_filtered` with the filtered documents.


Running the scripts will take approximately 1 hour to extract and filter the documents.
