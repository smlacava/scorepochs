 # scorEpochs - Python version
This is the Python version of the tool

Developed on Python 3.6

## Usage
This tool can be used through the command line (do not be afraid to put spaces, they will be automatically managed) or by importing it

In the last case you have two possibility: 
 - Import the function from the module:
 
  ```python
    from scorEpochs import scorEpochs 
    idx_best, epoch, scores = scorEpochs(cfg, data)
  ```
       
       
 - Import the module and use the function through the dot notation: 
 
  ```python
    idx_best, epoch, scores = scorEpochs(cfg, data)
  ```
  
## Required libraries
 - Numpy
 - Scipy
