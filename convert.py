import json
import os
import argparse

def get_conversation(node_id, mapping, list):
    node = mapping[node_id]
    if 'message' in node and node['message'] is not None:
        content_parts = node['message']['content']['parts']
        if len(content_parts) > 0:
            author_role = node['message']['author']['role']
            list.append(f"## {author_role}\n {''.join(content_parts)}")

    for child_id in node.get('children', []):
        get_conversation(child_id, mapping, list)

def main(input_file, output_dir):
    # Check if the directory exists
    if not os.path.isdir(output_dir):
        # If not, create the directory
        os.makedirs(output_dir)

    with open(input_file) as f:
        data = json.loads(f.read())
        for item in data:
            title = item["title"].replace("/","_").replace('"','')
            if title == "New chat":
                title = "New chat " + str(int(item["create_time"]))
            root_node_id = [node_id for node_id, node in item['mapping'].items() if node['parent'] is None][0]
            list = []
            get_conversation(root_node_id, item['mapping'], list)
            with open(f'{output_dir}/{title}.md', 'w') as outfile:
                outfile.write('\n'.join(list))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Your ChatGPT conversations to Markdown.')
    parser.add_argument('input_file', help='JSON file containing conversations')
    parser.add_argument('output_dir', help='Directory to save output Markdown files')
    
    args = parser.parse_args()
    main(args.input_file, args.output_dir)
