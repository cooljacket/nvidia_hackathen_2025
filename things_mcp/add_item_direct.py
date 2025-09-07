#!/usr/bin/env python3
"""
直接添加物品到Things MCP系统
绕过MCP服务器接口，避免事件循环冲突
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

# 导入things_mcp_server中的函数
from things_mcp_server import add_item


if __name__ == "__main__":
    # 获取命令行参数中的物品描述
    if len(sys.argv) > 1:
        description = ' '.join(sys.argv[1:])
    else:
        description = "测试物品"
        print("警告: 未提供物品描述，使用默认描述。")
        print("使用方法: python add_item_direct.py 物品描述")
    
    try:
        # 直接调用添加物品的函数
        result = add_item(description)
        
        # 打印结果
        if result.get("success", False):
            print(f"✅ 成功: {result.get('message')}")
            print(f"   ID: {result.get('item_id')}")
            print(f"   描述: {result.get('description')}")
        else:
            print(f"❌ 失败: {result.get('message')}")
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")