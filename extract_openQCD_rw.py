#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import sys
import os.path


def print_array(id,n,corrfile):
    arraysize=np.fromfile(corrfile,dtype="<i", count=1)
    arrayelem=np.fromfile(corrfile,dtype="<i", count=arraysize[0])
    arraytype=np.fromfile(corrfile,dtype="<i", count=1)
    datasize=(np.prod(arrayelem)*n)
    bunchsize=arrayelem[-1]

    if args.v:
        print("arraysize ", arraysize  )
        print("arrayelem ", arrayelem  )
        print("arraytype ", arraytype  )

    print("Here",datasize,bunchsize)
        
    lexyindex=0
    while(lexyindex<datasize/bunchsize):
  #      if(arraytype[0]==8):
  #          databunch=np.fromfile(corrfile,dtype="<f8", count=bunchsize)
  #      else:
  #          databunch=np.fromfile(corrfile,dtype="<i", count=bunchsize)
        index=lexyindex

        databunch=np.fromfile(corrfile,dtype="<f8", count=bunchsize)
        print(databunch)
        print(id,end=" ")
        for i in range(0,arraysize[0]-1):
            print(index % arrayelem[i],end=" ")
            index=index//arrayelem[i]
        #np.savetxt(sys.stdout, databunch,newline=" ")
        print()
        lexyindex+=1
    print("out")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True,
                    help='measure file (ps1)')
    parser.add_argument('-w', type=str, required=False,
                    help='reweighting factors file (rw1)')
    parser.add_argument('-v', required=False,
                    help='print to file the header info', action="store_true")
    
    args = parser.parse_args()
    inputmeasfilename=args.i
    rewffilename=args.w

if(not(os.path.isfile(inputmeasfilename))):
        sys.stderr.write("Cannot find the measure file (ps1)\n")
        sys.exit()


with open(inputmeasfilename) as corrfile:
    numrew = np.fromfile(corrfile,dtype="<i", count=1)[0]//2
    nfct=np.fromfile(corrfile,dtype="<i", count=numrew)
    nsrc=np.fromfile(corrfile,dtype="<i", count=numrew)
    print( "# num rew  ",numrew)
    print( "# nfct  ",nfct )
    print( "# nsrc  ",nsrc )

    
    while True:
        numconf = np.fromfile(corrfile,dtype="<i", count=1)
        
        if len(numconf) == 0 :
            break
        numconf=numconf[0]
        if args.v:
            print( "# conf id ",numconf )

        print("# Square norm of the source field number ")
        print_array(numconf,24,corrfile)
        print("# The logarithm, -ln(r), of the associated stochastic estimate")
        print_array(numconf,72,corrfile)
        sys.exit()

        



            


            
