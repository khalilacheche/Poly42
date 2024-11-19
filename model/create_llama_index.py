import os.path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,StorageContext, load_index_from_storage, Settings,ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

documents_dir = "../data/Wikipedia/documents_filtered"
save_dir = "documents/storage_wikipedia"
embedding_model = "BAAI/bge-base-en-v1.5"


# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name=embedding_model)

# check if storage already exists
if not os.path.exists(save_dir):
    # load the documents and create the index
    documents = SimpleDirectoryReader(documents_dir).load_data()
    index = VectorStoreIndex.from_documents(documents,show_progress=True)
    # store it for later
    index.storage_context.persist(persist_dir=save_dir)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=save_dir)
    index = load_index_from_storage(storage_context)

### Retriever
retriever = index.as_retriever()
nodes = retriever.retrieve("Does the number of layers in a neural network affect the model's ability to avoid overfitting?")
print(nodes[0].text)