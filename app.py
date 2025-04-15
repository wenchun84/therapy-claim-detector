from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 允許JSON包含非ASCII字符

# 違規詞彙列表 - 擴充自合規指南
violation_words = [
    # 明確違法用字（涉及醫療效能）
    # 1. 宣稱預防、改善、減輕、診斷或治療疾病
    '治療', '預防', '治癒', '排毒', '醫治', '根治', '防治', '醫療效果', 
    '改善過敏', '防止便秘', '降血壓', '清血', '調整內分泌', '恢復視力',
    '壯陽', '強精', '減輕過敏性皮膚病', '治失眠', '防止貧血', '改善血濁',
    '防止更年期的提早', '治療肌少症', '逆轉肌肉萎縮', '治療退化性關節炎',
    
    # 2. 宣稱產品對疾病及症狀有效
    '消滯', '降肝火', '改善喉嚨發炎', '祛痰止喘', '消腫止痛', '消除心律不整',
    '解毒', '改善更年期障礙', '關節炎', '關節退化', '清除血脂', '清除毒素',
    '溶解血栓', '溶解斑塊', '逆轉硬化狹窄', '恢復血管彈性', '遠離重症', '遠離後遺症',
    '根除心腦血管疾病',
    
    # 3. 宣稱減輕疾病相關體內成分
    '解肝毒', '降肝脂', '活化腦細胞', '再生年輕細胞', '減緩失智', '減緩骨質流失',
    '活化婦宮機能',
    
    # 4. 涉及中藥材效能詞彙
    '補腎', '溫腎', '滋腎', '固腎', '健脾', '補脾', '益脾', '溫脾',
    '和胃', '養胃', '補胃', '益胃', '養心', '清心火', '補心', '寧心',
    '清肺', '宣肺', '潤肺', '傷肺', '疏肝', '養肝', '瀉肝', '鎮肝',
    '澀腸', '潤腸', '活血', '化瘀',
    
    # 易生誤解或誇張用字
    '增強抵抗力', '強化細胞功能', '增智', '補腦', '增強記憶力', '改善體質',
    '解酒', '清除自由基', '排毒素', '分解有害物質', '平胃氣', '防止口臭',
    '激活全身長壽蛋白', '增生膠原蛋白', '提升男性能力', '保護眼睛', '增加血管彈性',
    
    # 涉及改變身體外觀的詞彙
    '豐胸', '預防乳房下垂', '減肥', '瘦身', '塑身', '增高', '使頭髮烏黑',
    '延遲衰老', '防止老化', '改善皺紋', '美白',
    
    # 其他誇張表述
    '根除', '完全消除', '永久恢復', '徹底解決', '無副作用', '百分百有效',
    '立即見效', '神奇療效'
]

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

@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html', title='食品廣告合規指南', active_tab='guidelines')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q', '')
    results = []
    
    if query:
        # 違法用字
        illegal_words = {
            '治療': {'reason': '明示療效', 'alternative': '調節生理機能'},
            '改善過敏': {'reason': '明示療效', 'alternative': '調整體質'},
            '防止便秘': {'reason': '明示便秘為病症', 'alternative': '使排便順暢'},
            '降血壓': {'reason': '明示療效', 'alternative': '調節生理機能'},
            '清血': {'reason': '明示療效', 'alternative': '促進新陳代謝'},
            '調整內分泌': {'reason': '明示療效', 'alternative': '調節生理機能'}
            # 可以從合規指南加入更多詞彙
        }
        
        # 易生誤解詞彙
        misleading_words = {
            '增強抵抗力': {'reason': '誇張或易生誤解', 'alternative': '調節生理機能'},
            '強化細胞功能': {'reason': '誇張或易生誤解', 'alternative': '調節生理機能'}
            # 可以從合規指南加入更多詞彙
        }
        
        # 合法詞彙
        legal_words = {
            '幫助牙齒骨骼正常發育': {'reason': '通常可用詞句'},
            '幫助消化': {'reason': '通常可用詞句'}
            # 可以從合規指南加入更多詞彙
        }
        
        # 搜尋違法用字
        for word, info in illegal_words.items():
            if query.lower() in word.lower():
                results.append({
                    'word': word,
                    'type': '違法用字',
                    'reason': info['reason'],
                    'alternative': info.get('alternative', '-')
                })
        
        # 搜尋易生誤解詞彙
        for word, info in misleading_words.items():
            if query.lower() in word.lower():
                results.append({
                    'word': word,
                    'type': '易生誤解詞彙',
                    'reason': info['reason'],
                    'alternative': info.get('alternative', '-')
                })
        
        # 搜尋合法詞彙
        for word, info in legal_words.items():
            if query.lower() in word.lower():
                results.append({
                    'word': word,
                    'type': '合法詞彙',
                    'reason': info['reason'],
                    'alternative': '-'
                })
    
    return render_template('search.html', title='搜尋結果', active_tab='guidelines', query=query, results=results)

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
