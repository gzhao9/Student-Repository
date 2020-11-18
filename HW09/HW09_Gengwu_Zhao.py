from datetime import datetime, timedelta, date
from typing import Tuple, Iterator,List
from prettytable import PrettyTable
from collections import defaultdict
import os,sys
def file_reader(path:str, fields: int, sep: str =',', header: bool=False) -> Iterator[List[str]]:
    try:
        a=open(path)
    except FileNotFoundError as e:
        print(e)
        sys.exit()
    lines=1
    while True:
        f=a.readline()
        if f != '':
            #Delete the last line break
            if f[-1]=='\n':
                f=f[:-1]
            result=f.split(sep)
            #if the length is not same, raise a ValueError
            if len(result)!=fields:
                raise ValueError(f"'{path}'has {len(result)} fields on line {lines} but expected {fields}")
            lines+=1
            #if header is true, pass the first line and change the header to false.
            if header:
                header=False
                continue
            for i,j in enumerate(result):
                result[i]=j.strip(' ')
            yield result
        else:
            break  
class Student:
    def __init__(self,cwid:str,name:str,major:str):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course = defaultdict(str)
    def __str__(self):
        pri=''
        for i,j in self.course.items():
            pri+=i+':'+j+'\n'
        return f"CWID:{self.cwid} name: {self.name}\nGrade of the cousre:\n{pri} "

class Instructors:
    def __init__(self,cwid:str,name:str,department:str):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.course=defaultdict(int)
    def __str__(self):
        pri=''
        for i,j in self.course.items():
            pri+=i+':'+j+'\n'
        return f"CWID:{self.cwid} name: {self.name}\n Students number of the cousre:\n {pri} "

class Repository:
    def __init__(self,path):
        os.chdir(path)
        self.path=path
        self.students=dict()
        self.instructors=dict()
        self.get_info()
    #get the info form the path
    def get_info(self):
        #get teh students info
        for line in file_reader(self.path+'students.txt',3,'\t'):
            if line[0] in self.students.keys():
                raise ValueError(f'The info of this students {line[0]} has been added')
            self.students[line[0]]=Student(line[0],line[1],line[2])
        #get the instructors info
        for line in file_reader(self.path+'instructors.txt',3,'\t'):
            if line[0] in self.instructors.keys():
                raise ValueError(f'The info of this instructors {line[0]} has been added')
            self.instructors[line[0]]=Instructors(line[0],line[1],line[2])
        #get the grade info
        for line in file_reader(self.path+'grades.txt',4,'\t'):
            if self.students[line[0]].course[line[1]] is not None:
                self.students[line[0]].course[line[1]]=line[2]
                self.instructors[line[3]].course[line[1]]+=1
            else:
                raise ValueError(f'The grade of this student {line[0]} has been added')
    
    def print_students_table(self):
        row:PrettyTable=PrettyTable()
        row.field_names=['cwid','name','major','course']
        for i,l in self.students.items():
            row.add_row([i,l.name,l.major,','.join(sorted(list(l.course.keys())))])
        print('Student Summary')
        print(row)

    def print_instructors_table(self):
        row1:PrettyTable=PrettyTable()
        row1.field_names=['cwid','name','department','course', 'students']
        for i,l in self.instructors.items():
            for x,y in l.course.items():
                row1.add_row([i,l.name,l.department,x,y])
        print('Instructor Summary')
        print(row1)
if __name__ == "__main__":
    t=Repository(os.getcwd()+"\\week09\\")
    print(t.students['11461'])
    t.print_students_table()
    t.print_instructors_table()