from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect
from models import History, Member
from app import db
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import json

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/history')
def history():
    history_list = History.query.order_by(History.id.desc()).all()
    total_data = calculate_total_data(history_list)
    total_distance = total_data[1]
    total_time = total_data[0]
    average_time = 0

    current_month = str(datetime.now().month)
    
    average_time = total_time / len(history_list)

    monthly_distances = get_monthly_distances(history_list)
    date_labels = get_days_of_current_month()
    
    return render_template('history.html', history_list=history_list, total_time=calculate_time(total_time),
     average_time=calculate_time(average_time), total_distance=total_distance, average_distance=total_distance, place=get_place(history_list),
     monthly_distances=monthly_distances, date_labels=date_labels, current_month=current_month)

@bp.route('/statistics')
def statistics():

    return render_template('statistics.html')

@bp.route('/submit', methods=['POST'])
def submit():
    print(datetime.strptime(request.form['rent_date'], '%Y-%m-%d').date())
    history = History(
        rent_date=datetime.strptime(request.form['rent_date'], '%Y-%m-%d').date().strftime('%Y-%m-%d'),
        rent_place=request.form['rent-place'],
        rent_time=datetime.strptime(request.form['rent-time'], '%H:%M').time().strftime('%H:%M:%S'),
        return_place=request.form['return-place'],
        return_time=datetime.strptime(request.form['return-time'], '%H:%M').time().strftime('%H:%M:%S'),
        distance=float(request.form['distance'])
    )
    db.session.add(history)
    db.session.commit()
    return redirect(url_for('main.history'))

@bp.route('/compare', methods=['POST'])
def compare():
    data = load_json_file('static/data.json')

    user_gender = request.form['gender']
    user_weight = float(request.form['weight'])
    user_age = request.form['age']

    # 비교 데이터 불러오기 (운동량, 탄소량, 이용거리, 이용시간)
    get_data = get_user_compare_data(data, user_gender, user_age)

    # 이용자 데이터(운동량, 탄소량) 계산
    history_list = History.query.order_by(History.id.desc()).all()
    total_data = calculate_total_data(history_list)
    exercise = total_data[1] * 0.001 * user_weight * 5.94 / 15 # km 단위로 계산
    carbon = total_data[1] * 0.001 * 0.232
    average_distance = total_data[1] / len(history_list)
    average_time = total_data[0] * 60 / len(history_list) # 분 단위로 변환 후 계산

    # 이용자 데이터 삽입
    get_data[0].insert(0, exercise)
    get_data[1].insert(0, carbon)
    get_data[2].insert(0, average_distance)
    get_data[3].insert(0, average_time)

    total_minutes = data['total']['이용시간']
    hours = total_minutes // 60
    minutes = total_minutes % 60
    data['total']['이용시간'] = f"{int(hours)} h {int(minutes)} m"
    print(get_data[0])
    return render_template('statistics.html', is_not_null=True, exercise=get_data[0], carbon=get_data[1], distance=get_data[2], time=get_data[3], tota_average_data=data['total'])


def calculate_time(time):
    hours = int(time)
    minutes = int((time - hours) * 60)
    time_str = f'{hours}시간 {minutes}분'

    return time_str

def get_place(list):

    place_counter = Counter()
    for history in list:
        place_counter[history.rent_place] += 1
        place_counter[history.return_place] += 1

    return place_counter.most_common(1)[0][0]

def get_monthly_distances(history_list):
    now = datetime.now()
    first_day_of_month = datetime(now.year, now.month, 1)
    if now.month == 12:
        last_day_of_month = datetime(now.year + 1, 1, 1)
    else:
        last_day_of_month = datetime(now.year, now.month + 1, 1)

    # Initialize the list with zeros
    monthly_distances = [0] * ((last_day_of_month - first_day_of_month).days)

    for history in history_list:
        rent_date = datetime.strptime(history.rent_date, '%Y-%m-%d')
        if first_day_of_month <= rent_date < last_day_of_month:
            # Subtract 1 from the day to use it as list index
            monthly_distances[rent_date.day - 1] += calculate_usage_time(history.rent_time, history.return_time)

    return monthly_distances

def get_days_of_current_month():
    now = datetime.now()
    first_day_of_month = datetime(now.year, now.month, 1)
    if now.month == 12:
        last_day_of_next_month = datetime(now.year + 1, 1, 1)
    else:
        last_day_of_next_month = datetime(now.year, now.month + 1, 1)

    date = first_day_of_month
    days_of_current_month = []
    while date < last_day_of_next_month:
        days_of_current_month.append(date.day)
        date += timedelta(days=1)

    return days_of_current_month

def calculate_usage_time(rent_time_str, return_time_str):

    rent_time = datetime.strptime(rent_time_str, '%H:%M:%S')
    return_time = datetime.strptime(return_time_str, '%H:%M:%S')
    usage_time = (return_time - rent_time).seconds / 3600  # 시간 단위로 변환

    return usage_time

def calculate_total_data(history_list):
    cal_total_time = 0
    total_distance = 0
    # 전체 이용시간 계산
    for history in history_list:
        usage_time = calculate_usage_time(history.rent_time, history.return_time)
        cal_total_time += usage_time
        total_distance += history.distance

    return cal_total_time, total_distance

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_user_compare_data(data, gender, age):
    selected_gender = data[gender]
    selected_age = data[age]
    total_data = data['total']

    user_selected_exercise = [total_data["운동량"], selected_age["운동량"], selected_gender["운동량"]]
    user_selected_carbon = [total_data["탄소량"], selected_age["탄소량"], selected_gender["탄소량"]]
    user_selected_distance = [total_data["이용거리"], selected_age["이용거리"], selected_gender["이용거리"]]
    user_selected_time = [total_data["이용시간"], selected_age["이용시간"], selected_gender["이용시간"]]

    return user_selected_exercise, user_selected_carbon, user_selected_distance, user_selected_time