import os
import requests
import zipfile
from pathlib import Path

def download_and_extract():
    url = "https://ndownloader.figshare.com/files/8606371"
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    data_dir = workspace_dir / "data"
    zip_path = workspace_dir / "anonymisedData.zip"

    # Create directories
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading dataset from {url}...")
    try:
        # Using a custom user-agent to ensure no blocking
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Download complete.")
        
        print("Extracting ZIP archive...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(data_dir)
        print(f"Extraction complete. Files extracted to: {data_dir}")
        
        # Remove zip file after extraction
        os.remove(zip_path)
        print("Cleaned up ZIP file.")
        
        # Verify files
        files = os.listdir(data_dir)
        print(f"Extracted files: {files}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        if zip_path.exists():
            os.remove(zip_path)

if __name__ == "__main__":
    download_and_extract()
