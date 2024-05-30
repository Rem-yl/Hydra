import hydra
from omegaconf import DictConfig, OmegaConf
from dataclasses import dataclass
from hydra.core.config_store import ConfigStore

@dataclass
class PostgresSQLConfig:
    driver: str = "postgresql"
    user: str = "jieru"
    password: str = "secret"

cs = ConfigStore.instance()
# Registering the Config class with the name `postgresql` with the config group `db`
cs.store(name="postgresql", group="db", node=PostgresSQLConfig)

@hydra.main(version_base=None, config_path="conf")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()