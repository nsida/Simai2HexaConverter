'''HexaStageTool
v0.3.2
new feature
warning 
irrational beat will limit to 4 decimal places
multiple{}in the same beat do not have a fail safe mechanism
compound hit times now show interger
v0.3.3


用()detect bpm DONE(未有用途,原本打算section offset:0 bpm:120)
syl E 可以reset cur_beat回 =0,方便note跟運鏡分開寫
E(bpm){time_sign}note/stage_movement
你可以用E來分隔開音符運鏡，甚至不同種類的雲鏡也可以分隔開

例如
{4},{16}6,5c,4c,3c,2c,1c,6c,5c,4c/1,2c,3c,4c,5c,6c,1c,2c,3o/4o,
E
{4},,,,,{1}caz[4:15]ios,caz[8:-30]ios,,caz[8:30]ios,,caz[8:-30]ios,,caz[4:75]is,
E
{4},,,,,{1}cpz[8:-2]lin,,,,,,cpz[4:2]i2,

出來的結果會是ing
--------------------------------------------------
n short lt 1.0
n catch lc 1.25
n catch lb 1.5
n catch rb 1.75
n catch rc 2.0
n catch rt 2.25
n catch lt 2.5
n catch lc 2.75
n catch lb 3.0
n short rt 3.0
n catch rc 3.25
n catch rb 3.5
n catch lb 3.75
n catch lc 4.0
n catch lt 4.25
n catch rt 4.5
n catch rc 4.75
n swipe out rb 5.0
n swipe out lb 5.0
--------------------------------------------------
a s_movecamera angle z 5.0 4.0 15.0 EaseInOutSine
a s_movecamera angle z 9.0 8.0 -30.0 EaseInOutSine
a s_movecamera angle z 17.0 8.0 30.0 EaseInOutSine
a s_movecamera angle z 25.0 8.0 -30.0 EaseInOutSine
a s_movecamera angle z 33.0 4.0 75.0 EaseInSine
a s_movecamera position z 5.0 8.0 -2.0 Linear
a s_movecamera position z 29.0 4.0 2.0 EaseInQuad
--------------------------------------------------

現在hexcom.hard.txt???
Y/N決定覆不覆蓋現有hexa data
angle
 # TODO : compress and buitifie code


 0.4.0:
 括號表示著譯 DONE
 錯easing會崩潰 DONE
 問Y/N沒有隔行 Done
 debug print toggle Done
 支援hard以外的難度 Done
 程式内部找[]或[#]數值現在使用def/return

 0.4.1:
 []在程式内部不再轉換成<>來處理

 新增<> function語法
 目前打算支援<addline:XXX> DONE
 <setbeat:XXX> 
 <changestage:XXX>[#XX]XXX
 0.4.2:
 現在如果發現chart.X.txt是用Converter generate出來的，會直接覆蓋掉所有line
 如果不是的話會先問要全部覆蓋，只覆蓋a n 還是在下方append結果

 

'''

import shutil
import re #import regex module
import os



is_generated_by_converter_flag = False
diff = input("Please input difficulty(filename) (For Example: Diff = hard):\nDiff = ")
DEBUG = input("Enable Debug Mode?(T/F):") or "F"


final_line_output = []
final_note_output = []
final_action_output = []
failed_syllabus = []
warn_syllabus = []
now_bpm = 0.0

start_beat = float(input("Please input starting Beat or input nothing for 0 (Default is 0):") or 0)


def log(s):
    if DEBUG.lower() == "t" :
        print(s)
    else:
        pass
    
try:
    hexcom_file = open(f"hexcom.{diff}.txt","r",encoding="utf-8")
    inputstr = hexcom_file.read()
    hexcom_file.close()
except:
    print(f"could not read hexcom.{diff}.txt")
    inputstr = ""


log(f"Input string read from file is: {inputstr}")

teststr = inputstr.replace("\n","") #remove all \n
teststr = re.sub("\(.+?\)","", teststr)#Remove "()" Content

addline_list = re.findall("<addline:.+?>",teststr)
for line in addline_list:
    log(line.replace("<addline:","").replace(">",""))
    final_line_output.append(line.replace("<addline:","").replace(">",""))
    teststr = re.sub(line,"",teststr)
    
log(f"Feeding in:\n {teststr}")


syllist = teststr.split(",") # use "," to determine the split
log (syllist)


cur = 0 #current position of processing
default_note_interval = 4  #4th-note interval is the default(Assume 4th-note if user forgot to set time signature
note_int = default_note_interval
cur_beat = start_beat

easing_dict = {'lin':'Linear',
               'clp':'clerp',
               'spr':'spring',
               
               'is':'EaseInSine',     
               'os':'EaseOutSine',
               'ios':'EaseInOutSine',
               
               'i2':'EaseInQuad',
               'o2':'EaseOutQuad',
               'io2':'EaseInOutQuad',

               'i3':'EaseInCubic',
               'o3':'EaseOutCubic',
               'io3':'EaseInOutCubic',
               
               'i4':'EaseInQuart',
               'o4':'EaseOutQuart',
               'io4':'EaseInOutQuart',

               'i5':'EaseInQuint',
               'o5':'EaseOutQuint',
               'io5':'EaseInOutQuint',
               
               'ic':'EaseInCirc',  
               'oc':'EaseOutCirc',
               'ioc':'EaseInOutCirc',
               
               'ibk':'EaseInBack',  
               'obk':'EaseOutBack',
               'iobk':'EaseInOutBack',

               'iex':'EaseInExpo',  
               'oex':'EaseOutExpo',
               'ioex':'EaseInOutExpo',
               
               'ibn':'EaseInBounce',  
               'obn':'EaseOutBounce',
               'iobn':'EaseInOutBounce',

               'iel':'EaseInElastic',  
               'oel':'EaseOutElastic',
               'ioel':'EaseInOutElastic',  

               '':'EASING_NOT_VALID',  
               }


lane_pos_dict = {'1':'rt','2':'rc','3':'rb','4':'lb','5':'lc','6':'lt'}
common_time_signatures = [128,96,64,48,32,24,16,12,8,6,4,3,2,1]

def is_int(num):
    return (round(num)-num == 0)

def error_message(num):
    log(f"error code: {num}")

def warn_syl_msg(reason):
    warn_syllabus.append("Beat "+ str(round(cur_beat,4))+": "+str(syllist[cur]) + " (reason: " + reason +")" )

def fail_syl_msg(reason):
    failed_syllabus.append("Beat "+ str(round(cur_beat,4))+": "+str(syllist[cur]))


def find_colbrac_num(XXX):
    x = float(re.findall("\[\d*\.*\d+:",XXX)[0].replace("[","").replace(":",""))
    y = float(re.findall(":-*\d*\.*\d+\]",XXX)[0].replace(":","").replace("]",""))
    return(x,y)

def find_hashbrac_num(XXX):
    x = float(re.findall("\[#\d*\.*\d+\]",XXX)[0].replace("[","").replace("]","").replace("#",""))
    return(x)

def find_ease(YYY):
    ease = easing_dict[re.findall("\].+$",YYY)[0].replace("]","")]
    return(ease)

def find_lane_name(ZZZ):
    x = lane_pos_dict[re.findall("^[1-6]",ZZZ)[0]] 
    return (x)


def simple_note():
    temp = str(syllist[cur])

    if re.match("^[1-6]$",temp):
        note_type = "short"
    elif re.match("^[1-6]c$",temp):
        note_type = "catch"
    elif re.match("^[1-6]i$",temp):
        note_type = "swipe in"
    elif re.match("^[1-6]o$",temp):
        note_type = "swipe out"
    else:
        log("not a valid simple note format")
        fail_syl_msg()

    note_pos = find_lane_name(temp)
    final_note_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)}")


def complex_note():
    
    temp = syllist[cur]
    log("temp is:")
    log(temp)
    note_type = ""
    data_format = ""
    num_1 = 0.0
    num_2 = 0.0
    num_3 = 0
    num_4 = 0.0
    if re.match("^[1-6](l)\[\d+:\d+\]$",temp): 
        note_type = "long"
        data_format = ":" 
        log("it is a long")
    elif re.match("^[1-6](l)\[#(\d*\.)?\d+\]$",temp):
        note_type = "long"
        data_format = "#"
        log("it is a long#")
    elif re.match("^[1-6](cl)\[\d+:\d+\]$",temp):
        note_type = "clong"
        data_format = ":" 
        log("it is a clong")
    elif re.match("^[1-6](cl)\[#(\d*\.)?\d+\]$",temp):
        note_type = "clong"
        data_format = "#" 
        log("it is a clong#")
    elif re.match("^[1-6](k)\[(\d*\.)?\d+:\d+\]$",temp):
        note_type = "compound"
        data_format = ":" 
        log("it is a compound")
    else:
        log("not a valid complex note format")
        fail_syl_msg("not a valid complex note format")
    log(temp)
  
    note_pos = find_lane_name(temp)

    log("num_1 = " + str(num_1))
    if data_format == ":":
        num_2,num_3 = find_colbrac_num(temp)

        log("num_2 = " + str(num_2))
        log("num_3 = " + str(num_3))
    elif data_format == "#":
        num_4 = find_hashbrac_num(temp)
        log("num_4 = " + str(num_4))
        
    
    if note_type == "compound":
        final_note_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_2)),4)} {'%.0f' %float(num_3)}")
        log(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_2)),4)} {'%.0f' %int(num_3)}")
    elif data_format == ":":
        final_note_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat + 4 * float(num_3) / float(num_2)),4)}")
        log(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat + 4 * float(num_3) / float(num_2)),4)}")
    elif data_format == "#" :
        final_note_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_4)),4)}")
        log(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_4)),4)}")

def stage_action():
    temp = syllist[cur]
    note_pos = ""
    change_object = ""
    attribute = ""
    axis = ""
    duration = 0.0
    amount = 0.0
    easing = ""

    try:
        note_pos = lane_pos_dict[re.findall("^[1-6]",temp)[0]]
    except:
        log("no note_pos")
        note_pos = ""
        
    if re.findall("^[1-6]t",temp):
        change_object = "trail"
    elif re.findall("^s[apAP]",temp):
        change_object = "stage"
    elif re.findall("^c[apAP]",temp):
        change_object = "camera"        
    else:
        error_message(1)
        
    if re.findall("^[1-6]to",temp):
        attribute = "opacity"
    elif re.findall("a[xyz]\[",temp):
        attribute = "angle"
    elif re.findall("A[xyz]\[",temp):
        attribute = "abs_angle"
    elif re.findall("p[xyz]\[",temp):
        attribute = "position"        
    elif re.findall("P[xyz]\[",temp):
        attribute = "abs_position"
    else:
        error_message(2)

    if re.findall("x\[",temp):
        axis = "x"
    elif re.findall("y\[",temp):
        axis = "y"
    elif re.findall("z\[",temp):
        axis = "z"
    else:
        error_message(3)

    log (find_colbrac_num(temp)[0])
    log (find_colbrac_num(temp)[1])
    duration = find_colbrac_num(temp)[0]
    amount = find_colbrac_num(temp)[1]

    try:
        easing = easing_dict[re.findall("\].+$",temp)[0].replace("]","")]
    except:
        fail_syl_msg("Not a valid Easing")
        easing = "EASING_NOT_VALID"

    if   re.match("^[1-6]to",temp):
        if amount > 1 or amount < 0:
            warn_syl_msg("opacity out of range")
        log(f"a changeopacity {change_object} {note_pos} {round(cur_beat,4)} {duration} {amount} {easing}")
        final_action_output.append(f"a changeopacity {change_object} {note_pos} {round(cur_beat,4)} {duration} {amount} {easing}")
        #a changeopacity trail rt 195.3 4 0.5 Linear
        
    elif re.match("^[1-6]t[apAP]",temp):
        if (attribute == "angle" or attribute == "abs_angle") and not is_int(amount):
            warn_syl_msg("angle is not interger")
        final_action_output.append(f"a s_move{change_object} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        log(f"a s_move{change_object} {note_pos} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        
    elif re.match("^[sc][apAP][xyz]\[",temp):
        if (attribute == "angle" or attribute == "abs_angle") and not is_int(amount):
            warn_syl_msg("angle is not interger")
        final_action_output.append(f"a s_move{change_object} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        log(f"a s_move{change_object} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        #a s_movetrail rt position z 195.3 4 0.5 Linear
        
    else:
        error_message(4)

def change_stage():

    temp = syllist[cur]
    stage_name = re.findall("<.+?>",temp)[0].replace("<","").replace(">","")
    duration = re.findall("\[#*\d*\.*\d+\]",temp)[0].replace("[#","").replace("]","")
    easing = find_ease(temp)

    log(f"stagename, duration, easing is :{stage_name},{duration},{easing}")

    final_action_output.append(f"a changestage {stage_name} {cur_beat} {duration} {easing}")
    log(f"stagename, duration, easing is :{stage_name},{duration},{easing}")
    #find <> content
    #find[#XX] content
    #find easing behind ]
    #output "a changestage rectangle 88 1 EasOoutBounce"
    
    
       
    ##START THE ACTUAL SYL DETECTION



while cur < len(syllist):

    log ("processing syllabus '" + syllist[cur]+"'")


    if re.match ("^E", syllist[cur]):#Detect "E"
        cur_beat = 0.0
        syllist[cur] = syllist[cur].replace("E","")
        log("End syllabus found, resetting beat to 0")


    ###check for time signature and get rid of the -brackets

    if re.findall("{#(\d*\.)?\d+}", syllist[cur]) or re.findall("{(\d*\.)?\d+}", syllist[cur]) :#Detect "{}"
        log("found time signature")
        temp = syllist[cur]#copy the data out of syllist[cur] to not mess up the original data
        log(temp) 
        if False:# To prevent some dumdum to break my script
            note_int = 94.87
            print ("you serious? Really? 0th-note? I have to add 3 lines of extra code just becuz dumdum like you are trying to type some non-sense devide by zero shit into the curly bracket")
            
        else:

            if re.findall("{#(\d*\.)?\d+}",temp):
                time_sign_temp = (re.findall("{#\d+[.]*[\d+]*}",temp))[0]
                log(f"time signature found is {time_sign_temp}")
                temp_behind = temp.replace(time_sign_temp,"")
                note_int = 4 / float(time_sign_temp.replace("{","").replace("}","").replace("#",""))
                log(f"time signature have been changed to {note_int}")
            
            elif re.findall("{(\d*\.)?\d+}",temp):
                time_sign_temp = (re.findall("{\d+[.]*[\d+]*}",temp))[0]
                log(f"time signature found is {time_sign_temp}")
                temp_behind = temp.replace(time_sign_temp,"")
                note_int = float(time_sign_temp.replace("{","").replace("}",""))
                log(f"time signature have been changed to {note_int}")
            else:
                log("It is a time signature but could not recognise")
                fail_syl_msg("It is a time signature but could not recognise")

        if note_int not in common_time_signatures: 
            warn_syl_msg(f"{note_int} is not a common time signature")
        else:
            log("it IS a common time signature")
        try:        
            syllist[cur] = temp_behind
            log(f"temp behind is {temp_behind}")
        except:
            pass
    else:
        log("no time signature")

    if re.findall("<setbeat:.+?>",syllist[cur]):
        try:
            cur_beat = float(re.findall("<setbeat:.+?>",syllist[cur])[0].replace("<setbeat:","").replace(">",""))
            log(f"setbeat to {cur_beat}")
        except:
            log("could not process setbeat info")
        syllist[cur] = re.sub("<setbeat:.+?>","",syllist[cur])
    ###

     
    ###check for both(/), give both_token and put the fisrt item into syllist[cur] to process
    both_token = len(re.findall("/", syllist[cur]))
    log(f"{both_token} both token")
    if both_token > 0:
        temp = syllist[cur]
   
        log(f"temp is {temp}")
        both_list = temp.split("/")
        log(both_list[0])
        syllist[cur] = str(both_list[0])
        
    else:
        pass
    while both_token > -1: #determine loop how many times base on (/)+1

        ##note type detection
        if re.match("^[1-6][coi]?$",syllist[cur]): #short/catch/long/clong are all processed here
            simple_note()
            log("simple")

        elif re.match("^[1-6](k|cl|l)\[(\d*\.)?\d+:\d+\]$",syllist[cur]) or re.match("^[1-6](cl|l)\[#(\d*\.)?\d+\]$",syllist[cur]):
            complex_note()
            log("complex")
            
        elif re.match("^(([1-6]to)|(([1-6]t|s|c)((a|p|A|P)[xyz])))\[(\d*\.)?\d+:-?(\d*\.)?\d+\]...*$",syllist[cur]):
            stage_action()
            log("stage_action found")                

        elif syllist[cur] == "":
            log("Empty Note")

        elif re.match("^<.+?>\[#*\d*\.*\d+\]...*$",syllist[cur]):
            change_stage()
            log("change_stage found")  
        else:
            log("item unregonisable")
            fail_syl_msg("item unregonisable")

            
        #note detection ends
    

        both_token -= 1 #subtract 1 both_token for the while loop
        try:  #(try to) put the next item in the both_list onto the first slot
            del both_list[0]
            log(f"first element in both Deleted,both list now:{both_list}")
            syllist[cur] = str(both_list[0])
        except:
            log("both process ended/it is not a both")

        log("syllabus processing done")

                 
    cur = cur + 1  #current comma index
    cur_beat = cur_beat + (4/note_int) # move to the next beat number

        
print("whole process finished!!!")


print("-"*50)
print("Generated by Simai2HexaConverter V0.3")
print("-"*50)
print("Warning:")
for x in warn_syllabus:
    print(x)
    
print("-"*50)

print("Problems:")
for x in failed_syllabus:
    log(x)
    
print("-"*50)

print("final_note_output:")
for x in final_note_output:
    print(x)
    
print("-"*50)

print("Stage:")
for x in final_action_output:
    print(x)

print("-"*50)



overwrite_choice = input(f"Do you want to directly overwrite lines in chart.{diff}.txt?(Y/N)\nY: Lines that start with a or n in chart.{diff}.txt will be overwrited\nN: Newly generated lines will be added under the existing lines in chart.{diff}.txt\n")
if overwrite_choice.lower() == "y" or overwrite_choice.lower() == "n" :
    shutil.copy(f"chart.{diff}.txt",f"chart.{diff}_backup.txt")#make a copy of the oringinal file in case the programme fucked up something
    storage = []#store the needed lines
    output_file = open(f"chart.{diff}.txt","r",encoding="utf-8")    
    
    if overwrite_choice.lower() == "y":

        for line in output_file.readlines():#find lines that are NOT start with a or n and put the line in storage[]
            output_file = open(f"chart.{diff}.txt","w",encoding="utf-8") 
            if re.match("^a s_move.+",line) or re.match("^n.+",line) or re.match("^-+",line) or re.match("^Generated by ",line) or re.match("^define StagePosition",line) or re.match("^a changestage.+",line): 
                log("Ignore: " + line)
                storage.append("")
            else:
                log("Append: " + line)
                storage.append(line)
    elif overwrite_choice.lower == "n" :     
        output_file = open(f"chart.{diff}.txt","a",encoding="utf-8")  

    
    import datetime

    for line in storage:    #write all the lines saved in storage[]
        output_file.writelines(line)
    output_file.writelines("\n"+"-"*50+"\n")
    output_file.writelines("Generated by simai2hexaconverter V0.3 @ "+ str(datetime.datetime.now()) + "\n")
    output_file.writelines("-"*50+"\n")
    for line in final_line_output:#write all the lines saved in final_line_output[]
        output_file.writelines(line+"\n")
    output_file.writelines("-"*50+"\n")
    for line in final_note_output:#write all the lines saved in final_note_output[]
        output_file.writelines(line+"\n")
    output_file.writelines("-"*50+"\n")
    for line in final_action_output:#write all the lines saved in final_action_output[]
        output_file.writelines(line+"\n")    
    output_file.writelines("-"*50+"\n")  
    output_file.close()
    print(f"Done Writing To chart.{diff}.txt")
else:
    log("Invalid response: Aborting changes")

input("Press ENTER to Exit Converter")
    






