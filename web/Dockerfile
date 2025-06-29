# 使用官方 Node.js 镜像（建议选择 LTS 版本）
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 拷贝 package.json 和 package-lock.json (如果存在)
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 拷贝项目源码
COPY . .

# 构建项目（如果你是开发环境，可以注释掉这一步）
RUN npm run build

# 暴露运行端口（根据你的项目实际使用的端口进行修改）
EXPOSE 9963

# 启动命令（根据你的启动脚本修改，比如 "preview" "dev"）
CMD ["npm", "run", "preview"]