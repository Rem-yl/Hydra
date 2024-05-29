# readme
学习python库-[Hydra](https://hydra.cc/docs/intro/), 用于配置yaml config

## 总结
1. 如果单纯使用`Hydra`做yaml config配置, 可以使用 `compose api`, 但是这样就没有办法使用 --multirun等机器学习调参的功能了;
2. 如果要使用调参功能, 则必须在config/*.yaml文件中把所有的参数全配出来, 然后主逻辑要包含在 `@hydra.main()` 装饰器下面
