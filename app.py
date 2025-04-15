from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='首頁')

@app.route('/about')
def about():
    return render_template('about.html', title='關於')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        file = request.files.get('file')
        
        # 檢查是否有文字輸入或文件上傳
        if not text_input and (not file or file.filename == ''):
            return render_template('upload.html', title='上傳', error='請輸入文字或上傳文件')
        
        # 處理文字輸入
        if text_input:
            # 這裡添加文字分析邏輯
            result = "您的文字已成功分析！"
            return render_template('result.html', title='分析結果', result=result, content=text_input)
        
        # 處理文件上傳
        if file:
            filename = file.filename
            # 這裡可以添加文件處理邏輯
            result = "您的文件已上傳並成功分析！"
            return render_template('result.html', title='分析結果', result=result, filename=filename)
    
    return render_template('upload.html', title='上傳')

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
