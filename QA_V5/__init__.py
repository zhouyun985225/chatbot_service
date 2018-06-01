import sys
import os


_curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) ))
nb_path = os.path.join(_curpath, 'NaiveBayes')
skl_path = os.path.join(_curpath, 'SKL')
res_path = os.path.join(_curpath, 'resource')
sys.path.append(_curpath)
sys.path.append(nb_path)
sys.path.append(skl_path)
sys.path.append(res_path)