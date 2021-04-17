from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__, template_folder='.')

@app.route("/")
def index():
    return render_template('nbgrader-index.html')

@app.route('/nbgrader-index.html', methods=['GET', 'POST','SUBMIT'] )
def contact():
    try:
        if request.method == 'POST':
        
            if request.files['names'] != None:        
                f = request.files['names']
                df = pd.read_pickle(f)
                return str(df.shape)
            else:
                return "HOLA YARA"
    except:
        return "hola yara"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)