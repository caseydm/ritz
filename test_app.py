from freezegun import freeze_time
from app import build_dates


@freeze_time('2016-07-01')
def test_dates():
    dates = build_dates()
    assert dates[0]['arrive'] == '07/01/2016'
    assert dates[0]['depart'] == '07/02/2016'
    assert dates[1]['arrive'] == '08/01/2016'
    assert dates[1]['depart'] == '08/02/2016'
