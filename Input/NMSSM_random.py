settings_file="NMSSM.py"
scans=["CheckUniNMSSM1", "CheckUniNMSSM2"]
scan_type="Random"
scan_points=5000000

append_points= False
include_HiggsBounds= False
include_HiggsSignals= False
include_MicrOmegas= False
check_saving=True

def condition_to_save(spc):
    if (spc.blocks['MINPAR'][1]<1000.):
        return(True)
    else:
        return(False)

blocks=['MODSEL','SMINPUTS','MINPAR','SPhenoInput','EXTPAR','MSD2IN','MSE2IN','MSL2IN','MSOFTIN','MSQ2IN','MSU2IN','TDIN','TEIN','TUIN']    
BLOCK=helper.init_blocks(blocks,scans)

BLOCK['ALL']['MODSEL']=[
    ['1',{'value': 0}],
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

BLOCK['ALL']['MINPAR']=[
    ['3',{'min':1.05,'max':50., 'distribution': "LOG"}]
    ]

BLOCK['ALL']['EXTPAR']=[
    ['61',{'min':-2.,'max':2., 'distribution': "LINEAR"}],
    ['62',{'min':-2.,'max':2., 'distribution': "LINEAR"}],
    ['63',{'min':-5000.,'max':5000., 'distribution': "LINEAR"}],
    ['64',{'min':-5000.,'max':5000., 'distribution': "LINEAR"}],        
    ['65',{'min': 200.,'max':5000., 'distribution': "LINEAR"}]    
    ]

BLOCK['ALL']['MSOFT']=[
    ['1',{'min':100.,'max':1500., 'distribution': "LINEAR"}],
    ['2',{'min':150.,'max':1500., 'distribution': "LINEAR"}],
    ['3',{'min':1500.,'max':3000., 'distribution': "LINEAR"}]  
    ]


BLOCK['ALL']['MSE2IN']=[
    ['1 1',{'value': 1.0E+06}],
    ['2 2',{'value': 1.0E+06}],  
    ['3 3',{'value': 1.0E+06}]
    ]

BLOCK['ALL']['MSELIN']=[
    ['1 1',{'value': 1.0E+06}],
    ['2 2',{'value': 1.0E+06}],  
    ['3 3',{'value': 1.0E+06}]
    ]

BLOCK['ALL']['MSD2IN']=[
    ['1 1',{'value': 4.0E+06}],
    ['2 2',{'value': 4.0E+06}],  
    ['3 3',{'value': 4.0E+06}]
    ]

BLOCK['ALL']['MSQ2IN']=[
    ['1 1',{'value': 4.0E+06}],
    ['2 2',{'value': 4.0E+06}],  
    ['3 3',{'min': 4.00E+04., 'max':9.00E+06, 'distribution': "LINEAR"}]
    ]

BLOCK['ALL']['MSQUIN']=[
    ['1 1',{'value': 4.0E+06}],
    ['2 2',{'value': 4.0E+06}],  
    ['3 3',{'min': 4.00E+04., 'max':9.00E+06, 'distribution': "LINEAR"}]
    ]


BLOCK['ALL']['TDIN']=[
    ['1 1',{'value': 0}],
    ['2 2',{'value': 0}],  
    ['3 3',{'value': 0}]
    ]

BLOCK['ALL']['TEIN']=[
    ['1 1',{'value': 0}],
    ['2 2',{'value': 0}],  
    ['3 3',{'value': 0}]
    ]

BLOCK['ALL']['TUIN']=[
    ['1 1',{'value': 0}],
    ['2 2',{'value': 0}],  
    ['3 3',{'min': -2500., 'max':2500., 'distribution': "LINEAR"}]
    ]

BLOCK['ALL']['SPhenoInput']=[
['  1',{'value': -1          }],
['  2',{'value':  0          }],
['  7',{'value':  0          }],
['  8',{'value':  3          }],
['  9',{'value':  1          }],
[' 10',{'value':  0          }],
[' 11',{'value': 0           }],
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





