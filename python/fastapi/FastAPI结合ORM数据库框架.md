# FastAPI结合ORM数据库框架

### fastapi和两款orm类型数据库连接框架兼容较好：

- **SQLAlchemy**
- **Tortoise-ORM**

### 两者都很适配，官方采用**SQLAlchemy**，不过**Tortoise-ORM**的异步特性与fastapi完美契合

官网文档[SQL (关系型) 数据库 - FastAPI (tiangolo.com)](https://fastapi.tiangolo.com/zh/tutorial/sql-databases/)

## SQLAlchemy

```python
pip install sqlalchemy
```

官方示例

创建连接

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

个人习惯使用下面的方式

例如连接mysql

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.base import mysql_username,mysql_password,mysql_host,mysql_port,mysql_db


# 数据库连接字符串
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型
Base = declarative_base()

Base.metadata.create_all(bind=engine)

```

然后创建一个生成器

```python
# models/database.py
from .base import SessionLocal

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db  # 使用生成器确保会话在使用后关闭
    finally:
        db.close()
```

用类映射数据库表

```python
# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime,func
# from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from .base import Base, engine


class IpDisabled(Base):
    __tablename__ = "ip_disabled"
    id = Column(Integer, primary_key=True, index=True)
    host_ip = Column(String(100), unique=True)
    ip = Column(String(100), unique=True)
    create_time = Column(DateTime,default=func.now())
    operator = Column(Integer)


Base.metadata.create_all(bind=engine)
```

接口处使用

```python
@ip_route.get("/disabled")
async def get(page:int = 1,db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
        获取被封禁的IP
    """
    # 使用 ORM 的 session.query() 并获取所有被封禁的 IP
    ips_query = db.query(IpDisabled).order_by("create_time").limit(10).offset(10*(page-1)).all()
    count = db.query(IpDisabled).count()

    # 将查询结果转换为 Pydantic 模型列表
    ips_list = [DisIpItem(id=ip.id, host_ip = ip.host_ip,ip=ip.ip, create_time=str(ip.create_time), operator=ip.operator) for ip in
                ips_query]
    return common.dataReturn(1, msg="disabled_ip", data={"data":ips_list, "total":count})
```

## Tortoise-ORM

创建连接

```python
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
register_tortoise(
    app,
    db_url="mysql://用户名:密码@127.0.0.1:3306/数据库表",
    #需要映射为表的类文件路径
    modules={"models": ["app.models.user_model", "app.models.project_model"]},
    generate_schemas=True,
    add_exception_handlers=True,
   )
```

建立模型

```python
from tortoise import fields, models


# 创建用户模型
class User(models.Model):
    uuid = fields.CharField(max_length=40, pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=80)

    def __str__(self):
        return self.name
```

创建crud方法

```python
from app.models.user_model import User


async def get_user_by_username(username: str):
    return await User.filter(username=username).first()


async def create_user(user_data):
    user_dict = user_data.dict()
    user = await User.create(**user_dict)
    return user
```

接口中调用

```python
from fastapi import APIRouter, HTTPException, Request


from app.controllers.crud import user_crud

@router.post("/login")
async def login(user_login: UserLogin):
    # 检测用户是否存在
    user = await user_crud.get_user_by_username(username=user_login.username)
    if not user:
        return common.dataReturn(code=0, msg="用户名或者密码错误")
    # 验证密码
    if not pwd_context.verify(user_login.password, user.password):
        return common.dataReturn(code=0, msg="用户名或者密码错误")

    return common.dataReturn(code=1, msg="登录成功")
```

