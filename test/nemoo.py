import nemo.collections.asr as nemo_asr
import os
import numpy as np

TOKEN_OFFSET = 100

def load_model(model_path):
    asr_model = nemo_asr.models.EncDecCTCModelBPE.restore_from(
      '/home/harveen/nemo_training/scripts/nemo_experiments/Conformer-CTC-BPE/2022-04-27_10-56-05/checkpoints/Conformer-CTC-BPE.nemo')
    return asr_model

def load_language_model(lm_path, asr_model, alpha=1.0, beta=1.0, beam_width=128):
    local_vocab = asr_model.decoder.vocabulary
    local_vocab = [chr(idx + TOKEN_OFFSET) for idx in range(len(local_vocab))]
    
    beam_search_lm = nemo_asr.modules.BeamSearchDecoderWithLM(
        vocab=local_vocab,
        beam_width=beam_width,
        alpha=alpha,
        beta=beta,
        lm_path=lm_path,
        num_cpus=max(os.cpu_count(), 1),
        input_tensor=False,
    )
    
    return beam_search_lm


def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum(axis=-1).reshape([x.shape[0], 1])

def transcribe(wav_file, logprobs=False):
    if type(wav_file) != list:
        wav_file = [wav_file]
    

    return asr_model.transcribe(wav_file, logprobs=logprobs)

def transcribe_with_lm(wav_file):
    logits = transcribe(wav_file, True)
    
    probs = [softmax(logits) for logits in logits]
    
    ids_to_text_func = asr_model.tokenizer.ids_to_text
    
    preds = []
    for prob in probs:
        beams_batch = beam_search_lm.forward(log_probs=prob.reshape(1, prob.shape[0], prob.shape[1]), 
                                         log_probs_length=None)
        for beams_idx, beams in enumerate(beams_batch):
            for candidate_idx, candidate in enumerate(beams):
                if ids_to_text_func is not None:
                    # For BPE encodings, need to shift by TOKEN_OFFSET to retrieve the original sub-word ids
                    pred_text = ids_to_text_func([ord(c) - TOKEN_OFFSET for c in candidate[1]])
                else:
                    pred_text = candidate[1]
        preds.append(pred_text)
                
    return preds

transcribe('user.wav')