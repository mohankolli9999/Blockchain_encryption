

from flask import Flask, render_template, request, session, url_for
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def sha256_hash(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    return sha256.hexdigest()

@app.route('/')
def index():
    # Clear the previous_hashed_output when returning to the index page
    session.pop('previous_hashed_output', None)
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get input string from the form
        input_string = request.form['input_string']

        # Retrieve the previous hashed output from the session or set it to an empty string for the first input
        previous_hashed_output = session.get('previous_hashed_output', '')

        # Combine the previous hashed output with the current input string
        combined_string = f"{previous_hashed_output}{input_string}"

        # Calculate the hash of the combined string
        hashed_output = sha256_hash(combined_string)

        # Update the session with the current hashed output for the next input
        session['previous_hashed_output'] = hashed_output

        return render_template('result.html', input_string=input_string, hashed_output=hashed_output)

if __name__ == '__main__':
    app.run(debug=True)
