# 部署记录

## 当前线上地址

- 公网访问地址：`http://43.163.233.104/`
- Flask 监听端口：`5000`
- nginx 对外端口：`80`

## 当前部署方式

服务器环境：

- 系统：OpenCloudOS
- 用户：`root`
- Python 环境：conda `lu_store`

当前应用运行方式：

```bash
cd /root/lu_store
conda activate lu_store
nohup python app.py > app.log 2>&1 &
```

当前 nginx 作用：

- 监听 `80` 端口
- 反向代理到 `http://127.0.0.1:5000`

## 常用命令

### 服务器更新代码

```bash
cd /root/lu_store
git pull
```

### 启动应用

```bash
cd /root/lu_store
conda activate lu_store
nohup python app.py > app.log 2>&1 &
```

### 查看进程

```bash
ps aux | grep app.py
ss -ltnp | grep 5000
```

### 停止应用

```bash
pkill -f "python app.py"
```

### 查看日志

```bash
tail -f /root/lu_store/app.log
```

### 检查 nginx

```bash
nginx -t
systemctl status nginx --no-pager
curl -I http://127.0.0.1/
```

## 当前已知事实

- Flask 已改为 `debug=False`
- 线上运行不再使用自动重载
- 当前方式适合原型阶段
- 如果后续需要更稳定的长期运行，下一步可以切换到 `gunicorn + systemd`
