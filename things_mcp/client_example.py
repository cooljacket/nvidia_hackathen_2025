#!/usr/bin/env python3
"""
Things MCP Server 客户端示例
演示如何与MCP服务器交互
"""

import asyncio
import json
from things_mcp_server import add_item, search_items, list_all_items


def demo_usage():
    """演示MCP服务器的使用"""
    
    print("=== Things MCP Server 客户端演示 ===\n")
    
    # 示例1: 添加物品
    print("1. 添加物品记录...")
    items_to_add = [
        "电动牙刷备用刷头，6个，放在储物柜第三排柜子的左侧",
        "小米充电宝，20000mAh，黑色，放在书桌抽屉里",
        "蓝牙耳机，AirPods Pro，白色，在床头柜上",
        "USB数据线，Type-C，2米长，在电脑包里"
    ]
    
    for item_desc in items_to_add:
        result = add_item(item_desc)
        print(f"   ✓ {result['message']}")
    
    print("\n2. 列出所有物品...")
    all_items = list_all_items()
    print(f"   {all_items['message']}")
    
    for item in all_items['items'][:3]:  # 只显示前3个
        print(f"   - {item['description']}")
    
    print("\n3. 语义化搜索演示...")
    search_queries = [
        "牙刷头",
        "充电设备",
        "音频设备",
        "连接线"
    ]
    
    for query in search_queries:
        print(f"\n   搜索: '{query}'")
        result = search_items(query, limit=2)
        
        if result['success'] and result['items']:
            for item in result['items']:
                similarity = item['similarity']
                description = item['description']
                print(f"     相似度: {similarity:.3f} - {description[:50]}...")
        else:
            print(f"     {result['message']}")
    
    print("\n=== 演示完成 ===")


def interactive_mode():
    """交互模式"""
    print("\n=== 交互模式 ===")
    print("输入命令:")
    print("1. add <物品描述> - 添加物品")
    print("2. search <查询词> - 搜索物品")
    print("3. list - 列出所有物品")
    print("4. quit - 退出")
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if command.lower() == 'quit':
                break
            elif command.lower() == 'list':
                result = list_all_items()
                print(f"\n{result['message']}")
                for item in result['items']:
                    print(f"  {item['id']}. {item['description']}")
                    
            elif command.startswith('add '):
                description = command[4:].strip()
                if description:
                    result = add_item(description)
                    print(f"\n{result['message']}")
                else:
                    print("请提供物品描述")
                    
            elif command.startswith('search '):
                query = command[7:].strip()
                if query:
                    result = search_items(query, limit=5)
                    print(f"\n{result['message']}")
                    for item in result['items']:
                        similarity = item['similarity']
                        description = item['description']
                        print(f"  相似度: {similarity:.3f} - {description}")
                else:
                    print("请提供搜索词")
            else:
                print("未知命令，请重试")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"错误: {e}")
    
    print("\n再见！")


def main():
    """主函数"""
    print("选择模式:")
    print("1. 演示模式")
    print("2. 交互模式")
    
    try:
        choice = input("请选择 (1/2): ").strip()
        
        if choice == '1':
            demo_usage()
        elif choice == '2':
            interactive_mode()
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\n程序已退出")


if __name__ == "__main__":
    main()