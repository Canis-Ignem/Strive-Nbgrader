from flask import Flask, render_template, request


app = Flask(__name__, template_folder='.')

@app.route("/")
def index():
    return render_template('nbgrader-index.html')

@app.route('/nbgrader-index.html', methods=['GET', 'POST','SUBMIT'] )
def contact():
    if request.method == 'POST':
        if request.form['create_folders'] == 'students':
            return "Welcome"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)