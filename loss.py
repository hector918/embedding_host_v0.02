# TODO: I made this contrastive loss up. You know how it is.


import torch
import torch.nn as nn
import torch.nn.functional as F



class ContrastiveLoss(nn.Module):
    def __init__(self, temperature=0.5):
        super(ContrastiveLoss, self).__init__()
        self.temperature = temperature

    def forward(self, z_i, z_j):
        z_i = F.normalize(z_i, dim=1)
        z_j = F.normalize(z_j, dim=1)
        
        similarity_matrix = torch.matmul(z_i, z_j.T) / self.temperature
        
        batch_size = z_i.size(0)
        mask = torch.eye(batch_size, dtype=torch.bool).to(z_i.device)
        
        positive_pairs = torch.diag(similarity_matrix)
        positive_loss = F.cross_entropy(similarity_matrix, torch.arange(batch_size).to(z_i.device))
        
        return positive_loss


def get_loss(args):   # Comment: Sorry I have to. It's a my sickness. It's a desease.
    return ContrastiveLoss()
