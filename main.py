import requests
import smtplib
from twilio.rest import Client
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


account_ssid =""
auth_code = ""
twilo_number =""



MAIL_ID = ""
PASSWORD_ID = ""




meter = {
    "apikey":"YY5hEbWO1YOQH1eivOIHFFTwm4u1yzV0"
}

RAIN_MESS = "Its going to rain today !"
NORMAL_MESS = "Sky is clear vvvvvvvvv"

html_Rain = '''
    <html>
        <body>
            <h1>Daily Weather report</h1>
            <p>Its Going To RAIN
            </p>
            <img src='cid:myimageid' width="700">
        </body>
    </html>
    '''

html_Normal = '''
    <html>
        <body>
            <h1>Daily Weather report</h1>
            <p>Sky Is Clear
            </p>
            <img src='cid:myimageid' width="700">
        </body>
    </html>
    '''


def attach_file_to_email(email_message, filename, extra_headers=None):
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)
    email_message.attach(file_attachment)


def f_t(far:bool)->bool:
    return (far - 32) * 5/9

def send_mail(message:str,temp:float):
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    
    if message=="RAIN":
        part2 = MIMEText(html_Rain, 'html')
    else:
        part2 = MIMEText(html_Normal,"html")
	        
    msg.attach(part2)
    attach_file_to_email(msg, 'chart.png', {'Content-ID': '<myimageid>'})
    connection.login(user=MAIL_ID,password=PASSWORD_ID)
    connection.sendmail(from_addr=MAIL_ID,to_addrs=MAIL_ID,msg=msg.as_string())
    connection.close()

def send_sms(message:str,temp:float):
    client = Client(account_ssid,auth_code)
    client.messages.create(
    to="+919043496112",
    from_=twilo_number,
    body=f"{message}\n Temp: {temp}")



response = requests.get(url="http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/2805916",params=meter)
data = response.json()
has_prec = [data[i]["HasPrecipitation"] for i in range(12)]
temp=[f_t(data[i]["Temperature"]["Value"]) for i in range(12)]
avg_temp = sum(temp)/len(temp)


plt.plot(temp)
plt.xlabel("TIME")
plt.ylabel("TEMP IN C")
plt.savefig('chart.png')

msg = MIMEMultipart('alternative')
msg['Subject'] = "Weather Report "
msg['From'] = MAIL_ID
msg['To'] = MAIL_ID



for i in range(12):
    if has_prec[i]==True:
        send_mail(message="RAIN",temp=avg_temp)
        send_sms(RAIN_MESS,avg_temp)
        break
    elif i==12 :
        send_mail(message="NORMAL",temp=avg_temp)
        send_sms(NORMAL_MESS,avg_temp)
        

