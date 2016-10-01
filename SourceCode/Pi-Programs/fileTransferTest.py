import os

text = raw_input("Enter a string to write to a text file and send to your PC via SSH: ")

f = open('testFile.txt', 'w')

f.write(text)
f.close()

os.system("scp testFile.txt daniel@192.168.42.12:~/Desktop/")

