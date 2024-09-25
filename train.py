# packages
import torch

from utils.logging import SmoothedValue
from utils.logging import Nexus


# train one epoch
def train_one_epoch(
        args,
        loader,
        model,
        optimizer,
        criterion,
        device,
        epoch,  ## TODO: you could try to implement scaler here
        ):
    
    model.train()
    nexus = Nexus(delimiter=" ")
    nexus.add_meter("lr", SmoothedValue(window_size=1, fmt="{value}"))
    nexus.add_meter("img/s", SmoothedValue(window_size=10, fmt="{value}"))
    ## TODO: of course this is not image, so you need to find the right meter
    header = f"Epoch: [{epoch}]"
    for i, (article1, article2) in enumerate(nexus.log_and_iterate(dataloader=loader, print_freq=args.print_freq, header=header)):
        start = time.time()
        article1, article2 = article1.to(device), article2.to(device)

        out1 = model(article1)
        out2 = model(article2)
        loss_v = criterion(out1, out2)

        optimizer.zero_grad()
        loss_v.backward()
        optimizer.step()

        nexus.update(loss=loss_v.item(), lr=optimizer.param_groups[0]["lr"])
        nexus.meters["img/s"].update(batch_size / (time.time() - start))
        ## TODO: I am not sure other meters, like acc or something


## This is in lack of a evaluation function
