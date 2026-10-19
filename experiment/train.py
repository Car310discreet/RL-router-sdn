from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from sdn_env import SDNEnv
from gnn_policy import GraphSAGEExtractor

def train_agent():
    print("[INFO] Initializing SDN Environment...")
    env = SDNEnv(src_ipv4="10.0.0.1", dst_ipv4="10.0.0.10", num_paths=5)
    
    # Validate the custom environment to ensure it complies with Gymnasium API
    check_env(env, warn=True)

    # Configure PPO to use our custom GraphSAGE Extractor
    policy_kwargs = dict(
        features_extractor_class=GraphSAGEExtractor,
        features_extractor_kwargs=dict(features_dim=64),
    )
    
    print("[INFO] Building GraphSAGE + PPO Model...")
    model = PPO(
        "MultiInputPolicy", 
        env, 
        policy_kwargs=policy_kwargs, 
        verbose=1,
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64
    )
    
    # Train the agent
    total_timesteps = 50000
    print(f"[INFO] Starting Training for {total_timesteps} timesteps...")
    model.learn(total_timesteps=total_timesteps)
    
    # Save the weights to replace your old .pkl file
    model.save("models/gnn_ppo_routing")
    print("[INFO] Model saved successfully.")

if __name__ == "__main__":
    train_agent()