# Things MCP Server 安装指南

## 系统要求

- Python 3.8+
- 至少2GB可用内存（用于嵌入模型）
- 网络连接（首次下载模型时）

## 安装步骤

### 1. 克隆或下载项目

```bash
# 如果使用git
git clone <repository-url>
cd things_mcp

# 或者直接下载并解压到目录
```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 3. （可选）安装和配置Ollama

如果你想使用Ollama作为嵌入模型提供者：

```bash
# 安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 启动Ollama服务
ollama serve

# 在新终端中拉取嵌入模型
ollama pull nomic-embed-text
```

## 快速开始

### 方法1: 使用启动脚本

```bash
python run_server.py
```

### 方法2: 直接运行服务器

```bash
python things_mcp_server.py
```

### 方法3: 运行客户端演示

```bash
python client_example.py
```

## 配置选项

### 数据库位置

默认情况下，SQLite数据库文件`things.db`会在项目根目录创建。你可以在`things_mcp_server.py`中修改路径：

```python
things_server = ThingsMCPServer(db_path="custom_path/things.db")
```

### 嵌入模型选择

项目支持两种嵌入模型：

1. **本地模型**（默认）: `sentence-transformers/all-MiniLM-L6-v2`
2. **Ollama模型**: `nomic-embed-text`

在`ThingsMCPServer`初始化时设置：

```python
# 使用本地模型
server = ThingsMCPServer(use_local_embedding=True)

# 使用Ollama模型
server = ThingsMCPServer(use_local_embedding=False)
```

## 测试安装

运行测试脚本验证安装：

```bash
python test_things_mcp.py
```

## 故障排除

### 1. 依赖安装失败

```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. 嵌入模型下载失败

```bash
# 手动下载模型
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### 3. Ollama连接失败

确保Ollama服务正在运行：

```bash
# 检查Ollama状态
curl http://localhost:11434/api/tags

# 重启Ollama服务
ollama serve
```

### 4. 数据库权限问题

确保项目目录有写权限：

```bash
chmod 755 .
```

## 性能优化

### 1. 使用GPU加速（如果可用）

安装GPU版本的PyTorch：

```bash
# CUDA版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# MPS版本（Apple Silicon）
pip install torch torchvision torchaudio
```

### 2. 调整嵌入模型

对于更好的中文支持，可以使用：

```python
self.embedding_model = SentenceTransformer('shibing624/text2vec-base-chinese')
```

## 集成到MCP客户端

将`mcp_config.json`添加到你的MCP客户端配置中：

```json
{
  "mcpServers": {
    "things-mcp": {
      "command": "python",
      "args": ["/path/to/things_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

## 下一步

- 查看 [README.md](README.md) 了解详细功能
- 运行 [client_example.py](client_example.py) 体验交互功能
- 根据需要修改配置和扩展功能