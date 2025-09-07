#!/bin/bash
# Things MCP Server 启动脚本

echo "=== Things MCP Server 启动 ==="

# 检查Python版本
python3 --version

# 安装依赖
echo "安装依赖..."
pip3 install -r requirements.txt

# 启动服务器
echo "启动服务器..."
python3 things_mcp_server.py