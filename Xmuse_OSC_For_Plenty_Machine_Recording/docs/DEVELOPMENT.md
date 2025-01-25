# 开发指南

## 开发环境设置

### 1. 克隆仓库
```bash
git clone https://github.com/AI-Xmuse/Xmuse-Coding.git
cd osc-data-receiver
```

### 2. 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

### 3. 安装开发依赖
```bash
# 安装基本依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 4. 配置开发工具
- 配置 IDE（推荐 PyCharm 或 VSCode）
- 安装推荐的插件：
  - Python
  - Pylint
  - Black Formatter
  - isort
  - mypy

## 代码规范

### 1. PEP 8 规范
- 使用 4 空格缩进
- 行长度限制在 79 字符
- 使用空行分隔函数和类
- 适当的命名规范：
  - 类名使用 CamelCase
  - 函数和变量使用 snake_case
  - 常量使用 UPPER_CASE

### 2. 类型注解
```python
from typing import List, Optional, Dict

def process_data(data: List[float], threshold: Optional[float] = None) -> Dict[str, float]:
    # 函数实现
    pass
```

### 3. 文档字符串
```python
def handle_message(self, port: int, address: str, *args) -> None:
    """处理接收到的 OSC 消息。

    Args:
        port (int): OSC 端口号
        address (str): 信号地址
        *args: 可变参数，包含信号数据

    Returns:
        None

    Raises:
        BufferError: 当缓冲区已满时
    """
    pass
```

### 4. 测试覆盖
- 单元测试覆盖率要求 > 80%
- 关键功能需要 100% 覆盖
- 包含边界条件测试

## 测试指南

### 1. 单元测试
```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_receiver.py

# 运行特定测试类或函数
python -m pytest tests/test_receiver.py::TestOSCDataReceiver::test_initialization
```

### 2. 集成测试
```bash
# 运行集成测试
python -m pytest tests/integration/

# 使用标记运行
python -m pytest -m "integration"
```

### 3. 性能测试
```bash
# 运行性能测试
python -m pytest tests/performance/

# 生成性能报告
python -m pytest --benchmark-only
```

### 4. 覆盖率报告
```bash
# 生成覆盖率报告
python -m pytest --cov=osc_receiver tests/

# 生成 HTML 报告
python -m pytest --cov=osc_receiver tests/ --cov-report=html
```

## 调试技巧

### 1. 日志调试
```python
import logging

logging.debug("详细的调试信息")
logging.info("一般信息")
logging.warning("警告信息")
```

### 2. 使用调试器
```python
import pdb; pdb.set_trace()  # 设置断点
```

### 3. 性能分析
```python
import cProfile
import pstats

# 使用性能分析器
profiler = cProfile.Profile()
profiler.enable()
# 运行代码
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('cumulative')
stats.print_stats()
```

## 发布流程

1. 版本号更新
2. 更新更改日志
3. 运行测试套件
4. 构建分发包
5. 上传到 PyPI

```bash
# 构建分发包
python setup.py sdist bdist_wheel

# 上传到 PyPI
twine upload dist/*
``` 