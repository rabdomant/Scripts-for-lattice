#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import sys
import os.path


def print_array(id,corrfile):
    arraysize=np.fromfile(corrfile,dtype="<i", count=1)
    arrayelem=np.fromfile(corrfile,dtype="<i", count=arraysize[0])
    arraytype=np.fromfile(corrfile,dtype="<i", count=1)
    datasize=(np.prod(arrayelem))
    bunchsize=arrayelem[-1]

    if args.v:
        print( "# Number of indexes=", arraysize )
        print( "# Indexes range=", arrayelem )
        print( "# Array type=",arraytype )

    lexyindex=0
    while(lexyindex<datasize/bunchsize):
        if(arraytype[0]==8):
            databunch=np.fromfile(corrfile,dtype="<f8", count=bunchsize)
            databunch*=-rew(numconf)/1024
        else:
            databunch=np.fromfile(corrfile,dtype="<i", count=bunchsize)
            databunch*=rew(numconf)
        index=lexyindex
        print(id,end=" ")
        for i in range(0,arraysize[0]-1):
            print(index % arrayelem[i],end=" ")
            index=index//arrayelem[i]
        np.savetxt(sys.stdout, databunch,newline=" ")
        print()
        lexyindex+=1
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True,
                    help='measure file (ps1)')
    parser.add_argument('-w', type=str, required=False,
                    help='combine with reweighting factors file (rw1)')
    parser.add_argument('-v', required=False,
                    help='print to file the header info', action="store_true")
    
    args = parser.parse_args()
    inputmeasfilename=args.i
    rewffilename=args.w

if(not(os.path.isfile(inputmeasfilename))):
        sys.stderr.write("Cannot find the measure file (ps1)\n")
        sys.exit()


if(rewffilename):
    if(os.path.isfile(rewffilename)):
        rw={}
        with open(rewffilename) as rewfile:
            for line in rewfile:
                if not line.startswith('#'):
                    ldata=line.split()
                    rw[int(ldata[0])]=float(ldata[-1])
    else:
        sys.stderr.write("Cannot find the reweighting factors file (rw1)\n")
        sys.exit()

def rew(i):
    try:
        if i in rw.keys():
            return rw[i]
    except NameError:
        return 1.0
    else:
        sys.stderr.write("Missing the reweighting factor for conf number "+str(i)+" \n")
        sys.exit()
 
#print(rw)


with open(inputmeasfilename) as corrfile:
    x = np.fromfile(corrfile,dtype="<i", count=6)

   
    #source type
    mtype=x[0]

    #number of flavours
    nf=x[1]

    #number of source points
    nx=x[2]

    #T max
    tmax=x[3]

    #Max flow time
    ntm=x[4]

    #number of sources
    nsrc=x[5]
        
    if(mtype==0):
        nsrc=1

    if args.v:
        print(f"# Source type {mtype}")
        print(f"# Number of flavours {nf}")
        print(f"# Number of source points {nx}")
        print(f"# T max {tmax}")
        print(f"# Max flow time {ntm}")
        print(f"# Number of sources {nsrc}")
    
    if(nx!=0):
        mx = np.fromfile(corrfile,dtype="<i", count=4*nx).reshape(nx,4)
        if args.v:
            print( "# Sources locations: ")
            for i in range(nx):
                print("#\t",mx[i])
    if(ntm!=0):
        tm = np.fromfile(corrfile,dtype="<f8", count=ntm)
        if args.v:
            print( "# Flow times:",tm)


    while True:
        numconf = np.fromfile(corrfile,dtype="<i", count=1)
        if len(numconf) == 0 :
            break
        numconf=numconf[0]
        if args.v:
            print( "# conf id ",numconf , type(numconf))

        print("# PP ")
        print_array(numconf,corrfile)
        print("# PA ")
        print_array(numconf,corrfile)

        if(ntm>0):
            print("# flow ")
            print_array(numconf,corrfile)




            


            
