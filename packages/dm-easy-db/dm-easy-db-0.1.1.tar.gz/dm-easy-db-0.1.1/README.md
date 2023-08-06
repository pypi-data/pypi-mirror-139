# db公共模块

通用的数据库连接模块，目前能支持到mysql、pg、hive、impala、phoenix的连接和操作

## 功能规划

- [x] 基础功能：通用的连接接口，避免频繁操作原始的数据库接口
- [ ] 线程池
- [ ] 异步操作

## 使用说明

```python
# 引入相应的数据库连接 目前支持mysql、impala、hive、pg、phoenix
# 分别对应MysqlDB、ImpalaDB、HiveDB、PgDB、PhoenixDB
from easy_db.db import MysqlDB

mysql_db = MysqlDB(
    user='bigdata',
    password='bluemoon2018#',
    database='xxl-job',
    host='192.168.235.3',
    port=3306
)

res = mysql_db.select('select * from demo')
print(res)

```

### 安装说明

#### 方法1

1. 使用git clone 把项目下载到本地
2. 进入项目目录，运行python setup.py install 安装

#### 方法2

直接把db.py 复制到项目中，引入相关的函数和类即可使用

#### 方法3

pip install dm-easy-db

Package name: dm-easy-db
Ver: 0.1.0
