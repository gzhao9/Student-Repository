from datetime import datetime, timedelta, date
from typing import Tuple, Iterator,List
from prettytable import PrettyTable
from collections import defaultdict
#from HW08_Gengwu_Zhao import file_reader
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
    def __init__(self,cwid:str,name:str,major:str,remind_course=list()):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.complete_course=list()
        self.remind_course=dict()
        self.gpa=0
        self.course = defaultdict(str)
        self.change_remind_course(remind_course)
    
    def change_remind_course(self,require_course:list()):
        for i in require_course:
            self.remind_course[i.course]=i

    def get_course_info(self):
        grade_value={'A':4.0,'A-':3.75,'B+':3.25,'B':3.0,'B-':2.75,'C+':2.25,'C':2.0,'C-':0,'D+':0,'D':0,'D-':0,'F':0}
        sums=0
        for i,j in self.course.items():
            sums+=grade_value[j]
            if grade_value[j]!=0:
                self.complete_course.append(i)
                if i in self.remind_course.keys():
                    del self.remind_course[i]
        if len(self.course.values())!=0:
            self.gpa=sums/len(self.course.values())
    
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

class Course:
    def __init__(self,Major:str,Required:str,course:str):
        self.mjao=Major
        self.required=Required
        self.course=course
    def __str__(self):
        return f"Course: {self.course} Major: {self.mjao} Required: {self.required} "

class Repository:
    def __init__(self,path):
        os.chdir(path)
        self.path=path
        self.students=dict()
        self.instructors=dict()
        self.major=defaultdict(list)
        self.get_info()
    #get the info form the path
    def get_info(self):

        #get the Major info
        for line in file_reader(self.path+'majors.txt',3,'\t',True):
            self.major[line[0]].append(Course(line[0],line[1],line[2]))

        #get the students info
        for line in file_reader(self.path+'students.txt',3,';',True):
            if line[0] in self.students.keys():
                raise ValueError(f'The info of this students {line[0]} has been added')
            self.students[line[0]]=Student(line[0],line[1],line[2],self.major[line[2]])
        
        #get the instructors info
        for line in file_reader(self.path+'instructors.txt',3,'|',True):
            if line[0] in self.instructors.keys():
                raise ValueError(f'The info of this instructors {line[0]} has been added')
            self.instructors[line[0]]=Instructors(line[0],line[1],line[2])
        
       
        #get the grade info
        for line in file_reader(self.path+'grades.txt',4,'|',True):
            if self.students[line[0]].course[line[1]] is not None:
                self.students[line[0]].course[line[1]]=line[2]
                self.instructors[line[3]].course[line[1]]+=1
            else:
                raise ValueError(f'The grade of this student {line[0]} has been added')
        
        #Calculate student course information
        for i in self.students.keys():
            self.students[i].get_course_info()

    def print_students_table(self):
        row:PrettyTable=PrettyTable()
        row.field_names=['Cwid','Name','Major','Complete Courses','Remaining Requireed','Remaining Electives','Gpa']
        for i,l in self.students.items():
            rc=list()
            ec=list()
            for x in l.remind_course.values():
                if x.required=='R':
                    rc.append(x.course)
                else:
                    ec.append(x.course)
            row.add_row([i,l.name,l.major,sorted(l.complete_course),sorted(rc),sorted(ec),round(l.gpa, 2)])
        print('Student Summary')
        print(row)
    
    def print_major_table(self):
        row:PrettyTable=PrettyTable()
        row.field_names=['Major','Require Course','Electives']
        for i,l in self.major.items():
            rc=list()
            ec=list()
            for x in l:
                if x.required=='R':
                    rc.append(x.course)
                else:
                    ec.append(x.course)
            row.add_row([i,sorted(rc),sorted(ec)])
        print('Major Summary')
        print(row)

    def print_instructors_table(self):
        row1:PrettyTable=PrettyTable()
        row1.field_names=['Cwid','Name','Department','Course', 'Students']
        for i,l in self.instructors.items():
            for x,y in l.course.items():
                row1.add_row([i,l.name,l.department,x,y])
        print('Instructor Summary')
        print(row1)

if __name__ == "__main__":
    t=Repository(os.getcwd()+"\\week10\\")
    print(t.students['11461'])
    t.print_major_table()
    t.print_students_table()
    t.print_instructors_table()