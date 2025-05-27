import os
from datetime import date, timedelta
from src import sport_plan

TEST_DB = "test.db"


def setup_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
    sport_plan.engine = sport_plan.create_engine(os.environ["DATABASE_URL"], echo=False)
    sport_plan.init_db()


def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_profile_and_session():
    profile = sport_plan.UserProfile(name="Alice", age=30, weight=60.0, height=170.0, sports="['course']")
    sport_plan.add_profile(profile)

    sessions = sport_plan.list_sessions()
    assert sessions == []

    sess_date = date.today()
    session = sport_plan.SessionModel(date=sess_date, activity_type="course", duration=30, rpe=5)
    sport_plan.add_session(session)

    sessions = sport_plan.list_sessions()
    assert len(sessions) == 1
    assert sessions[0].activity_type == "course"


def test_acwr_computation():
    today = date.today()
    for i in range(28):
        d = today - timedelta(days=i)
        sport_plan.add_session(sport_plan.SessionModel(date=d, activity_type="course", duration=20, rpe=5))

    sessions = sport_plan.list_sessions()
    acute = sport_plan.compute_acute_load(sessions, today)
    chronic = sport_plan.compute_chronic_load(sessions, today)
    acwr = sport_plan.compute_acwr(sessions, today)

    assert acute > 0
    assert chronic > 0
    assert abs(acwr - (acute / chronic)) < 1e-5
