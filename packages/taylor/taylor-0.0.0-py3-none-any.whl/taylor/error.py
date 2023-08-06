
import numpy as np

# TODO: implement friendly error functin for user
#       something like below (make sure it makes sense)

def rel_error(A_measured,A_true):
    #computes the relative error between two arrays,
    #even when one of them contains near zero values
    zero_threshold = 1e-14
    error_abs_val = np.abs(A_measured - A_true)

    #replaces all zeros with ones to prevent divide by zero errors
    safe_denominator = np.where((np.abs(A_true)<zero_threshold),1.0,np.abs(A_true))
    error_rel = error_abs_val/safe_denominator
    return 
