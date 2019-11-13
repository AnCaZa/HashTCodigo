import sys
import os
import re
file_dir = os.path.dirname(__file__)
sys.path.append("Sources")
from Sources import AnalizadorSintatico
if __name__ == "__main__":
    a = AnalizadorSintatico.AnalizadorSintatico()
    