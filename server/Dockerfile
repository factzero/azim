# 使用 slim 版本作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖（如果存在 requirements.txt）
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# 暴露应用运行端口
EXPOSE 9981

# 启动命令
CMD ["python3", "server_app.py"]