# Basic Tuorial

## Specifying a config file

给 `config`添加不存在的属性要使用 `++`前缀

```shell
$ python 1.1_get_started.py ++db.timeout=50

db:
  driver: mysql
  user: omry
  pass: secret
  timeout: 50
```

## Using the config object

这一节讲到, 我们可以在yaml文件中使用变量, 如下:

```yaml
# config/config_object.yaml

node:                         # Config is hierarchical
  loompa: 10                  # Simple value
  zippity: ${node.loompa}     # Value interpolation
  do: "oompa ${node.loompa}"  # String interpolation
  waldo: ???                  # Missing value, must be populated prior to access 
```

```shell
$ python 2.1_using_config_object.py

Error executing job with overrides: []
Traceback (most recent call last):
  File "/Users/yule/Desktop/code/Hydra/2.1_using_config_object.py", line 13, in main
    cfg.node.waldo                        # raises an exception
omegaconf.errors.MissingMandatoryValue: Missing mandatory value: node.waldo
    full_key: node.waldo
    object_type=dict

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
```

从上面的输出结果来看, 在yaml文件中我们可以使用${value}来使用变量值

## Selecting default configs

你可以对默认config中的多个值进行设定:

```yaml
defaults:
 - db: mysql
 - db/mysql/engine: innodb      # 设定mysql.engine的默认值
```

你也可以清空默认值, 通过添加前缀 `~`

```shell
python 1.2_composition_example.py ~db

{}

```

## 默认参数和自己添加的参数顺序问题

这一节要解决的是：当默认的参数与自己添加的参数发生冲突时应该是个什么优先级问题

1. 如果你想要用自己的参数覆盖默认的参数, 则添加 `_self_`在Defaults List的**结尾**;
2. 用默认的参数覆盖自己定义的参数, 则添加 `_self_`在Defaults List的**开头**;

```yaml
defaults:
  - db: mysql
  - _self_

db:
  user: root
```

使用这样的默认配置, 我们定义的 `db.user=root`就会覆盖默认值

```yaml
db:
  driver: mysql  # db/mysql.yaml
  pass: secret   # db/mysql.yaml 
  user: root     # config.yaml
```

## Putting it all together

把前面介绍的config group等等概念都串起来, 这里就不用代码演示了, 直接贴官方教程的结果
首先我们的 `conf`文件夹组成如下:

```text
├── conf
│   ├── config.yaml
│   ├── db
│   │   ├── mysql.yaml
│   │   └── postgresql.yaml
│   ├── schema
│   │   ├── school.yaml
│   │   ├── support.yaml
│   │   └── warehouse.yaml
│   └── ui
│       ├── full.yaml
│       └── view.yaml
└── my_app.py
```

我们可以设置默认配置:

```yaml
defaults:
  - db: mysql
  - ui: full
  - schema: school
```

最终我们可以得到下面的配置结果:

```yaml
db:
  driver: mysql
  user: omry
  pass: secret
ui:
  windows:
    create_db: true
    view: true
schema:
  database: school
  tables:
  - name: students
    fields:
    - name: string
    - class: int
  - name: exams
    fields:
    - profession: string
    - time: data
    - class: int

```

## Multi-run

`Hydra`比较核心的功能, 基本上选这个库就是奔着做实验调参方便来的。
如果只是用它用作读取配置文件的话,那么其实直接读yaml文件也就够用了。所以这块儿要好好研究一下怎么用, 努力做好调参侠。

有以下三种方式可以启动Multi-run

- Configure `hydra.mode`

  ```shell
  $ python my_app.py hydra.mode=MULTIRUN db=mysql,postgresql schema=warehouse,support,school


  [2021-01-20 17:25:03,317][HYDRA] Launching 6 jobs locally
  [2021-01-20 17:25:03,318][HYDRA]        #0 : db=mysql schema=warehouse
  [2021-01-20 17:25:03,458][HYDRA]        #1 : db=mysql schema=support
  [2021-01-20 17:25:03,602][HYDRA]        #2 : db=mysql schema=school
  [2021-01-20 17:25:03,755][HYDRA]        #3 : db=postgresql schema=warehouse
  [2021-01-20 17:25:03,895][HYDRA]        #4 : db=postgresql schema=support
  [2021-01-20 17:25:04,040][HYDRA]        #5 : db=postgresql schema=school
  ```
- 在命令行添加 `--multirun(-m)`参数

  ```shell
  python my_app.py --multirun db=mysql,postgresql schema=warehouse,support,school
  python my_app.py -m db=mysql,postgresql schema=warehouse,support,school
  ```

  - 通过 `hydra.sweeper.params`
    可以通过配置这个config来决定跑哪些参数任务

    例如使用下面的配置:

    ```yaml
    hydra:
        sweeper:
        	params:
            	db: mysql,postgresql
            	schema: warehouse,support,school
    ```

    使用上面的方法配置input config和直接在命令行中配置的效果是一样的, 如果用上面的方法和命令行同时进行配置的话, 那么命令行的配置优先
    如果使用上面的配置方法同时在命令行输入配置, 则得到的效果如下:

    ```shell
        $ python my_app.py -m db=mysql

        [2021-01-20 17:25:03,317][HYDRA] Launching 3 jobs locally
        [2021-01-20 17:25:03,318][HYDRA]        #0 : db=mysql schema=warehouse
        [2021-01-20 17:25:03,458][HYDRA]        #1 : db=mysql schema=support
        [2021-01-20 17:25:03,602][HYDRA]        #2 : db=mysql schema=school
    ```

    可以看到原本在 `sweep`中配置的实验组应有 `postgresql`, 但是命令行输入的 `mysql`配置覆盖掉了

### Additional sweep types

Hydra支持不同种类的sweeps, 这个不是很懂, 后面研究一下吧

```python
    x=range(1,10)                  # 1-9
    schema=glob(*)                 # warehouse,support,school
    schema=glob(*,exclude=w*)      # support,school
```

### Sweeper

[ ] 默认的sweeper logic 内置于 Hydra 中。其他sweepers 以插件形式提供。例如，Ax Sweeper 可以自动找到最佳参数组合！

### Launcher

默认情况下，Hydra 会在本地串行运行 multi-run jobs。其他launchers可作为插件在不同集群上并行启动。例如，JobLib 启动器可以在本地计算机上使用多进程并行执行不同的参数组合。

---

## Output/Working directory

Hydra 可以为每次运行创建一个目录，并在该输出目录中执行代码，从而解决每次运行都需要指定新输出目录的问题。默认情况下，该输出目录用于存储 Hydra 的运行输出（配置、日志等）。

```shell
$ python 2.2_output_working_dir.py 

Working directory : /Users/yule/Desktop/code/Hydra
Output directory  : /Users/yule/Desktop/code/Hydra/outputs/2024-05-29/16-58-53
```

可以查看 `outputs`文件夹的结构

```shell
$ tree -a outputs/2024-05-29/16-58-53

outputs/2024-05-29/16-58-53
├── .hydra
│   ├── config.yaml
│   ├── hydra.yaml
│   └── overrides.yaml
└── 2.2_output_working_dir.log
```

- `config.yaml` : 用户最终得到的config配置(可能被命令行覆盖过了)
- `hydra.yaml` : Hydra配置
- `overrides.yaml` : 显示哪些配置被命令行覆盖了

可以参考[here](https://hydra.cc/docs/configure_hydra/workdir/)自定义working dir

### Automatically change current working dir to job's output dir

通过设置 `hydra.job.chdir=True`，可以配置 Hydra 的 `@hydra.main` 装饰器，在将控制权传递给用户装饰的 main 函数之前，调用 `os.chdir` 来更改 python 的工作目录。从 Hydra v1.2 开始，`hydra.job.chdir` 的默认值为 False。设置 `hydra.job.chdir=True` 可以方便地使用输出目录来存储应用程序的输出（例如数据库转储文件）。

```shell
$ python 2.2_output_working_dir.py db.user=ley hydra.job.chdir=True

Working directory : /Users/yule/Desktop/code/Hydra/outputs/2024-05-29/17-14-31
Output directory  : /Users/yule/Desktop/code/Hydra/outputs/2024-05-29/17-14-31
```

### Changing or disabling Hydra's output subdir

您可以通过覆盖 hydra.output_subdir 来更改 .hydra 子目录名称。您可以将 hydra.output_subdir 改写为空，从而禁止创建子目录。

```shell
$ python 2.2_output_working_dir.py db.user=ley hydra.job.chdir=True hydra.output_subdir=null

Working directory : /Users/yule/Desktop/code/Hydra/outputs/2024-05-29/17-17-26
Output directory  : /Users/yule/Desktop/code/Hydra/outputs/2024-05-29/17-17-26
```

```shell
$ tree -a outputs/2024-05-29/17-17-26

outputs/2024-05-29/17-17-26
└── 2.2_output_working_dir.log
```

可以看到添加 `hydra.output_subdir=null`之后就没有 `.hydra`目录生成了。也可以将 `hydra.output_subdir=ley`将 `.hydra`目录名替换为 `ley`

### Accessing the original working directory in your application

上文提到可以设置 `hydra.job.chdir=True` 来更改python当前工作目录, 当然我们可以获得原始的工作目录, 通过 `get_original_cwd()` and `to_absolute_path()` in `hydra.utils`:

```python
from hydra.utils import get_original_cwd, to_absolute_path

@hydra.main(version_base=None)
def my_app(_cfg: DictConfig) -> None:
    print(f"Current working directory : {os.getcwd()}")
    print(f"Orig working directory    : {get_original_cwd()}")
    print(f"to_absolute_path('foo')   : {to_absolute_path('foo')}")
    print(f"to_absolute_path('/foo')  : {to_absolute_path('/foo')}")

if __name__ == "__main__":
    my_app()
```

```shell
Current working directory  : /Users/omry/dev/hydra/outputs/2019-10-23/10-53-03
Original working directory : /Users/omry/dev/hydra
to_absolute_path('foo')    : /Users/omry/dev/hydra/foo
to_absolute_path('/foo')   : /foo
```

工作目录的名称可以[here](https://hydra.cc/docs/configure_hydra/workdir/)自定义

## Logging

Hydra使用python的logging模块。
在默认情况下, Hydra logs at the **INFO level** to both the console and a log file in the automatic working directory.

可以通过设置 `hydra.verbose=true`使Hydra记录 `DEBUG`级别的log

- hydra.verbose=true : Sets the log level of all loggers to DEBUG
- hydra.verbose=NAME : Sets the log level of the logger NAME to DEBUG.Equivalent to import logging; logging.getLogger(NAME).setLevel(logging.DEBUG).
- hydra.verbose=[NAME1,NAME2]: Sets the log level of the loggers NAME1 and NAME2 to DEBUG

```shell
$ python my_app.py hydra.verbose=true
```

You can disable the logging output by setting `hydra/job_logging` to disabled
You can also set `hydra/job_logging=none` and `hydra/hydra_logging=none` if you do not want Hydra to configure the logging.

Logging 可以在[here](https://hydra.cc/docs/configure_hydra/logging/)被自定义

## Debugging

可以使用 `--cfg`通过不运行代码来获取config配置

```shell
$ python 1.1_get_started.py --cfg job

db:
  driver: mysql
  user: omry
  pass: secret
```

The `--cfg` option takes one argument indicating which part of the config to print:

- job: Your config
- hydra: Hydra's config
- all: The full config, which is a union of job and hydra.

You can use --package or -p to display a subset of the configuration:

```shell
$ python 1.1_get_started.py --cfg job --package db
# @package db
driver: mysql
user: omry
pass: secret
```

The --info flag can provide information about various aspects of Hydra and your application:

  --info all: Default behavior, prints everything
  --info config: Prints information useful to understanding the config composition:
  Config Search Path, Defaults Tree, Defaults List and the final config.
  --info defaults: Prints the Final Defaults List
  --info defaults-tree: Prints the Defaults Tree
  --info plugins: Prints information about installed plugins

## Tab completion

不重要, 过了
