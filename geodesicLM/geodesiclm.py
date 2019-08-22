import numpy
from . import _geodesiclm


def geodesiclm(func, x0, **kwargs):
    """
    Arguments for leastsq:
    (note the only required arguments are func and x0, all others will be set to a default value)

    func -- a routine for calculting the residuals
    func_args -- a tuple of arguments to pass to func

    x0 -- the initial parameter guess (passed as a numpy array)

    jacobian -- a routine for calculating the jacobian matrix.  If not passed, a finite difference estimate is used.
    jacobian_args -- a tuple of arguments to pass to jacobian
    h1 -- controls the step size for calculating a finite difference estimate of the jacobian

    Avv -- a routine for calculating the directional second derivative
    Avv_args -- a tuple of arguments to pass to Avv.  Avv will be called as Avv(x,v,*Avv_args) where x is the parameter guess and v is the direction to calculate the second derivative
    h2 -- controls the step size for calculating a finite difference estimate of the directional second derivative

    eps -- a number estimating the accuracy to which the function is evaluated

    maxiters -- a list of integers [maxiter, maxfev, maxjev, maxaev] (the maximum number of allowed iterations, function evaluations, jacobian evaluations, and acceleration evaluations)

    tols -- a list of floats controlling stopping criteria: [artol, Cmin, gtol, xtol, xrtol, ftol, frtol, maxlam]
       artol = cosine of the angle between the unfit residuals and the range of the jacobian -- typically set to ~.01
       Cmin = stop when the cost is less than this value
       gtol = stop when the gradient is less than this value
       xtol = stop when the step size becomes smaller than this value
       xrtol = stop when the relative change in each parameter is less than this value
       ftol = stop when the cost decreases by less than this value for 3 consecutive iterations
       frtol = stop when the relative decrease in the cost is less than this value for 3 consecutive iterations
       maxlam = stop when the damping term is larger than maxlam
       minlam = stop when the damping term is smaller than minlam for 3 consective steps

    print_level -- an integer indicating how much information to print, ranges from 0 to 5 (higher number prints mor details).  Typically only needed for debugging

    method_flags -- a list of integers controlling details of the algorithm (imethod, iaccel, ibold, ibroyden).  See documentation in geodesiclm code for details about these parameters

    method_params -- a list of floats controlling details of the algorithm (factor_initial, factor_accept, factor_reject, avmax).  See documentation in geodesiclm code for details.

    callback -- a callback function to be called after each iteration

    m -- an integer specifying the number of residuals
    """

    ## Check for kwargs

    ## func_args
    if 'func_args' in kwargs:
        func_extra_args = kwargs['func_args']
    elif 'args' in kwargs:
        func_extra_args = kwargs['args']
    else:
        func_extra_args = ()

    ## jacobian, h1, jacobian_extra_args
    if 'jacobian' in kwargs:
        jacobian = kwargs['jacobian']
        h1 = -1.0
        if 'jacobian_args' in kwargs:
            jacobian_extra_args = kwargs['jacobian_args']
        elif 'args' in kwargs:
            jacobian_extra_args = kwargs['args']
        else:
            jacobian_extra_args = ()
        analytic_jac = True
    else:
        jacobian = jacobian_dummy
        jacobian_extra_args = ()
        if 'h1' in kwargs:
            h1 = kwargs['h1']
        else:
            h1 = 1.49012e-08
        analytic_jac = False

    ## Avv, h2, Avv_args
    if 'Avv' in kwargs:
        Avv = kwargs['Avv']
        h2 = -1.0
        if 'Avv_args' in kwargs:
            Avv_extra_args = kwargs['Avv_args']
        elif 'args' in kwargs:
            Avv_extra_args = kwargs['args']
        else:
            Avv_extra_args = ()
        analytic_Avv = True
    else:
        Avv = Avv_dummy
        Avv_extra_args = ()
        if 'h2' in kwargs:
            h2 = kwargs['h2']
        else:
            h2 = 0.1
        analytic_Avv = False

    ## center_diff
    if 'center_diff' in kwargs:
        center_diff = kwargs['center_diff']
    else:
        center_diff = False

    ## callback
    if 'callback' in kwargs:
        callback = kwargs['callback']
    else:
        callback = callback_dummy

    ## info
    info = 0

    ## dtd
    dtd = numpy.empty((len(x0), len(x0)), order='F')
    if 'dtd' in kwargs:
        dtd[:, :] = kwargs['dtd'][:, :]  # guarantee that order = 'F'
    else:
        dtd[:, :] = numpy.eye(len(x0))[:, :]

    if 'damp_mode' in kwargs:
        damp_mode = kwargs['damp_mode']
    else:
        damp_mode = 1

    ## maxiter
    if 'maxiter' in kwargs:
        maxiter = kwargs['maxiter']
    else:
        maxiter = 200 * (len(x0) + 1)

    ## maxfev
    if 'maxfev' in kwargs:
        maxfev = kwargs['maxfev']
    else:
        maxfev = 0

    ## maxjev
    if 'maxjev' in kwargs:
        maxjev = kwargs['maxjev']
    else:
        maxjev = 0

    ## maxaev
    if 'maxaev' in kwargs:
        maxaev = kwargs['maxaev']
    else:
        maxaev = 0

    ## maxlam
    if 'maxlam' in kwargs:
        maxlam = kwargs['maxlam']
    else:
        maxlam = -1.0

    ## minlam
    if 'minlam' in kwargs:
        minlam = kwargs['minlam']
    else:
        minlam = -1.0

    ## artol
    if 'artol' in kwargs:
        artol = kwargs['artol']
    else:
        artol = 0.001

    ## Cgoal
    if 'Cgoal' in kwargs:
        Cgoal = kwargs['Cgoal']
    else:
        Cgoal = 1.49012e-08

    ## gtol
    if 'gtol' in kwargs:
        gtol = kwargs['gtol']
    else:
        gtol = 1.49012e-08

    ## xtol
    if 'xtol' in kwargs:
        xtol = kwargs['xtol']
    else:
        xtol = 1.49012e-08

    ## xrtol
    if 'xrtol' in kwargs:
        xrtol = kwargs['xrtol']
    else:
        xrtol = -1.0

    ## ftol
    if 'ftol' in kwargs:
        ftol = kwargs['ftol']
    else:
        ftol = 1.49012e-08

    ## frtol
    if 'frtol' in kwargs:
        frtol = kwargs['frtol']
    else:
        frtol = -1.0

    ## print_level
    if 'print_level' in kwargs:
        print_level = kwargs['print_level']
    else:
        print_level = 3

    ## print_unit
    print_unit = 6

    if 'imethod' in kwargs:
        imethod = kwargs['imethod']
    else:
        imethod = 0

    ## iaccel
    if 'iaccel' in kwargs:
        iaccel = kwargs['iaccel']
    else:
        iaccel = 1

    ## ibold
    if 'ibold' in kwargs:
        ibold = kwargs['ibold']
    else:
        ibold = 2

    ## ibroyden
    if 'ibroyden' in kwargs:
        ibroyden = kwargs['ibroyden']
    else:
        ibroyden = 0

    ## initialfactor
    if 'initialfactor' in kwargs:
        initialfactor = kwargs['initialfactor']
    else:
        if imethod < 10:
            initialfactor = 0.001
        else:
            initialfactor = 100.0

    ## factoraccept
    if 'factoraccept' in kwargs:
        factoraccept = kwargs['factoraccept']
    else:
        factoraccept = 3.0

    ## factorreject
    if 'factorreject' in kwargs:
        factorreject = kwargs['factorreject']
    else:
        factorreject = 2.0

    ## avmax
    if 'avmax' in kwargs:
        avmax = kwargs['avmax']
    else:
        avmax = 0.75

    ## m
    if 'm' in kwargs:
        _m = kwargs['m']
    else:
        _m = len(func(x0, *func_extra_args))

    fvec = numpy.empty((_m,))
    fjac = numpy.empty((_m, len(x0)), order='F')

    niters = numpy.empty((1,), dtype=numpy.int32)
    nfev = numpy.empty((1,), dtype=numpy.int32)
    njev = numpy.empty((1,), dtype=numpy.int32)
    naev = numpy.empty((1,), dtype=numpy.int32)
    converged = numpy.empty((1,), dtype=numpy.int32)

    x = x0.copy()

    _geodesiclm.geodesiclm(
        func,
        jacobian,
        Avv,
        x,
        fvec,
        fjac,
        callback,
        info,
        analytic_jac,
        analytic_Avv,
        center_diff,
        h1,
        h2,
        dtd,
        damp_mode,
        niters,
        nfev,
        njev,
        naev,
        maxiter,
        maxfev,
        maxjev,
        maxaev,
        maxlam,
        minlam,
        artol,
        Cgoal,
        gtol,
        xtol,
        xrtol,
        ftol,
        frtol,
        converged,
        print_level,
        print_unit,
        imethod,
        iaccel,
        ibold,
        ibroyden,
        initialfactor,
        factoraccept,
        factorreject,
        avmax,
        func_extra_args=func_extra_args,
        jacobian_extra_args=jacobian_extra_args,
        Avv_extra_args=Avv_extra_args,
    )

    if 'full_output' in kwargs:
        full_output = kwargs['full_output']
    else:
        full_output = 0

    if full_output:
        if converged[0] == 1:
            msg = 'artol'
        elif converged[0] == 2:
            msg = 'Cgoal'
        elif converged[0] == 3:
            msg = 'gtol'
        elif converged[0] == 4:
            msg = 'xtol'
        elif converged[0] == 5:
            msg = 'xrtol'
        elif converged[0] == 6:
            msg = 'ftol'
        elif converged[0] == 7:
            msg = 'frtol'
        elif converged[0] == -1:
            msg = 'iters'
        elif converged[0] == -2:
            msg = 'nfev'
        elif converged[0] == -3:
            msg = 'njev'
        elif converged[0] == -4:
            msg = 'naev'
        elif converged[0] == -5:
            msg = 'maxlam'
        elif converged[0] == -6:
            msg = 'minlam'
        elif converged[0] == -10:
            msg = 'user_termination'
        elif converged[0] == -11:
            msg = 'func_fail'
        info = {
            'converged': converged[0],
            'iters': numpy.array([niters[0], nfev[0], njev[0], naev[0]]),
            'msg': msg,
            'fvec': fvec,
            'fjac': fjac,
        }
        return x, info
    else:
        return x


def jacobian_dummy(x, *args):
    pass


def Avv_dummy(x, v, *args):
    pass


def callback_dummy(x, v, a, fvec, fjac, acc, lam, dtd, fvec_new, accepted):
    return 0
