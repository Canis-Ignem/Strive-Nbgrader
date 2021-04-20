import pandas as pd
import os
import argparse
from glob import glob
import pandas as pd
import sqlite3 as sql


parser = argparse.ArgumentParser(description="NBGRADER partner script")
parser.add_argument('--students', metavar = 's', type = str, required = False)
parser.add_argument('--assignment', metavar = 'a', type = str, required = False)
parser.add_argument('--collect', metavar = 'c', type = str, required = False)
parser.add_argument('--validate', metavar = 'v', type = str, required = False)
parser.add_argument('--grades', metavar = 'g', type = str, required = False)

args = vars(parser.parse_args())

user = os.listdir('/home/')[0]
SUBMISSIONS = '/home/'+ user + "/submitted/"
AUTOGRADED = '/home/'+ user + "/autograded/"



def add_submissions(pth):

    for notebook in os.listdir(pth):
        df = pd.read_excel("./student_codes.xlsx")
        name = df['Name'][ int( notebook[:2] ) ]
        #print("mv "+ pth +"/"+ notebook +" "+ SUBMISSIONS + name +"/"+ notebook[2:5])
        os.system("mv "+ pth +"/"+ notebook +" "+ SUBMISSIONS + "\""+ name + "\"" +"/"+ notebook[2:5])
        #print(SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook , SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook[2:])
        os.rename(SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook , SUBMISSIONS +  name  +"/"+ notebook[2:5] +"/"+notebook[2:] )

def preprocess_df(df):

    for i in range(df["Names"].shape[0]):
        df["Names"][i] = df["Names"][i].replace(" ","_")
    return df


def create_dirs(df):

    #df = preprocess_df(df)

    for name in df["Name"]:
        print(name)
        os.system("mkdir "+SUBMISSIONS+ "\""+ name + "\"")
        os.system("mkdir "+AUTOGRADED+ "\""+ name + "\"")

def validate_assignment(name):

    try:
        #os.system("cd ~")
        os.system("cd ~ \n nbgrader autograde "+ name)
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
        
       
        report = " The student:  {} \n Assigment:   {} \n Total marks: {}/{}".format(student,nb,grades['auto_score'].sum(),max_score['max_score'].sum())
        #print(report)
        return report
    except:
        #print("No submission for that student")
        return "No submission for this student"

def create_assignment(assig):

    for student in os.listdir(SUBMISSIONS):
            pth = SUBMISSIONS+ "\""+ student + "\"" + "/" + assig
            pth2 = AUTOGRADED+ "\""+ student + "\"" + "/" + assig
            os.system("mkdir "+pth)
            os.system("mkdir "+pth2)
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
    


'''***************************************************+
                                                      +
--s + pth to the xlsx with the names                   +                     
--a + name of the assignment to add                   +
--c + pth to where the students notebooks are stored  +
--v + name of the assignmment to grade                +
--g + name of the student and of the assignment       +
                                                      +
******************************************************
'''

if __name__ == '__main__':
    main()
