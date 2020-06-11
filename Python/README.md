 # scorEpochs - Python version
This is the Python version of the tool

Developed on Python 3.6

## Usage
This tool can be used through the command line (do not be afraid to put spaces, they will be automatically managed) or by importing it

In the last case you have two possibility: 
 - Import the function from the module:
 
   <div class="text-orange mb-2">from</div> scorEpochs <div class="text-orange mb-2">import</div> scorEpochs 
   
   idx_best<div class="text-orange mb-2">,</div> epoch<div class="text-orange mb-2">,</div> scores = scorEpochs(cfg<div class="text-orange mb-2">,</div> data)
       
       
 - Import the module and use the function through the dot notation: 
 
    idx_best<div class="text-orange mb-2">,</div> epoch<div class="text-orange mb-2">,</div> scores = scorEpochs.scorEpochs(cfg<div class="text-orange mb-2">,</div> data)

## Required libraries
 - Numpy
 - Scipy
