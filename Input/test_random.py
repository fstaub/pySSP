settings_file="MSSM.py"
scans=["FirstTryRandom", "SecondTryRandom"]
scan_type="Random"
scan_points=2

append_points= False
include_HiggsBounds= True
include_HiggsSignals= True
include_MicrOmegas= False
check_saving=True

def condition_to_save(spc):
    if (spc.blocks['MINPAR'][1]<1000.):
        return(True)
    else:
        return(False)

blocks=['MODSEL','SMINPUTS','MINPAR','SPhenoInput']    
BLOCK=helper.init_blocks(blocks,scans)

BLOCK['ALL']['MODSEL']=[
    ['1',{'value': 1}],
    ['2',{'value': 1}],  
    ['6',{'value': 1}]
    ]

BLOCK['ALL']['SMINPUTS']=[
 ['2', {'value': 1.166370E-05}],    
 ['3', {'value': 1.187000E-01}],    
 ['4', {'value': 9.118870E+01}],    
 ['5', {'value': 4.180000E+00}],    
 ['6', {'value': 1.735000E+02}],    
 ['7', {'value': 1.776690E+00}] ]   

BLOCK['FirstTryRandom']['MINPAR']=[
    ['1',{'min':200., 'max':2000., 'distribution': "LINEAR"}],
    ['2',{'value':"MINPAR['1']"}],    
#    ['2',{'value':500.}],    
    ['3',{'min':5.,'max':50., 'distribution': "LINEAR"}],     
    ['4',{'value': 1.}],
    ['5',{'value': 0.}]        
    ]

BLOCK['SecondTryRandom']['MINPAR']=BLOCK['FirstTryRandom']['MINPAR']

BLOCK['ALL']['SPhenoInput']=[
['  1',{'value': -1          }],
['  2',{'value':  0          }],
['  7',{'value':  0          }],
['  8',{'value':  3          }],
['  9',{'value':  1          }],
[' 10',{'value':  0          }],
[' 11',{'value': 1           }],
[' 13',{'value': 0           }],
[' 14',{'value': 0           }],
[' 12',{'value': 1.000E-04   }],
[' 15',{'value': 1.000E-30   }],
[' 16',{'value': 0           }],
[' 19',{'value': -2          }],
[' 31',{'value': -1          }],
[' 32',{'value': 0           }],
[' 34',{'value': 1.000E-04   }],
[' 35',{'value': 40          }],
[' 36',{'value': 5           }],
[' 37',{'value': 1           }],
[' 38',{'value': 2           }],
[' 50',{'value': 1           }], 
[' 51',{'value': 0           }],
[' 52',{'value': 0           }],
[' 55',{'value': 0           }],
[' 57',{'value': 0           }],
[' 65',{'value': 1           }],
[' 66',{'value': 1           }],
[' 67',{'value': 1           }],
[' 75',{'value': 1           }],
[' 76',{'value': 1           }],
[' 77',{'value': 0           }],
[' 78',{'value': 0           }],
[' 79',{'value': 1           }],
[' 86',{'value': 0.          }],
['510',{'value': 0.          }],
['515',{'value': 0           }],
['520',{'value': 1.          }], 
['521',{'value': 1.          }],
['525',{'value': 0.          }],
['530',{'value': 1.          }],
['550',{'value': 0.          }]]




yu=[
    ['2 2',{'value': "yu['1 1']"}],
    ['1 1',{'min': 0., 'max':1., 'steps':3}],  
    ['3 3',{'value': "yu['1 1']"}]
    ]


