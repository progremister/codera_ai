# Install Flask if you haven't already
# pip install Flask

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process-code', methods=['POST'])
def process_code():
    if request.is_json:
        content = request.get_json()
        code_string = content['code']
        # Get the first three words from the code string
        first_three_words = ' '.join(code_string.split()[:3])
        return jsonify({"response": first_three_words})
    else:
        return "Invalid request", 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
