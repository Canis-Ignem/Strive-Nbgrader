import pandas as pd
import os
import argparse
from glob import glob
import pandas as pd
import sqlite3 as sql



BATCHES = ["Mar21","May21"]



#/home/jon/Documents/Strive/nbgrader_submissions/ml4
parser = argparse.ArgumentParser(description="NBGRADER partner script")
parser.add_argument('--students', metavar = 's', type = str, required = False)
parser.add_argument('--assignment', metavar = 'a', type = str, required = False)
parser.add_argument('--collect', metavar = 'c', type = str, required = False)
parser.add_argument('--validate', metavar = 'v', type = str, required = False)
parser.add_argument('--grades', metavar = 'g', type = str, required = False)
parser.add_argument('--deliver', metavar = 'd', type = str, required = False)

args = vars(parser.parse_args())

SUBMISSIONS = ""
AUTOGRADED = ""

batch = input("Please select a batch: {} ".format(BATCHES) )
print(batch)
for b in BATCHES:
    if b == batch:
        user = os.listdir('/home/')[0]
        SUBMISSIONS = '/home/'+ user +"/"+ b + "/submitted/"
        AUTOGRADED = '/home/'+ user + "/"+ b + "/autograded/"
        print(SUBMISSIONS)

user = os.listdir('/home/')[0]
#SUBMISSIONS = "~/submitted/"

def add_submissions(pth):
    df = pd.read_excel("./student_codes.xlsx")
    abs_path = "/home/jon/Documents/Strive/nbgrader_submissions/"+ pth
    for notebook in os.listdir("/home/jon/Documents/Strive/nbgrader_submissions/"+ pth):
        if notebook.lower() == "readme.md":
            continue
        else:
            name = df['Name'][ int( notebook[:2] ) ]
            print(name,notebook)
            os.system("cp "+ "/home/jon/Documents/Strive/nbgrader_submissions/"+ pth +"/"+ notebook +" "+ SUBMISSIONS + "\""+ str(name) + "\"" +"/"+ notebook[2:5])
            #print(SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook , SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook[2:])
            os.rename(SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook , SUBMISSIONS +  str(name)  +"/"+ notebook[2:5] +"/"+notebook[2:] )

def preprocess_df(df):

    for i in range(df["Names"].shape[0]):
        df["Names"][i] = df["Names"][i].replace(" ","_")
    return df

def deliver_extra_files(pth,ex):
    
    df = pd.read_excel("./student_codes.xlsx")
    for i in range(df['Name'].shape[0]):

        print("cp -r "+ "\"" + pth + "\"" + " "+ SUBMISSIONS + "\""+ str(df['Name'][i])+ "\"" +"/"+ ex)
        os.system("cp -r " + "\"" + pth + "\"" + " "+ SUBMISSIONS + "\""+ str(df['Name'][i]) + "\"" +"/"+ ex)

def create_dirs(df):

    #df = preprocess_df(df)

    for email in df["Email"]:
        print(email)
        #print("mkdir "+SUBMISSIONS+ "\""+ email + "\"")
        os.system("mkdir "+SUBMISSIONS+ "\""+ email + "\"")
        os.system("mkdir "+AUTOGRADED+ "\""+ email + "\"")

def validate_assignment(name):

    try:
        #os.system("cd ~")
        os.system("cd ~ \n nbgrader autograde --force "+ name)
    except:
        print("Couldn't find said assignment")
        
        
def get_grades(student, nb):
    
    try:
        con = sql.connect("/home/jon/gradebook.db")
        
        q1 = "SELECT id FROM assignment where name ='{}'".format(nb)
        ass_id = pd.read_sql_query( q1 , con).values[0][0]
        q2 = "Select id from submitted_assignment where student_id = '{}' and assignment_id = '{}'".format(student,ass_id)
        nb_id = pd.read_sql_query( q2 , con).values[0][0]

        q3 = "Select id from submitted_notebook where assignment_id = '{}'".format(nb_id)
        nb_id = pd.read_sql_query( q3 , con).values[0][0]

        q4 = "Select auto_score,cell_id from grade where notebook_id = '{}'".format(nb_id)
        grades = pd.read_sql_query( q4 , con)

        cell_list = grades['cell_id'].values.tolist()
        as_str = ','.join("\'"+str(cell_list[i])+ "\'"  for i in range(len(cell_list)))
        q5 = "Select max_score from grade_cells where id IN ({})".format( as_str )
        max_score = pd.read_sql_query( q5 , con)
        #print(max_score['max_score'].sum())
       
        report = " The student:  {} \n Assigment:   {} \n Total marks: {}/{}".format(student,nb,grades['auto_score'].sum(),max_score['max_score'].sum())
        #print(report)
        return report
    except:
        #print("No submission for that student")
        return "No submission for this student"

def create_assignment(assig):

    for student in os.listdir(SUBMISSIONS):
            pth = SUBMISSIONS+ "\""+ student + "\"" + "/" + assig
            os.system("mkdir "+pth)
            #print("mkdir "+pth)

def main():

    '''
    if args['collect'] == None and args['students'] == None and args['assignment'] == None and args['validate'] == None :
        print("No arguments \n Ending")
        return
    '''

    if args['students'] != None:

        df = pd.read_excel(args['students'])
        create_dirs(df)

    if args['assignment'] != None:

        assingment = args['assignment']
        create_assignment(assingment)
        
    
    if args['collect'] != None:
        add_submissions(args['collect'])

    if args['validate'] != None:
        validate_assignment(args['validate'])
    
    if args['grades'] != None:
        s = args['grades'].split(",")
        res = get_grades(s[0],s[1])
        print(res)
    if args['deliver'] != None:
        s = args['deliver'].split(",")
        deliver_extra_files(s[0],s[1])
        


'''***************************************************+
                                                      +
--s + pth to the xlsx with the names                  +                     
--a + name of the assignment to add                   +
--c + pth to where the students notebooks are stored  +
--v + name of the assignmment to grade                +
--g + name of the student and of the assignment       +
--d + path  to file and exercise separated by ','     +
                                                      +
******************************************************
'''

if __name__ == '__main__':
    main()
