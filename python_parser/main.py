import sys
import os
import json
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import git
from pygments.lexers import guess_lexer_for_filename

def clone_repository(repo_url):
    base_path = os.path.abspath("/Users/kyrylo/Python/repositories")
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

def tokenize_java(code):
    tokens = code.split()
    return tokens

def analyze_code(repo_path):
    code_tokens = {}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d != '.git']
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_text_file(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        code = file.read()
                        try:
                            lexer = guess_lexer_for_filename(file_path, code)
                            language = lexer.aliases[0]
                        except Exception:
                            language = 'unknown'
                        tokens = tokenize_java(code) if language == 'java' else code.split()
                        code_tokens[file_name] = {
                            "tokens": tokens,
                            "language": language
                        }
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
    return code_tokens




def save_to_json(data, output_file='code_structure.json'):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <repository_url>")
    else:
        repo_url = sys.argv[1]
        repo_path = clone_repository(repo_url)
        if repo_path:
            code_data = analyze_code(repo_path)
            save_to_json(code_data)
