import os
import shutil
from tqdm import tqdm
import argparse

# Copy files in the 'documents_last' directory that do not match the categories to 'kept_files' directory
def copy_files_to_keep(documents_dir, categories_to_remove, kept_files_dir):
    if not os.path.exists(kept_files_dir):
        os.makedirs(kept_files_dir)
        
    files = os.listdir(documents_dir)
    with tqdm(total=len(files), desc="Processing files") as pbar:
        for file_name in files:
            keep_file = True
            for category in categories_to_remove:
                if file_name.startswith(category):
                    keep_file = False
                    break  # Break the loop if file matches a category to remove
            if keep_file:
                src_path = os.path.join(documents_dir, file_name)
                dst_path = os.path.join(kept_files_dir, file_name)
                shutil.copy2(src_path, dst_path)
            pbar.update(1)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--documents_dir', type=str, default='documents', help='Directory containing the documents')
    args.add_argument('--kept_files_dir', type=str, default='documents_filtered', help='Directory to save the kept files')

    # Paths
    documents_dir = 'documents'
    kept_files_dir = 'documents_filtered'
    categories_to_remove = ['Analysis_of_variance','Calculus','Categorical_data','Chemical_engineering','Communication','Computational_science','Computer_data','Computer_languages','computer_networks','computing_and_society','computing_by_computer_model','Control_theory','Decision_theory','Data_analysis','Deductive_reasoning','Design_of_experiments','Digital_electronics','Ecology','Electrical_components','Electronic_circuits','Energy','Equations','Formal_sciences','Geometry','Heuristics','Inductive_reasoning','Information_systems','Information_science','Information_technology','integrated_circuits','Internet','Logic_and_statistics','Management','Nanotechnology','Operations_research','Non_parametric_statistics','Parametric_statistics','Real_time_computing','Sampling_(statistics)','Semiconductors','Statistical_theory','Structural_engineering','Summary_statistics','Survival_analysis','Theorems','Theoretical_physics']

    # Copy the files
    copy_files_to_keep(documents_dir, categories_to_remove, kept_files_dir)
