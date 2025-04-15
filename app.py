from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        file = request.files.get('file')
        
        if not text_input and (not file or file.filename == ''):
            return render_template('index.html', title='文章檢測', error='請輸入文字或上傳文件')
        
        if text_input:
            # 文字分析邏輯
            result = "檢測結果：您的聲明文字中有潛在違規內容。按照《食品標示宣傳廣告及不實標示易生誤解或具有虛偽誇張內容之認定基準》，療效相關聲明不應包含「排除體內毒素」、「遠離疾病困擾」等醫療效果宣稱。"
            return render_template('result.html', title='檢測結果', result=result, content=text_input)
        
        if file:
            filename = file.filename
            result = "檢測結果：您上傳的文件中有潛在違規內容。按照《食品標示宣傳廣告及不實標示易生誤解或具有虛偽誇張內容之認定基準》，療效相關聲明不應包含過度的健康效果宣稱。"
            return render_template('result.html', title='檢測結果', result=result, filename=filename)
    
    return render_template('index.html', title='文章檢測', active_tab='article')

@app.route('/word')
def word():
    return render_template('word.html', title='單詞檢測', active_tab='word')

@app.route('/stats')
def stats():
    return render_template('stats.html', title='違規統計', active_tab='stats')

@app.route('/examples')
def examples():
    return render_template('examples.html', title='違規案例', active_tab='examples')

@app.route('/about')
def about():
    return render_template('about.html', title='關於我們', active_tab='about')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        return render_template('thank_you.html', title='謝謝您的訊息', name=name)
    return render_template('contact.html', title='聯繫我們', active_tab='contact')

if __name__ == '__main__':
    app.run(debug=True)
