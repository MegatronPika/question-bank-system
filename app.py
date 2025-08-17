#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import random
import datetime
import os
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# 数据文件路径
QUESTIONS_FILE = 'full_questions.json'
USER_DATA_FILE = 'user_data.json'

def load_questions():
    """加载题目数据"""
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def load_user_data():
    """加载用户数据"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'users': {},
        'user_profiles': {},
        'wrong_questions': {},
        'exam_records': {}
    }

def save_user_data(data):
    """保存用户数据"""
    # 转换set为list以便JSON序列化
    for user_id in data['users']:
        if 'answered_questions' in data['users'][user_id]:
            data['users'][user_id]['answered_questions'] = list(data['users'][user_id]['answered_questions'])
        if 'wrong_questions' in data['users'][user_id]:
            data['users'][user_id]['wrong_questions'] = list(data['users'][user_id]['wrong_questions'])
    
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def get_client_ip():
    """获取客户端IP"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def get_user_agent():
    """获取用户代理"""
    return request.headers.get('User-Agent', '')

def create_session_id():
    """创建会话ID"""
    ip = get_client_ip()
    user_agent = get_user_agent()
    return hashlib.md5(f"{ip}:{user_agent}".encode()).hexdigest()

def is_logged_in():
    """检查用户是否已登录"""
    return 'user_id' in session

def require_login(f):
    """登录验证装饰器"""
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_user_data():
    """获取当前用户数据"""
    user_data = load_user_data()
    user_id = session.get('user_id')
    
    if not user_id or user_id not in user_data['users']:
        return None, None
    
    # 将list转换回set
    if 'answered_questions' in user_data['users'][user_id]:
        user_data['users'][user_id]['answered_questions'] = set(user_data['users'][user_id]['answered_questions'])
    if 'wrong_questions' in user_data['users'][user_id]:
        user_data['users'][user_id]['wrong_questions'] = set(user_data['users'][user_id]['wrong_questions'])
    
    if user_id not in user_data['wrong_questions']:
        user_data['wrong_questions'][user_id] = []
    
    if user_id not in user_data['exam_records']:
        user_data['exam_records'][user_id] = []
    
    return user_data, user_id

@app.route('/')
def index():
    """主页"""
    if is_logged_in():
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user_data = load_user_data()
        
        # 检查用户名是否存在
        if username not in user_data['user_profiles']:
            return jsonify({'success': False, 'message': '用户名不存在'})
        
        # 验证密码
        if not check_password_hash(user_data['user_profiles'][username]['password'], password):
            return jsonify({'success': False, 'message': '密码错误'})
        
        # 登录成功
        session['user_id'] = username
        session['session_id'] = create_session_id()
        session['login_time'] = datetime.datetime.now().isoformat()
        
        # 更新用户登录信息
        user_data['user_profiles'][username]['last_login'] = datetime.datetime.now().isoformat()
        user_data['user_profiles'][username]['last_ip'] = get_client_ip()
        user_data['user_profiles'][username]['last_user_agent'] = get_user_agent()
        
        save_user_data(user_data)
        
        return jsonify({'success': True, 'message': '登录成功'})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        # 验证输入
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'})
        
        if len(username) < 3:
            return jsonify({'success': False, 'message': '用户名至少3个字符'})
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': '密码至少6个字符'})
        
        if password != confirm_password:
            return jsonify({'success': False, 'message': '两次输入的密码不一致'})
        
        user_data = load_user_data()
        
        # 检查用户名是否已存在
        if username in user_data['user_profiles']:
            return jsonify({'success': False, 'message': '用户名已存在'})
        
        # 创建新用户
        user_data['user_profiles'][username] = {
            'password': generate_password_hash(password),
            'created_time': datetime.datetime.now().isoformat(),
            'last_login': None,
            'last_ip': None,
            'last_user_agent': None
        }
        
        # 初始化用户数据
        user_data['users'][username] = {
            'answered_questions': set(),
            'wrong_questions': set(),
            'wrong_count': {}
        }
        
        user_data['wrong_questions'][username] = []
        user_data['exam_records'][username] = []
        
        save_user_data(user_data)
        
        return jsonify({'success': True, 'message': '注册成功，请登录'})
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/random_practice')
@require_login
def random_practice():
    """随机做题页面"""
    return render_template('random_practice.html')

@app.route('/get_random_question', methods=['POST'])
@require_login
def get_random_question():
    """获取随机题目"""
    data = request.get_json()
    mode = data.get('mode', 'all')
    
    questions = load_questions()
    user_data, user_id = get_user_data()
    
    if not user_data or not user_id:
        return jsonify({'error': '用户数据不存在'})
    
    if mode == 'unanswered':
        answered = user_data['users'][user_id]['answered_questions']
        available_questions = [q for q in questions if q['id'] not in answered]
        if not available_questions:
            return jsonify({'error': '已刷完所有题库，请选择全量题库或者错题库进行练习'})
    elif mode == 'wrong':
        wrong_questions = user_data['users'][user_id]['wrong_questions']
        available_questions = [q for q in questions if q['id'] in wrong_questions]
        if not available_questions:
            return jsonify({'error': '暂无错题记录'})
    else:
        available_questions = questions
    
    question = random.choice(available_questions)
    
    return jsonify({
        'id': question['id'],
        'content': question['content'],
        'options': question['options'],
        'type': question['type'],
        'score': question['score']
    })

@app.route('/submit_answer', methods=['POST'])
@require_login
def submit_answer():
    """提交答案"""
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer')  # 可能是字符串或列表
    
    questions = load_questions()
    question = next((q for q in questions if q['id'] == question_id), None)
    
    if not question:
        return jsonify({'error': '题目不存在'})
    
    user_data, user_id = get_user_data()
    
    if not user_data or not user_id:
        return jsonify({'error': '用户数据不存在'})
    
    user_data['users'][user_id]['answered_questions'].add(question_id)
    
    # 处理多选题答案
    if question['type'] == 2:  # 多选题
        # 确保user_answer是列表格式
        if isinstance(user_answer, str):
            user_answer = [user_answer] if user_answer else []
        elif user_answer is None:
            user_answer = []
        
        # 多选题答案比较
        correct_answers = set(question['correct_answer'].split(','))
        user_answers = set(user_answer)
        is_correct = correct_answers == user_answers
    else:
        # 单选题和判断题
        is_correct = user_answer == question['correct_answer']
    
    if not is_correct:
        user_data['users'][user_id]['wrong_questions'].add(question_id)
        
        wrong_record = {
            'question_id': question_id,
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'timestamp': datetime.datetime.now().isoformat(),
            'question_content': question['content'],
            'analysis': question['analysis'],
            'type': question['type']
        }
        user_data['wrong_questions'][user_id].append(wrong_record)
        
        if question_id not in user_data['users'][user_id]['wrong_count']:
            user_data['users'][user_id]['wrong_count'][question_id] = 0
        user_data['users'][user_id]['wrong_count'][question_id] += 1
    
    save_user_data(user_data)
    
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': question['correct_answer'],
        'analysis': question['analysis']
    })

@app.route('/exam')
@require_login
def exam():
    """考试页面"""
    return render_template('exam.html')

@app.route('/start_exam', methods=['POST'])
@require_login
def start_exam():
    """开始考试"""
    questions = load_questions()
    
    single_choice = [q for q in questions if q['type'] == 1]
    multi_choice = [q for q in questions if q['type'] == 2]
    true_false = [q for q in questions if q['type'] == 3]
    
    exam_questions = (
        random.sample(single_choice, 50) +
        random.sample(multi_choice, 50) +
        random.sample(true_false, 50)
    )
    
    random.shuffle(exam_questions)
    
    exam_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    user_data, user_id = get_user_data()
    exam_info = {
        'exam_id': exam_id,
        'start_time': datetime.datetime.now().isoformat(),
        'questions': exam_questions,
        'status': 'ongoing'
    }
    user_data['exam_records'][user_id].append(exam_info)
    save_user_data(user_data)
    
    return jsonify({
        'exam_id': exam_id,
        'questions': exam_questions
    })

@app.route('/submit_exam', methods=['POST'])
@require_login
def submit_exam():
    """提交考试"""
    data = request.get_json()
    exam_id = data.get('exam_id')
    answers = data.get('answers', {})
    
    user_data, user_id = get_user_data()
    
    exam_record = None
    for record in user_data['exam_records'][user_id]:
        if record['exam_id'] == exam_id:
            exam_record = record
            break
    
    if not exam_record:
        return jsonify({'error': '考试记录不存在'})
    
    total_score = 0
    wrong_answers = []
    
    for question in exam_record['questions']:
        question_id = question['id']
        user_answer = answers.get(str(question_id), '')
        correct_answer = question['correct_answer']
        
        # 处理多选题答案
        if question['type'] == 2:  # 多选题
            if isinstance(user_answer, str):
                user_answer = [user_answer] if user_answer else []
            elif user_answer is None:
                user_answer = []
            
            correct_answers = set(correct_answer.split(','))
            user_answers = set(user_answer)
            is_correct = correct_answers == user_answers
        else:
            is_correct = user_answer == correct_answer
        
        if is_correct:
            total_score += question['score']
        else:
            wrong_answers.append({
                'question_id': question_id,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'question_content': question['content'],
                'analysis': question['analysis'],
                'type': question['type'],
                'score': question['score']
            })
            
            user_data['users'][user_id]['wrong_questions'].add(question_id)
            user_data['users'][user_id]['answered_questions'].add(question_id)
            
            if question_id not in user_data['users'][user_id]['wrong_count']:
                user_data['users'][user_id]['wrong_count'][question_id] = 0
            user_data['users'][user_id]['wrong_count'][question_id] += 1
    
    exam_record['end_time'] = datetime.datetime.now().isoformat()
    exam_record['status'] = 'completed'
    exam_record['total_score'] = total_score
    exam_record['wrong_answers'] = wrong_answers
    
    save_user_data(user_data)
    
    return jsonify({
        'total_score': total_score,
        'wrong_answers': wrong_answers
    })

@app.route('/wrong_questions')
@require_login
def wrong_questions():
    """错题记录页面"""
    return render_template('wrong_questions.html')

@app.route('/get_wrong_questions', methods=['POST'])
@require_login
def get_wrong_questions():
    """获取错题记录"""
    data = request.get_json()
    sort_by = data.get('sort_by', 'timestamp')
    
    user_data, user_id = get_user_data()
    wrong_records = user_data['wrong_questions'][user_id]
    
    questions_by_type = {
        1: [],
        2: [],
        3: []
    }
    
    for record in wrong_records:
        questions_by_type[record['type']].append(record)
    
    for q_type in questions_by_type:
        if sort_by == 'timestamp':
            questions_by_type[q_type].sort(key=lambda x: x['timestamp'], reverse=True)
        elif sort_by == 'count':
            questions_by_type[q_type].sort(
                key=lambda x: user_data['users'][user_id]['wrong_count'].get(x['question_id'], 0),
                reverse=True
            )
        elif sort_by == 'id':
            questions_by_type[q_type].sort(key=lambda x: x['question_id'])
    
    return jsonify({
        'single_choice': questions_by_type[1],
        'multi_choice': questions_by_type[2],
        'true_false': questions_by_type[3]
    })

@app.route('/profile')
@require_login
def profile():
    """用户资料页面"""
    user_data, user_id = get_user_data()
    if user_data and user_id:
        profile_info = user_data['user_profiles'][user_id]
        return render_template('profile.html', profile=profile_info, user_id=user_id)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 