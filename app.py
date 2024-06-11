from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        command = request.form['command']
        # Vulnerable code 1
        output = os.popen(command).read()

        # Vulnerable code 1 fix 
        # output = os.popen(command).read()
        return render_template_string('''
            <!doctype html>
            <title>Command Injection</title>
            <h1>Command Injection Vulnerability Example</h1>
            <form method=post>
                Command: <input type=text name=command>
                <input type=submit value=Run>
            </form>
            <h2>Output:</h2>
            <pre>{{output}}</pre>
        ''', output=output)
    return render_template_string('''
        <!doctype html>
        <title>Command Injection</title>
        <h1>Command Injection Vulnerability Example</h1>
        <form method=post>
            Command: <input type=text name=command>
            <input type=submit value=Run>
        </form>
    ''')

if __name__ == '__main__':
    # vulnerable code 2
    # app.run(debug=True)
