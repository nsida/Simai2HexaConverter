'''HexaStageTool




'''


import re #import regex module

final_output = []
final_stage_output = []
failed_syllabus = []
warn_syllabus = []


start_beat = float(input("Please input starting Beat or input nothing for 0 (Default is 0):") or 0)

iputstrbackup = "1/2/3,{8}2,1,2l[4:1],3cl[.1:2.9],4k[.1:8],E"
dummystr = "{16}1to<1:1>lin,3tAx<45:37>ios,5tPx<0.1:99.99>i5,cax<3:1.3>io2,spx<97:-1.25>ioel"
inputstr = input("Please input hex-com string (or input nothing for dummy_test_string):") or dummystr

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

def error_message(num):
    print(f"error code: {num}")

def fail_syl_msg():
    failed_syllabus.append("Beat "+str(cur_beat)+": "+str(syllist[cur]))

def stage_action():
    
    pass


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
    final_output.append(f"n {note_type} {note_pos} {cur_beat}")



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
        print (f"a changeopacity {change_object} {note_pos} {cur_beat} {duration} {amount} {easing}")
        final_stage_output.append(f"a changeopacity {change_object} {note_pos} {cur_beat} {duration} {amount} {easing}")
        #a changeopacity trail rt 195.3 4 0.5 Linear
        
    elif re.match("^[1-6]t[apAP]",temp):
        final_stage_output.append(f"a s_move{change_object} {attribute} {axis} {cur_beat} {duration} {amount} {easing}")
        print (f"a s_move{change_object} {note_pos} {attribute} {axis} {cur_beat} {duration} {amount} {easing}")
        
    elif re.match("^[sc][apAP][xyz]<",temp):
        final_stage_output.append(f"a s_move{change_object} {attribute} {axis} {cur_beat} {duration} {amount} {easing}")
        print (f"a s_move{change_object} {attribute} {axis} {cur_beat} {duration} {amount} {easing}")
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
        fail_syl_msg()
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
        final_output.append(f"n {note_type} {note_pos} {cur_beat} {cur_beat+float(num_2)} {float(num_3)}")
        print(f"n {note_type} {note_pos} {cur_beat} {cur_beat+float(num_2)} {int(num_3)}")
    elif data_format == ":":
        final_output.append(f"n {note_type} {note_pos} {cur_beat} {cur_beat + 4 * float(num_3) / float(num_2)}")
        print(f"n {note_type} {note_pos} {cur_beat} {cur_beat + 4 * float(num_3) / float(num_2)}")
    elif data_format == "#" :
        final_output.append(f"n {note_type} {note_pos} {cur_beat} {cur_beat+float(num_4)}")
        print(f"n {note_type} {note_pos} {cur_beat} {cur_beat+float(num_4)}")
    

    
    
    ##START THE ACTUAL SYL DETECTION



while cur < len(syllist):

    print ("processing syllabus '" + syllist[cur]+"'")


###check for time signature and get rid of it

    if re.findall("^{#(\d*\.)?\d+}", syllist[cur]) or re.findall("^{(\d*\.)?\d+}", syllist[cur]) :
        print("found time signature")
        temp = syllist[cur]#copy the data out of syllist[cur] to not mess up the original data
        print(temp) 

        if re.findall("^{#(\d*\.)?\d+}",temp):
            time_sign_temp = (re.findall("{#\d+[.]*[\d+]*}",temp))[0]
            print(f"time signature found is {time_sign_temp}")
            temp_behind = temp.replace(time_sign_temp,"")
            note_int = 4 / float(time_sign_temp.replace("{","").replace("}","").replace("#",""))
            print(f"time signature have been changed to {note_int}")
            
        elif re.findall("^{(\d*\.)?\d+}",temp):
            time_sign_temp = (re.findall("{\d+[.]*[\d+]*}",temp))[0]
            print(f"time signature found is {time_sign_temp}")
            temp_behind = temp.replace(time_sign_temp,"")
            note_int = float(time_sign_temp.replace("{","").replace("}",""))
            print(f"time signature have been changed to {note_int}")
        else:
            print("It is a time signature but could not recognise")
            fail_syl_msg()
            
        syllist[cur] = temp_behind
        print(f"temp behind is {temp_behind}")
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
            fail_syl_msg()

            
            
        #note detection ends
    

        both_token -= 1 #subtract 1 both_token for the while loop
        try:  #(try) to put the next item in the both_list onto the first slot
            del both_list[0]
            print(f"first element in both Deleted,both list now:{both_list}")
            syllist[cur] = str(both_list[0])
        except:
            print("both process ended/it is not a both")

        print("syllabus processing done")

                 
    cur = cur + 1  #current comma index
    cur_beat = cur_beat + (4/note_int) # move to the next beat number

        
print("whole process finished!!! generating hexa chart format...")

print ("-"*100+"\nHexa chart data:")


print("Problems:")
for x in failed_syllabus:
    print (x)
    
print ("-"*100)

for x in final_output:
    print (x)
    
print ("-"*100)

for x in final_stage_output:
    print (x)





