import sys
import os
import json
from datetime import date, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src import sport_plan

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')


def setup_module(module):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def teardown_module(module):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def test_add_profile_and_session():
    profile = sport_plan.UserProfile('Alice', 30, 60.0, 170.0, ['course'])
    sport_plan.add_profile(profile)

    assert os.path.exists(DATA_FILE)
    data = sport_plan.load_data()
    assert len(data['profiles']) == 1
    assert data['profiles'][0]['name'] == 'Alice'

    sess_date = date.today().isoformat()
    session = sport_plan.Session(sess_date, 'course', 30, 5)
    sport_plan.add_session(session)

    data = sport_plan.load_data()
    assert len(data['sessions']) == 1
    assert data['sessions'][0]['activity_type'] == 'course'


def test_acwr_computation():
    today = date.today()
    # create sessions with srpe = 100 each day for 28 days
    for i in range(28):
        d = (today - timedelta(days=i)).isoformat()
        sport_plan.add_session(sport_plan.Session(d, 'course', 20, 5))

    sessions = sport_plan.list_sessions()
    acute = sport_plan.compute_acute_load(sessions, today)
    chronic = sport_plan.compute_chronic_load(sessions, today)
    acwr = sport_plan.compute_acwr(sessions, today)

    assert acute > 0
    assert chronic > 0
    assert abs(acwr - (acute / chronic)) < 1e-5
