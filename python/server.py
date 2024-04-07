import os
import git
import shutil
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def clone_repository(repo_url):
    base_path = os.path.abspath("./repositories")
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    target_path = os.path.join(base_path, repo_name)
    
    try:
        os.makedirs(target_path, exist_ok=True)
        git.Repo.clone_from(repo_url, target_path)
        print(f"Repository cloned successfully to {target_path}")
        return target_path
    except Exception as e:
        print(f"An error occurred while cloning the repository: {e}")
        return None

def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read()
        return True
    except UnicodeDecodeError:
        return False
    
def send_code_to_llm(code):
    url = 'http://localhost:11434/api/chat'  # This URL should point to your LLM service
    payload = {
        "model": "llama2",  # or whichever model you're using
        "temperature": 0.6,  # adjust as needed
        "messages": [
            {"role": "system", "content": "Analyze this code:"},
            {"role": "user", "content": code}
        ]
    }
    response = requests.post(url, json=payload)
    return response.json()

def concatenate_code(repo_path):
    all_code = ""
    for root, dirs, files in os.walk(repo_path):
        if '.git' in root:
            continue
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_text_file(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        code = file.read()
                        normalized_code = ' '.join(code.split())
                        all_code += normalized_code + ' '
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
    return all_code.strip()

def delete_repository(repo_path):
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        print(f"Deleted repository at {repo_path}")

@app.route('/process-repo', methods=['POST'])
def process_repo():
    if request.is_json:
        content = request.get_json()
        repo_url = content['repo_url']
        
        repo_path = clone_repository(repo_url)
        if repo_path:
            combined_code = concatenate_code(repo_path)
            delete_repository(repo_path)  # Clean up after processing
            
            # Send the combined code to LLM for analysis
            llm_response = send_code_to_llm(combined_code)
            return jsonify(llm_response)
        else:
            return jsonify({"error": "Failed to clone and process the repository"})
    else:
        return "Invalid request", 400


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
