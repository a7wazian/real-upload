import os
import random
import requests
import shutil
import time

def download_file(url, destination, max_speed=102400, timeout=180):

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0
    start_time = time.time()  # Start time of the download
    try:
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    elapsed_time = time.time() - start_time
                    download_speed = downloaded_size / elapsed_time  # Instant download speed
                    download_speed_MB = download_speed / (1024 * 1024)  # Convert to megabytes per second
                    progress = (downloaded_size / total_size) * 100
                    print(f"Downloading... {progress:.2f}% completed, Download Speed: {download_speed_MB:.2f} MB/s", end='\r')
                    # Control download speed
                    if download_speed > max_speed:
                        remaining_time = (downloaded_size / max_speed) - elapsed_time
                        if remaining_time > 0:
                            time.sleep(remaining_time)
                    # Check timeout
                    if elapsed_time > timeout:
                        raise TimeoutError("Download timed out")
    except KeyboardInterrupt:
        print("\nDownload interrupted by user!")
    except TimeoutError:
        print("\nDownload timed out!")
        os.remove(destination)  # Remove the partially downloaded file if the download times out
    else:
        print("\nDownload completed!")

def main():
    file_path = "urls.txt"
    with open(file_path, "r") as file:
        urls = file.readlines()
    random_url = random.choice(urls).strip()  # Randomly select one URL from the list
    file_name = random_url.split("/")[-1]
    print(f"Downloading file from: {random_url}")
    download_file(random_url, file_name, max_speed=12000*1024, timeout=180)  # Max speed in bytes per second, timeout in seconds
    try:
        os.remove(file_name)  # Remove the downloaded file
        print(f"File {file_name} removed!\n")
    except FileNotFoundError:
        print(f"File {file_name} not found!\n")

if __name__ == "__main__":
    main()
