
import requests
import pandas as pd
import time
from tqdm import tqdm

failed_competitions = []
def get_kernel_view_model(competition_url, author_user_name, kernel_slug, max_retries=6):
    global failed_competitions
    url = "https://www.kaggle.com/api/i/kernels.LegacyKernelsService/GetKernelViewModel"

    headers = {
        "accept": "application/json",
        "accept-language": "en-IN,en;q=0.9,ml-IN;q=0.8,ml;q=0.7,en-GB;q=0.6,en-US;q=0.5,id;q=0.4,ar;q=0.3",
        "content-type": "application/json",
        "origin": "https://www.kaggle.com",
        "priority": "u=1, i",
        "referer": "https://www.kaggle.com/competitions/titanic/code",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "x-kaggle-build-version": "9ce5d950acf3f19742f3cf2452aec088d368e212",
        "x-xsrf-token": "CfDJ8H3GHv39YMxDjEpKbXZX9wH9SBSLK5XB5fm4EMmJ2Z45En9LQWeqwxls6pBWklIgUzJBNtmcwAu2VTISy-FxXjpBnmINabkmYiCOF4J8Fg7ikA",
        "cookie": "_ga=GA1.1.142829654.1724970927; _ga_T7QHS60L4Q=GS1.1.1727546524.18.1.1727546554.0.0.0; ACCEPTED_COOKIES=true; ka_sessionid=7de5bfe771577548bfbf7b01654a404f; GCLB=CJySpouzhrvIahAD; build-hash=9ce5d950acf3f19742f3cf2452aec088d368e212; CSRF-TOKEN=CfDJ8H3GHv39YMxDjEpKbXZX9wFZJKjiPtMtGRByy61voDRkd4p_tFcDNuO3kY99oH5N0H8ThJIbobUyHrwIjZyvboITfb_2MkGkTxJ67ntuZw; XSRF-TOKEN=CfDJ8H3GHv39YMxDjEpKbXZX9wH9SBSLK5XB5fm4EMmJ2Z45En9LQWeqwxls6pBWklIgUzJBNtmcwAu2VTISy-FxXjpBnmINabkmYiCOF4J8Fg7ikA; CLIENT-TOKEN=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpc3MiOiJrYWdnbGUiLCJhdWQiOiJjbGllbnQiLCJzdWIiOiIiLCJuYnQiOiIyMDI1LTA4LTAyVDAxOjQ0OjQ4LjI0NjU2NDFaIiwiaWF0IjoiMjAyNS0wOC0wMlQwMTo0NDo0OC4yNDY1NjQxWiIsImp0aSI6ImZjNzA1NTYxLWUzNWYtNDUzZC1iOTQwLTc4OTZjYzA0MjJiMyIsImV4cCI6IjIwMjUtMDktMDJUMDE6NDQ6NDguMjQ2NTY0MVoiLCJhbm9uIjp0cnVlLCJmZiI6WyJLZXJuZWxzT3BlbkluQ29sYWJMb2NhbFVybCIsIk1ldGFzdG9yZUNoZWNrQWdncmVnYXRlRmlsZUhhc2hlcyIsIlVzZXJMaWNlbnNlQWdyZWVtZW50U3RhbGVuZXNzVHJhY2tpbmciLCJLZXJuZWxzU2V0dGluZ3NUYWIiLCJLZXJuZWxzUGF5VG9TY2FsZSIsIlVuaWZpZWRWb3Rlc1JlYWQiLCJCZW5jaG1hcmtzTGFuZGluZyIsIkRhdGFzZXRzU2ltaWxhclJlZnJlc2giLCJSZW5hbWVDb250cmlidXRvclRvS2FnZ2xlciIsIlJldmlzZWRDb21wZXRpdGlvbkdtUGx1c0xldmVscyIsIlJlZGlyZWN0S2FnZ2xlT3JnQmVuY2htYXJrcyIsIkNvbW11bml0eVdyaXRlVXBzIiwiRmVhdHVyZWRNb2RlbHNTaGVsZiIsIkRhdGFzZXRQb2xhcnNEYXRhTG9hZGVyIiwiS2VybmVsc0ZpcmViYXNlTG9uZ1BvbGxpbmciLCJGcm9udGVuZEVycm9yUmVwb3J0aW5nIiwiQWxsb3dGb3J1bUF0dGFjaG1lbnRzIiwiVGVybXNPZlNlcnZpY2VCYW5uZXIiLCJSZWdpc3RyYXRpb25OZXdzRW1haWxTaWdudXBJc09wdE91dCIsIkRhdGFzZXRVcGxvYWRlckR1cGxpY2F0ZURldGVjdGlvbiJdfQ=="
    }

    data = {
        "authorUserName": author_user_name,
        "kernelSlug": kernel_slug,
        "kernelVersionId": 0
    }


    retries = 0
    backoff = 2  # Initial wait time in seconds

    while retries < max_retries:
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors

            return response.json()  # Return the JSON response if successful
        except requests.exceptions.RequestException as e:
            print(f"Attempt {retries + 1} failed: {e}")
            retries += 1
            if retries < max_retries:
                sleep_time = backoff ** retries
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retries reached. Returning None.")
                failed_competitions.append(competition_url)
                return None  # Return None if all retries fail


def extract_public_score(api_response):
    """Extracts the best public score from the API response."""
    try:
        score =  api_response['kernel'].get('bestPublicScore', None)
        return score
    except (TypeError, KeyError):
        return None


def process_kernels(csv_file, output_file="all_competitions_kernels_combined_2.csv"):
    df = pd.read_csv(csv_file)

    # Initialize empty lists to store data
    kernel_metadata_list = []
    public_score_list = []
    save_interval = 250


    for i, row in tqdm(df.iterrows(), total=len(df)):
        kernel_handle = row['kernel-handle']
        author_user_name, kernel_slug = kernel_handle.split('/')

        # Fetch metadata
        api_response = get_kernel_view_model(
            f"https://www.kaggle.com/code/{kernel_handle}",
            author_user_name,
            kernel_slug
        )

        # Store metadata and public score
        kernel_metadata_list.append(api_response)
        public_score_list.append(extract_public_score(api_response) if api_response else None)

        # Save CSV after every save_interval rows
        if (i + 1) % save_interval == 0 or i == len(df) - 1:
            df.loc[:i, "kernel-metadata"] = pd.Series(kernel_metadata_list)
            df.loc[:i, "public-score"] = pd.Series(public_score_list)
            df.to_csv(output_file, index=False)
            print(f"Progress saved at row {i + 1}...")

    print(f"Final CSV saved as {output_file}")
    print(f"Total Failures :  {len(failed_competitions)}")
    print(f"Failed competitions :  {failed_competitions}")


process_kernels(csv_file="all_competitions_kernels_combined.csv",
                output_file="all_competitions_kernels_combined_2.csv")