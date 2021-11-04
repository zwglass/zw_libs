# 测试 zw lib 操作 postgresql (docker环境)

### 先创建 docker image: zwglass/test_zwdblib_postgresql

```
cd /Users/zhaoshenghua/development/shell_text/db/zw_db_lib/test_project/test_postgresql_docker           # 进入项目文件夹
docker build -t zwglass/test_zwdblib_postgresql:1.0 .
```

### 启动 docker 容器

```
cd /Users/zhaoshenghua/development/shell_text/db/zw_db_lib/test_project/test_postgresql_docker
docker-compose up -d --build
```
