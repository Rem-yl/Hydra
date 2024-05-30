# Configuring Hydra
## Introduction
这章内容详见[here](https://hydra.cc/docs/configure_hydra/intro/#top-level-hydra-settings)

Hydra也是高度可配置的
Hydra的配置文件由下面几个部分组成:
```yaml
# hydra/config
defaults:
  - job_logging : default     # Job's logging config
  - launcher: basic           # Launcher config
  - sweeper: basic            # Sweeper config
  - output: default           # Output directory
```

### Accessing the Hydra config
有两种方法可以获取Hydra的配置:
1. 在你的config中, 使用`hydra`相对路径
    ```yaml
    # your config.yaml
    config_name: ${hydra:job.name}  # 获取hydra配置
2. 在代码中使用`HydraConfig`接口
   ```python
   from hydra.core.hydra_config import HydraConfig

    @hydra.main()
    def my_app(cfg: DictConfig) -> None:
        print(HydraConfig.get().job.name)
    ```

### Top-level Hydra settings
The following fields are present at the top level of the Hydra Config.

- mode: Optional, one of RUN or MULTIRUN. See multirun for more info.
- searchpath: A list of paths that Hydra searches in order to find configs. See overriding hydra.searchpath
- job_logging and hydra_logging: Configure logging settings. See logging and customizing logging.
- sweeper: Sweeper plugin settings. Defaults to basic sweeper.
- launcher: Launcher plugin settings. Defaults to basic launcher.
- callbacks: Experimental callback support.
- help: Configures your app's --help CLI flag. See customizing application's help.
- hydra_help: Configures the --hydra-help CLI flag.
- output_subdir: Configures the .hydra subdirectory name. See changing or disabling the output subdir.
- verbose: Configures per-file DEBUG-level logging. See logging.