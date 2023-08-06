
import itertools
import numpy as np

from taylor import rules


def diff(fun,x,order,args=(),mask=None,rule='forward',delta=None,
         idx_order='default'):
    """
    fun : {function}
        function whose derivative is sought
        has function definition
            def fun(x,*args):
    x : {scalar, array}
        independent variable with respect to which the derivative
            will be computed
    order : {integer}
        order of desired derivative
        1: first derivative (gradient),
        2: second derivative (Hessian), ...
    args : {tuple}
        tuple of additional arguments to fun
    mask : {integer or array}
        array of same shape as the returned derivative where
            element = 1 -> this entry should be computed,
            element = 0 -> entry should not be computed
    rule : {string}
        finite difference rule
        choose from: {'forward','backward','central'}
    delta : {float or array}
        scalar/array of same shape as x that specifies the finite
            difference step size
    idx_order : {string}
        string indicating how indices of derivative object should be
            ordered when returned
        'default' : indices corresponding to derivatives are
                        ordered first
        'natural' : indices corresponding to elements of function
                        output are ordered first (like in Jacobians)
    """

    if (not isinstance(args,tuple)):
        print(f'ERROR: optional args input must be at tuple')

    if (rule not in rules.implemented_rule_names()):
        print(f'ERROR: selected finite difference rule {rule} is not implemented')
    
    # run test evaluation to evaluate output shape
    fun_output = fun(x,*args)
    if (isinstance(fun_output,float)):
        fun_output_shape = ()
    elif (isinstance(fun_output,np.ndarray)):
        fun_output_shape = fun_output.shape
    else:
        print(f'ERROR: function does not return a float or numpy array')

    # get dimension of x
    if (isinstance(x,(float,int))):
        x = np.array(x,dtype='float')
        x_shape = x.shape
    elif (isinstance(x,np.ndarray)):
        x_shape = x.shape
            
    # partition modes of output into derivatives and output
    # derivative index space stored at the front of full index space
    #     so the a[i] convention can be used slice all remaining modes
    #     of the array and seamless deal with functions that output
    #     any shape array
    derivative_index_space = [dim for dim in list(x_shape)]*order
    output_index_space = list(fun_output_shape)
    derivative_shape =  derivative_index_space + output_index_space 

    derivative = np.zeros(derivative_shape)

    # set finite differences step size(s)
    if (delta is None):
        step_size = 1e-6 # default step size
        delta = np.full(x_shape,step_size)
    elif (isinstance(delta,float)):
        step_size = delta
        delta = np.full(x_shape,step_size)
    elif (isinstance(delta,np.nd.array)):
        if (x.shape != delta.shape):
            print(f'ERROR: setting delta as array requires it be the same shape as x')
    else:
        print(f'ERROR: delta must be one of {None,float,array}')
        
    # create iterator for multindex over derivative index space
    index_range_array = [np.arange(elem,dtype='i') for elem in
                         derivative_index_space]
    multi_index_iterator = itertools.product(*index_range_array)

    # TODO: use symmetry of higher order derivatives to save work
    #       by computing unique elements and symmetrizing
    # TODO: implement masking via masked arrays or similar
    cur_rule = rules.rule_selector(rule)
    for i_m in multi_index_iterator:
        derivative[i_m] = cur_rule(fun,x,order,i_m,x_shape,args,delta)

    # TODO: figure out proper way to order indices
    #       *OFFER OPTIONS*
    #if (idx_order == 'natural'):
    if (False): # something like this
        axes = tuple(list(range(len(derivative_shape))))
        reversed_axes = tuple(reversed(axes))
        #numpy.transpose(derivative,axes=reversed_axes)

    return derivative

