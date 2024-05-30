import logging
from omegaconf import DictConfig
import hydra

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(name)s [line:%(lineno)d] %(levelname)s %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    logger = get_logger(__name__)
    logger.info("Info level message")
    logger.info("test")

if __name__ == "__main__":
    main()

