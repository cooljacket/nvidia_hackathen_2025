#!/usr/bin/env python3
"""
Things MCP Server 启动脚本
"""

import sys
import subprocess
import os
from pathlib import Path


def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastmcp
        import sentence_transformers
        import openai
        import numpy
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False


def check_ollama():
    """检查Ollama是否运行"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✓ Ollama服务正在运行")
            return True
        else:
            print("⚠ Ollama服务未响应")
            return False
    except Exception:
        print("⚠ Ollama服务未运行（将使用本地嵌入模型）")
        return False


def main():
    """主函数"""
    print("=== Things MCP Server 启动器 ===\n")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查Ollama（可选）
    check_ollama()
    
    print("\n启动 Things MCP Server...")
    
    # 启动服务器
    try:
        from things_mcp_server import mcp
        print("服务器启动成功！")
        print("\n可用工具:")
        print("- add_item: 添加物品记录")
        print("- search_items: 语义化搜索物品")
        print("- list_all_items: 列出所有物品")
        print("\n按 Ctrl+C 停止服务器")
        
        # mcp.run()
        mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")

        
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()