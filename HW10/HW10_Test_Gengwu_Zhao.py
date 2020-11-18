import unittest,os
from HW10_Gengwu_Zhao import Repository
class TestRepository(unittest.TestCase):
    def test_Repository(self):
        t=Repository(os.getcwd()+"\\week10\\")
        #test the instructors info
        self.assertEqual(t.instructors['98760'].name,'Darwin, C')
        self.assertEqual(t.instructors['98765'].course['SSW 567'],4)
        self.assertEqual(t.instructors['98760'].department,'SYEN')
        #test the students info
        self.assertEqual(t.students['11788'].name,'Fuller, E')
        self.assertEqual(t.students['11788'].major,'SYEN')
        self.assertEqual(t.students['11461'].course['SYS 800'],'A')
        self.assertEqual(t.students['11461'].course['SYS 100000'],'')
        self.assertEqual(round(t.students['11461'].gpa,2),3.92)
        
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)