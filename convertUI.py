import sys, pprint
from pyside2uic import compileUi
pyfile = open('C:/Users/nic/Documents/maya/scripts/testUI.py', 'w')
compileUi('C:/Users/nic/Documents/maya/scripts/test.ui', pyfile, False, 4,False)
pyfile.close()