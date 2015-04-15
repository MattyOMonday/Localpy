# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:28:36 2015

@author: Matty
"""
#import cmdlinewords as cw

import os
import glob
import importlib
import wordreplacer
import CONFIG
import errorlogger
cw = importlib.import_module((CONFIG.command_line_translations)[:-3])
class translatedFile():
    """    
    holds all the data required to translate an alternate-language python file into 
    English, as well as to run that file
    """
        
    def __init__(self, file_name):
        self.file_name = file_name
        self.translated_name = self.add_suffix(file_name)
        self.translated = False
        self.translate_failed = False
        
    def add_suffix(self,file_name):
        if("." in file_name):
            suffix_loc = file_name.index(".")
            return file_name[:suffix_loc] + "_translated.py"
        else:
            return file_name + "_translated.py"
            
    def translate(self,keep_output = False):
        try:
            self.translated = True;
            wordreplacer.translate(self.file_name,"trans.py")
            if keep_output:
                wordreplacer.translate(self.file_name,self.translated_name)
            errorlogger.add_error_logging("trans.py")
        except:
            self.translate_failed = True
            print (cw.file_not_found%self.file_name)
            
    def run(self):
        if(not self.translated):
            self.translate()
        #I know this is bad and I'm really sorry but it's the best I can do.
        if not self.translate_failed:
            #check the file for syntax errors
            synt_errs = errorlogger.check_for_errors("trans.py")            
            if(synt_errs[0]):
                return self.handle_synt_errs(synt_errs[1])
            else:
                os.system("python trans.py")
                return self.handle_errs()

    def handle_synt_errs(self,e):
        err_line = e.lineno - 3
        s = open(self.file_name,"r")
        lines = s.readlines()   
        err_lines = "*"+lines[err_line-1][:-1]+"*\n"
        return (cw.syntax_error%err_line) + "\n" + err_lines
            
    def handle_errs(self):
        s = open("err_log.txt","r")
        lines = s.readlines()
        s.close()
        if(not lines[0] == "no error"):
            err_type = wordreplacer.translate_string(lines[0],orig_lang = "english")            
            err_line = int(lines[1])-3
            s = open(self.file_name,"r")
            lines = s.readlines()   
            err_lines = "*"+lines[err_line-1][:-1]+"*\n"
            return (cw.error_msg%(err_type[:-1],err_line)) +"\n"+ err_lines
        else:
            return ""
    
    def get_name(self):
        return self.file_name
    def get_translated_name(self):
        return self.translated_name
    def get_translated(self):
        return self.translated
        
class directoryHandler():
    """
    keeps track of the current working directory (cwd)
    """
    def __init__(self,cwd = os.getcwd()):
        self.cwd = cwd
        self.cd_up()
    def cd(self,path):
        """
        Go to the specified directory
        """
        self.cwd = path
            
    def cd_up(self):
        """
        Go up one directory level
        """
        parts = self.cwd.split("\\")
        self.cwd = ""
        for i in parts[:-1]:
            self.cwd += i + "\\"
        self.cwd = self.cwd[:-1]
            
    def get_cwd(self):
        return self.cwd
        
    def ls(self):
        files = []
        for i in glob.glob(self.cwd+"\\*"):
            files.append(i.split("\\")[-1])
        return files
    
class eventHandler():
    """
    Handles user input
    """
    def __init__(self):
        self.line_num = 0
        self.command_list = []
        self.directory = directoryHandler()
        self.help_dict = cw.help_dict
        
    def get_line_num(self):
        return self.line_num
        
    def handle_event(self,event):
        self.command_list.append(event)
        self.line_num+=1        
            
        if (cw.help_cmd in event):
            return self.print_help(event)
        
        elif (cw.run_cmd in event):
            return self.run_file(event)
            
        elif (event == cw.bye):
            return self.clean_up()
            
        elif (cw.ls in event):
            return self.print_files(event)
            
        elif(cw.cd in event):
            return self.cd(event)
        
        elif(event == cw.cwd):
            return self.print_cwd()
            
        elif(event == cw.cmds):
            return self.print_commands()
            
        elif(event == cw.trans):
            return self.print_translated()
        else:
            return (cw.cmd_not_found%event)
                    
    def cd(self,event):
        dir_name = event.split()[-1]
        #print(cw.out_phrase+"[%i]"%self.line_num)
        if (cw.cd_sub1) in event:
            self.directory.cd_up()
            return (self.directory.get_cwd())
        else:
            dir_name = event.split()[-1]
            if not dir_name[0] in "\\/":
                dir_name = self.directory.get_cwd() + "\\" + dir_name
            if "." in dir_name or glob.glob(dir_name+"\\*") == []:
                return(cw.empty_dir%dir_name)
            else:
                self.directory.cd(dir_name)
                return (self.directory.get_cwd())
                
    def clean_up(self):
        os.remove("cmdlinewords.pyc")
        os.remove("wordreplacer.pyc")
        try:
            os.remove("trans.py")
            os.remove("trans.pyc")
        except:
            pass
        return (cw.bye_msg)

    def print_files(self,event):
        files = self.directory.ls()
        #print (cw.out_phrase+"[%i]: "%self.line_num)
        result = self.directory.get_cwd()+"\n"
        
        if cw.ls_sub1 in event:
            for i in files:
                if cw.special_extension in i:
                    result += i +"\n"
        else:
            for i in files:
                result += i +"\n"
        return result
                
    def print_cwd(self):
        #print (cw.out_phrase+"[%i]: "%self.line_num)
        return self.directory.get_cwd()
        
    def print_help(self,event):
        cmd = event.split()[-1]
        #print (cw.out_phrase+"[%i]: "%self.line_num)
        if cmd in self.help_dict.keys():
            return self.help_dict[cmd]
        else:
            return cw.cmd_not_found%cmd
            
    def print_commands(self):
        result = ""
        for i in self.help_dict.keys():
            result += i + "\n"
        return result
        
    def print_translated(self):
        #print (cw.out_phrase+"[%i]: "%self.line_num)
        result = ""
        for i in cw.translatedPackages:
            result += i + " (%s)\n"%wordreplacer.translate_string(i,orig_lang="english")
        return result
        
    def run_file(self,event):
        file_name = event.split()[-1]
        #print (cw.out_phrase+"[%i]: "%self.line_num)       
        file_to_run = translatedFile(self.directory.get_cwd() +"\\"+file_name)
        return file_to_run.run()
        
    def get_dir(self):
        return self.directory
            
def remove_extension(file_name):
    parts = file_name.split(".")            
    return parts[0]
def main():
    print cw.start_msg
    user_input = ""
    ui = eventHandler()
    while(not user_input == cw.bye):
        user_input = raw_input(">>>")
        print ui.handle_event(user_input)

if __name__ == "__main__":
    main()
    
