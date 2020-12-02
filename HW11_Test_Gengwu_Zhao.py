import unittest,os
from HW11_Gengwu_Zhao import Repository
class TestRepository(unittest.TestCase):
    def test_Repository(self):
        t=Repository(os.getcwd()+"\\week11\\")
        #test the instructors info
        self.assertEqual(t.instructors['98764'].name,'Cohen, R')
        self.assertEqual(t.instructors['98763'].course['SSW 810'],4)
        self.assertEqual(t.instructors['98762'].department,'CS')
        #test the students info
        self.assertEqual(t.students['10103'].name,'Jobs, S')
        self.assertEqual(t.students['10183'].major,'SFEN')
        self.assertEqual(t.students['10103'].course['CS 501'],'B')
        self.assertEqual(t.students['10115'].course['SYS 100000'],'')
        self.assertEqual(round(t.students['10183'].gpa,2),4.0)
        
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)