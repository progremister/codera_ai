import sys
import os
import git
import requests  # Import the requests library here

def clone_repository(repo_url):
    base_path = os.path.abspath("/Users/kyrylo/Python/Parser/repositories")
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

def concatenate_code(repo_path):
    all_code = ""
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d != '.git']  
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

def send_to_server(code):
    url = 'http://localhost:8000/process-code' 
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={"code": code}, headers=headers)
    if response.status_code == 200:
        print("Response from server:", response.json())
    else:
        print("Failed to send code to server")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Parser.py <repository_url>")
    else:
        repo_url = sys.argv[1]
        repo_path = clone_repository(repo_url)
        if repo_path:
            combined_code = concatenate_code(repo_path)
            send_to_server(combined_code)
