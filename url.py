import os
import subprocess

def is_nginx_installed():
    try:
        # Use the full path to nginx if necessary, for example: /usr/sbin/nginx
        subprocess.run(["nginx", "-v"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

def install_nginx():
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "nginx"], check=True)
        print("Nginx installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install Nginx.")
        exit(1)

def create_files(num_files, file_size, file_names):
    base_path = '/var/www/html'
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
        
    for i in range(num_files):
        file_name = file_names[i] + '.zip'
        file_path = os.path.join(base_path, file_name)
        with open(file_path, 'wb') as f:
            f.seek(int(file_size * 1024 * 1024 * 1024) - 1)
            f.write(b'\0')

def generate_download_links(subdomain, file_names):
    links = []
    for file_name in file_names:
        download_link = f"https://{subdomain}/{file_name}.zip"
        links.append(download_link)
    return links

def write_links_to_file(links):
    with open('urls.txt', 'w') as f:
        for link in links:
            f.write(link + '\n')

def main():
    # Check if nginx is installed
    if not is_nginx_installed():
        print("Nginx is not installed. Installing...")
        install_nginx()

    # Get inputs from user
    num_files = int(input("Enter the number of files to create: "))
    file_size_gb = float(input("Enter the size of each file in GB: "))
    subdomain = input("Enter the subdomain: ")
    file_names = []
    for i in range(num_files):
        file_name = input(f"Enter name for file {i+1}: ")
        file_names.append(file_name)

    # Create files
    create_files(num_files, file_size_gb, file_names)

    # Generate download links
    download_links = generate_download_links(subdomain, file_names)

    # Write links to url.txt
    write_links_to_file(download_links)

    print(f"Files created successfully. Download links saved in urls.txt.")

if __name__ == "__main__":
    main()
