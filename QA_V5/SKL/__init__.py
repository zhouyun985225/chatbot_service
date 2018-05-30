import sys
import os

_curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) ))
sys.path.append(_curpath)