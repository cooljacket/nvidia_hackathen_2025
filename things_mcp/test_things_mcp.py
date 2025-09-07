#!/usr/bin/env python3
"""
Things MCP Server 测试脚本
"""

import json
from things_mcp_server import add_item, search_items, list_all_items


def test_things_mcp():
    """测试Things MCP服务器功能"""
    
    print("=== Things MCP Server 测试 ===\n")
    
    # 测试数据
    test_items = [
        "电动牙刷备用刷头，6个，放在储物柜第三排柜子的左侧",
        "小米充电宝，20000mAh，黑色，放在书桌抽屉里",
        "蓝牙耳机，AirPods Pro，白色，在床头柜上",
        "USB数据线，Type-C，2米长，在电脑包里",
        "维生素C片，100片装，放在药箱里",
        "笔记本电脑充电器，联想ThinkPad，在办公桌下面"
    ]
    
    print("1. 测试添加物品记录...")
    for i, item in enumerate(test_items, 1):
        result = add_item(item)
        print(f"   {i}. {result['message']}")
    
    print("\n2. 测试列出所有物品...")
    all_items = list_all_items()
    print(f"   {all_items['message']}")
    
    print("\n3. 测试语义化搜索...")
    search_queries = [
        "牙刷",
        "充电宝",
        "耳机",
        "数据线",
        "维生素",
        "充电器"
    ]
    
    for query in search_queries:
        print(f"\n   搜索: '{query}'")
        result = search_items(query, limit=3)
        
        if result['success'] and result['items']:
            for item in result['items']:
                similarity = item['similarity']
                description = item['description']
                print(f"     相似度: {similarity:.3f} - {description}")
        else:
            print(f"     {result['message']}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_things_mcp()