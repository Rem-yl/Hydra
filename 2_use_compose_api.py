from hydra import compose, initialize
from omegaconf import OmegaConf

if __name__ == "__main__":
    # context initialization
    with initialize(version_base=None, config_path="config"):
        cfg = compose(config_name="config")
        print(OmegaConf.to_yaml(cfg))

    print(cfg)    # 可以正常输出参数
    # global initialization
    initialize(version_base=None, config_path="config")
    cfg = compose(config_name="config")
    print(OmegaConf.to_yaml(cfg))