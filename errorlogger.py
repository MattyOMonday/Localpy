# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 15:28:25 2015

@author: Matty
"""
import sys
header = \
[
'import sys',
'import traceback',
'try:'
]

non_err_footer = \
[
's = open("err_log.txt","w")',
's.write("no error")',
's.close()'
]

err_footer = \
[
'err_info = sys.exc_info()',
'err_type = str(err_info[0]).split(".")[-1][:-2]',
'err_line = traceback.tb_lineno(err_info[2])',
's = open("err_log.txt","w")',
's.write(str(err_type)+"\\n")',
's.write(str(err_line))',
's.close()'
]

class Logger(object):
    def __init__(self, filename="trash.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

def add_error_logging(file_name):
    """
    Wraps the whole file in a tray/except loop, 
    and then writes the results of any error to a text file
    """    
    
    s = open(file_name,"r")
    lines = s.readlines()
    s.close()
    new_lines = []
    for i in header:
        new_lines.append(i+"\n")
    for i in lines:
        new_lines.append("\t"+i)
    new_lines.append("\n")
    for i in non_err_footer:
        new_lines.append("\t"+i+"\n")
    new_lines.append("except Exception as e:\n")
    for i in err_footer:
        new_lines.append("\t"+i+"\n")
    s = open(file_name,"w")
    for i in new_lines:
        s.write(i)
    s.close()

def check_for_errors(file_name):
    saved_stdout = sys.stdout
    sys.stdout = open("trash.txt","r") 
    try:         
        execfile(file_name)
        sys.stdout = saved_stdout
        return (False,False)
    except Exception as e:
        sys.stdout = saved_stdout
        if type(e) == SyntaxError:
            return (True,e)
        else:
            return (False,True)


