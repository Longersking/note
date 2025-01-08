# 数据库迁移

### 使用场景，当需要修改定义的数据库中表的数据时，就可以利用aerich进行迁移改动

例如

```python
class Asset(models.Model):
    aid = fields.CharField(max_length=50, pk=True)
    asset_name = fields.CharField(max_length=150)
    target_name = fields.CharField(max_length=150)
    url = fields.CharField(max_length=500)
    ip = fields.CharField(max_length=250)
    port = fields.CharField(max_length=50)
    pid = fields.CharField(max_length=50)
    project = fields.ForeignKeyRelation('models.Project', related_name='assets')
```

这是一个orm映射的类，现在希望给类添加几个字段，同时同步到数据库中的表中

这个时候就可以用到aerich工具

安装

```python
pip install aerich
```

初始化配置信息

![image-20241003200954825](W:\note\python\fastapi\tortoise数据库迁移\image-20241003200954825.png)

根据此消息可以使用aerich读取对应的数据库信息

```python
aerich init -t app.config.TORTOISE_ORM
```

然后如果是第一次使用的话需要使用此命令

```
aerich init-db
```

初始化

然后修改类

```python
 class Asset(models.Model):   
    aid = fields.CharField(max_length=50, pk=True)
    asset_name = fields.CharField(max_length=150)
    target_name = fields.CharField(max_length=150)
    url = fields.CharField(max_length=500)
    ip = fields.CharField(max_length=250)
    port = fields.CharField(max_length=50)
    cms = fields.CharField(max_length=250)
    res = fields.CharField(max_length=250)
    vul_type = fields.CharField(max_length=50)
    pid = fields.CharField(max_length=50)
    project = fields.ForeignKeyRelation('models.Project', related_name='assets')

```

使用下面命令追踪表变化

```python
aerich migrate
```

最后执行对应的表变化

```python
aerich upgrade
```

![image-20241003201325282](W:\note\python\fastapi\tortoise数据库迁移\image-20241003201325282.png)