"""
This script downloads Kaggle kernels listed in a CSV file.

- The CSV file should have two columns:
  1. `kernel-handle`: The handle of the kernel on Kaggle (e.g., `author/kernel-name`).
  2. `local-filename`: The desired filename for saving the kernel locally.

- The script downloads kernels to a temporary directory and renames them based on `local-filename`.
- If a download fails, the script retries up to 2 times, doubling the wait time (initially 5 seconds) between retries.
- The final files are saved in the `code_files` directory (default).
- Temporary files are cleaned up after processing.
"""

import pandas as pd
import subprocess
import os
import glob
import time

def download_kernels_from_csv(csv_filename, output_dir="code_files", temp_dir="temp_downloads"):
    try:
        # Ensure the output and temp directories exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)

        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_filename)

        # Iterate through the rows and download each kernel
        for index, row in df.iterrows():
            kernel_handle = row["kernel-handle"]
            local_filename = row["local-filename"]
            temp_path = temp_dir
            final_path = os.path.join(output_dir, local_filename)

            # Build the Kaggle command
            command = ["kaggle", "kernels", "pull", kernel_handle, "-p", temp_path]

            retries = 2
            sleep_time = 5
            while retries >= 0:
                try:
                    # Execute the command
                    result = subprocess.run(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                    # Check for errors
                    if result.returncode != 0:
                        raise Exception(f"Error: {result.stderr}")

                    # Find the downloaded file in the temp directory
                    matching_files = glob.glob(os.path.join(temp_path, f"{kernel_handle.split('/')[1]}*.*"))

                    if matching_files:
                        downloaded_file = matching_files[0]  # Take the first match
                        os.rename(downloaded_file, final_path)  # Move and rename the file
                        print(f"Kernel '{kernel_handle}' successfully saved to '{final_path}'")
                        break
                    else:
                        print(f"No matching file found for kernel '{kernel_handle}' in '{temp_path}'")
                        break

                except Exception as e:
                    print(f"Failed to download kernel '{kernel_handle}': {e}")
                    if retries > 0:
                        print(f"Retrying in {sleep_time} seconds... ({retries} retries left)")
                        time.sleep(sleep_time)
                        retries -= 1
                        sleep_time *= 2  # Double the sleep time for the next retry
                    else:
                        print(f"Exhausted retries for kernel '{kernel_handle}'")
                        break

        # Clean up the temp directory
        for temp_file in glob.glob(os.path.join(temp_dir, "*")):
            os.remove(temp_file)

    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")

if __name__ == "__main__":
    csv_filename = "all_competitions_kernels.csv"  # Replace with your CSV file
    download_kernels_from_csv(csv_filename)
