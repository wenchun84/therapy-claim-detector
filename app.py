from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上傳文件大小為16MB

# 確保上傳目錄存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', title='首頁')

@app.route('/about')
def about():
    return render_template('about.html', title='關於')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 檢查是否有文件部分
        if 'file' not in request.files:
            return render_template('upload.html', title='上傳', error='沒有選擇文件')
        
        file = request.files['file']
        
        # 如果用戶未選擇文件，browser也會提交一個沒有檔名的空文件部分
        if file.filename == '':
            return render_template('upload.html', title='上傳', error='沒有選擇文件')
        
        if file:
            # 保存文件
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # 這裡可以添加文件分析代碼
            result = "您的文件已上傳並成功分析！"
            
            return render_template('result.html', title='分析結果', result=result, filename=file.filename)
    
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
