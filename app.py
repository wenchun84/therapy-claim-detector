from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 允許JSON包含非ASCII字符

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        file = request.files.get('file')
        
        # 檢查是否有文字輸入或文件上傳
        if not text_input and (not file or file.filename == ''):
            return render_template('index.html', title='文章檢測', active_tab='article', error='請輸入文字或上傳文件')
        
        # 處理文字輸入
        if text_input:
            # 違規詞彙列表
            violation_words = ['治療', '預防', '治癒', '排毒', '醫治', '根治', '防治', '醫療效果', 
                          '治愈', '防護', '癒合', '消炎', '抑菌', '抗病毒', '抗癌', '保肝', 
                          '護肝', '改善疾病', '痊癒', '降血壓', '降血糖', '降膽固醇']
            
            # 檢查是否含有違規詞彙
            found_violations = []
            for word in violation_words:
                if word in text_input:
                    found_violations.append(word)
            
            if found_violations:
                result = f"檢測結果：您的聲明文字中發現潛在違規內容。按照《食品標示宣傳廣告及不實標示易生誤解或具有虛偽誇張內容之認定基準》，以下詞彙可能暗示醫療效果：{', '.join(found_violations)}"
                return render_template('result.html', title='檢測結果', active_tab='article', result=result, content=text_input, found_violations=found_violations)
            else:
                result = "檢測結果：您的聲明文字未發現明顯違規內容。但請注意，即使未使用明確的醫療用語，某些表述方式仍可能因整體語境而被視為暗示醫療效果。建議謹慎使用療效相關描述。"
                return render_template('result.html', title='檢測結果', active_tab='article', result=result, content=text_input, found_violations=None)
        
        # 處理文件上傳
        if file:
            filename = file.filename
            # 這裡添加文件處理邏輯
            result = "檢測結果：您上傳的文件中可能有潛在違規內容。按照《食品標示宣傳廣告及不實標示易生誤解或具有虛偽誇張內容之認定基準》，療效相關聲明不應包含過度的健康效果宣稱。"
            return render_template('result.html', title='檢測結果', active_tab='article', result=result, filename=filename, found_violations=None)
    
    return render_template('index.html', title='文章檢測', active_tab='article')

@app.route('/word', methods=['GET', 'POST'])
def word():
    result = None
    keyword = None
    
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        
        if not keyword:
            return render_template('word.html', title='單詞檢測', active_tab='word', error='請輸入要檢測的單詞')
        
        # 違規詞彙列表
        violation_words = ['治療', '預防', '治癒', '排毒', '醫治', '根治', '防治', '醫療效果', 
                          '治愈', '防護', '癒合', '消炎', '抑菌', '抗病毒', '抗癌', '保肝', 
                          '護肝', '改善疾病', '痊癒', '降血壓', '降血糖', '降膽固醇']
        
        # 檢查是否含有違規詞彙
        is_violation = keyword in violation_words
        
        if is_violation:
            result = f"「{keyword}」屬於違規用詞，不建議在食品或保健品宣傳中使用。此類詞彙暗示醫療效果，違反《食品安全衛生管理法》相關規定。"
        else:
            result = f"「{keyword}」未在常見違規詞彙列表中發現。但請注意，即使單詞本身合規，整體句子可能因上下文或組合方式而違規。"
    
    return render_template('word.html', title='單詞檢測', active_tab='word', result=result, keyword=keyword)

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
        # 這裡您可以添加處理表單數據的代碼
        return render_template('thank_you.html', title='謝謝您的訊息', active_tab='contact', name=name)
    return render_template('contact.html', title='聯繫我們', active_tab='contact')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html', title='食品廣告合規指南', active_tab='guidelines')
