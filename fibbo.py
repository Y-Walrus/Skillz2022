

def fibbo(x,y,z,c):
    if(c==0):
        c=c+1
        fibbo(x,y,z,c)
        print(x)
    elif(c==1):
        c=c+1
        print(y)
        fibbo(x,y,z,c)
    elif(c<z):
        print(x+y)
        p=x
        x=y
        y=y+p
        c=c+1
        fibbo(x,y,z,c)


fibbo(0,1,10,0)
    
    
        
