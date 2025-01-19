# kaggle-crawler

To download the notebook files and process the codes, run the follwoing scripts in this order
1. [fetch_kernel_metadata.py](scripts%2Ffetch_kernel_metadata.py) : This saves a csv containing top notebooks from all competitions. 
2. [download_kernels.py](scripts%2Fdownload_kernels.py) : This uses the kaggle cli to download all notebook files.
3. [extract_code_contents.py](scripts%2Fextract_code_contents.py) : This extracts the code and markup text contents from the notebook files and saves as txt files.  