import os
import json
import argparse
from tqdm import tqdm


def get_node_data(node_name, node_value):
    #print(node_name)
    #print(node_value.keys())    
    document_title = node_name
    document_content = node_value["content"]
    children_values = []
    children = node_value["subsections"] if "subsections" in node_value else {}
    for child_name, child_value in children.items():
        if child_name in ["See also", "References", "External links", "Further reading", "Notes", "Bibliography", "Footnotes", "Citations", "Sources", "General sources", "Gallery", "Further info"]:
            continue

        child_title = document_title.replace("Category:","") +", " +child_name
        #print(children_values,get_node_data(child_title, child_value))
        children_values = children_values + get_node_data(child_title, child_value)
    children_values.append({"title": document_title, "content": document_content})
    return children_values





if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--categories_dir", default="categories", type=str)
    args.add_argument("--documents_dir", default="documents", type=str)
    args = vars(args.parse_args())
    categories_dir = args["categories_dir"]
    documents_dir = args["documents_dir"]

    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)

    for category in tqdm(os.listdir(categories_dir)):
        category_file = os.path.join(categories_dir, category)
        with open(category_file, 'r') as f:
            category_data = json.load(f)
        data = {"content": "", "subsections": category_data}
        category_documents = get_node_data(category_file.split("/")[-1].replace(".json",""),data)
        for document in category_documents:
            keepcharacters = (' ','.','_')
            save_name = document["title"]
            save_name = "".join(c for c in save_name if c.isalnum() or c in keepcharacters).rstrip()
            document_file = os.path.join(documents_dir, save_name+".txt")
            if len(document["content"]) == 0:
                continue
            try:
                with open(document_file, 'w') as f:
                    f.write(document["title"]+"\n"+document["content"])
            except OSError as e:
                if e.errno == 63:
                    print("Name too long: ", document_file)
                else:
                    print(e)
            except Exception as e:
                print(e)


