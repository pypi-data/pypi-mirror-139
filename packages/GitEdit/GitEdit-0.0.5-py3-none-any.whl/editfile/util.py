import os

from sympy import frac
def plist(m=0,data=[]):
    for i in data:
        if type(i) is list:
           plist(m+1,i)    
        else:
           print( " "*10*m +i) 
          
def plist(m=0,data=[]):
    for i in data:
        if type(i) is list:
           plist(m+1,i)    
        else:
            print( " "*10*m +i) 
    pass


out = ""
tileColor = "green"
textColor = "black"

def toMarkDown(file,data,m=0):
   global out
   global tileColor
   global textColor 
   d1 = '<details style="color:{color};">'.format(color=tileColor)
   d2 = '</details>'
   s1 = '<summary style="color:{color};">'.format(color=tileColor)
   s2 = '</summary>'
   u1 = '<ul>'
   u2 = '</ul>'
   l1 = '<li>'
   l2 = '</li>'
   sp1 = '<span style="color:{color};">'.format(color=textColor)
   sp2 = '</span>'
  

   for i in data:

       if type(i) is list:           
           #print(out)
           out += "key"
           out = out.replace(d2+"key",u1)
           #print("--====")          
           toMarkDown(file,i,m+1)           
           out += d2+u2
       else:
           
           out += d1+s1+sp1+i+sp2+s2+d2           
           #file.write(str(m)+d1+s1+i+s2+d2)  
           #print(i)
           pass
        
   pass


#plist(data = topic )


print(os.getcwd())

def createMDfile(filename):

    path = os.getcwd()
    
    dir = filename.split("/")
    if len(dir) == 1:
     path = os.path.join(path,filename)
     file = open(filename,"+w")
     file.write('')
     return file
    else:
     dir = "\\".join(dir[:-1])
     if not os.path.exists(dir):
      mode = 0o666
      try:
       os.makedirs(dir,mode) 
      except:
       pass
     #print(out)
     path = os.path.join(path,filename)
     file = open(filename,"+w")
     file.write('')
     return file
    

def createContent(file="",expandColor="green",color="black",data=[]):
  global tileColor 
  global textColor

  tileColor = expandColor 
  textColor = color
  
  if file != "":
   file = createMDfile(file)
   toMarkDown(file,data)
   file.write(out)
   file.close()
   print("==Completed Successfully==")
  else:
   print(out)  


def m(val):
    return '<img src="https://render.githubusercontent.com/render/math?math={val}">'.format(val=val)






