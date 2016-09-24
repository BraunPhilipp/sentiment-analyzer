
"""
Log multiple instances to same file.
"""

def log(msg):
    f = open('error.log', 'a')
    f.write(msg+'\n')
    f.close()

def clear():
    f = open('error.log', 'w')
    f.write('')
    f.close()
