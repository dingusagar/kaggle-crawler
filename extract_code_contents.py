import json
import os
from glob import glob

def extract_code_from_ipynb(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    code_cells = []
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':  # Extract code cells
            code = ''.join(cell.get('source', []))  # Combine lines of code
            code_cells.append(code)
        elif cell.get('cell_type') == 'markdown':  # Extract markdown cells (optional)
            markdown = ''.join(cell.get('source', []))
            code_cells.append(f"# {markdown}")  # Add as comment

    return code_cells

def process_files(input_folder, output_folder="processed-codes"):
    try:
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)

        # Gather all .ipynb and .py files in the input folder
        files = glob(os.path.join(input_folder, "*.*"))
        unsuccessful_files = []

        for file_path in files:
            file_name = os.path.basename(file_path)

            try:
                # Keep the original filename with .txt extension
                output_file_name = f"{file_name}.txt"
                output_file_path = os.path.join(output_folder, output_file_name)

                ext = os.path.splitext(file_name)[-1]

                if ext == ".ipynb":
                    # Process Jupyter notebook files
                    code_cells = extract_code_from_ipynb(file_path)
                    processed_code = "\n".join(code_cells)
                elif ext == ".py":
                    # Process Python script files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        processed_code = f.read()
                else:
                    print(f"Warning: Unknown file extension '{ext}' for file '{file_name}'. Skipping.")
                    unsuccessful_files.append(file_name)
                    continue

                # Save the processed code to a text file
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(processed_code)

                print(f"Processed {file_path} -> {output_file_path}")

            except Exception as e:
                print(f"Failed to process file '{file_name}': {e}")
                unsuccessful_files.append(file_name)

        # Print summary of unsuccessful files
        if unsuccessful_files:
            print(f"\n{len(unsuccessful_files)} file(s) could not be processed:")
            for failed_file in unsuccessful_files:
                print(f"- {failed_file}")

    except Exception as e:
        print(f"An error occurred while setting up file processing: {e}")

if __name__ == "__main__":
    input_folder = "code_files"  # Replace with the folder containing .ipynb and .py files
    process_files(input_folder)
