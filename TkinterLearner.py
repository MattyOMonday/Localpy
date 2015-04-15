# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:26:45 2015

@author: Matty
"""
import PitonCommandLineNew as cmd
import Tkinter as tk


class guiEventHandler(cmd.eventHandler):
    def handle_synt_errs(self,e):
        pass

class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    Method written by Brian Oakley of the StackOverflow forums
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.letters = "abcdefghijklmnopqrstuvwxyz_0123456789"
        
    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            index_end = "%s+%sc" % (index, count.get())
            
            last_index = "%s+%sc" %(index, count.get())
            self.mark_set("matchEnd", index_end)
            #if(self.check_letters(index,"front") and self.check_letters(index_end,"end")):            
                #self.tag_add(tag, "matchStart", "matchEnd")
            if(self.check_bookends(index+"-1c",last_index)):            
                self.tag_add(tag, index, index_end)
            

            
    def highlight_quote(self, pattern, tag, start ="1.0", end = "end",
                        regexp = False):
        
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        #count = tk.IntVar()
        while True:            
            #index = self.search(pattern, "matchEnd","searchLimit",
            #                    count=count, regexp=regexp)
            break
            
    def check_bookends(self,start,end):
        if ((not ("1.0" in start)) and (self.get(start).lower() in self.letters)):
            return False
        if (self.get(end).lower() in self.letters):
            return False
        return True
        
class Application(tk.Frame):
    """A GUI Application"""
    def __init__(self,master):
        """initialize the frame"""
        tk.Frame.__init__(self,master)
        self.counts = 0
        self.cmd_hdl = cmd.eventHandler()
        self.grid()
        self.create_widgets2()
        self.def_keywords()
        
        
    def create_widgets2(self):
        self.inst_lbl = tk.Label(self, text = "LocalPy IDE - Redefine your favorite python keywords")
        self.inst_lbl.grid(row = 0, column = 0, columnspan=4, sticky = tk.W)
        
        self.txt_lbl = tk.Label(self, text = "File Name:")
        self.txt_lbl.grid(row = 1, column = 0, sticky = tk.W)
        
        self.txt_ent = tk.Entry(self)
        self.txt_ent.grid(row = 1, column = 1, columnspan = 2, sticky = tk.W)
        
        self.load_bttn = tk.Button(self,text="Load", command = self.load)
        self.load_bttn.grid(row = 2, column = 0, sticky = tk.W)
        
        self.save_bttn = tk.Button(self,text="Save", command = self.save)
        self.save_bttn.grid(row = 2, column = 1, sticky = tk.W)
        
        self.run_bttn = tk.Button(self,text="Run", command = self.run)
        self.run_bttn.grid(row = 2, column = 2, sticky = tk.W)
        
        self.configure_ide()
        
        self.configure_browser()
        self.configure_log()
        
        
    def configure_ide(self):        
        self.txt_box = CustomText(self, width = 50, height = 32, wrap = tk.WORD)       
        self.txt_box.grid(row = 3, column=0, rowspan =10, columnspan = 5, sticky = tk.W)
        self.txt_box.tag_configure("purple", foreground="#bf56bb")
        self.txt_box.tag_configure("blue",foreground="#0000ff")
        self.txt_box.bind("<space>",self.color_text)
        self.txt_box.bind("<Tab>",self.redef_tab)        
        self.txt_box.bind("<Return>",self.redef_enter)

    def configure_browser(self):
        self.bsr_lbl = tk.Label(self, text = "File Browser")
        self.bsr_lbl.grid(row = 3, column = 6, columnspan=1, sticky = tk.W)
        
        self.bsr_btn_bck = tk.Button(self,text="<--", command = self.cd_up)      
        self.bsr_btn_bck.grid(row =3, column = 7, sticky = tk.W)
        
        self.bsr_btn_fwd = tk.Button(self,text="-->", command = self.cd_dn)      
        self.bsr_btn_fwd.grid(row =3, column = 8, sticky = tk.W)        
        
        self.bsr_box = tk.Listbox(self, width = 60, height = 20)   
        self.bsr_box.grid(row = 4, column=6, rowspan =3, columnspan = 5, sticky = tk.W)   
            
        self.bsr_box.bind("<Button-1>",self.cd_dn)
        self.bsr_box.bind("<Button-2>",self.cd_up)
        self.update_file_listings()
            
    def cd_up(self,event = tk.Event()):
        self.cmd_hdl.get_dir().cd_up()
        self.update_file_listings()
             
    def cd_dn(self,event = tk.Event()):
        selection = self.bsr_box.curselection()
        if(not selection == ()):        
            dir_name = self.bsr_box.get(selection)
            if("." in dir_name):
                self.txt_ent.delete(0,tk.END)
                self.txt_ent.insert(0,dir_name)
            else:
                self.cmd_hdl.cd("cd " +dir_name)
                self.update_file_listings()
            
    def update_file_listings(self):
        self.bsr_box.delete(0,tk.END)
        files = self.cmd_hdl.print_files("").split("\n")[1:]        
        for i in files:        
            self.bsr_box.insert(tk.END, i)
    def configure_log(self):
        self.log_lbl = tk.Label(self, text = "Event Log:")
        self.log_lbl.grid(row = 7, column = 6, columnspan=2, sticky = tk.W)
        
        self.log_box = CustomText(self, width = 45, height = 9, wrap = tk.WORD)   
        self.log_box.grid(row = 8, column=6, columnspan = 5, sticky = tk.W)
        
    
    def color_text(self,event):
        self.txt_box.tag_remove("purple",0.0,tk.END)
        self.txt_box.tag_remove("blue",0.0,tk.END)        
        for i in self.res_words:
            self.txt_box.highlight_pattern(i,"purple")
        for i in self.def_funcs:
            self.txt_box.highlight_pattern(i,"blue")
            
    def redef_tab(self,event):
        #changes number of spaces made by tab to 4
        self.txt_box.insert(tk.END,"    ")
        return 'break'

    def redef_enter(self,event):
        #sets the number of spaces on the new line to match the previous line
        text = self.txt_box.get('end -1 lines',tk.END)
        newline = ""
        if text[-2] == ":":
            newline+="    "
        for i in text:
            if not(i == " "):
                break
            newline +=" "
        self.txt_box.insert(tk.END,"\n"+newline)
            
        return 'break'
        
    def load(self):
        file_name = self.txt_ent.get()
        s = open(self.cmd_hdl.get_dir().get_cwd()+"\\"+str(file_name),"r")
        lines = s.read().replace("\t","    ")
        s.close()
        self.txt_box.delete("0.0",tk.END)
        self.txt_box.insert("0.0",lines)
        self.color_text(tk.Event())        
        
    def save(self):
        file_name = self.txt_ent.get()
        text =str(self.txt_box.get("0.0",tk.END)).replace("    ","\t")
        s = open(self.cmd_hdl.get_dir().get_cwd()+"\\"+str(file_name),"w")
        s.write(text)
        s.close()
    def run(self):
        file_name = self.txt_ent.get()
        self.cmd_hdl.run_file(file_name)
    
    def def_keywords(self):
        s = open("keywords.py","r")
        lines = s.readlines()
        self.res_words = []
        self.def_funcs = []
        on_res_words = True
        for i in lines:
            if(not i[0] == "#" and on_res_words):
                self.res_words.append(i.split()[1])
            if(not i[0] == "#" and not on_res_words):
                self.def_funcs.append(i.split()[1])
            if(i == "#built in functions\n"):
                on_res_words = False
            if(i == "#default modules\n"):
                break
            
root = tk.Tk()
root.title("Simple GUI")
root.geometry("800x600")
app = Application(root)


root.mainloop()
