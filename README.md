# geodesicLM

The repo contains the geodesic Levenberg-Marquardt minimization algorithm 
developed by [Mark Transtrum](https://www.physics.byu.edu/faculty/transtrum/) 
and [James Sethna](http://sethna.lassp.cornell.edu) et al. 
The Fortran source code comes from the [geodesicLM](https://sourceforge.net/projects/geodesiclm/) 
SourceForce repo.  

## Installation

### package managers

```
$ pip install geodesicLM
```

### from source

Get the source
```
$ git clone https://github.com/mjwen/geodesicLM.git
```
and then install by
```
$ pip install -e ./geodesicLM
```

## Example

This Python interface follows [Scipy least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html).
See [examply_python.py](https://github.com/mjwen/geodesicLM/blob/master/examples/example_python.py)
for an example. 

For more information, see [docs](https://github.com/mjwen/geodesicLM/tree/master/docs). 
