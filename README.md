# Convert your ChatGPT conversations to Markdown

## Overview
This project consists of a Python script, `convert.py`, which is designed to process conversation data from ChatGPT and convert it into Markdown format. The script takes a JSON file containing conversation data and outputs a series of Markdown files, each representing a conversation thread.

You can export your data by following this documenation below

[https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data](https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data)



## Getting Started

### Prerequisites
- Python 3.x
- Access to the command line or terminal

### Installation
No additional libraries are required for this script, as it only uses modules from the Python Standard Library.

### Usage
1. **Prepare Your Data:** Ensure your conversation data is in a JSON format compatible with the script.
2. **Run the Script:** Use the command line to navigate to the directory containing `convert.py` and run the following command:

   ```bash
   python convert.py [input_file] [output_dir]
   ```

   - Replace `[input_file]` with the path to your JSON file containing the conversation data.
   - Replace `[output_dir]` with the path to the directory where you want the Markdown files to be saved.

   Example:

   ```bash
   python convert.py conversations.json output
   ```

3. **Check Output:** After running the script, the Markdown files will be saved in the specified output directory, with each file representing a conversation from the input data.

## File Structure
- `convert.py`: The main script that processes the JSON data and converts it to Markdown format.
- `README.md`: This file, containing instructions and information about the project.

## License
This project is open source and available under MIT.