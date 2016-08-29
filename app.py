from robobrowser import RoboBrowser
import time
from datetime import datetime, timedelta


def getSoup(arrive, depart):
    browser = RoboBrowser(parser='html.parser')
    browser.open('http://www.marriott.com/reservation/availabilitySearch.mi?propertyCode=AHNRZ')

    form = browser.get_form(action='/reservation/availabilitySearch.mi?isSearch=false')

    form['fromDate'].value = arrive
    form['toDate'].value = depart
    form['flexibleDateSearch'] = 'true'
    form['clusterCode'] = 'GOV'

    # submit form
    browser.submit_form(form)
    return browser


def parseRates(soup):
    # get calendar rows
    table = soup.find('table')
    body = table.find('tbody')
    rows = body.find_all('tr')

    rates = []

    # get values from each cell
    for r in rows:
        cells = r.find_all('a')
        for c in cells:
            p = c.find('p')
            spans = p.find_all('span')
            resDate = spans[1].text + spans[2].text  # reservation date
            price = c.find_all('p')[1].text
            price = price.strip(' \t\n\r')
            rates.append({'date': resDate, 'price': price})

    return rates


def buildDates():
    dates = []
    today = datetime.now()
    nextMonth = today + timedelta(days=30)
    dates.append({
            'arrive': today.strftime('%m/%d/%Y'),
            'depart': (today + timedelta(days=1)).strftime('%m/%d/%Y')
        })
    dates.append({
            'arrive': nextMonth.strftime('%m/%d/%Y'),
            'depart': (nextMonth + timedelta(days=1)).strftime('%m/%d/%Y')
        })
    return dates

dates = buildDates()
rates = []

# get rates for this month and next month
for d in dates:
    soup = getSoup(d['arrive'], d['depart'])
    rates += parseRates(soup)
    time.sleep(2)

print(rates)
