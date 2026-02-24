"""
Z(n): r[n]=0
S(n):r[n]=r[n]+1
T(m,n): r[n]=r[m]
J(m,n,q): if r[n]=r[m] go to instruction q, else go to next instruction
"""
import re

def runURM(listofinstr,reg):
    """
    This method receives as parameter a list of instructions (which
    correspond to a given URM program) and some initialization of the
    registers (reg is a list of numbers). The method should simulate
    the behaviour of the URM program with those initial values of the
    registers.
    """
    i=0
    while i<len(listofinstr):
        line = listofinstr[i]
        i+=1
        if line[0]=='Z':
            reg[line[1]-1]=0
        elif line[0]=='S':
            reg[line[1]-1]+=1
        elif line[0]=='T':
            reg[line[2]-1]=reg[line[1]-1]
        elif line[0]=='J' and reg[line[1]-1]==reg[line[2]-1]:
            i=line[3]-1
    return reg[0]    

def readURM(filename):
    """
    This method reads line by line the entries in the file who's name
    is given as a parameter, and returns a pair in which the first element
    is a list of lists, and the second one is a number that represents
    the highest index of the registers used in the URM program. Each list
    in listofinstr corresponds to a line in the input file, and it simply
    separates each instruction into its components. For example, 2.J(2,3,5)
    becomes ['J',2,3,5].
    """  
    listofinstr=[]
    regmax=0
    for line in open(filename):
        if len(line):
            s1=r'[Jj]\([1-9][0-9]*,[1-9][0-9]*,[1-9][0-9]*'
            s2=r'[Tt]\([1-9][0-9]*,[1-9][0-9]*'            
            s3=r'[Ss]\([1-9][0-9]*'
            s4=r'[Zz]\([1-9][0-9]*'
            searchLine = r'[1-9][0-9]*\.\s?('+s1+r'|'+s2+r'|'+s3+r'|'+s4+r')\)'
            m = re.search(searchLine,line)
            if m:
                instr=m.group(0).replace('.',',').replace('(',',').replace(')','').split(',')[1:]
                instr=[instr[0].strip().upper()]+[int(i) for i in instr[1:]]
                listofinstr.append(instr)
                ma=max(instr[1:3])
                if ma>regmax:
                    regmax=ma
            else:
                print(("The file does not have the correct format: "+line))
                return [],0

        else:
            print("The file has empty lines")
            return [],0
    return listofinstr,regmax  


import sys


##Para comprobar el nivel de cumplimiento de los objetivos de la practica se puede usar el comando
##    python URM.py funcion.txt 5 5
##donde funcion.txt es uno de los dos ficheros que se tienen que entregar.
##Si la funcion tiene solo una variable, el comando es
##    python URM.py funcion.txt 5

if __name__ == "__main__":
    if len(sys.argv)>=2:
        filenameURM=sys.argv[1]
        narg=len(sys.argv)
        rango1=int(sys.argv[2]) if narg>=3 else 1
        rango2=int(sys.argv[3]) if narg>=4 else 1
    else:
        filenameURM="P2n5m.txt"
        rango1=5
        rango2=5
    listofinstr,regmax = readURM(filenameURM)
    if len(listofinstr)>0:
        listofreg=[[i,j]+[0]*(regmax-2) for i in range(rango1) for j in range(rango2)] 
        for reg in listofreg:
            print(("Initial configuration of registers: "+" ".join([str(i) for i in reg])))
            result=runURM(listofinstr,reg)
            print(("Output: %s"%result))




