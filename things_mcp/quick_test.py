#!/usr/bin/env python3
"""
快速验证脚本 - 测试Things MCP Server是否正常工作
"""

def quick_test():
    """快速测试基本功能"""
    print("=== Things MCP Server 快速测试 ===\n")
    
    try:
        # 导入函数
        from things_mcp_server import add_item, search_items, list_all_items
        print("✓ 成功导入所有函数")
        
        # 测试添加物品
        print("\n1. 测试添加物品...")
        result = add_item("测试物品：苹果手机充电线，白色，放在书桌抽屉")
        if result['success']:
            print(f"✓ {result['message']}")
        else:
            print(f"✗ {result['message']}")
            return False
        
        # 测试列出物品
        print("\n2. 测试列出物品...")
        result = list_all_items()
        if result['success']:
            print(f"✓ {result['message']}")
            if result['items']:
                print(f"   最新物品: {result['items'][0]['description']}")
        else:
            print(f"✗ {result['message']}")
            return False
        
        # 测试搜索
        print("\n3. 测试语义搜索...")
        result = search_items("充电线", limit=1)
        if result['success']:
            print(f"✓ {result['message']}")
            if result['items']:
                item = result['items'][0]
                print(f"   找到物品: {item['description']}")
                print(f"   相似度: {item['similarity']:.3f}")
        else:
            print(f"✗ {result['message']}")
            return False
        
        print("\n=== 所有测试通过！✓ ===")
        return True
        
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        print("请先安装依赖: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Things MCP Server 工作正常！")
        print("\n下一步可以:")
        print("1. 运行完整测试: python test_things_mcp.py")
        print("2. 启动交互模式: python client_example.py")
        print("3. 启动MCP服务器: python things_mcp_server.py")
    else:
        print("\n❌ 存在问题，请检查错误信息")