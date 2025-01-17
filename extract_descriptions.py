import json
from bs4 import BeautifulSoup
import os

def read_html_file(filename):
    """Reads the content of an HTML file and returns it as a string."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def extract_description_by_id(html_content, element_id):
    """Extracts text content from an element with a specific ID in the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    description_section = soup.find(id=element_id)
    if description_section:
        return description_section.get_text(strip=True)
    else:
        return None

def extract_meta_description(html_content):
    """Extracts the content of the meta tag with name='description' in the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description and 'content' in meta_description.attrs:
        return meta_description['content']
    else:
        return None

def extract_dataset_description(html_content):
    """Extracts dataset description from the competition data page."""
    soup = BeautifulSoup(html_content, 'html.parser')
    dataset_section = soup.find('h2', string=lambda text: text and "Dataset Description" in text)
    if dataset_section:
        parent_div = dataset_section.find_next('div')
        if parent_div:
            return parent_div.get_text(strip=True)
        # If no direct sibling div, look further in the section
        return dataset_section.find_next(string=True).strip()
    return None

def get_html_filenames_from_json(json_file):
    """Reads a JSON file and returns a list of HTML filenames."""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return [item[0] for item in data]

def process_overview_page(file_path, extracted_data):
    """Processes an overview HTML page to extract descriptions."""
    try:
        html_content = read_html_file(file_path)

        # Extract description by ID
        description_by_id = extract_description_by_id(html_content, "description")
        if description_by_id:
            print(f"Overview Page - Description by ID: {description_by_id}")
            extracted_data['description'] = description_by_id
        else:
            print("Overview Page - Description section by ID not found.")

        # Extract meta description
        meta_description = extract_meta_description(html_content)
        if meta_description:
            print(f"Overview Page - Meta Description: {meta_description}")
            extracted_data['meta_description'] = meta_description
        else:
            print("Overview Page - Meta description not found.")

    except FileNotFoundError:
        print(f"Overview file not found: {file_path}")
    except Exception as e:
        print(f"Error processing overview page {file_path}: {e}")

    return extracted_data

def process_data_page(file_path, extracted_data):
    """Processes a data HTML page to extract dataset descriptions."""
    try:
        html_content = read_html_file(file_path)

        # Extract dataset description
        dataset_description = extract_dataset_description(html_content)
        if dataset_description:
            print(f"Data Page - Dataset Description: {dataset_description}")
            extracted_data['dataset_description'] = dataset_description
        else:
            print("Data Page - Dataset description not found.")

    except FileNotFoundError:
        print(f"Data file not found: {file_path}")
    except Exception as e:
        print(f"Error processing data page {file_path}: {e}")

    return extracted_data

def process_html_files(base_folder_overview, base_folder_data, html_files):
    """Processes both overview and data HTML files."""
    final_result = {}
    for html_file in html_files:
        extracted_data = {}

        # Process overview page
        overview_path = os.path.join(base_folder_overview, html_file)
        print(f"\nProcessing Overview Page: {overview_path}")
        extracted_data = process_overview_page(overview_path, extracted_data)

        # Process data page
        data_path = os.path.join(base_folder_data, html_file)
        print(f"\nProcessing Data Page: {data_path}")
        extracted_data = process_data_page(data_path, extracted_data)

        final_result[html_file] = extracted_data
    return final_result

def save_extracted_data(result, output_file):
    """Saves the extracted data to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    print(f"\nFinal extracted data has been saved to {output_file}")

def main():
    # Path to the JSON file
    json_file = "meta_files/competitions_sortedbysize.json"

    # Get the list of HTML filenames from the JSON
    html_files = get_html_filenames_from_json(json_file)

    # Define the base folders for overview and data pages
    base_folder_overview = "competition_pages_overview"
    base_folder_data = "competition_pages_data"

    # Process the HTML files
    result = process_html_files(base_folder_overview, base_folder_data, html_files)

    # Save the result to a JSON file
    save_extracted_data(result, "extracted_data.json")

if __name__ == "__main__":
    main()
