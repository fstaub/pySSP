from operator import mul
import itertools
import numpy
import argparse
import importlib
import os
import subprocess
import sys
import time
import shutil
import random

def replace_blocks_by_name(in_string,all_blocks):
    out_string=in_string
    for i in all_blocks:
        out_string = out_string.replace(i,"numblocks['"+i+"']")
    return out_string    
    
def generateBlock(inblock,all_blocks):
 global steps
 global stepvar
 temp=dict()
 for x in range(0,len(inblock)):
  if 'value' in inblock[x][1]:
   if isinstance(inblock[x][1]['value'],str):
     temp[inblock[x][0]]=replace_blocks_by_name(inblock[x][1]['value'],all_blocks)
   else:    
     temp[inblock[x][0]]=inblock[x][1]['value']
  else: 
   if 'steps' in inblock[x][1]:   
       temp[inblock[x][0]]=str(inblock[x][1]['min']) +"+(step["+str(stepvar)+"])*"+str((inblock[x][1]['max']-inblock[x][1]['min'])/(inblock[x][1]['steps']-1))
       steps.append(inblock[x][1]['steps'])
       stepvar+=1
   else:
       temp[inblock[x][0]]=str(inblock[x][1]['min']) +"+(step["+str(stepvar)+"])*"+str((inblock[x][1]['max']-inblock[x][1]['min']))
       stepvar+=1
 return temp 

def writeblock(name,lhfile):
    clist = numblocks[name]
    lhfile.write("Block "+name.upper()+" # \n")
    for key in clist:
     if isinstance(clist[key],str): 
         if isinstance(eval(clist[key]),str):     
            lhfile.write(' %s %10.4e # \n' % (key, 1.*eval(eval(clist[key]))))
         else:
            lhfile.write(' %s %10.4e # \n' % (key, 1.*eval(clist[key])))
     else:
         lhfile.write(' %s %10.4e # \n' % (key, 1.*clist[key]))


def run_spheno(settings,out_file):
   if os.path.exists(settings["SPheno_output"]):
      os.remove(settings["SPheno_output"]) 
   subprocess.call(settings["SPheno_binary"],shell=True,stdout=std_out,stderr=std_err)

def write_lh_file(blocks,name):
        lh=open(name,"w+")   
        for y in range(0,len(blocks)):  
           writeblock(blocks[y],lh)
        lh.close 

def parse_hb_results(spc_file):
    for line in open(os.path.join(temp_dir,"HiggsBounds_results.dat")):
      li=line.strip()
      if not li.startswith("#"):
        hb_res=filter(None,line.rstrip().split(' '))
        
    subprocess.call("echo \"Block HIGGSBOUNDS # \" >> "+spc_file,shell=True,stdout=std_out,stderr=std_err)      
    for i in range(1,len(hb_res)):
        subprocess.call("echo \""+str(i)+" "+str(hb_res[i])+" # \" >> "+spc_file,shell=True,stdout=std_out,stderr=std_err)  
          
        
def run_higgsbounds(settings,out_file):
     subprocess.call(settings["HiggsBounds_call"]+" "+temp_dir+"/",shell=True,stdout=std_out,stderr=std_err)
     parse_hb_results(out_file)
     
def run_higgssignals(settings,out_file):
#     print "HS" 
    i=1

def run_micromegas(settings,out_file):
    i=1
    
def run_point(settings,out_file):  
    run_spheno(settings,out_file)
    if os.path.exists(settings["SPheno_output"]):
        if settings["include_HiggsBounds"]==True:
            run_higgsbounds(settings,settings["SPheno_output"])
        if settings["include_HiggsSignals"]==True:
            run_higgssignals(settings,settings["SPheno_output"]) 
        if settings["include_MicrOmegas"]==True:
            run_micromegas(settings,settings["SPheno_output"])             
        subprocess.call("cat "+settings["SPheno_output"]+" >> "+out_file,shell=True,stdout=std_out,stderr=std_err)
        subprocess.call("echo \"ENDOFPARAMETERPOINT\" >> "+out_file,shell=True,stdout=std_out,stderr=std_err)

def runscan(filename):
    settings=locals()
    scan_info=locals()
    execfile("Input/"+filename,scan_info)
    execfile("ModelsSettings/"+scan_info["settings_file"],settings)    

    for i in range(0,len(scan_info["blocks"])):
        numblocks[scan_info["blocks"][i]]=generateBlock(eval(scan_info["blocks"][i]),scan_info["blocks"])

    if scan_info["scan_type"]=="Grid":
      all_i = []
      for y in range(0,len(steps)):
        all_i.append(range(0,steps[y]))
      alist=list(itertools.product(*all_i))
    elif scan_info["scan_type"]=="Random":
      steps.append(scan_info['scan_points'])
    
    out_dir=os.path.join(cwd,"Output",scan_info["scan"])
    if scan_info["append_points"]==False and os.path.exists(out_dir):
         shutil.rmtree(out_dir)
    
    os.makedirs(out_dir)
    out_file=os.path.join(out_dir,"SpectrumFiles.spc")
    os.chdir(temp_dir)   
    print "Scan:                   "+str(scan_info["scan"])
    print "Total number of points: "+str(reduce(mul, steps, 1))
    for x in range(0,reduce(mul, steps, 1)):
        output_stream = sys.stdout
        output_stream.write('Current point: %s\r' % (x+1))
        output_stream.flush()
        if scan_info["scan_type"]=="Grid":        
         for y in range(0,stepvar):
           step[y]=alist[x][y]
        if scan_info["scan_type"]=="Random":        
         for y in range(0,stepvar):
           step[y]=random.random()   
        write_lh_file(scan_info["blocks"],settings["SPheno_input"])   
        run_point(settings,out_file)
    print "All done!"
    os.chdir(cwd)

        
print "---------------------------------"        
print " running pySSP                   "
print "---------------------------------"

steps=[]
stepvar=0
step={}
numblocks={};
cwd = os.getcwd()    

print random.random()
       
parser = argparse.ArgumentParser(description='Please give the name of the input file.')
parser.add_argument('inputfile', metavar='File', type=str, nargs='+', help='an integer for the accumulator')
args = parser.parse_args()

timestamp= str(time.time()).replace(".","")
temp_dir=os.path.join(cwd,"Temp",timestamp)
os.makedirs(temp_dir)

std_out= open(os.path.join(cwd,"Temp","stdout.txt"),"wb")
std_err= open(os.path.join(cwd,"Temp","stderr.txt"),"wb")

for i in args.inputfile:
    runscan(i)
    
std_out.close()
std_err.close()