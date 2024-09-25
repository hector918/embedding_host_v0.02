import torch
from transformers import AutoModel, AutoModelForSequenceClassfication


_model_meta = {
        "gpt2",
        "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf",
        "meta-llama/Llama-2-70b-hf",
        }

'''
_model_meta = {
        "gpt2": {
            "pretraining": "gpt2",
            "task": "language_modeling",
            },
        "llama2-7b": {
            "pretraining": "meta-llama/Llama-2-7b-hf",
            "task": "language_modeling",
            },
        "llama2-13b": {
            "pretraining": "meta-llama/Llama-2-13b-hf",
            "task": "language_modeling",
            },
        "llama2-70b": {
            "pretraining": "meta-llama/Llama-2-70b-hf",
            "task": "language_modeling",
            }.
         } '''  
        # TODO: I just randomly included some models. I am sure if there are available on huggingface. And I am not even sure if the names are correct. A proper implementation of this part would require a survey of LLMs. BTW, fuck large language models.
# TODO: I have never used this before. So you better get familiar with this before actually running.


def get_model(args):
    if args.backbone not in _model_meta:
        raise ValueError(f"Model {args.backbone} not found!")

    model = AutoModel.from_pretrained(args.backbone)
    return model
