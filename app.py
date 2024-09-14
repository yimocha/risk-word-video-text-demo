from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from videoTools import video_to_text

from TextRiskTools import check_banned_word, check_banned_word_list_text
# 删除临时的 WAV 文件（可选）
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_risk_word.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 定义数据模型
class TabRiskWord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    risk_name = db.Column(db.String(100), nullable=False)
    risk_level = db.Column(db.String(80), nullable=False)
    reason = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<TabRiskWord {self.risk_name}>'


# 导入数据文件
def execute_sql_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        sql = file.read()
    with app.app_context():
        db.session.execute(text(sql))
        db.session.commit()


# 创建数据库
with app.app_context():
    db.create_all()
    # 插入数据
    count = TabRiskWord.query.count()
    if count == 0:
        execute_sql_file('data.sql')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('a.html')


@app.route('/add_risk_word', methods=['POST'])
def add_risk_word():
    if 'risk_name' not in request.form or 'risk_level' not in request.form or 'reason' not in request.form:
        return jsonify({'msg': '参数错误'}), 400

    risk_name = request.form['risk_name']
    risk_level = request.form['risk_level']
    reason = request.form['reason']

    if not risk_name:
        return jsonify({'msg': '违禁词不能为空'}), 400

    if not risk_level:
        return jsonify({'msg': '违禁等级不能为空'}), 400

    if not reason:
        return jsonify({'msg': '解析不能为空'}), 400

    has_name = TabRiskWord.query.filter_by(risk_name=risk_name).count()
    if has_name > 0:
        return jsonify({'msg': '词语已经存在'}), 500

    new_risk_word = TabRiskWord(risk_name=risk_name, risk_level=risk_level, reason=reason)
    db.session.add(new_risk_word)
    db.session.commit()
    return jsonify({'data': new_risk_word, 'code': 200, 'msg': 'ok'})


@app.route('/update_word', methods=['POST'])
def update_word():
    if 'id' not in request.form:
        return jsonify({'msg': '参数错误'}), 400

    word_id = request.form['id']
    if not word_id:
        return jsonify({'msg': '关键参数错误'}), 400

    word = TabRiskWord.query.get(word_id)  # 获取需要更新的

    if word:
        word.risk_name = request.form['risk_name']
        word.risk_level = request.form['risk_level']
        word.reason = request.form['reason']
        db.session.commit()

    return jsonify({'data': word, 'code': 200, 'msg': 'ok'})


@app.route('/get_word/<int:word_id>')
def get_word(word_id):
    if word_id is None or word_id == '':
        return jsonify({'msg': '参数错误'}), 400

    word = TabRiskWord.query.get(word_id)  # 获取所有

    result = {'id': word.id, 'risk_name': word.risk_name, 'risk_level': word.risk_level, 'reason': word.reason}

    return jsonify({'data': result, 'code': 200, 'msg': 'ok'})


@app.route('/get_risk_words')
def get_risk_words():
    risk_list = TabRiskWord.query.all()  # 获取所有
    result = [{'id': word.id, 'risk_name': word.risk_name, 'risk_level': word.risk_level, 'reason': word.reason} for
              word in risk_list]
    return jsonify({'data': result, 'code': 200, 'msg': 'ok'})


@app.route('/video2audio', methods=['POST'])
def video2audio():
    # 获取当前脚本的目录路径
    script_dir = os.path.dirname(__file__)
    # 构造文件路径
    file_path = os.path.join(script_dir, 'video.mp4')
    # 保存上传的文件
    request.files['video'].save(file_path)
    text = video_to_text(file_path)
    print(text)
    return render_template('index.html', result=text)


@app.route('/video2audio2text', methods=['POST'])
def video2audio2text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # 获取当前脚本的目录路径
    script_dir = os.path.dirname(__file__)
    # 构造文件路径
    file_path = os.path.join(script_dir, 'video.mp4')

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 保存上传的文件
    file.save(file_path)
    # 视频转文本
    text = video_to_text(file_path)

    if text == '':
        return jsonify({'data': '参数出错', 'code': 400, 'msg': '参数出错'})

    ## 导出结果
    # 使用列表推导式获取所有 banned_word 的值
    result = check_banned_word_list_text(text, TabRiskWord.query.all())
    return jsonify({'data': result, 'code': 200, 'msg': 'ok'})


@app.route('/checkRiskWord', methods=['POST'])
def check_risk_word():
    text = request.form.get('checkText')

    if text == '':
        return jsonify({'data': '参数出错', 'code': 400, 'msg': '参数出错'})

    list = TabRiskWord.query.all()
    # 使用列表推导式获取所有 banned_word 的值
    result = check_banned_word_list_text(text, list)
    return jsonify({'data': result, 'code': 200, 'msg': 'ok'})


if __name__ == '__main__':
    app.run()
