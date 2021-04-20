import smtplib
from nbgrader_utils import get_grades
import pandas as pd

sender_email = "jonperezetxebarria@gmail.com"

data = pd.read_excel("./student_codes.xlsx")

def send_emails(assig):

    for i in range(data.shape[0]):
        subject = "Grade "+assig
        
        receiver_email = data['EMAIL'][i]
        body = get_grades(data['Name'][i], assig)
        #print(receiver_email)
        #print(mess)

        pas= ""
        with open("./pass",'r') as f:
            pas = f.readline()

        message = f'Subject: {subject}\n\n{body}'


        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.login(sender_email, pas)
            s.sendmail(sender_email, receiver_email, message)         
            print( "Successfully sent email")
            s.quit()
        except Exception as vx:
            
            print(vx)
        
send_emails("ml1")