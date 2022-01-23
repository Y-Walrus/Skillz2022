

def fibbo(x,y,z,c):
    if(c==0):
        c=c+1
        fibbo(x,y,z,c)
    elif(c==1):
        c=c+1
        fibbo(x,y,z,c)
    elif(c<z):
        p=x
        x=y
        y=y+p
        c=c+1
        fibbo(x,y,z,c)


fibbo(0,1,10,0)
    
    
        
