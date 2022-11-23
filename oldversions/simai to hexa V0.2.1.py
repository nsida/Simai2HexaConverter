'''simai2hexatool
語法:
基本上跟simai差不多,只是多了cl,l,i,o,k等的指令

{}是指音符間距
例如:
 {4}指4分拍子間距,每個逗號都是1拍子間距
所以{16}1,1,1,1,就是指16分的縱連,每個逗號(,)是0.25拍間距

以下是note/語法的種類:


這是軌道的編號,例如1就是rt,2是rc,一直到6是lt
    6  1
 5        2   <----這樣
    4  3

{}:拍子間距符號，這個括號裏的數字代表之後所有逗號(,)都是的拍子間距
單數字: 代表short，格式是軌道編號
+c: 代表catch，格式是軌道編號+c
+l: 代表long，格式是軌道編號+l[幾分拍:多少個]，或者是軌道編號+l[幾分拍]
cl: 代表clong，格式是軌道編號+cl[幾分拍:多少個]，或者是軌道編號+cl[#長度]
i: 代表swipe in，格式是軌道編號+i
o: 代表swipe out，格式是軌道編+o號
k: 代表compound，格式是軌道編號+k[長度:需要打擊次數]

例如:
6c:lt
1l[8]:rt (l)ong,長度8拍
2cl[3]:rc (cl)ong,長度3拍
5i:lc swipe (i)n
4o:lb swipe (o)ut
1k[8:32]:rt (k)ompound/compound,長度8拍,要打32下

同拍子的音符可以這樣寫: 5i/3c  或是 1l[8]/4k[8:12]/3i (現在支援無限個音符同拍)


舉個例Depersonalization的開頭就會寫成:
{16}
6,5c,4c,3c,2c,1c,6c,5c,4c/
1,2c,3c,4c,5c,6c,1c,2c,3o/
4o

todo:reduce/cleanup code

Change log:
縮短了def long/clong/compound()


^{[+-]?(\d*\.)?\d+}$  :  regex for {15.5}
^{#[+-]?(\d*\.)?\d+}$   :   regex for {#15.5}
^[1-6](k|cl|l)<(\d*\.)?\d+:(\d*\.)?\d+>$  :regex for 6l[7.5:90.5]

'''



import re #import regex module

final_output = []
failed_syllabus = [] 
one = 1

start_beat = float(input("Please input starting Beat or input nothing for 0 (Default is 0):") or 0)

iputstrbackup = "1/2/3,{8}2,1,2l[4:1],3cl[.1:2.9],4k[.1:8],E"
dummystr = "{16}6,5c,4c,3c,2c,1c,6c,5c,4c/1,2c,3c,4c,5c,6c,1c,2c,3o/4oi"
inputstr = input("Please input hex-com string (or input nothing for dummy_test_string):") or dummystr

teststr =  inputstr.replace("\n","") #remove all \n

teststr_delleftbrac = re.sub("\[","<",teststr)
teststr_delbrac = re.sub("\]",">",teststr_delleftbrac)

syllist = teststr_delbrac.split(",") # use "," to determine the split
print (syllist)


cur = 0 #current position of processing
default_note_interval = 4  #4th-note interval is the default
note_int = default_note_interval
cur_beat = start_beat




lane_pos_dict = {'1':'rt','2':'rc','3':'rb','4':'lb','5':'lc','6':'lt'}

def fail_syl_msg():
    failed_syllabus.append("Beat "+str(cur_beat)+": "+str(syllist[cur]))

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

    note_pos = lane_pos_dict[str(re.findall("[1-6]",temp)).replace("[","").replace("]","").replace("\'","")]
    final_output.append(f"n {note_type} {note_pos} {cur_beat}")



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

for x in final_output:
    print (x)
print ("-"*100)
print("Problems:")
for x in failed_syllabus:
    print (x)
print ("-"*100)



