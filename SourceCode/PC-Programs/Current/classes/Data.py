import numpy as np

class GetData(object):
    def __init__(self):  
        self.arr = []
        self.arr1 = []
        self.arr_bot = []
        self.arr_bot1 = []
    def Data_top_x(self):
        self.arr = np.loadtxt("file1.txt")
        return self.arr
    
    def Data_top_y(self):
        self.arr1 = np.loadtxt("file2.txt")
        return self.arr1
        
    def Data_bottom_x(self):
        self.arr_bot = np.loadtxt("file3.txt")
        return self.arr_bot
        
    def Data_bottom_y(self):
        self.arr_bot1 = np.loadtxt("file4.txt")
        return self.arr_bot1