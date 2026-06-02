import os
import requests
import re

UPLOAD_URL = "https://catbox.moe/user/api.php"

def upload_image(filepath):
    try:
        with open(filepath, 'rb') as f:
            files = {'fileToUpload': f}
            data = {'reqtype': 'fileupload'}
            response = requests.post(UPLOAD_URL, files=files, data=data)
            if response.status_code == 200:
                return response.text.strip()
    except Exception as e:
        print(f"Error uploading {filepath}: {e}")
    return None

def main():
    directory = 'images'
    url_mapping = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            print(f"Uploading {filepath}...")
            url = upload_image(filepath)
            if url:
                print(f"Success: {url}")
                rel_path = os.path.relpath(filepath, '.')
                posix_path = rel_path.replace('\\', '/')
                sub_path = posix_path.split('/', 1)[-1]
                url_mapping[sub_path] = url
            else:
                print(f"Failed to upload {filepath}")

    print("Updating HTML and CSS files...")
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'images' in root or 'images_temp' in root:
            continue
        for file in files:
            if file.endswith(('.html', '.css')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for sub_path, url in url_mapping.items():
                    # Exact string replacements to handle common ways it was referenced
                    new_content = new_content.replace(f"Images/{sub_path}", url)
                    new_content = new_content.replace(f"images/{sub_path}", url)
                    new_content = new_content.replace(f"./Images/{sub_path}", url)
                    new_content = new_content.replace(f"./images/{sub_path}", url)

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {filepath}")

if __name__ == '__main__':
    main()
