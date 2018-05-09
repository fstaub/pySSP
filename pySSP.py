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
import math
import pyslha
import time
import datetime
import multiprocessing as mp

def replace_blocks_by_name(in_string,all_blocks):
    out_string=in_string
    for i in all_blocks:
        out_string = out_string.replace(i,"numblocks['"+i+"']")
    return out_string    
    
def generateBlock(inblock,all_blocks,stepvar,steps):
 temp=dict()
 for x in range(0,len(inblock)):
  if 'value' in inblock[x][1]:
   if isinstance(inblock[x][1]['value'],str):
     temp[inblock[x][0]]=replace_blocks_by_name(inblock[x][1]['value'],all_blocks)
   else:    
     temp[inblock[x][0]]=inblock[x][1]['value']
  else: 
   if 'steps' in inblock[x][1]:
       if inblock[x][1]['distribution']=="LINEAR":
          temp[inblock[x][0]]=str(inblock[x][1]['min']) +"+(step["+str(stepvar)+"])*"+str((inblock[x][1]['max']-inblock[x][1]['min'])/(inblock[x][1]['steps']-1))
       elif inblock[x][1]['distribution']=="LOG":
          temp[inblock[x][0]]="math.exp("+str(math.log(inblock[x][1]['min'])) +"+(step["+str(stepvar)+"])*"+str((math.log(inblock[x][1]['max'])-math.log(inblock[x][1]['min']))/(inblock[x][1]['steps']-1))+")"
       else:
          print "Unknown distribution!" 
       steps.append(inblock[x][1]['steps'])
       stepvar+=1
   else:
       if inblock[x][1]['distribution']=="LINEAR":
          temp[inblock[x][0]]=str(inblock[x][1]['min']) +"+(step["+str(stepvar)+"])*"+str((inblock[x][1]['max']-inblock[x][1]['min']))
       elif inblock[x][1]['distribution']=="LOG":
          temp[inblock[x][0]]="math.exp("+str(math.log(inblock[x][1]['min'])) +"+(step["+str(stepvar)+"])*"+str((math.log(inblock[x][1]['max'])-math.log(inblock[x][1]['min'])))+")"
       else:
          print "Unknown distribution!"   
       stepvar+=1
 
 return temp, stepvar

def writeblock(name,lhfile,step):
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

def write_lh_file(blocks,name,step):
        lh=open(name,"w+")   
        for y in range(0,len(blocks)):  
           writeblock(blocks[y],lh,step)
        lh.close 

def parse_hb_results(spc_file,core):
    for line in open(os.path.join(temp_dir,str("id"+core),"HiggsBounds_results.dat")):
      li=line.strip()
      if not li.startswith("#"):
        hb_res=filter(None,line.rstrip().split(' '))
        
    subprocess.call("echo \"Block HIGGSBOUNDS # \" >> "+spc_file,shell=True,stdout=std_out,stderr=std_err)      
    for i in range(1,len(hb_res)):
        subprocess.call("echo \""+str(i)+" "+str(hb_res[i])+" # \" >> "+spc_file,shell=True,stdout=std_out,stderr=std_err) 
        
def parse_hs_results(spc_file,core):
    for line in open(os.path.join(temp_dir,"id"+core,"HiggsSignals_results.dat")):
      li=line.strip()
      if not li.startswith("#"):
        hs_res=filter(None,line.rstrip().split(' '))
        
    subprocess.call("echo \"Block HIGGSSIGNALS # \" >> "+spc_file,shell=True,stdout=std_out,stderr=std_err)      
    for i in range(1,len(hs_res)):
        subprocess.call("echo \""+str(i)+" "+str(hs_res[i])+" # \" >> "+spc_file,shell=True,stdout=std_out,stderr=std_err)          
          
        
def run_higgsbounds(settings,out_file,core):
     subprocess.call(settings["HiggsBounds_call"]+" "+temp_dir+"/id"+core+"/",shell=True,stdout=std_out,stderr=std_err)
     parse_hb_results(out_file,core)
     
def run_higgssignals(settings,out_file,core):
     subprocess.call(settings["HiggsSignals_call"]+" "+temp_dir+"/id"+core+"/",shell=True,stdout=std_out,stderr=std_err)
     parse_hs_results(out_file,core)

def run_micromegas(settings,out_file,core):
    shutil.copyfile(settings["SPheno_output"],os.path.join(settings["Micromegas_directory"][int(core)],settings["Micromegas_input"]))
    os.chdir(settings["Micromegas_directory"][int(core)])
    subprocess.call("./"+settings["Micromegas_binary"],shell=True,stdout=std_out,stderr=std_err)
    if os.path.exists(settings["Micromegas_output"]):
        subprocess.call("echo \"Block DARKMATTER # \" >> "+os.path.join(temp_dir,"id"+core,out_file),shell=True,stdout=std_out,stderr=std_err)
        subprocess.call("cat "+settings["Micromegas_output"]+" >> "+os.path.join(temp_dir,"id"+core,out_file),shell=True,stdout=std_out,stderr=std_err)
    os.chdir(temp_dir+"/id"+core) 
    
def run_point(settings,out_file,core):  
    run_spheno(settings,out_file)
    if os.path.exists(settings["SPheno_output"]):
        spc = pyslha.read(settings["SPheno_output"])
        if 'include_HiggsBounds' in settings:
         if settings["include_HiggsBounds"]==True:
            run_higgsbounds(settings,settings["SPheno_output"],core)
        if 'include_HiggsSignals' in settings:    
         if settings["include_HiggsSignals"]==True:
            run_higgssignals(settings,settings["SPheno_output"],core) 
        if 'include_MicrOmegas' in settings:    
         if settings["include_MicrOmegas"]==True and spc.blocks['LSP'][1]==settings["Micromegas_candidate"]:
            run_micromegas(settings,settings["SPheno_output"],core)
        if 'check_saving' in settings:    
         if settings["check_saving"]==True:
            save_point=settings["condition_to_save"](spc)
         else:
            save_point=True
        else:
            save_point=True    
            
        if save_point==True:    
          subprocess.call("cat "+settings["SPheno_output"]+" >> "+out_file,shell=True,stdout=std_out,stderr=std_err)
          subprocess.call("echo \"ENDOFPARAMETERPOINT\" >> "+out_file,shell=True,stdout=std_out,stderr=std_err)
          

def run_file(filename,ct,total):
    print "Reading file: ",filename
    settings=locals()
    scan_info=locals()
    execfile("Input/"+filename,scan_info)
    execfile("ModelsSettings/"+scan_info["settings_file"],settings)    
   
    scan_info["BLOCK"]['Current']={}
    
    st=1
    for i in scan_info['scans']:
        run_scan(i,scan_info,settings,st,len(scan_info["scans"]))
        st+=1
        
       
def run_points(scan_info,settings,steps,stepvar,step,out_file,crange,alist,core):
    if os.path.exists("id"+core):
         shutil.rmtree("id"+core)
    os.makedirs("id"+core)
    os.chdir("id"+core)
    global nr_steps
    for x in crange: #range(0,reduce(mul, steps, 1)):
        if core=="0":
          output_stream = sys.stdout
          output_stream.write('Finished:                  %.2f%%\r' % (100.*(x)/crange[-1]))
          output_stream.flush()
        if scan_info["scan_type"]=="Grid":        
         for y in range(0,stepvar):
           step[y]=alist[x][y]
        if scan_info["scan_type"]=="Random":        
         for y in range(0,stepvar):
           step[y]=random.random()   
        write_lh_file(scan_info["blocks"],settings["SPheno_input"],step)   
        run_point(settings,out_file,core)
        
def run_scan(scan,scan_info,settings,ct,total): 
    steps=[]
    stepvar=0
    step={}
    for i in scan_info["blocks"]:
        if i in scan_info["BLOCK"][scan]:
           scan_info["BLOCK"]['Current'][i]=scan_info["BLOCK"][scan][i]
        else:   
           scan_info["BLOCK"]['Current'][i]=scan_info["BLOCK"]['ALL'][i] 
        numblocks[i], stepvar=generateBlock(scan_info["BLOCK"]['Current'][i],scan_info["blocks"],stepvar,steps)
    if scan_info["scan_type"]=="Grid":
      all_i = []
      for y in range(0,len(steps)):
        all_i.append(range(0,steps[y]))
      alist=list(itertools.product(*all_i))
    elif scan_info["scan_type"]=="Random":
      steps.append(scan_info['scan_points'])
    
    out_dir=os.path.join(cwd,"Output",scan)
    if scan_info["append_points"]==False and os.path.exists(out_dir):
         shutil.rmtree(out_dir)
    
    os.makedirs(out_dir)
    out_file=os.path.join(out_dir,"SpectrumFiles.spc")
    os.chdir(temp_dir)   
    print "-------------------------------------------------------------------"    
    print "Scan ("+str(ct)+"/"+str(total)+"):                "+str(scan)
    print "-------------------------------------------------------------------"  
    start_time=time.time()
    print "Started:                   "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d, %H:%M:%S'))
    print "Type:                      "+str(scan_info["scan_type"])
    print "Run HiggsBounds:           "+str(scan_info["include_HiggsBounds"])
    print "Run HiggsSignals:          "+str(scan_info["include_HiggsSignals"])
    print "Run Micromegas:            "+str(scan_info["include_MicrOmegas"])        
    print "Total number of points:    "+str(reduce(mul, steps, 1))
    
    total=reduce(mul, steps, 1)/scan_info["use_cores"]
    
    nr_steps=1
    processes = [mp.Process(target=run_points, args=(scan_info,settings,steps,stepvar,step,out_file+str(x),range(x*total,(x+1)*total),alist,str(x))) for x in range(scan_info["use_cores"])]
    
    for p in processes:
       p.start()
       
    for p in processes:
       p.join()
    
    #run_points(scan_info,settings,steps,stepvar,step,out_file+str(1),range(0,reduce(mul, steps, 1)),alist,str(1))
    
    print "All done!                             "
    print "Time Needed:               "+str(time.time()-start_time)+"s"
    os.chdir(cwd)

        

print "               _____ _____ _____  "
print "              / ____/ ____|  __ \ "
print "  _ __  _   _| (___| (___ | |__) |"
print " | '_ \| | | |\___ \\___ \|  ___/ "
print " | |_) | |_| |____) |___) | |     "
print " | .__/ \__, |_____/_____/|_|     "
print " | |     __/ |                    "
print " |_|    |___/                     "
                                         

cwd = os.getcwd()    

     
parser = argparse.ArgumentParser(description='Please give the name of the input file.')
parser.add_argument('inputfile', metavar='File', type=str, nargs='+', help='an integer for the accumulator')
args = parser.parse_args()

timestamp= str(time.time()).replace(".","")
temp_dir=os.path.join(cwd,"Temp",timestamp)
os.makedirs(temp_dir)

std_out= open(os.path.join(cwd,"Temp","stdout.txt"),"wb")
std_err= open(os.path.join(cwd,"Temp","stderr.txt"),"wb")

global n_steps
n_steps=1

ct=1
for i in args.inputfile:
#    steps=[]
#    stepvar=0
#    step={}
    numblocks={}
    run_file(i,ct,len(args.inputfile))
    ct+=1 
std_out.close()
std_err.close()






# To-Do
# - Fit?
# - MCMC?