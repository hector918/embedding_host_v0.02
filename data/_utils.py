# packages
import torch
from torch.utils.data import DataLoader

from transformers import AutoTokenizer

from data.dataset import News


# get data
def get_data(args):
    # TODO: It should take another argument that is about the split of dataset
    tokenizer = AutoTokenizer.from_pretrained(args.backbone)

    data = News(tokenizer=tokenizer, max_length=args.tokenizer_max_length)

    return data


# get loader
def get_loader(args, data):
    loader = DataLoader(
            data,
            batch_size=args.batch_size,
            shuffle=True,
            num_workers=args.num_workers,
            pin_memory=True,
            )
    return loader
