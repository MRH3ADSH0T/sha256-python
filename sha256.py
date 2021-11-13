# https://github.com/MRH3ADSH0T/sha256-python/
# 
from math import modf, sqrt # necessary imports

def rightR(a, b): # define right rotation function
    return (a>>b)|(a<<(32-b)) & 0xFFFFFFFF

def isP(a): # is "a" prime?
    for i in range(2,a):
        if a%i==0: return False
    else: return True

def bits(msg): # returns str of bits
    out=[]
    for i in msg:
        c=str(bin(ord(i)))[2:]
        out.append((c[::-1]+"0"*(8-len(c)))[::-1])
    return ''.join(i for i in out)

def sha(inp):

    h0,h1,h2,h3,h4,h5,h6,h7=int(modf(2**(1/2))[0]*(1<<32)),int(modf(3**(1/2))[0]*(1<<32)),int(modf(5**(1/2))[0]*(1<<32)), int(modf(7**(1/2))[0]*(1<<32)), int(modf(11**(1/2))[0]*(1<<32)), int(modf(13**(1/2))[0]*(1<<32)), int(modf(17**(1/2))[0]*(1<<32)), int(modf(19**(1/2))[0]*(1<<32))# fractional parts of the sqrts of the first 8 primes (2..19)

    primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]
    
    k=[int(modf(i**(1/3))[0]*(1<<32)) for i in primes] 
    
    msg=bits(inp) # convert from text to bits

    L=len(msg)
    msg+="1" # append a singe bit
    

    msg+=(447-L)*"0" # ensures len(msg) will be a multiple of 512 after preprocessing

    l=str(bin(L))[2:] # append original message length as a 64-bit number
    msg+=(l[::-1]+"0"*(64-len(l)))[::-1]

    chunks=[msg[i:i+512] for i in range(0, len(msg), 512)]

    for i in chunks: # process each chunk
        w=np.zeros((1,64)).tolist()[0] # initialize word list
        for j in range(16): # the next 2 "for" statements populate the word list
            w[j]=int(i[32*j:32*j+32],2)
        for j in range(16,64):
            s0,s1=rightR(int(w[j-15]),7)^rightR(int(w[j-15]),18)^(int(w[j-15])>>3),rightR(int(w[j-2]),17)^rightR(int(w[j-2]),19)^(int(w[j-2])>>10)
            w[j]=(int(w[j-16])+s0+int(w[j-7])+s1)%2**32

        a,b,c,d,e,f,g,h=h0,h1,h2,h3,h4,h5,h6,h7 # assign working variables for processing

        for j in range(64): # begin processing words and msg in 64 rounds

            s1,ch=rightR(e,6)^rightR(e,11)^rightR(e,25),(e&f)^((~e)&g) # s1 processes
            temp1=(h+s1+ch+k[j]+int(w[j]))#%2**32

            #s0=rightR(a,2)^rightR(a,13)^rightR(a,22) # s0 processes
            #maj=(a&b)^(a&c)^(b&c)
            temp2=((rightR(a,2)^rightR(a,13)^rightR(a,22))+((a&b)^(a&c)^(b&c)))%2**32

            h=g
            g=f
            f=e
            e=(d+temp1)%2**32
            d=c
            c=b
            b=a
            a=(temp1+temp2)%2**32

        h0,h1,h2,h3,h4,h5,h6,h7=h0+a,h1+b,h2+c,h3+d,h4+e,h5+f,h6+g,h7+h
        
    #a=[h0,h1,h2,h3,h4,h5,h6,h7]
    h=[str(hex(h0%2**32))[2:],str(hex(h1%2**32))[2:],str(hex(h2%2**32))[2:],str(hex(h3%2**32))[2:],str(hex(h4%2**32))[2:],str(hex(h5%2**32))[2:],str(hex(h6%2**32))[2:],str(hex(h7%2**32))[2:]]

    return ''.join((i[::-1]+"0"*(8-len(i)))[::-1] for i in h)
    
if __name__=="__main__":

    while True:
        text=input(">>> ")

        print(sha(text))
