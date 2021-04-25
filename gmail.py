import smtplib
from nbgrader_utils import get_grades
import pandas as pd
import numpy as np
sender_email = "jonperezetxebarria@gmail.com"




def send_emails(assig):
    
    data = pd.read_excel("./student_codes.xlsx")
    data = data.dropna(axis='rows')

    for i in range(data.shape[0]):
        
            subject = "Grade "+assig
            print(data.values[i][0])
            
            body = get_grades(data.values[i][0], assig)
            receiver_email = data.values[i][3]
            #print(receiver_email)
            #print(mess)

            pas= ""
            with open("./pass",'r') as f:
                pas = f.readline()

            message = f'Subject: {subject}\n\n{body}'
            #print(message)
            
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.login(sender_email, pas)
                s.sendmail(sender_email, receiver_email, message)         
                print( "Successfully sent email to: ", receiver_email)
                s.quit()
            except Exception as vx:
                
                print(vx)
            
send_emails("ml3")