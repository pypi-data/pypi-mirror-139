# fastmongo
![](https://img.shields.io/badge/Python-3.8.6-green.svg)

#### 介绍
快速使用pymongo

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip install fastmongo
```
2.  pip安装（使用阿里云镜像加速）
```shell script
pip install fastmongo -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1.  demo
```python
import fastmongo
query_res = fastmongo.safe_find(db='test', collection='test')
```