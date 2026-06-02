import os

directory = '.'

for root, dirs, files in os.walk(directory):
    if '.git' in root:
        continue
    for filename in files:
        if filename.endswith('.html') or filename.endswith('.css'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            new_content = content.replace('Images/', 'images/').replace('images_temp/', 'images/')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f'Updated {filepath}')
