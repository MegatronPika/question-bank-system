#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import random
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 在生产环境中应该使用更安全的密钥

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

def get_user_id():
    """获取当前用户ID"""
    return session.get('user_id', 'default_user')

def get_user_data():
    """获取当前用户数据"""
    user_data = load_user_data()
    user_id = get_user_id()
    
    if user_id not in user_data['users']:
        user_data['users'][user_id] = {
            'answered_questions': set(),
            'wrong_questions': set(),
            'wrong_count': {}
        }
    else:
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
    return render_template('index.html')

@app.route('/random_practice')
def random_practice():
    """随机做题页面"""
    return render_template('random_practice.html')

@app.route('/get_random_question', methods=['POST'])
def get_random_question():
    """获取随机题目"""
    data = request.get_json()
    mode = data.get('mode', 'all')  # all, unanswered, wrong
    
    questions = load_questions()
    user_data, user_id = get_user_data()
    
    if mode == 'unanswered':
        # 从未做过的题目中选择
        answered = user_data['users'][user_id]['answered_questions']
        available_questions = [q for q in questions if q['id'] not in answered]
        if not available_questions:
            return jsonify({'error': '已刷完所有题库，请选择全量题库或者错题库进行练习'})
    elif mode == 'wrong':
        # 从错题库中选择
        wrong_questions = user_data['users'][user_id]['wrong_questions']
        available_questions = [q for q in questions if q['id'] in wrong_questions]
        if not available_questions:
            return jsonify({'error': '暂无错题记录'})
    else:
        # 全量题库
        available_questions = questions
    
    # 随机选择一道题
    question = random.choice(available_questions)
    
    return jsonify({
        'id': question['id'],
        'content': question['content'],
        'options': question['options'],
        'type': question['type'],
        'score': question['score']
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    
    questions = load_questions()
    question = next((q for q in questions if q['id'] == question_id), None)
    
    if not question:
        return jsonify({'error': '题目不存在'})
    
    user_data, user_id = get_user_data()
    
    # 记录已答题目
    user_data['users'][user_id]['answered_questions'].add(question_id)
    
    # 判断答案是否正确
    is_correct = user_answer == question['correct_answer']
    
    if not is_correct:
        # 记录错题
        user_data['users'][user_id]['wrong_questions'].add(question_id)
        
        # 记录错题详情
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
        
        # 累计错题次数
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
def exam():
    """考试页面"""
    return render_template('exam.html')

@app.route('/start_exam', methods=['POST'])
def start_exam():
    """开始考试"""
    questions = load_questions()
    
    # 按题型筛选题目
    single_choice = [q for q in questions if q['type'] == 1]
    multi_choice = [q for q in questions if q['type'] == 2]
    true_false = [q for q in questions if q['type'] == 3]
    
    # 随机选择题目
    exam_questions = (
        random.sample(single_choice, 50) +
        random.sample(multi_choice, 50) +
        random.sample(true_false, 50)
    )
    
    # 打乱题目顺序
    random.shuffle(exam_questions)
    
    # 生成考试ID
    exam_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存考试信息
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
def submit_exam():
    """提交考试"""
    data = request.get_json()
    exam_id = data.get('exam_id')
    answers = data.get('answers', {})
    
    user_data, user_id = get_user_data()
    
    # 找到考试记录
    exam_record = None
    for record in user_data['exam_records'][user_id]:
        if record['exam_id'] == exam_id:
            exam_record = record
            break
    
    if not exam_record:
        return jsonify({'error': '考试记录不存在'})
    
    # 计算分数和错题
    total_score = 0
    wrong_answers = []
    
    for question in exam_record['questions']:
        question_id = question['id']
        user_answer = answers.get(str(question_id), '')
        correct_answer = question['correct_answer']
        
        # 判断答案
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
            
            # 记录到错题库
            user_data['users'][user_id]['wrong_questions'].add(question_id)
            user_data['users'][user_id]['answered_questions'].add(question_id)
            
            # 累计错题次数
            if question_id not in user_data['users'][user_id]['wrong_count']:
                user_data['users'][user_id]['wrong_count'][question_id] = 0
            user_data['users'][user_id]['wrong_count'][question_id] += 1
    
    # 更新考试记录
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
def wrong_questions():
    """错题记录页面"""
    return render_template('wrong_questions.html')

@app.route('/get_wrong_questions', methods=['POST'])
def get_wrong_questions():
    """获取错题记录"""
    data = request.get_json()
    sort_by = data.get('sort_by', 'timestamp')  # timestamp, count, id
    
    user_data, user_id = get_user_data()
    wrong_records = user_data['wrong_questions'][user_id]
    
    # 按题型分组
    questions_by_type = {
        1: [],  # 单选题
        2: [],  # 多选题
        3: []   # 判断题
    }
    
    for record in wrong_records:
        questions_by_type[record['type']].append(record)
    
    # 排序
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 