
import os

notebooks_dir = r"Y:\ENICar\cours\5th Sem\CybSec\project\NetGuardian-AI\notebooks\kaggle"
files_to_check = [
    "02_data_preparation.ipynb",
    "03_hybrid_model_training.ipynb",
    "06_model_comparison.ipynb"
]

target_string = "your_file.csv"
replacement = "cicids2017_cleaned.csv"

for filename in files_to_check:
    file_path = os.path.join(notebooks_dir, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target_string in content:
                new_content = content.replace(target_string, replacement)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"FIXED: {filename}")
            else:
                print(f"OK (No placeholder): {filename}")
                
        except Exception as e:
            print(f"ERROR reading {filename}: {e}")
    else:
        print(f"NOT FOUND: {filename}")
