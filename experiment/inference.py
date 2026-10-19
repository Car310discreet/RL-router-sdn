import time
from stable_baselines3 import PPO
from sdn_env import SDNEnv

def run_inference():
    print("[INFO] Loading trained GraphSAGE+PPO model...")
    # Load the frozen weights
    model = PPO.load("models/gnn_ppo_routing")
    
    # Initialize the environment in inference mode
    env = SDNEnv(src_ipv4="10.0.0.1", dst_ipv4="10.0.0.10", num_paths=5)
    obs, info = env.reset()
    
    print("[INFO] Starting continuous routing optimization...")
    
    try:
        while True:
            # The model evaluates the PyG graph state and outputs the best path index
            action, _states = model.predict(obs, deterministic=True)
            print(f"[INFERENCE] Selected Optimal Path Index: {action}")
            
            # Execute the routing decision and get the updated network state
            obs, reward, terminated, truncated, info = env.step(action)
            
            print(f"[INFERENCE] Received Reward: {reward:.2f}\n")
            
            # Re-evaluate the network every 10 seconds
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n[INFO] Inference stopped by user. Cleaning up flows...")
        import floodlightRestApi
        floodlightRestApi.deleteAllFlows()

if __name__ == "__main__":
    run_inference()