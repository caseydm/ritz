import os
import time
from datetime import datetime, timedelta
from robobrowser import RoboBrowser
import sendgrid
from sendgrid.helpers.mail import *


def get_soup(arrive, depart):
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


def parse_rates(soup, year):
    # year passed to append to reservation date
    year = datetime.strptime(year, '%m/%d/%Y')
    year = year.strftime('%Y')

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

            # convert date to reader friendly format
            res_date = spans[1].text + spans[2].text + '/' + year
            res_date = datetime.strptime(res_date, '%m/%d/%Y')
            res_date = res_date.strftime('%A, %b %d')

            # reservation cost
            price = c.find_all('p')[1].text
            price = price.strip(' \t\n\r')
            rates.append({'date': res_date, 'price': price})

    return rates


def build_dates():
    dates = []
    today = datetime.now()
    next_month = today + timedelta(days=30)

    # now
    dates.append({
        'arrive': today.strftime('%m/%d/%Y'),
        'depart': (today + timedelta(days=1)).strftime('%m/%d/%Y')
    })

    # next month
    dates.append({
        'arrive': next_month.strftime('%m/%d/%Y'),
        'depart': (next_month + timedelta(days=1)).strftime('%m/%d/%Y')
    })

    return dates


def get_rates():
    dates = build_dates()
    rates = []

    # get rates for this month and next month
    for d in dates:
        soup = get_soup(d['arrive'], d['depart'])
        rates += parse_rates(soup, d['arrive'])
        time.sleep(2)

    # sort rates by date
    rates.sort(key=lambda x: datetime.strptime(x['date'], '%A, %b %d'))

    return rates


def email_results(rates):
    # sendgrid setup
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

    # message
    message = 'Available dates for Ritz Lake Oconee:<br><br>'
    for rate in rates:
        message += rate['date'] + ': ' + rate['price'] + '<br>'

    from_email = Email('casey@caseym.me')
    subject = 'Ritz Hotel Rates'
    to_email = Email('caseym@gmail.com')
    content = Content('text/html', message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)


# run program
rates = get_rates()
for rate in rates:
    print(rate['date'], rate['price'])
email_results(rates)
