# LLaMa Indexes

This directory should contain the LLaMA indexes used for the RAG model. We uploaded the indexes to a Hugging Face repository due to their size. You can download the indexes using these commands in a Python interpreter:

```python
from huggingface_hub import snapshot_download
snapshot_download(repo_id="tafrika/llama_indexes",cache_dir="./")
```

The files are relatively large (23 GB for the Wikipedia index and 4 GB for MIT OCW), so the download may take some time.
