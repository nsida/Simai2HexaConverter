'''HexaStageTool
v0.3.2
new feature
warning 
irrational beat will limit to 4 decimal places
multiple{}in the same beat do not have a fail safe mechanism
compound hit times now show interger
v0.3.3
預定功能
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

出來的結果會是
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

現在hexcom.hard.txt


'''

import shutil
import re #import regex module

final_output = []
final_stage_output = []
failed_syllabus = []
warn_syllabus = []
now_bpm = 0.0

start_beat = float(input("Please input starting Beat or input nothing for 0 (Default is 0):") or 0)


dummystr = "(170){4}1cl[#16.5555555],1k[81.5:6],(165)1cl[1:7],,1l[1:7]/1,E1to<1:1>lin/3tAx<45:37>ios,5tPx<0.1:99.99>i5,cax<3:1.3>io2,spx<97:-1.25>ioel/1/2/3,{8}2,1,2l[4:1],3cl[1:2],4k[.1:8],"
try:
    hexcom_file = open("hexcom.hard.txt","r",encoding="utf-8")
    inputstr = hexcom_file.read()
    print(f"Input string read from file is: {inputstr}")
except:
    print("could not read hex-com.hard.txt")

teststr =  inputstr.replace("\n","") #remove all \n

teststr_delleftbrac = re.sub("\[","<",teststr)#replace [] with <> since [] messes with regex
teststr_delbrac = re.sub("\]",">",teststr_delleftbrac)

syllist = teststr_delbrac.split(",") # use "," to determine the split
print (syllist)


cur = 0 #current position of processing
default_note_interval = 4  #4th-note interval is the default(Assume 4th-note if user forgot to set time signature
note_int = default_note_interval
cur_beat = start_beat

'''
[c|s|(1-6)] [opaPA][xyz] <數:數> [XX/XXX]
if first = c --> movecamera
        = s --> movestage
        = 1-6 movetrail
if (XXX) changestage XXX



full regex for stage movement syl : ^(([1-6]to)|(([1-6]t|s)((a|p|A|P)[xyz])))<(\d*\.)?\d+:(\d*\.)?\d+>...*$


'''
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
               }


lane_pos_dict = {'1':'rt','2':'rc','3':'rb','4':'lb','5':'lc','6':'lt'}
common_time_signatures = [128,96,64,48,32,24,16,12,8,6,4,3,2,1]

def error_message(num):
    print(f"error code: {num}")

def warn_syl_msg(reason):
    warn_syllabus.append("Beat "+ str(round(cur_beat,4))+": "+str(syllist[cur]) + " (reason: " + reason +")" )

def fail_syl_msg(reason):
    failed_syllabus.append("Beat "+ str(round(cur_beat,4))+": "+str(syllist[cur]))


def brac_num(XXX):
    num1 = str(re.findall("<(\d*\.)?\d+:",XXX).replace("<","").replace(":","").replace("[","").replace("]","").replace("\'",""))
    num2 = str(re.findall(":(\d*\.)?\d+>",XXX).replace(":","").replace(">","").replace("[","").replace("]","").replace("\'",""))
    return(num1,num2)

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
        print("not a valid simple note format")
        fail_syl_msg()

    note_pos = lane_pos_dict[str(re.findall("^[1-6]",temp)).replace("[","").replace("]","").replace("\'","")]
    final_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)}")



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
        note_pos = lane_pos_dict[str(re.findall("^[1-6]",temp)).replace("[","").replace("]","").replace("\'","")]
    except:
        print("no note_pos")
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
    elif re.findall("a[xyz]<",temp):
        attribute = "angle"
    elif re.findall("A[xyz]<",temp):
        attribute = "abs_angle"
    elif re.findall("p[xyz]<",temp):
        attribute = "position"        
    elif re.findall("P[xyz]<",temp):
        attribute = "abs_position"
    else:
        error_message(2)

    if re.findall("x<",temp):
        axis = "x"
    elif re.findall("y<",temp):
        axis = "y"
    elif re.findall("z<",temp):
        axis = "z"
    else:
        error_message(3)
    
    duration = float(str(re.findall("<\d*\.*\d+:",temp)).replace("<","").replace(":","").replace("[","").replace("]","").replace("\'",""))
    amount = float(str(re.findall(":-?\d*\.*\d+>",temp)).replace(":","").replace(">","").replace("[","").replace("]","").replace("\'",""))
    easing = easing_dict[str(re.findall(">.+$",temp)).replace(">","").replace("[","").replace("]","").replace("\'","")]


    if   re.match("^[1-6]to",temp):
        if amount > 1 or amount < 0:
            warn_syl_msg("opacity out of range")
        print (f"a changeopacity {change_object} {note_pos} {round(cur_beat,4)} {duration} {amount} {easing}")
        final_stage_output.append(f"a changeopacity {change_object} {note_pos} {round(cur_beat,4)} {duration} {amount} {easing}")
        #a changeopacity trail rt 195.3 4 0.5 Linear
        
    elif re.match("^[1-6]t[apAP]",temp):
        final_stage_output.append(f"a s_move{change_object} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        print (f"a s_move{change_object} {note_pos} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        
    elif re.match("^[sc][apAP][xyz]<",temp):
        final_stage_output.append(f"a s_move{change_object} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        print (f"a s_move{change_object} {attribute} {axis} {round(cur_beat,4)} {duration} {amount} {easing}")
        #a s_movetrail rt position z 195.3 4 0.5 Linear
        
    else:
        error_message(4)

        

    


def complex_note():
    
    temp = syllist[cur]
    print("temp is:")
    print(temp)
    note_type = ""
    data_format = ""
    num_1 = 0.0
    num_2 = 0.0
    num_3 = 0
    num_4 = 0.0
    if re.match("^[1-6](l)<\d+:\d+>$",temp): 
        note_type = "long"
        data_format = ":" 
        print("it is a long")
    elif re.match("^[1-6](l)<#(\d*\.)?\d+>$",temp):
        note_type = "long"
        data_format = "#"
        print("it is a long#")
    elif re.match("^[1-6](cl)<\d+:\d+>$",temp):
        note_type = "clong"
        data_format = ":" 
        print("it is a clong")
    elif re.match("^[1-6](cl)<#(\d*\.)?\d+>$",temp):
        note_type = "clong"
        data_format = "#" 
        print("it is a clong#")
    elif re.match("^[1-6](k)<(\d*\.)?\d+:\d+>$",temp):
        note_type = "compound"
        data_format = ":" 
        print("it is a compound")
    else:
        print("not a valid complex note format")
        fail_syl_msg("not a valid complex note format")
    print(temp)
  
    num_1 = str(re.findall("^[1-6]",temp)).replace("\'","").replace("[","").replace("]","")
    print ("num_1 = " + num_1)
    if data_format == ":":
        num_2 = str(re.findall("\d*\.*\d+:",temp)).replace(":","").replace("\'","").replace("[","").replace("]","")
        num_3 = str(re.findall(":\d+",temp)).replace(":","").replace("\'","").replace("[","").replace("]","")      
        print ("num_2 = " + num_2)
        print ("num_3 = " + num_3)
    elif data_format == "#":
        num_4 = str(re.findall("#.*>$",temp)).replace("#","").replace(">","").replace("\'","").replace("[","").replace("]","")  
        print ("num_4 = " + num_4)
        
    note_pos = lane_pos_dict[str(num_1).replace("[","").replace("]","").replace("\'","")]
 

    if note_type == "compound":
        final_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_2)),4)} {'%.0f' %float(num_3)}")
        print(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_2)),4)} {'%.0f' %int(num_3)}")
    elif data_format == ":":
        final_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat + 4 * float(num_3) / float(num_2)),4)}")
        print(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat + 4 * float(num_3) / float(num_2)),4)}")
    elif data_format == "#" :
        final_output.append(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_4)),4)}")
        print(f"n {note_type} {note_pos} {round(cur_beat,4)} {round((cur_beat+float(num_4)),4)}")
    

    
    
    ##START THE ACTUAL SYL DETECTION



while cur < len(syllist):

    print ("processing syllabus '" + syllist[cur]+"'")

    if re.match ("^E", syllist[cur]):
        cur_beat = 0.0
        syllist[cur] = syllist[cur].replace("E","")
    
    if re.findall("\((\d*\.)?\d+\)", syllist[cur]):
        print("found BPM")
        temp = syllist[cur]#copy the data out of syllist[cur] to not mess up the original data
        print(temp) 

        now_bpm_temp = str(re.findall("\((\d*\.)?\d+\)",temp)).replace("(","").replace(")","").replace("[","").replace("]","").replace("\'","")

        if re.findall("\((\d*\.)?\d+\)",temp):
            now_bpm_temp = (re.findall("\(\d+[.]*[\d+]*\)",temp))[0]
            print(f"BPM found is {now_bpm_temp}")
            temp_behind = temp.replace(now_bpm_temp,"")
            now_bpm = float(now_bpm_temp.replace("(","").replace(")",""))
            print(f"time signature have been changed to {now_bpm}")
            
    
        else:
            print("It is a BPM but could not recognise")
            fail_syl_msg("It is a BPM but could not recognise")


        try:        
            syllist[cur] = temp_behind
            print(f"temp behind is {temp_behind}")
        except:
            pass
    else:
        print("no BPM")
    



    
###check for time signature and get rid of it

    if re.findall("\)?{#(\d*\.)?\d+}", syllist[cur]) or re.findall("\)?{(\d*\.)?\d+}", syllist[cur]) :
        print("found time signature")
        temp = syllist[cur]#copy the data out of syllist[cur] to not mess up the original data
        print(temp) 

        if re.findall("{#(\d*\.)?\d+}",temp):
            time_sign_temp = (re.findall("{#\d+[.]*[\d+]*}",temp))[0]
            print(f"time signature found is {time_sign_temp}")
            temp_behind = temp.replace(time_sign_temp,"")
            note_int = 4 / float(time_sign_temp.replace("{","").replace("}","").replace("#",""))
            print(f"time signature have been changed to {note_int}")
            
        elif re.findall("{(\d*\.)?\d+}",temp):
            time_sign_temp = (re.findall("{\d+[.]*[\d+]*}",temp))[0]
            print(f"time signature found is {time_sign_temp}")
            temp_behind = temp.replace(time_sign_temp,"")
            note_int = float(time_sign_temp.replace("{","").replace("}",""))
            print(f"time signature have been changed to {note_int}")
        else:
            print("It is a time signature but could not recognise")
            fail_syl_msg("It is a time signature but could not recognise")


        if note_int not in common_time_signatures: #not working
            warn_syl_msg(f"{note_int} is not a common time signature")
        else:
            print("it IS a common time signature")
        try:        
            syllist[cur] = temp_behind
            print(f"temp behind is {temp_behind}")
        except:
            pass
    else:
        print("no time signature")

    ###

     
    ###check for both(/), give both_token and put the fisrt item into syllist[cur] to process
    both_token = len(re.findall("/", syllist[cur]))
    print (f"{both_token} both token")
    if both_token > 0:
        temp = syllist[cur]
   
        print(f"temp is {temp}")
        both_list = temp.split("/")
        print(both_list[0])
        syllist[cur] = str(both_list[0])
        
    else:
        pass
    while both_token > -1: #determine loop how many times base on (/)+1

        ##note type detection
        if re.match("^[1-6][coi]?$",syllist[cur]): #short/catch/long/clong are all processed here
            simple_note()
            print("simple")

        elif re.match("^[1-6](k|cl|l)<(\d*\.)?\d+:\d+>$",syllist[cur]) or re.match("^[1-6](cl|l)<#(\d*\.)?\d+>$",syllist[cur]):
            complex_note()
            print("complex")
            
        elif re.match("^(([1-6]to)|(([1-6]t|s|c)((a|p|A|P)[xyz])))<(\d*\.)?\d+:-?(\d*\.)?\d+>...*$",syllist[cur]):
            stage_action()
            print("stage_action found")                

        elif syllist[cur] =="":
            print("Empty Note")
            
        else:
            print("item unregonisable")
            fail_syl_msg("item unregonisable")

            
        #note detection ends
    

        both_token -= 1 #subtract 1 both_token for the while loop
        try:  #(try to) put the next item in the both_list onto the first slot
            del both_list[0]
            print(f"first element in both Deleted,both list now:{both_list}")
            syllist[cur] = str(both_list[0])
        except:
            print("both process ended/it is not a both")

        print("syllabus processing done")

                 
    cur = cur + 1  #current comma index
    cur_beat = cur_beat + (4/note_int) # move to the next beat number

        
print("whole process finished!!!")


print ("-"*50)
print ("Generated by Simai2HexaConverter V0.3")
print ("-"*50)
print("Warning:")
for x in warn_syllabus:
    print (x)
    
print ("-"*50)

print("Problems:")
for x in failed_syllabus:
    print (x)
    
print ("-"*50)

print("Final_output:")
for x in final_output:
    print (x)
    
print ("-"*50)

print("Stage:")
for x in final_stage_output:
    print (x)

print ("-"*50)
overwrite_choice = input("Do you want to overwrite lines in chart.hard.txt?(Y/N)")
if overwrite_choice == "Y":
    shutil.copy("chart.hard.txt","chart.hard_backup.txt")#make a copy of the oringinal file in case the programme fucked up something
    output_file = open("chart.hard.txt","r",encoding="utf-8")

    storage = []#store the needed lines

    for line in output_file.readlines():#find lines that are NOT start with a or n and put the line in storage[]
        if re.match("^[an] .+",line) or re.match("^-+",line) or re.match("^Generated by ",line): 
            print("Delete: " + line)
            storage.append("")
        else:
            print("Preserve: " + line)
            storage.append(line)

    output_file.close()   #reopen the file in write mode
    output_file = open("chart.hard.txt","w",encoding="utf-8")
        
    for line in storage:    #write all the lines saved in storage[]
        output_file.writelines(line)
    output_file.writelines("-"*50+"\n")
    output_file.writelines("Generated by simai2hexaconverter V0.3"+"\n")
    output_file.writelines("-"*50+"\n")
    for line in final_output:#write all the lines saved in final_output[]
        output_file.writelines(line+"\n")
    output_file.writelines("-"*50+"\n")
    for line in final_stage_output:#write all the lines saved in final_output[]
        output_file.writelines(line+"\n")    
    output_file.writelines("-"*50+"\n")  
    output_file.close()
elif overwrite_choice == "N":
    print("dontdothis")
else:
    print("whatareudoing")
    






