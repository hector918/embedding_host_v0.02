# TODO: Ensure dataset is properly split.

import os

import pandas as pd

import torch
from torch.utils.data import Dataset
from torch.utils.data import Dataloader

from data._gen_data import get_df



class News(Dataset):
    csv_path = "/scratch/ym2380/data/news/news.csv"
    article_column_name = "description"   ### TODO: This is not article
    
    def __init__(self, tokenizer, max_length):
        if not os.path.exists(self.csv_path):
            self._download_csv()
        self.data = pd.read_csv(self.csv_path)

        self.tokenizer = tokenizer   ### TODO: use pre-tokenization would be more efficient
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        article = str(self.data[self.article_column_name][idx])

        encoding = self.tokenizer.encode_plus(
                article,
                add_special_tokens=True,
                max_length=self.max_length,
                padding="max_length",
                return_attention_mask=True,
                return_tensors="pt",
                )
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()
        
        return (input_ids, attention_mask)
    
    def _download_csv(self):
        df = get_df(db_name="rss_reader")

        _csv_dir = os.path.dirname(self.csv_path)
        if not os.path.exists(_csv_dir):
            os.makedirs(_csv_dir)
        df.to_csv(self.csv_file, index=False)
