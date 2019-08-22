#!/bin/bash

#f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm  -lmkl_gf_lp64 -lmkl_lapack95_lp64 -lmkl_blas95_lp64  -lmkl_core -lmkl_sequential -lgfortran

#f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm -lmkl_core -lmkl_gf_lp64 -lmkl_sequential -lmkl_lapack95_lp64 -lmkl_blas95_lp64 -lgfortran


#f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm -lmkl_gf_lp64  -lmkl_intel_lp64 -lmkl_sequential -lmkl_core  -lgfortran


#f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm  -Wl,--start-group -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -Wl,--end-group -lpthread -Wl,--as-needed


#f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm  -L/home/wenz/Applications/anaconda2/lib  -lmkl_intel_lp64 -lmkl_sequential -lmkl_core  -lgfortran



#f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm  -L/home/wenz/Applications/anaconda2/lib  -lmkl_core -lmkl_intel_lp64 -lmkl_sequential -lgfortran


# it is strange that if we work on the conda enviroment, we do not need to specify lapack
# blas library any more. I assume that this will somehow be added automatically.
# still need to figure out how.
# It worked with scipy installed, without scipy (only mkl) it won't work.

#f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm  -lmkl_core -lmkl_intel_lp64 -lmkl_sequential -lgfortran
f2py -c geodesiclm.pyf -L../geodesicLM -lgeodesiclm  -lgfortran

