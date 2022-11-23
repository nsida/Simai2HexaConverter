#simai2hexatool
#語法:
#基本上跟simai差不多,只是多了cl,l,i,o,k等的指令
#
#{}是指音符間距
#例如:
# {4}指4分拍子間距,每個逗號都是1拍子間距
#所以{16}1,1,1,1,就是指16分的縱連,每個逗號(,)是0.25拍間距

#以下是note/語法的種類
#單個數字代表tap,例如1就是rt,2是rc,一直到6是lt
#    6  1
# 5        2   <----這樣
#    4  3
#
#{}:拍子間距符號，這個括號裏的數字代表之後所有逗號(,)都是的拍子間距
#單數字: 代表short，格式是軌道編號
#+c: 代表catch，格式是軌道編號+c
#+l: 代表long，格式是軌道編號+l[幾分拍:多少個]
#cl: 代表clong，格式是軌道編號+cl[幾分拍:多少個]
#i: 代表swipe in，格式是軌道編號+i
#o: 代表swipe out，格式是軌道編+o號
#k: 代表compound，格式是軌道編號+k[長度:需要打擊次數]
#
#例如:
#6c:lt 
#1l[8]:rt (l)ong,長度8拍
#2cl[3]:rc (cl)ong,長度3拍
#5i:lc swipe (i)n
#4o:lb swipe (o)ut
#1k[8:32]:rt (k)ompound/compound,長度8拍,要打32下
#
#同拍子的音符可以這樣寫: 5i/3c  或是 1l[8]/4k[8:12]/3i (現在支援無限個音符同拍)
#
#
#舉個例Depersonalization的開頭就會寫成:
#{16}
#6,5c,4c,3c,2c,1c,6c,5c,4c/
#1,2c,3c,4c,5c,6c,1c,2c,3o/
#4o
#
#
import re #import regex module


final_output = [] 
one = 1

start_beat = float(input("Please input starting Beat (Default is 0):"))

iputstrbackup = "1/2/3,{8}2,1,2l[4:1],3cl[8:2],4k[8:8],E"
inputstr = "6,5c,4c,3c,2c,1c,6c,5c,4c/1,2c,3c,4c,5c,6c,1c,2c,3o/4o"
teststr =  inputstr.replace("\n","") #remove all \n

teststr_delleftbrac = re.sub("\[","<",teststr)
teststr_delbrac = re.sub("\]",">",teststr_delleftbrac)

syllist = teststr_delbrac.split(",") # use "," to determine the split
print (syllist)


cur = 0 #current position of processing
default_note_interval = 16  #4th-note interval is the default
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

        ##note format detection
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
            
        elif syllist[cur] == "":
            print("empty note")


        else:
            print("item unregonisable")
        #note detection ends
    

        both_token -= 1 #subtract 1 both_token for the while loop
        try:  #(try) to put the next item in the both_list onto the first slot
            del both_list[0]
            print(f"first element in both Deleted,both list now:{both_list}")
            syllist[cur] = str(both_list[0])
        except:
            print("both process ended/it is not a both")

        
       
        
              
    cur = cur + 1  #since seperate by "," , moving onto next item means 1comma have passed
    cur_beat = cur_beat + (4/note_int) # {}

        
print("whole process finished!!! generating hexa chart format...")

for x in final_output:
    print (x)


