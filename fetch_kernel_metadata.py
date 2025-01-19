import subprocess
import pandas as pd
from io import StringIO
import json
import re
from tqdm import tqdm

def extract_competition_handles_from_file(json_filename):
    try:
        # Load JSON data from the file
        with open(json_filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        handles = []
        for item in json_data:
            if isinstance(item, list) and len(item) > 1 and isinstance(item[1], dict):
                href = item[1].get("href", "")
                tags = item[1].get("tags", [])
                if "competitions" in href and "Tabular" in tags:
                    handle = href.split("/competitions/")[-1]
                    handles.append(handle)
        return handles
    except Exception as e:
        print(f"An error occurred while extracting competition handles: {e}")
        return []

def get_kaggle_kernels(competition_handle, sort_by="voteCount", topk=5):
    try:
        # Build the Kaggle command with required parameters
        command = ["kaggle", "kernels", "list", "--csv", "--competition", competition_handle, "--sort-by", sort_by, "--page-size", str(topk)]

        # Run the Kaggle command and capture the output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr}")

        # Parse the CSV data into a Pandas DataFrame
        csv_data = result.stdout
        df = pd.read_csv(StringIO(csv_data))
        return df

    except Exception as e:
        print(f"An error occurred: {e} while fetching kernels for competition: {competition_handle}")
        return pd.DataFrame()

def get_top_kaggle_kernels(competition_handle):
    kernal_dfs = []

    df = get_kaggle_kernels(competition_handle, sort_by="voteCount", topk=5)
    kernal_dfs.append(df)

    df = get_kaggle_kernels(competition_handle, sort_by="hotness", topk=5)
    kernal_dfs.append(df)

    df = get_kaggle_kernels(competition_handle, sort_by="scoreDescending", topk=5)
    kernal_dfs.append(df)

    df = get_kaggle_kernels(competition_handle, sort_by="viewCount", topk=5)
    kernal_dfs.append(df)

    df = get_kaggle_kernels(competition_handle, sort_by="voteCount", topk=5)
    kernal_dfs.append(df)

    df = pd.concat(kernal_dfs, ignore_index=True)

    if df.empty:
        return None

    # Remove duplicate rows based on kernel-handle
    df.drop_duplicates(subset="ref", inplace=True)

    df.rename(columns={"ref": "kernel-handle"}, inplace=True)
    df["competition-handle"] = competition_handle
    df["local-filename"] = df["kernel-handle"].apply(lambda kernel_ref: create_local_filename(kernel_ref))

    return df

def create_local_filename(kernel_ref):
    try:
        # Separate account name and notebook name, then sanitize
        parts = kernel_ref.split("/")
        if len(parts) == 2:
            account_name, notebook_name = parts
        else:
            raise ValueError(f"Invalid kernel_ref format: {kernel_ref}")

        sanitized_account_name = re.sub(r"[\\/:*?\"<>|]", "_", account_name)
        sanitized_notebook_name = re.sub(r"[\\/:*?\"<>|]", "_", notebook_name)

        # Create the output filename with account name and notebook name separated by "__"
        return f"{sanitized_account_name}__{sanitized_notebook_name}.ipynb"

    except Exception as e:
        print(f"Error creating local filename for {kernel_ref}: {e}")
        return None

def download_kaggle_notebook(kernel_ref, output_path="."):
    try:
        # Get the local filename
        local_filename = create_local_filename(kernel_ref)
        output_file = f"{output_path}/{local_filename}"

        # Build the Kaggle command to download the kernel
        command = ["kaggle", "kernels", "pull", kernel_ref, "-p", output_path]

        # Run the command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr}")

        print(f"Kernel '{kernel_ref}' downloaded successfully to '{output_file}'")

    except Exception as e:
        print(f"An error occurred while downloading the kernel: {e}")

if __name__ == "__main__":

    json_filename = "meta_files/competitions_sortedbysize.json"  # Replace with your JSON file
    competition_handles = extract_competition_handles_from_file(json_filename)
    print("Extracted competition handles:", competition_handles)
    print(f"Total {len(competition_handles)} with Tabular tag")

    competition_handles = competition_handles[:5] # UNCOMMENT TO RUN ON ALL


    all_kernels = []

    failed_competitions = []
    for competition_handle in tqdm(competition_handles):
        # print(f"Processing competition: {competition_handle}")
        df = get_top_kaggle_kernels(competition_handle=competition_handle)
        # Add columns for competition handle, kernel handles, and local filenames

        if df is not None:
            all_kernels.append(df)
        else:
            print(f"Failed to load kernels for competition: {competition_handle}")
            failed_competitions.append(competition_handle)

    if all_kernels:
        combined_df = pd.concat(all_kernels, ignore_index=True)
        combined_df.drop_duplicates(subset="kernel-handle", inplace=True)
        combined_csv = "all_competitions_kernels.csv"
        combined_df.to_csv(combined_csv, index=False)
        print(f"Failed {len(failed_competitions)} competitions: {failed_competitions}")
        print(f"Combined DataFrame saved to {combined_csv}. Rows : {len(combined_df)}")
    else:
        print("No kernels data available to combine.")
