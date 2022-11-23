import re #import regex module


final_output = [] 
one = 1

start_beat = float(input("Please input starting Beat (Default is 0):"))

inputstr = "1/2/3,{8}2,1,2l[4:1],3cl[8:2],4k[8:8],E"
teststr =  inputstr.replace("\n","") #remove all \n

teststr_delleftbrac = re.sub("\[","<",teststr)
teststr_delbrac = re.sub("\]",">",teststr_delleftbrac)

syllist = teststr_delbrac.split(",") # use "," to determine the split
print (syllist)


cur = 0 #current position of processing
default_note_interval = 4  #4th-note interval is the default
note_int = default_note_interval
cur_beat = start_beat

def long_note():
    temp = syllist[cur] #copy the data out of syllist[cur] to not mess up the original data
    list_pos   = str(re.findall("\dl<", temp)).replace("l<","") #remove the unneccesory detection char
    list_numer = str(re.findall("<\d:", temp)).replace("<","").replace(":","") #remove the unneccesory detection char
    list_denom = str(re.findall(":\d>", temp)).replace(":","").replace(">","") #remove the unneccesory detection char
       
    pos = int(list_pos[2]) #convert the "list" back to number
    numer = int(list_numer[2]) #convert the "list" back to number
    denom = int(list_denom[2]) #convert the "list" back to number
    end_beat = cur_beat + (denom/ numer *4 )
    if   pos == 1:
        note_pos = "rt"
    elif pos == 2:
        note_pos = "rc"
    elif pos == 3:
        note_pos = "rb"
    elif pos == 4:
        note_pos = "lb"
    elif pos == 5:
        note_pos = "lc"
    elif pos == 6:
        note_pos = "lt"
    else:
        print("note_pos not valid")
        
    #finding all 3 numbers
    print (f"Hold at {pos}th lane,length is {denom} {numer}-th notes, end at {end_beat}")
    print ("n long " + note_pos + " " + str(cur_beat) + " " +str(end_beat))
    final_output.append("n long " + note_pos + " " + str(cur_beat) + " " +str(end_beat))
    
def clong_note():
    temp = syllist[cur] #copy the data out of syllist[cur] to not mess up the original data
    list_pos   = str(re.findall("\dcl<", temp)).replace("l<","") #remove the unneccesory detection char
    list_numer = str(re.findall("<\d:", temp)).replace("<","").replace(":","") #remove the unneccesory detection char
    list_denom = str(re.findall(":\d>", temp)).replace(":","").replace(">","") #remove the unneccesory detection char
       
    pos = int(list_pos[2]) #convert the "list" back to number
    numer = int(list_numer[2]) #convert the "list" back to number
    denom = int(list_denom[2]) #convert the "list" back to number
    end_beat = cur_beat + (denom/ numer *4 )
    if   pos == 1:
        note_pos = "rt"
    elif pos == 2:
        note_pos = "rc"
    elif pos == 3:
        note_pos = "rb"
    elif pos == 4:
        note_pos = "lb"
    elif pos == 5:
        note_pos = "lc"
    elif pos == 6:
        note_pos = "lt"
    else:
        print("note_pos not valid")
        
    #finding all 3 numbers
    print (f"Catch-Hold at {pos}th lane,length is {denom} {numer}-th notes, end at {end_beat}")
    print ("n clong " + note_pos + " " + str(cur_beat) + " " +str(end_beat))
    final_output.append("n clong " + note_pos + " " + str(cur_beat) + " " +str(end_beat))
    
def compound_note():
    temp = syllist[cur] #copy the data out of syllist[cur] to not mess up the original data
    list_pos   = str(re.findall("\dk<", temp)).replace("l<","") #remove the unneccesory detection char
    list_numer = str(re.findall("<\d:", temp)).replace("<","").replace(":","") #remove the unneccesory detection char
    list_denom = str(re.findall(":\d>", temp)).replace(":","").replace(">","") #remove the unneccesory detection char
       
    pos = int(list_pos[2]) #convert the "list" back to number
    numer = int(list_numer[2]) #convert the "list" back to number
    denom = int(list_denom[2]) #convert the "list" back to number
    end_beat = cur_beat + (denom/ numer *4 )
    if   pos == 1:
        note_pos = "rt"
    elif pos == 2:
        note_pos = "rc"
    elif pos == 3:
        note_pos = "rb"
    elif pos == 4:
        note_pos = "lb"
    elif pos == 5:
        note_pos = "lc"
    elif pos == 6:
        note_pos = "lt"
    else:
        print("note_pos not valid")
        
    #finding all 3 numbers
    print (f"Compound at {pos}th lane,length is {denom} {numer}-th notes, end at {end_beat}")
    print ("n compound " + note_pos + " " + str(cur_beat) + " " +str(end_beat))
    final_output.append("n compound " + note_pos + " " + str(cur_beat) + " " +str(end_beat))



##START THE ACTUAL SYL DETECTION



while cur < len(syllist):
    print ("processing syllabus '" + syllist[cur]+"'")


###check for time signature and get rid of it 
    if len(re.findall("{\d}", syllist[cur])) != 0:
        print("found time signature")
        temp = syllist[cur]#copy the data out of syllist[cur] to not mess up the original data
        print(temp) 
        time_sign_temp = (re.findall("{\d}",temp))[0]
        
        temp_behind = temp.translate({ord(i): None for i in time_sign_temp})
        print(f"temp behind is {temp_behind}")
        print(f"time signature found is {time_sign_temp}")
        syllist[cur] = temp_behind

        note_int = int(time_sign_temp.replace("{","").replace("}",""))
        print(f"time signature have been changed to {note_int}")
        
    else:
        print("no time signature")
###

###check for both(/)
    both_token = len(re.findall("/", syllist[cur]))
    print (f"{both_token} both token")
    if both_token > 0:
        temp = syllist[cur]
   
        print(f"temp is {temp}")
        both_list = temp.split("/")#later change to 
        print(both_list[0])
        syllist[cur] = str(both_list[0])
        
    

        
    else:
        pass
#FLAG1
    
        
    if syllist[cur] == "1":
        print(f"n short rt {cur_beat}")
        final_output.append(f"n short rt {cur_beat}")
              
    elif syllist[cur] == "2":
        print(f"n short rc {cur_beat}")
        final_output.append(f"n short rc {cur_beat}")
        
    elif syllist[cur] == "3":
        print(f"n short rb {cur_beat}")
        final_output.append(f"n short rb {cur_beat}")
        
    elif syllist[cur] == "4":
        print(f"n short lb {cur_beat}")
        final_output.append(f"n short lb {cur_beat}")    
                     
    elif syllist[cur] == "5":
        print(f"n short lc {cur_beat}")
        final_output.append(f"n short lc {cur_beat}")    
              
    elif syllist[cur] == "6":
        print(f"n short lt {cur_beat}")
        final_output.append(f"n short lt {cur_beat}")

    elif syllist[cur] == "1c":
        print(f"n catch rt {cur_beat}")
        final_output.append(f"n catch rt {cur_beat}")
              
    elif syllist[cur] == "2c":
        print(f"n catch rc {cur_beat}")
        final_output.append(f"n catch rc {cur_beat}")
        
    elif syllist[cur] == "3c":
        print(f"n catch rb {cur_beat}")
        final_output.append(f"n catch rb {cur_beat}")
        
    elif syllist[cur] == "4c":
        print(f"n catch lb {cur_beat}")
        final_output.append(f"n catch lb {cur_beat}")    
                     
    elif syllist[cur] == "5c":
        print(f"n catch lc {cur_beat}")
        final_output.append(f"n catch lc {cur_beat}")    
              
    elif syllist[cur] == "6c":
        print(f"n catch lt {cur_beat}")
        final_output.append(f"n catch lt {cur_beat}")
        
    elif syllist[cur] == "1i":
        print(f"n swipe in rt {cur_beat}")
        final_output.append(f"n swipe in rt {cur_beat}")
              
    elif syllist[cur] == "2i":
        print(f"n swipe in rc {cur_beat}")
        final_output.append(f"n swipe in rc {cur_beat}")
        
    elif syllist[cur] == "3i":
        print(f"n swipe in rb {cur_beat}")
        final_output.append(f"n swipe in rb {cur_beat}")
        
    elif syllist[cur] == "4i":
        print(f"n swipe in lb {cur_beat}")
        final_output.append(f"n swipe in lb {cur_beat}")    
                     
    elif syllist[cur] == "5i":
        print(f"n swipe in lc {cur_beat}")
        final_output.append(f"n swipe in lc {cur_beat}")    
              
    elif syllist[cur] == "6i":
        print(f"n swipe in lt {cur_beat}")
        final_output.append(f"n swipe in lt {cur_beat}")

    elif syllist[cur] == "1o":
        print(f"n swipe out rt {cur_beat}")
        final_output.append(f"n swipe out rt {cur_beat}")
              
    elif syllist[cur] == "2o":
        print(f"n swipe out rc {cur_beat}")
        final_output.append(f"n swipe out rc {cur_beat}")
        
    elif syllist[cur] == "3o":
        print(f"n swipe out rb {cur_beat}")
        final_output.append(f"n swipe out rb {cur_beat}")
        
    elif syllist[cur] == "4o":
        print(f"n swipe out lb {cur_beat}")
        final_output.append(f"n swipe out lb {cur_beat}")    
                     
    elif syllist[cur] == "5o":
        print(f"n swipe out lc {cur_beat}")
        final_output.append(f"n swipe out lc {cur_beat}")    
              
    elif syllist[cur] == "6o":
        print(f"n swipe out lt {cur_beat}")
        final_output.append(f"n swipe out lt {cur_beat}")
        
       
    elif len(re.findall("\dl<\d:\d>", syllist[cur])) != 0:
        print("long found")
        long_note()
              
    elif len(re.findall("\dcl<\d:\d>", syllist[cur])) != 0:
        print("clong found")
        clong_note()

    elif len(re.findall("\dk<\d:\d>", syllist[cur])) != 0:
        print("compound found")
        compound_note()



    else:
        print("item unregonisable")

    
    if both_token > 0:
        both_token -= 1
        del both_list[0]
        print(f"first element in both Deleted,both list now:{both_list}")
        syllist[cur] = str(both_list[0])

         #jump to FLAG1
    else:
        break
        
       
        
              
    cur = cur + 1
    cur_beat = cur_beat + (4/note_int)
print("process finished")

for x in final_output:
    print (x)


