# Things MCP Server - 物品管理MCP服务器

一个基于FastMCP构建的物品管理服务器，提供智能的物品记录和语义化搜索功能。

## 功能特性

- **物品记录**: 添加物品的详细描述信息
- **语义化搜索**: 使用AI嵌入向量进行智能搜索，不依赖关键词匹配
- **本地化部署**: 支持本地Ollama模型，保护数据隐私
- **轻量级设计**: 适合家庭物品管理场景

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置要求

### 1. 安装Ollama（可选）

如果需要使用Ollama进行嵌入向量生成：

```bash
# 安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 拉取嵌入模型（可选）
ollama pull nomic-embed-text
```

### 2. 本地嵌入模型

默认使用`sentence-transformers`的`all-MiniLM-L6-v2`模型，首次运行时会自动下载。

## 使用方法

### 启动服务器

```bash
python things_mcp_server.py
```

### 可用工具

#### 1. add_item - 添加物品记录

```python
# 示例调用
result = await add_item("电动牙刷备用刷头，6个，放在储物柜第三排柜子的左侧")
```

#### 2. search_items - 语义化搜索物品

```python
# 示例调用
result = await search_items("牙刷头", limit=5)
```

#### 3. list_all_items - 列出所有物品

```python
# 示例调用
result = await list_all_items()
```

## 配置文件

项目包含`mcp_config.json`配置文件，可以直接在支持MCP的客户端中使用。

## 技术架构

- **框架**: FastMCP
- **数据库**: SQLite
- **嵌入模型**: sentence-transformers (本地) 或 Ollama
- **搜索算法**: 余弦相似度匹配

## 示例使用场景

```python
# 添加物品
await add_item("小米充电宝，20000mAh，黑色，放在书桌抽屉里")
await add_item("蓝牙耳机，AirPods Pro，白色，在床头柜上")
await add_item("USB数据线，Type-C，2米长，在电脑包里")

# 搜索物品
await search_items("充电宝")  # 会找到小米充电宝
await search_items("耳机")    # 会找到蓝牙耳机
await search_items("数据线")  # 会找到USB数据线
```

## 注意事项

1. 首次运行时会下载嵌入模型，需要网络连接
2. 数据存储在本地SQLite数据库中
3. 支持中文物品描述和搜索
4. 搜索结果按相似度排序返回

## 扩展功能

可以根据需要扩展以下功能：
- 物品分类管理
- 图片识别和存储
- 位置地图可视化
- 物品状态跟踪（借出/归还）
- 批量导入/导出