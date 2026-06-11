# lu_store

一个基于 Flask 的商品描述工具原型项目。

当前阶段重点不是业务功能，而是先把最小网站原型和公网部署链路跑通。

## 当前状态

- 已完成最小 Flask 原型页
- 已推送到 GitHub 仓库
- 已部署到腾讯云服务器
- 已通过 nginx 反向代理到 `http://43.163.233.104/`
- 当前后端以 `nohup python app.py > app.log 2>&1 &` 方式后台运行

## 本地开发

项目当前主要使用 conda 环境。

```powershell
conda activate lu_store
pip install -r requirements.txt
python app.py
```

本地访问：

```text
http://127.0.0.1:5000/
```

## 项目结构

```text
lu_store/
  app.py
  requirements.txt
  templates/
    index.html
  static/
    style.css
  docs/
    DEPLOYMENT.md
    TODO.md
```

## 相关文档

- [部署记录](docs/DEPLOYMENT.md)
- [待办清单](docs/TODO.md)
