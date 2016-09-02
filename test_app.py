from datetime import datetime
from app import build_dates

def test_dates(monkeypatch):
    monkeypatch.setattr(datetime.now(), 'expanduser', mockreturn)
    dates = build_dates()
    assert datetime.now() == FAKETIME

# today = datetime(2016, 6, 30)