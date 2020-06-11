 # scorEpochs - Python version
This is the Python version of the tool

Developed on Python 3.6

## Usage
This tool can be used through the command line (do not be afraid to put spaces, they will be automatically managed) or by importing it

In the last case you have two possibility: 
 - Import the function from the module:
 
   <font color="orange">from</font> scorEpochs <font color="orange">import</font> scorEpochs 
   
   idx_best<font color="orange">,</font> epoch<font color="orange">,</font> scores = scorEpochs(cfg<font color="orange">,</font> data)
       
       
 - Import the module and use the function through the dot notation: 
 
    idx_best<font color="orange">,</font> epoch<font color="orange">,</font> scores = scorEpochs.scorEpochs(cfg<font color="orange">,</font> data)

## Required libraries
 - Numpy
 - Scipy
