from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='首頁')

@app.route('/about')
def about():
    return render_template('about.html', title='關於')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # 這裡您可以添加處理表單數據的代碼
        return render_template('thank_you.html', name=name)
    return render_template('contact.html', title='聯繫我們')

if __name__ == '__main__':
    app.run(debug=True)
