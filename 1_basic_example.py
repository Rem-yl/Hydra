'''
basic中的例子只能将主要代码的逻辑写在hydra.main中
无法返回cfg, 非常的不灵活
但是使用compose api又没有办法使用hydra多任务调参的优势, 牛逼的
'''

import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="config", config_name="config")
def get_config(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    return cfg  # 返回值是None


if __name__ == "__main__":
    cfg = get_config()
    print(cfg)      # None