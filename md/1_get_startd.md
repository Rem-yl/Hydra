# Quick start
1. 如果你想要用`Hdra`调参, 请将参数在config中配置好, 并且将主要逻辑代码写在`@hydra.main()`装饰器下;
2. 如果你只想用来解析参数配置, 请使用 `compose API`作为替代

```bash
pip install hydra-core --upgrade
```

## Basic example
**Config:**
```yaml
# config/config.yaml
db:
  driver: mysql
  user: omry
  pass: secret
```

**示例**
```python
'''
python 1.1_get_started.py
'''

import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    main()
```
> `cfg`仅在`@hydra.main()`中有效, 如果你要return cfg, 会发现返回值是None, 因此主要逻辑代码只能写在main里面

You can learn more about OmegaConf [here](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) later.

```shell
$ python train.py

db:
  driver: mysql
  user: omry
  pass: secret
```

当然也可以在命令行更改参数配置
```shell
$ python 1.1_get_started.py db.user=root

db:
  driver: mysql
  user: root
  pass: secret
```

## Composition example
你可以想使用两种完全不同的database, 对应到机器学习实验上来看就是, 你想使用完全不同的模型(vgg or resnet18)。你可以将两种不同的配置文件放在同一个文件夹下, 形成一个`config group`

```text
conf
├── config_composition.yaml
└── db
    ├── clickhouse.yaml
    └── mysql.yaml
```

其中, `db`目录下的yaml文件如下
```yaml
# mysql.yaml
driver: mysql
user: omry
pass: secret
timeout: 20
```

现在你可以通过读取`config_composition`来选择你的db并配置db的参数了!

```shell
$ python 1.2_composition_example.py db=clickhouse

db:
  driver: clickhouse
  user: root
  pass: clssql
  timeout: 30
```

## Multirun
可以添加`-m`参数来实现不同参数run
```shell
$ python 1.2_composition_example.py -m db=clickhouse,mysql

[2024-05-29 15:12:22,831][HYDRA] Launching 2 jobs locally
[2024-05-29 15:12:22,831][HYDRA]        #0 : db=clickhouse
db:
  driver: clickhouse
  user: root
  pass: clssql
  timeout: 30

[2024-05-29 15:12:22,963][HYDRA]        #1 : db=mysql
db:
  driver: mysql
  user: omry
  pass: secret
  timeout: 20
```
然后你就会发现目录下面多了`multirun`和`outputs`目录, 这两个目录是干嘛的且听下文分解ß