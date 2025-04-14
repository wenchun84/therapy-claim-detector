from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='首頁')

@app.route('/about')
def about():
    return render_template('about.html', title='關於')

if __name__ == '__main__':
    app.run(debug=True)
