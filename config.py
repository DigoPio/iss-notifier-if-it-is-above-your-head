import requests
from datetime import datetime
import smtplib
from secret import Secret

secret = Secret()

MY_EMAIL = secret.my_email
MY_PASSWORD = secret.password
MY_LAT = -12.964150
MY_LONG = -38.505821

def is_iss_close():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data['iss_position']['longitude'])
    iss_latitude = float(data['iss_position']['latitude'])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    else:
        return False
# ------------------------------------------------------------------------------------------------ #

def is_dark():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0
    }
    response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_hour = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset_hour = int(data['results']['sunset'].split('T')[1].split(':')[0])
    time_now = datetime.now()
    hour_now = time_now.hour
    if hour_now >= sunset_hour or hour_now <= sunrise_hour:
        return True
    else:
        return False


def send_email():
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f'Subject:Attention!!\n\nLook up to the sky! ISS is passing by!!'
        )
