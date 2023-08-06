#imports
try:
    import os
    import time
except ImportError:
    print("Import Error.\nPlease install 'os' and 'time'.")
#license
Creator = "Shane Sarzedas"
CreatorEmail = "shane.sarzedas@gmail.com"
__version__ = "0.0.2"
#commands
def wait(num1=1 or num2):
    time.sleep(num1 or num2)
def createtxt(filename):
    f = open(filename+".txt", "+w")
    writing = input("What should be in the file?\n")
    f.write(writing)
    print("succesfully created!")
def createpy(filename):
    f = open(f"{filename}.py", "+w")
    writing = input("what should be in the file?\n")
    f.write(writing)
    f.close()
def openfile(filename):
    try:
        fp = open(filename, "r")
        print(fp.read())
        fp.close()
    except FileNotFoundError:
        print("try again later")
def deletefile(filename):
    try:
        os.remove(filename)
        print(f"{filename} has been removed")
    except FileNotFoundError:
        print("File not found")
#please do not copy this code.
