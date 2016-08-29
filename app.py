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

    ratesDict = []

    # get values from each cell
    for r in rows:
        cells = r.find_all('a')
        for c in cells:
            p = c.find('p')
            spans = p.find_all('span')
            resDate = spans[1].text + spans[2].text  # reservation date
            price = c.find_all('p')[1].text  # price
            price = price.strip(' \t\n\r')  # price stripped
            ratesDict.append({'date': resDate, 'price': price})

    return ratesDict


def buildDates():
    dates = []
    today = datetime.now()
    nextMonth = today + timedelta(days=30)

    # now
    dates.append({
        'arrive': today.strftime('%m/%d/%Y'),
        'depart': (today + timedelta(days=1)).strftime('%m/%d/%Y')
    })

    # next month
    dates.append({
        'arrive': nextMonth.strftime('%m/%d/%Y'),
        'depart': (nextMonth + timedelta(days=1)).strftime('%m/%d/%Y')
    })

    return dates


def getRates():
    dates = buildDates()
    rates = []

    # get rates for this month and next month
    for d in dates:
        soup = getSoup(d['arrive'], d['depart'])
        rates += parseRates(soup)
        time.sleep(2)

    return rates


# run program
rates = getRates()
for rate in rates:
    print(rate['date'], rate['price'])
