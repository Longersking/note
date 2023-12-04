# mysql基本操作

- ```mysql
  show databases; #查看所有数据库
  ```

- ```mysql
  use [数据库];#选择数据库
  ```

- ```mysql
  show tables;#查看当前数据库下所有的表
  ```

- ```mysql
  insert into [表名] values ([字段值1],[字段值2],[字段值3]) ; #向表中插入数据
  ```

- ```mysql 
  delete from [表名] values ([字段值1],[字段值2],[字段值3]); #删除表中部分数据
  ```

- ```mysql 
  update [表名] set 字段1 = 字段值1,where 字段 = 字段值; #修改表中字段1的数据
  ```

- ```mysql
  select * from [表名] where 条件1 and/or 条件2; #根据条件查询表中数据
  ```

  