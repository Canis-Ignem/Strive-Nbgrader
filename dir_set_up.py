import pandas as pd
import os
import argparse
from glob import glob


parser = argparse.ArgumentParser(description="NBGRADER partner script")
parser.add_argument('--students', metavar = 's', type = str, required = False)
parser.add_argument('--assignment', metavar = 'a', type = str, required = False)
parser.add_argument('--collect', metavar = 'c', type = str, required = False)
parser.add_argument('--validate', metavar = 'v', type = str, required = False)

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


def main():

    if args['collect'] == None and args['students'] == None and args['assignment'] == None and args['validate'] == None :
        print("No arguments \n Ending")
        return

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
    


'''***************************************************+
                                                      +
--s + pth to the pkl with the names                   +                     
--a + name of the assignment to add                   +
--c + pth to where the students notebooks are stored  +
--v + name of the assignmment to grade                +
                                                      +
******************************************************
'''

if __name__ == '__main__':
    main()
