# This contains code that enables decibel math

import numpy as np

def add_decibels(dB,coherent = False):
    
    if coherent:
        summation = 20 * np.log10(sum(10**(dB/20)))
    else:
        summation = 10 * np.log10(sum(10**(dB/10)))

    return summation

def unpack_decibels(dB,reference,squared = True):

    if squared:
        value = reference * 10**(dB/20)
    else:
        value = reference * 10**(dB/10)

    return value
