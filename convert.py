import json
import os
import argparse
from datetime import datetime

def sanitize_filename(filename):
    if filename is None or filename.strip() == "":
        return "noname"
    invalid_characters = '<>:"/\\|?*\n\t'
    for char in invalid_characters:
        filename = filename.replace(char, '')
    return filename

def get_conversation(node_id, mapping, list, last_author=None):
    node = mapping[node_id]
    if node.get('message') and 'content' in node['message'] and 'parts' in node['message']['content']:
        content_parts = node['message']['content']['parts']
        parts_text = []
        for part in content_parts:
            if isinstance(part, str):
                parts_text.append(part)
            elif isinstance(part, dict):
                parts_text.append(str(part))
        if parts_text:
            author_role = node['message']['author']['role']
            if author_role != "system" and author_role != last_author:
                list.append(f"## {author_role}\n{''.join(parts_text)}")
            elif author_role != "system":
                list.append(f"{''.join(parts_text)}")
            last_author = author_role

    for child_id in node.get('children', []):
        get_conversation(child_id, mapping, list, last_author)

def generate_unique_filename(base_path, title, existing_titles):
    title = title if title.strip() != "" else "noname"
    if title not in existing_titles:
        existing_titles[title] = 0
    else:
        existing_titles[title] += 1

    version = existing_titles[title]
    if version == 0:
        file_path = os.path.join(base_path, f"{title}.md")
    else:
        file_path = os.path.join(base_path, f"{title}_v{version}.md")
    
    return file_path

def main(input_file, output_dir, use_date_folders):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        existing_titles = {}
        for item in data:
            title = item.get("title")
            title = sanitize_filename(title)
            root_node_id = next(node_id for node_id, node in item['mapping'].items() if node.get('parent') is None)
            list = []
            get_conversation(root_node_id, item['mapping'], list)

            if use_date_folders:
                date_iso = datetime.fromtimestamp(item["create_time"]).date().isoformat()
                date_folder = os.path.join(output_dir, date_iso)
                if not os.path.isdir(date_folder):
                    os.makedirs(date_folder)
                file_path = generate_unique_filename(date_folder, title, existing_titles)
            else:
                file_path = generate_unique_filename(output_dir, title, existing_titles)

            print(f"Attempting to write to: {file_path}")
            with open(file_path, 'w', encoding='utf-8') as outfile:
                outfile.write('\n'.join(list))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process conversation data.')
    parser.add_argument('input_file', help='JSON file containing conversations')
    parser.add_argument('output_dir', help='Directory to save output Markdown files')
    parser.add_argument('--use-date-folders', action='store_true', help='Store files under date-based folders')

    args = parser.parse_args()
    main(args.input_file, args.output_dir, args.use_date_folders)
