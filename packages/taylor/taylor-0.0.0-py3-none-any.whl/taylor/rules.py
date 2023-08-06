
import copy
import itertools
import numpy as np

def implemented_rule_names():
    # returns all implemented rules (all keys of rule dictionary)
    #     as an iterable of strings
    return rule_dict().keys()


def rule_selector(rule_name):
    # returns function pointer corresponding to rule_name
    return rule_dict()[rule_name]


def rule_dict():
    # dictionary keys are rule names, items are respective function
    #     pointers
    # basically a hardcoded info variable
    d = {
        "forward" : forward,
        }
    return d


def forward(fun,x,order,i_m,x_shape,args,delta):
    """
    Computes element of derivate object using forward difference
    scheme

    fun : {function}
        function whose derivative is sought
        has function definition
            def fun(x,*args):
    x : {scalar, array}
        independent variable the derivative will be computed with
        respect to
    order : {integer}
        number of derivatives to take
    i_m : {tuple}
        multi-index of the element of the derivative to be computed
    x_shape : {tuple)
        shape of object with respect to which fun is differentiated
    args : {tuple}
        additional arguments to fun
    delta : {numpy array}
        contains value of finite difference step size for every
        element of x
    """

    i_m_stride = len(x_shape)

    for i_p, perm_tuple in enumerate(itertools.product([0,1],repeat=order)):
        perm_vec_sum = sum(perm_tuple) #tuple sum

        # make finite difference step on x as given by perm_vec
        x_cur = copy.deepcopy(x)
        for i_b, bit in enumerate(perm_tuple):
            if (bit):
                # extract index of x to be stepped then step it
                i_start = int(i_m_stride*i_b)
                i_end = i_start + i_m_stride
                i_x = i_m[i_start:i_end] # index of an element in x
                # the object we are differentiating with respect to
                x_cur[i_x] += delta[i_x]

        # evaluate numerator of finite difference fraction
        if (i_p == 0): #initialize variable in first iteration
            numerator  = np.power(-1,order-perm_vec_sum)*fun(x_cur,*args)
        else:
            numerator += np.power(-1,order-perm_vec_sum)*fun(x_cur,*args)

    # evaluate denominator of finite difference fraction
    denominator = 1.0
    for i_o in range(order):
        i_start = int(i_m_stride*i_b)
        i_end = i_start + i_m_stride
        i_x = i_m[i_start:i_end] # index of an element in x
        # the object we are differentiating with respect to
        denominator *= delta[i_x]


    # compute element of derivative object
    elem = numerator/denominator 
    return elem


