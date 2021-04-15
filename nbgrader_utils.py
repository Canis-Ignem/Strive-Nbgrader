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



def add_submissions(pth):

    for notebook in os.listdir(pth):
        name = df['Names'][ int( notebook[:2] ) ]
        os.system("mv "+ pth +"/"+ notebook +" "+ SUBMISSIONS + name +"/"+ notebook[2:5])
        os.rename(SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook , SUBMISSIONS + name +"/"+ notebook[2:5] +"/"+notebook[2:] )

def preprocess_df(df):

    for i in range(df["Names"].shape[0]):
        df["Names"][i] = df["Names"][i].replace(" ","_")
    return df


def create_dirs(df):

    df = preprocess_df(df)

    for name in df["Names"]:
        os.system("mkdir "+SUBMISSIONS+name)

def validate_assignment(name):

    try:
        #os.system("cd ~")
        os.system("cd ~ \n nbgrader autograde "+ name)
    except:
        print("Couldn't find said assignment")
        
        
def get_grades(student, nb):
    
    con = sql.connect("/home/jon/gradebook.db")
    q1 = "SELECT id FROM assignment where name ='{}'".format(nb)
    ass_id = pd.read_sql_query( q1 , con).values[0][0]
    q2 = "Select id from submitted_assignment where student_id = '{}' and assignment_id = '{}'".format(student,ass_id)
    nb_id = pd.read_sql_query( q2 , con).values[0][0]
    q3 = "Select id from submitted_notebook where assignment_id = '{}'".format(nb_id)
    nb_id = pd.read_sql_query( q3 , con).values[0][0]
    q4 = "Select auto_score from grade where notebook_id = '{}'".format(nb_id)
    grades = pd.read_sql_query( q4 , con)
    report = " The tudent:  {} \n Assigment:   {} \n Total marks: {}".format(student,nb,grades['auto_score'].sum())
    print(report)

def main():

    '''
    if args['collect'] == None and args['students'] == None and args['assignment'] == None and args['validate'] == None :
        print("No arguments \n Ending")
        return
    '''
    if args['students'] != None:

        df = pd.read_pickle(args['students'])
        create_dirs(df)
        print("Here is a full list of the student folders: \n")
        os.system("cd "+SUBMISSIONS +"\n ls")

    if args['assignment'] != None:

        assingment = args['assignment']

        for student in os.listdir(SUBMISSIONS):
            pth = os.path.join(SUBMISSIONS,student)
            pth = os.path.join(pth,assingment)
            os.system("mkdir "+pth)
    
    if args['collect'] != None:
        add_submissions(args['collect'])

    if args['validate'] != None:
        validate_assignment(args['validate'])
    
    if args['grades'] != None:
        s = args['grades'].split()
        get_grades(s[0],s[1])
    


'''***************************************************+
                                                      +
--s + pth to the pkl with the names                   +                     
--a + name of the assignment to add                   +
--c + pth to where the students notebooks are stored  +
--v + name of the assignmment to grade                +
--g + name of the student and of the assignment       +
                                                      +
******************************************************
'''

if __name__ == '__main__':
    main()