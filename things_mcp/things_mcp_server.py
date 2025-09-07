#!/usr/bin/env python3
"""
Things MCP Server - 物品管理MCP服务器
提供物品记录和语义化查询功能
"""

import sqlite3
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel


class ItemRecord(BaseModel):
    """物品记录模型"""
    id: Optional[int] = None
    description: str
    embedding: Optional[List[float]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ThingsMCPServer:
    """物品管理MCP服务器"""
    
    def __init__(self, db_path: str = "things.db", use_local_embedding: bool = True):
        self.db_path = db_path
        self.use_local_embedding = use_local_embedding
        
        # 初始化数据库
        self._init_database()
        
        # 初始化嵌入模型
        if use_local_embedding:
            print("正在加载本地嵌入模型...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = None
            
        # 配置OpenAI客户端（用于Ollama）
        self.openai_client = openai.OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Ollama不需要真实的API key
        )
    
    def _init_database(self):
        """初始化SQLite数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                embedding TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_embedding(self, text: str) -> List[float]:
        """获取文本嵌入向量"""
        if self.use_local_embedding and self.embedding_model:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        else:
            # 使用Ollama生成嵌入（如果支持）
            try:
                response = self.openai_client.embeddings.create(
                    model="nomic-embed-text",  # 或其他支持的嵌入模型
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"获取嵌入向量失败: {e}")
                return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        if not vec1 or not vec2:
            return 0.0
        
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    async def add_item(self, description: str) -> Dict[str, Any]:
        """添加物品记录"""
        try:
            # 生成嵌入向量
            embedding = self._get_embedding(description)
            
            # 保存到数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO items (description, embedding, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (description, json.dumps(embedding), now, now))
            
            item_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": f"成功添加物品记录，ID: {item_id}",
                "item_id": item_id,
                "description": description
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"添加物品记录失败: {str(e)}"
            }
    
    async def search_items(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """语义化搜索物品"""
        try:
            # 获取查询的嵌入向量
            query_embedding = self._get_embedding(query)
            
            if not query_embedding:
                return {
                    "success": False,
                    "message": "无法生成查询嵌入向量"
                }
            
            # 从数据库获取所有物品
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, description, embedding, created_at FROM items')
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return {
                    "success": True,
                    "message": "暂无物品记录",
                    "items": []
                }
            
            # 计算相似度并排序
            results = []
            for row in rows:
                item_id, description, embedding_str, created_at = row
                
                if embedding_str:
                    try:
                        item_embedding = json.loads(embedding_str)
                        similarity = self._cosine_similarity(query_embedding, item_embedding)
                        
                        results.append({
                            "id": item_id,
                            "description": description,
                            "similarity": similarity,
                            "created_at": created_at
                        })
                    except json.JSONDecodeError:
                        continue
            
            # 按相似度排序
            results.sort(key=lambda x: x["similarity"], reverse=True)
            
            # 返回前N个结果
            top_results = results[:limit]
            
            return {
                "success": True,
                "message": f"找到 {len(top_results)} 个相关物品",
                "query": query,
                "items": top_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"搜索物品失败: {str(e)}"
            }
    
    async def list_all_items(self) -> Dict[str, Any]:
        """列出所有物品"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, description, created_at FROM items ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            items = []
            for row in rows:
                items.append({
                    "id": row[0],
                    "description": row[1],
                    "created_at": row[2]
                })
            
            return {
                "success": True,
                "message": f"共有 {len(items)} 个物品记录",
                "items": items
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"获取物品列表失败: {str(e)}"
            }


# 创建MCP服务器实例
things_server = ThingsMCPServer()

# 业务逻辑函数（可直接调用）
async def add_item_async(description: str) -> Dict[str, Any]:
    """添加物品记录（异步版本）"""
    return await things_server.add_item(description)

async def search_items_async(query: str, limit: int = 5) -> Dict[str, Any]:
    """搜索物品（异步版本）"""
    return await things_server.search_items(query, limit)

async def list_all_items_async() -> Dict[str, Any]:
    """列出所有物品（异步版本）"""
    return await things_server.list_all_items()

# 同步包装函数（用于直接调用）
def add_item(description: str) -> Dict[str, Any]:
    """添加物品记录（同步版本）"""
    return asyncio.run(add_item_async(description))

def search_items(query: str, limit: int = 5) -> Dict[str, Any]:
    """搜索物品（同步版本）"""
    return asyncio.run(search_items_async(query, limit))

def list_all_items() -> Dict[str, Any]:
    """列出所有物品（同步版本）"""
    return asyncio.run(list_all_items_async())

# 创建FastMCP应用
mcp = FastMCP("Things MCP Server")

@mcp.tool()
async def add_item_tool(description: str) -> str:
    """
    添加物品记录
    
    Args:
        description: 物品的详细描述，包括名称、数量、位置等信息
        
    Returns:
        添加结果的JSON字符串
    """
    result = await add_item_async(description)
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
async def search_items_tool(query: str, limit: int = 5) -> str:
    """
    语义化搜索物品
    
    Args:
        query: 要搜索的物品名称或描述
        limit: 返回结果的最大数量，默认为5
        
    Returns:
        搜索结果的JSON字符串
    """
    result = await search_items_async(query, limit)
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
async def list_all_items_tool() -> str:
    """
    列出所有物品记录
    
    Returns:
        所有物品记录的JSON字符串
    """
    result = await list_all_items_async()
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import uvicorn
    
    print("启动 Things MCP Server...")
    print("可用工具:")
    print("1. add_item - 添加物品记录")
    print("2. search_items - 语义化搜索物品")
    print("3. list_all_items - 列出所有物品")
    
    # 运行MCP服务器
    mcp.run()