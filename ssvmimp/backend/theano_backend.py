from __future__ import division, print_function, absolute_import
import theano
from theano import tensor as T
import numpy as np
import sys
from .. import interpret


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
                    border_mode='valid')[:,:,:,0]
                    + biases[None,:,None])
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


def get_interpretation_func_dynamic_filter_imp(filters):

    filters = filters.astype("float32")
    filter_imp_mats = (interpret.get_per_base_filter_contrib_nomismatch(
                                 filters=filters)).astype("float32")

    #filters has the shape: num_filt x len x alphabet_size
    assert len(filters.shape)==3
    assert filters.shape==filter_imp_mats.shape
    
    #figure out the bias for an exact match to each filter
    biases = -(np.sum(np.max(filters, axis=-1),axis=-1)-1)
    onehot_var = T.TensorType(dtype=theano.config.floatX,
                                    broadcastable=[False]*3)("onehot")
    filter_grad_var = T.TensorType(dtype=theano.config.floatX,
                                  broadcastable=[False]*2)("filter_grad_var")

    theano_filters = T.as_tensor_variable(
                      x=filters, name="filters")
    theano_biases = T.as_tensor_variable(x=biases, name="biases")

    filter_exact_matches = 1.0*((T.nnet.conv.conv2d(
        input=onehot_var[:,None,:,:],
        filters=theano_filters[:,None,::-1,::-1],
        border_mode='valid')[:,:,:,0] + biases[None,:,None])
        > 0.0)

    total_match_counts = T.sum(filter_exact_matches, axis=2)
    per_seq_norm = T.sqrt(T.sum(T.square(total_match_counts), axis=1))
    per_match_imp = (1.0*filter_grad_var)/(per_seq_norm[:,None])

    #match_counts = T.sum(filter_exact_matches, axis=2)
    #pseudocount the denominator to avoid nans
    #per_match_imp = (filter_imp_var/\
    #                 (match_counts + 0.01*(match_counts<1.0)))
    filter_exact_match_imp = filter_exact_matches*per_match_imp[:,:,None]

    #get the inverse of the filter importance mats; will have the
    #shape of inv_filter_imp_mats is alphabet_size x num_filt x len
    #note that the last axis is reversed deliberately
    inv_filter_imp_mats = filter_imp_mats.transpose(2,0,1)[:,:,::-1]

    theano_inv_filters = T.as_tensor_variable(
                            x=inv_filter_imp_mats, name="inv_filters")

    #border_mode='full' will apply the filter wherever it partially overlaps,
    #which is what we need to reconstruct our original input size.
    importance_scores = T.nnet.conv.conv2d(
        input=filter_exact_match_imp[:,:,:,None],
        filters=theano_inv_filters[:,:,::-1,None],
        border_mode='full')[:,:,:,0] 
    importance_scores = importance_scores.transpose(0,2,1)

    func = theano.function([onehot_var, filter_imp_var],
                            importance_scores,
                            allow_input_downcast=True)

    def batchwise_func(onehot, filter_grad, batch_size, progress_update):
        return np.array(run_function_in_batches(
                            func=func,
                            input_data_list=[onehot, filter_grad],
                            batch_size=batch_size,
                            progress_update=progress_update))
    return batchwise_func


def get_interpretation_func_dynamic_hyp_contribs(filters):

    filters = filters.astype("float32")
    filter_perbase_mats = (interpret.get_per_base_filter_contrib_nomismatch(
                                 filters=filters)).astype("float32")

    #filters has the shape: num_filt x len x alphabet_size
    assert len(filters.shape)==3
    assert filters.shape==filter_perbase_mats.shape
    
    #figure out the bias for exact matches to filters
    exact_biases = -(np.sum(np.max(filters, axis=-1),axis=-1)-1)
    #figure out the bias that allows a single mismatch to the filters
    inexact_biases = -(np.sum(np.max(filters, axis=-1),axis=-1)-2)
    onehot_var = T.TensorType(dtype=theano.config.floatX,
                                    broadcastable=[False]*3)("onehot")
    filter_grad_var = T.TensorType(
                        dtype=theano.config.floatX,
                        broadcastable=[False]*2)("filter_grad_var")
    theano_filters = T.as_tensor_variable(
                      x=filters, name="filters")

    conv_result = T.nnet.conv.conv2d(
        input=onehot_var[:,None,:,:],
        filters=theano_filters[:,None,::-1,::-1],
        border_mode='valid')[:,:,:,0]

    filter_exact_matches = 1.0*((conv_result + exact_biases[None,:,None])
                                > 0.0)
    filter_inexact_matches = 1.0*((conv_result + inexact_biases[None,:,None])
                                  > 0.0)

    total_match_counts = T.sum(filter_exact_matches, axis=2)
    per_seq_norm = T.sqrt(T.sum(T.square(total_match_counts), axis=1))
    #pseudocount the denominator to avoid nans
    per_match_hyp_imp = 1.0*(filter_grad_var/
                             (per_seq_norm+0.000001)[:,None])
    filter_inexact_hyp_imp = filter_inexact_matches*per_match_hyp_imp[:,:,None]

    #get the inverse of the filter importance mats; will have the
    #shape of inv_filter_perbase_mats is alphabet_size x num_filt x len
    #note that the last axis is reversed deliberately
    inv_filter_perbase_mats = filter_perbase_mats.transpose(2,0,1)[:,:,::-1]

    theano_inv_filters = T.as_tensor_variable(
                            x=inv_filter_perbase_mats, name="inv_filters")

    #border_mode='full' will apply the filter wherever it partially overlaps,
    #which is what we need to reconstruct our original input size.
    hyp_importance_scores = T.nnet.conv.conv2d(
        input=filter_inexact_hyp_imp[:,:,:,None],
        filters=theano_inv_filters[:,:,::-1,None],
        border_mode='full')[:,:,:,0] 
    hyp_importance_scores = hyp_importance_scores.transpose(0,2,1)

    func = theano.function([onehot_var, filter_grad_var],
                            hyp_importance_scores,
                            allow_input_downcast=True)

    def batchwise_func(onehot, filter_grad, batch_size, progress_update):
        return np.array(run_function_in_batches(
                            func=func,
                            input_data_list=[onehot, filter_grad],
                            batch_size=batch_size,
                            progress_update=progress_update))
    return batchwise_func


def get_interpretation_func(filters, filter_imp_mats):

    filters = filters.astype("float32")
    filter_imp_mats = filter_imp_mats.astype("float32")

    #filters has the shape: num_filt x len x alphabet_size
    assert len(filters.shape)==3
    assert filters.shape==filter_imp_mats.shape
    
    #figure out the bias for an exact match to each filter
    biases = -(np.sum(np.max(filters, axis=-1),axis=-1)-1)
    onehot_var = T.TensorType(dtype=theano.config.floatX,
                                      broadcastable=[False]*3)("onehot")
    theano_filters = T.as_tensor_variable(
                      x=filters, name="filters")
    theano_biases = T.as_tensor_variable(x=biases, name="biases")

    filter_exact_matches = 1.0*((T.nnet.conv.conv2d(
        input=onehot_var[:,None,:,:],
        filters=theano_filters[:,None,::-1,::-1],
        border_mode='valid')[:,:,:,0] + biases[None,:,None])
        > 0.0)
    match_counts = T.sum(filter_exact_matches, axis=2)
    normalized_match_counts = (match_counts/
        (T.sqrt(T.sum(match_counts*match_counts,axis=1))[:,None]))

    #pseudocount the denominator to avoid nans
    per_match_norm = normalized_match_counts/(match_counts + 0.01*(match_counts<1.0))
    filter_exact_match_imp = filter_exact_matches*per_match_norm[:,:,None]

    #get the inverse of the filter importance mats; will have the
    #shape of inv_filter_imp_mats is alphabet_size x num_filt x len
    #note that the last axis is reversed deliberately
    inv_filter_imp_mats = filter_imp_mats.transpose(2,0,1)[:,:,::-1]

    theano_inv_filters = T.as_tensor_variable(
                            x=inv_filter_imp_mats, name="inv_filters")

    #border_mode='full' will apply the filter wherever it partially overlaps,
    #which is what we need to reconstruct our original input size.
    importance_scores = T.nnet.conv.conv2d(
        input=filter_exact_match_imp[:,:,:,None],
        filters=theano_inv_filters[:,:,::-1,None],
        border_mode='full')[:,:,:,0] 
    importance_scores = importance_scores.transpose(0,2,1)

    func = theano.function([onehot_var], importance_scores,
                            allow_input_downcast=True)

    def batchwise_func(onehot, batch_size, progress_update):
        return np.array(run_function_in_batches(
                            func=func,
                            input_data_list=[onehot],
                            batch_size=batch_size,
                            progress_update=progress_update))
    return batchwise_func
