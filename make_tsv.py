import hashlib
import base64
import requests

def get_file_size(url):
    response = requests.head(url)
    return int(response.headers.get('Content-Length', 0))

def get_md5_checksum(url):
    response = requests.get(url, stream=True)
    hash_md5 = hashlib.md5()
    for chunk in response.iter_content(chunk_size=4096):
        hash_md5.update(chunk)
    return base64.b64encode(hash_md5.digest()).decode('utf-8')

def create_url_list(urls, output_file):
    with open(output_file, 'w') as file:
        # Write the format specifier
        file.write("TsvHttpData-1.0\n")
        for url in sorted(urls):
            try:
                size = get_file_size(url)
                md5_checksum = get_md5_checksum(url)
                file.write(f"{url}\t{size}\t{md5_checksum}\n")
            except Exception as e:
                print(f"Failed to process {url}: {e}")

if __name__ == "__main__":
    urls = [
        'https://raw.githubusercontent.com/cd-public/books/main/pg34405.txt',
        'https://raw.githubusercontent.com/cd-public/books/main/pg38539.txt',
        'https://raw.githubusercontent.com/cd-public/books/main/pg33698.txt',
        'https://raw.githubusercontent.com/cd-public/books/main/pg37610.txt',
        'https://raw.githubusercontent.com/cd-public/books/main/pg38622.txt'
    ]
    create_url_list(urls, 'url_list.tsv')
