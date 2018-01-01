from __future__ import division, print_function, absolute_import
import theano
from theano import tensor as T
import numpy as np
import sys


def run_function_in_batches(func,
                            input_data_list,
                            learning_phase=None,
                            batch_size=10,
                            progress_update=1000,
                            multimodal_output=False):
    #func has a return value such that the first index is the
    #batch. This function will run func in batches on the inputData
    #and will extend the result into one big list.
    #if multimodal_output=True, func has a return value such that first
    #index is the mode and second index is the batch
    assert isinstance(input_data_list, list), "input_data_list must be a list"
    #input_datas is an array of the different input_data modes.
    to_return = [];
    i = 0;
    while i < len(input_data_list[0]):
        if (progress_update is not None):
            if (i%progress_update == 0):
                print("Done",i)
                sys.stdout.flush()
        func_output = func(*([x[i:i+batch_size] for x in input_data_list]
                                +([] if learning_phase is
                                   None else [learning_phase])
                        ))
        if (multimodal_output):
            assert isinstance(func_output, list),\
             "multimodal_output=True yet function return value is not a list"
            if (len(to_return)==0):
                to_return = [[] for x in func_output]
            for to_extend, batch_results in zip(to_return, func_output):
                to_extend.extend(batch_results)
        else:
            to_return.extend(func_output)
        i += batch_size;
    return to_return


#return counts for number of nonnegative matches to the filters per seq
def get_gapped_kmer_embedding_func(filters, biases):

    #filters should be: out_channels, rows, ACGT
    filters = filters.astype("float32")
    biases = biases.astype("float32")
    onehot_var = theano.tensor.TensorType(dtype=theano.config.floatX,
                                      broadcastable=[False]*3)("onehot")
    theano_filters = theano.tensor.as_tensor_variable(
                      x=filters, name="filters")
    theano_biases = theano.tensor.as_tensor_variable(x=biases, name="biases")
    match_counts = T.sum(1.0*((theano.tensor.nnet.conv.conv2d(
                    input=onehot_var[:,None,:,:],
                    filters=theano_filters[:,None,::-1,::-1],
                    border_mode='valid')[:,:,:,0] + biases[None,:,None])
                    > 0.0), axis=2)
    func = theano.function([onehot_var], match_counts,
                            allow_input_downcast=True)
    def batchwise_func(onehot, batch_size, progress_update):
        return np.array(run_function_in_batches(
                            func=func,
                            input_data_list=[onehot],
                            batch_size=batch_size,
                            progress_update=progress_update))
    return batchwise_func
