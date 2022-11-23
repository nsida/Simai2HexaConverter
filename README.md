simai to hexa V0.1.0


語法:
基本上跟simai差不多,只是多了cl,l,i,o,k等的指令

{}是指音符間距
例如:
{4}指4分拍間距,每個逗號都是1拍子間距
{#4}是4拍子間距，每個逗號都是4拍子間距
{}裏的數字 = 4 / {#}裏的數字
所以{16}1,1,1,1,跟{#0.25}1,1,1,1, 一樣


以下是note/語法的種類:

這是軌道的編號,例如1就是rt,2是rc,一直到6是lt
   6 1
 5     2   <----這樣
   4 3

{}:拍子間距符號，這個括號裏的數字代表之後所有逗號(,)都是的拍子間距
單數字: 代表short，格式是軌道編號
c: 代表catch，格式是軌道編號+c
l: 代表long，格式是軌道編號+l[幾分拍:多少個]，或者是軌道編號+l[#長度]
cl: 代表clong，格式是軌道編號+cl[幾分拍:多少個]，或者是軌道編號+cl[#長度]
i: 代表swipe in，格式是軌道編號+i
o: 代表swipe out，格式是軌道編號+o
k: 代表compound，格式是軌道編號+k[長度(拍子):需要打擊次數]

例如:
6c:lt short
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


0.2.0

主要是縮減臃腫的代碼
現在clong,long[x:y]格式裏的xy只支援正整數,compound[x:y]格式裏x支援小數
現在會顯示有問題的note/字元跟該note/字元相應的拍子數

0.2.1
bug fix:


0.3
支援基本運鏡語法

目前支援語法:
1.changeopactity trail
2.movetrail
3.movestage
4.movecamera(未植入，是bug)

運鏡格式:
{[1-6號軌](如有)} {camera/stage/trail}{opactity/angle/position(大寫代表abs)}{xyz(如有)} [時間長度 : 移動幅度] {算式簡寫}

例如 1tPx[4:0.5]lin，就是一號軌道更變x軸"絕對位置",4拍時間移動到x=0.5(絕對位置),算式是linear
saz[32:-360]ios，就是舞臺(stage)更變角度，用32拍時間z軸旋轉-360°(相對),算式是easeInOutSine


以下是可接受的輸入:
ABCD[E:F]G:

A:軌道編號1-6 (如果後面是trail需要加上)
B:c/s/t (代表camera/stage/trail)
C:a/A/p/P/o (代表angle/abs_Angle/position/abs_Position/opacity)
D:x/y/z (xyz軸)
E:包括小數的任意正數 (運鏡時間拍子長度)
F:包括小數、負數的任意數字 (移動的幅度/角度/不透明度)
G:下列的算式簡稱:

	'算式簡稱':'算式'

               'lin':'Linear',
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

已知bug:
未支援movecamera
changeopacity未有限制0~1
movecamera/movestage 在output裏會多出一個空格
4個字母的運鏡算式簡稱未被正常讀取

預定改動:
bug fix
增加warning:如發現不正常的note，不影響output結果的情況下把note加到warning list(例如把opacity改到大於1)


