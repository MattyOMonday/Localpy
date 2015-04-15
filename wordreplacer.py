import CONFIG


s = open(CONFIG.python_translations,"r")
lines = s.readlines()
s.close()
split_lines = []
letters = "abcdefghijklmnopqrstuvwxyz_"
for i in lines:
	if(not i[0] == "#"):
		split_lines.append(i.split())
def special_replace(string,orig,replace):
    start_loc = 0    
    #get the index of orig
    while(orig in string[start_loc:]):
        start_loc = string.index(orig,start_loc)
        end_loc = start_loc+len(orig)
        nl_start = True
        nl_end = True
        if start_loc > 0:
            if string[start_loc-1:start_loc].lower() in letters:
                nl_start = False
        if end_loc < len(string):
            if string[end_loc:end_loc+1].lower() in letters:
                nl_end = False
        if(nl_start and nl_end):
            string = string[:start_loc] + replace + string[end_loc:]
        start_loc+=1
    return string

def translate(file_name,output_name, orig_lang = "translated"):
    s = open(file_name,"r")
    trans_lines = s.readlines()
    s.close()
    
    t = open(output_name,"w")
    for line in trans_lines:
        for change in split_lines:
            if orig_lang == "translated":
                if change[1] in line:
                    line = special_replace(line,change[1],change[0])
            if orig_lang == "english":
                if change[0] in line:
                    line = special_replace(line,change[0],change[1])
        t.write(line)
    t.close()
def translate_string(orig, orig_lang = "translated"):
    for change in split_lines:
        if orig_lang == "translated":
            if change[1] in orig:
                orig = special_replace(orig,change[1],change[0])
        if orig_lang == "english":
            if change[0] in orig:
                orig = special_replace(orig,change[0],change[1])
    return orig
    
