# Configuring Hydra
## Introduction
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