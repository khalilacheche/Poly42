Main Contributors:
- Khalil Haroun Achache
- Ali Raed Ben Mustapha
- Farah Briki
For more details on our approach, please refer to the pdf in `pdfs/tafrika.pdf`
## Reproducing Resultsx

To reproduce our results, follow these steps:

1. Install the required libraries inside `model/requirements.txt`
2. Download the LlaMa-Index saved indexes from our [HuggingFace repository](https://huggingface.co/datasets/tafrika/llama_indexes/tree/main).
3. Run the `model/evaluator.py` script (changing the `main_config.yaml` file as required)

### (Optional) Index Creation

If you wish to create the indexes yourself:

1. Extract the document data into the `data` folder, following the instructions in the corresponding `README.md` file.
2. Execute the script located at `model/create_llama_index.py`. Ensure to adjust the `documents_dir` and `save_dir` variables as necessary.

