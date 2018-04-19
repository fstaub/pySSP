def init_blocks(blocks,scans):
      BLOCK={}
      BLOCK['ALL']={}
      for j in range(0,len(scans)):
          BLOCK[scans[j]]={}
      return(BLOCK)
  
  
print "loaded"  