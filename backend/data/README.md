# Dataset Access & Download Guide

## Overview
This repository includes datasets required for the Phishing Website Detection System. The datasets are currently hosted in a Microsoft OneDrive folder, and for convenience, they are also directly included in this repository.

## Available Datasets
The following CSV files are used in the project:

- `final_merged_dataset.csv` – Main dataset used for model training and evaluation  
- `hosting_websites.csv` – Contains hosting-related domain information  
- `url_shorteners.csv` – List of known URL shortening services  

## Dataset Links File
A text file is provided that contains all dataset download links:
- `dataset_links.txt`


This file includes direct links to each dataset stored in the OneDrive folder.

## Downloading Datasets from OneDrive

Follow these steps to download the datasets manually:

1. Open the `dataset_links.txt` file  
2. Copy any dataset link you want to download  
3. Paste the link into your browser  
4. Open the Microsoft OneDrive page  
5. Click on the **Download** button  
6. Save the file to your desired project directory (recommended: `/data/` or project root)

## Recommended Folder Structure

After downloading, organize your files like this:
## Recommended Folder Structure

```
phishing-website/
│
├── data/
│   ├── final_merged_dataset.csv
│   ├── hosting_websites.csv
│   └── url_shorteners.csv
```

## Note
Since the dataset files are relatively small in size, they have been directly included in this repository for ease of access. This allows users to quickly get started without needing to download them separately.

However, the OneDrive links are still provided for:
- Backup access  
- Future updates  
- Scalability if dataset size increases  

## Future Considerations
If the dataset size grows larger in future versions:
- Files may be removed from the repository  
- Only external download links will be maintained  
- Automated download scripts may be added  