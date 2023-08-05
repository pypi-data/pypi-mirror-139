# envx
![](https://img.shields.io/badge/Python-3.8.6-green.svg)

#### 介绍
环境信息的管理模块
- 使用目录
    - Windows 系统
    ```text
    使用目录：C:\env\
    ```
    
    - macOS 系统
    ```text
    使用目录：/Users/env/
    ```
    
    - Linux 系统
    ```text
    使用目录：/env/
    ```

- 文件内容格式
```text
HOST=192.168.0.1
PORT=6379
```

- 读取结果格式
```json
{
  "HOST": "192.168.0.1", 
  "PORT": "6379"
}
```


#### 安装教程

1.  pip安装
```shell script
pip install envx
```
2.  pip安装（使用淘宝镜像加速）
```shell script
pip install envx -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1.  demo
```python
import envx
redis_env = envx.read('redis.env')
```

2.  文件名区分大小写