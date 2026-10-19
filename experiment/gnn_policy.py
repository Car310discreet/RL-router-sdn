import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import torch_geometric.nn as pyg_nn

class GraphSAGEExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim=64):
        # We output a features_dim sized vector for the RL agent
        super(GraphSAGEExtractor, self).__init__(observation_space, features_dim)
        
        # Determine input feature size from the observation space dict
        n_input_features = observation_space.spaces["x"].shape[1]
        
        # Define the GraphSAGE layers
        self.conv1 = pyg_nn.SAGEConv(n_input_features, 128)
        self.conv2 = pyg_nn.SAGEConv(128, features_dim)
        self.relu = nn.ReLU()

    def forward(self, observations):
        """
        Extracts the PyTorch tensors from the Gym dict observation space and passes 
        them through the GraphSAGE network.
        """
        # Observations arrive as batch tensors
        x = observations["x"] 
        edge_index = observations["edge_index"]

        # If batch size is 1, squeeze to fit PyG requirements
        if len(x.shape) == 3:
            x = x.squeeze(0)
            edge_index = edge_index.squeeze(0)
            
        # FIX: Ensure edge_index is strictly of integer type (torch.int64 / long)
        edge_index = edge_index.long()
            
        # Message Passing Layer 1
        x = self.conv1(x, edge_index)
        x = self.relu(x)
        
        # Message Passing Layer 2
        x = self.conv2(x, edge_index)
        
        # Global pooling: Aggregate the entire graph into a single vector
        graph_embedding = torch.mean(x, dim=0, keepdim=True)
        
        return graph_embedding