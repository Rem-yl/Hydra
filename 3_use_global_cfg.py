import hydra
from omegaconf import DictConfig, OmegaConf

def add_conf(cfg: DictConfig):
    cfg.model.name = "resnet18"

    return cfg

@hydra.main(version_base=None, config_path="config", config_name="config")
def get_config(cfg: DictConfig):
    cfg = add_conf(cfg)
    print(OmegaConf.to_yaml(cfg))
    
if __name__ == "__main__":
    get_config()
