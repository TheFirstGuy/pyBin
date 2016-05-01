hexMap = { '0' : "0000", '1' : "0001", '2' : "0010", '3' : "0011", '4' : "0100",
           '5' : "0101", '6' : "0110", '7' : "0111", '8' : "1000", '9' : "1001",
           'A' : "1010", 'B' : "1011" , 'C' : "1100", 'D' : "1101", 'E' : "1110",
           'F' : "1111", '.' : "."}

binMap = {  "0000" : '0', "0001" : '1' , "0010" : '2' , "0011" : '3', "0100" : '4',
            "0101" : '5', "0110" : '6', "0111" : '7' ,  "1000" : '8', "1001" : '9',
            "1010" : 'A', "1011" : 'B', "1100" : 'C',  "1101" : 'D' ,  "1110" : 'E',
           "1111" : 'F', '.' : "."}

def binToDec( bNum ):
    isNeg = False
    if(bNum[0] == '1'):
        isNeg = True
        bNum = twoComp(bNum)
    cnt = 0
    power = bNum.index('.') - 2
    isDec = False
    for i in range(1, len(bNum)):
        #print(cnt)
        if(bNum[i] == '.'):
            isDec = True
            power = 0
        elif( isDec == False ):
            cnt += (2**power) * int(bNum[i])
            power -= 1
        elif( isDec ):
            power += 1
            cnt += (1/(2**power))*int(bNum[i])
    if(isNeg):
        return -1 * cnt
    else:
        return cnt

def twoComp( bNum ):
    i = len(bNum) - 1
    bNum = list(bNum)
    flip = False
    while( i >= 0 ):
        if(bNum[i] == '.'):
            i -= 1
            continue
        if(flip):
            if(bNum[i] == '1'):
                bNum[i] = '0'
            elif(bNum[i] == '0'):
                bNum[i] = '1'
        else:
            if(bNum[i] == '1'):
                flip = True
        i -= 1
    s = ""
    for i in bNum:
         s+= i
    return s
        

def hexToBin( hNum ):
    s = ""
    for i in range(0, len(hNum)):
        s += hexMap[hNum[i]]
    return s


def hexToDec( hNum ):
    return binToDec(hexToBin(hNum))
	
def fixedAdd(left, right):
    i = len(left) - 1
    carry = 0
    s = ""
    while(i >= 0):
        if(left[i] == '.'):
            s = '.' + s
            i -= 1
            continue
        t = int(left[i]) + int(right[i]) + carry
        if(t == 0 or t == 2):
            s = '0' + s  
        else:
            s = '1' + s
        if(t == 3 or t == 2):
            carry = 1
        else:
            carry = 0
        i -= 1
    return s, carry

def add(left, right):
    '''
    Adds two binary (no fixed point) numbers together.
    '''
    left, right = pad(left, right)
    s, carry = fixedAdd(left,right)
    if(carry == 1):
        s = str(carry) + s
    return s
    

def pad(left, right):
    '''
    Pads two binary numbers so they are of the same size
    '''
    lessBit = ""
    moreBit = ""
    if(len(left) < len(right)):
        lessBit = left
        moreBit = right
    else:
        lessBit = right
        moreBit = left
    pad = len(moreBit) - len(lessBit)
    for i in range(0, pad):
        lessBit = '0' + lessBit
    return lessBit, moreBit
    

def mult(left, right):
    '''
    Multiplies two binary numbers of variable length
    '''
    decimal = None
    #Strip left and right of decimal and keep track of
    #decimal place
    if('.' in left):
        decimal = len(left) - 1 - left.index('.')
        left = left.split('.')
        left = left[0] + left[1]
    if('.' in right):
        if( decimal != None ):
            decimal += len(right) - 1 - right.index('.')
        else:
            decimal = len(right) - 1 - right.index('.')
        right = right.split('.')
        right = right[0] + right[1]
    i, x = len(left) - 1, 0
    result = ""
    #Multiply
    while( i >= 0 ):
        s = ""
        if( left[i] == '0'):
            i -= 1
        else:
            for j in range(0, x):# pad decimal places
                s += '0'
            s = right + s
            result = add(result,s)
            i -= 1
        x += 1
    #Insert decimal place
    s = result[0:len(result) - decimal]
    print(decimal)
    s += '.'
    s += result[len(result) - decimal:]
    return s

def binToHex(num):
    '''
    Converts binary number to hex
    '''
    decimal = None
    if '.' in num:
        decimal = num.index('.')
    index = len(num) - 1
    left , right = "", num
    if(decimal != None ):
        left = num[0:decimal]
        t = len(left) % 4
        if( t != 0):
            for i in range(0, 4 - t):
                left = '0' + left
        right = num[decimal + 1:]
        t = len(right) % 4
        if( t != 0):
            for i in range(0, 4 - t):
                right += '0'
    else:
        t = len(right) % 4
        for i in range(0, 4 - t):
            right = '0' + right
    b, e = 0, 4
    rl, rr = "" , ""
    while( b < len(left)):
        rl += binMap[left[b:e]]
        b = e
        e += 4
    b, e = 0, 4
    while( b < len(right)):
        rr += binMap[right[b:e]]
        b = e
        e += 4
    if(decimal == None):
        return rl + rr
    return rl + '.' + rr    
        
                
def hexMult( left, right ):
    '''
    Takes to hex numbers and multiplies them.
    Returns hex number
    '''
    r = mult(hexToBin(left), hexToBin(right))
    return binToHex(r)

def hexMult20(left, right):
    '''
    Takes two 20 bit fixed point hex numbers and returns
    a 20 bit hex number
    '''
    r = mult(hexToBin(left), hexToBin(right))
    decimal = r.index('.')
    print(r)
    r = r[0] + r[decimal - 3: decimal + 17]
    return binToHex(r)
    

'''def add( left, right, bits = 20 ):
    num1 = hexToDec(left)
    num2 = hexToDec(right)
    res = num1 + num2
    return decToBin( res, bits)
'''
def decToBin( num , bits = 20):
    decimal = int(num)
    fraction = num - decimal
    if(num < 0):
        decimal *= -1
        fraction *= -1
    s = ""
    cnt = 0
    while( decimal > 0 ):
        s = str(decimal%2) + s
        decimal = decimal//2
        cnt += 1
        
    s += "."
    while(fraction != 0 and cnt < bits):
        fraction *= 2
        print(fraction)
        if( fraction > 1):
                s += '1'
                fraction -= 1
        else:
            s += '0'
        cnt += 1
    if( num < 0 ):
        s = twoComp( s )
    return s

            
        
        
'''def binToHex( bNum ):
    decimal = bNum.index('.')
    index = decimal + 1
    s = ""
    while(index + 4 =< len(bNum)):
        sub = bNum[index:index+4]
'''      
        
def addh( left, right):
    num1 = hexToDec(left)
    num2 = hexToDec(right)
    res = num1 + num2
    return decToBin( res, bits)
    
