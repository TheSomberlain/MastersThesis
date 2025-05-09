import os
from mmengine.config import Config
from mmengine.runner import Runner
from mmengine.runner import set_random_seed 

def main():
    # Load the configuration from the provided config file
    config_file = 'train_config.py'  # Path to your config
    cfg = Config.fromfile(config_file)

    # Set random seed for reproducibility
    set_random_seed(42, deterministic=False)

    # Ensure work_dir exists
    if not os.path.exists(cfg.work_dir):
        os.makedirs(cfg.work_dir)

    # Create a Runner from config and start training
    runner = Runner.from_cfg(cfg)
    runner.train()

if __name__ == '__main__':
    main()