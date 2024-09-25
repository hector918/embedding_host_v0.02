# packages
import sys
import os
import argparse

import torch
import torch.optim as optim

from data import get_data, get_loader
from loss import get_loss

# argparse
def get_args():
    parser = argparse.AugmentParser()

    parser.add_argument("--lr", type=float, required=True)
    parser.add_argument("--batch_size", type=int, required=True)
    parser.add_argument("--num_epochs", type=int, required=True)
    parser.add_argument("--optimizer", default="adam", required=True)

    parser.add_argument(
            "--backbone",
            default="meta-llama/Llama-2-7b-hf",
            required=True,)

    parser.add_argument("--tokenizer_max_length", type=int, default=512, required=True)  ### TODO: I am not sure how to set the max length

    parser.add_argument("--num_workers", type=int, default=8, required=True)

    args = parser.parse_args()
    return args


# get device
def get_device():   ### TODOs: of course you need to consider DDP, every thing needs to be changed
    return 0

# get optimizer
def get_optimizer(args, model):
    if args.optimizer.lower == "adam":
        return optim.Adam(model.parameters(), lr=args.lr)



# main
if __name__ == "__main__":
    ## config
    args = get_args()
    device = get_device()

    ## data  ### TODO: again, very significantly, we didn't split the data
    train_set = get_data(args)
    train_loader = get_loader(args, train_set)

    ## model
    model = get_model(args)
    model.to(device)

    ## loss & optimizer
    loss = get_loss(args)
    optimizer = get_optimizer(args, model)
    ## TODO: you might need a scheduler

    ## train
    # TODO: And I am not sure if there are some important training techniques that could be used here
    # TODO: And I didn't add resume here. And this is important for DDP
    # TODO: Didn't add test only mode. As I don't even have a evaluater
    for epoch in range(args.start_epoch, args.epochs):
        train_one_epoch(
                args,
                model,
                criterion,
                optimizer,
                dataloader,
                device,
                epoch,
                )
        ## TODO: no evaluation

    total_time = time.time() - start_time
    total_time_str = str(datetime.timedelta(seconds=int(total_time)))
    print(f"Training time {total_time_str}")
