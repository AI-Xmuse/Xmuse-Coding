# 开发指南

本指南将帮助你了解如何参与 EEG-Analyze 的开发。

## 开发环境设置

1. 克隆仓库并安装开发依赖：

```bash
# 克隆仓库
git clone https://github.com/your-username/eeg-analyze.git
cd eeg-analyze

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install -e .
```

2. 安装额外的开发工具：

```bash
pip install pytest pytest-cov black flake8 mypy
```

## 代码风格

我们使用以下工具来保证代码质量：

1. Black 用于代码格式化：
```bash
black eeg_analyze tests
```

2. Flake8 用于代码检查：
```bash
flake8 eeg_analyze tests
```

3. MyPy 用于类型检查：
```bash
mypy eeg_analyze
```

## 项目结构

```
eeg_analyze/
├── __init__.py
├── analyzer.py      # 分析器模块
├── data_loader.py   # 数据加载模块
├── preprocessor.py  # 预处理模块
├── visualizer.py    # 可视化模块
└── utils/          # 工具函数
    └── __init__.py

tests/              # 测试目录
├── __init__.py
├── test_analyzer.py
├── test_data_loader.py
├── test_preprocessor.py
└── test_visualizer.py

docs/               # 文档目录
├── api/           # API文档
├── guide/         # 用户指南
└── examples/      # 示例代码
```

## 添加新功能

1. 创建新的功能分支：
```bash
git checkout -b feature/your-feature-name
```

2. 编写代码和测试：
   - 遵循现有的代码风格
   - 添加适当的文档字符串
   - 编写单元测试

3. 运行测试：
```bash
pytest tests/
```

4. 检查代码覆盖率：
```bash
pytest --cov=eeg_analyze tests/
```

## 扩展现有功能

### 1. 添加新的预处理方法

在 `preprocessor.py` 中：

```python
def new_preprocessing_method(data: np.ndarray, **kwargs) -> np.ndarray:
    """
    新的预处理方法
    
    Parameters
    ----------
    data : np.ndarray
        输入数据
    **kwargs : dict
        其他参数
        
    Returns
    -------
    np.ndarray
        处理后的数据
    """
    # 实现你的预处理逻辑
    return processed_data
```

### 2. 添加新的分析方法

在 `analyzer.py` 中：

```python
def new_analysis_method(self, data: np.ndarray, **kwargs) -> dict:
    """
    新的分析方法
    
    Parameters
    ----------
    data : np.ndarray
        输入数据
    **kwargs : dict
        其他参数
        
    Returns
    -------
    dict
        分析结果
    """
    # 实现你的分析逻辑
    return results
```

### 3. 添加新的可视化方法

在 `visualizer.py` 中：

```python
def new_visualization_method(
    self,
    data: np.ndarray,
    save_dir: str,
    **kwargs
) -> None:
    """
    新的可视化方法
    
    Parameters
    ----------
    data : np.ndarray
        输入数据
    save_dir : str
        保存目录
    **kwargs : dict
        其他参数
    """
    # 实现你的可视化逻辑
    plt.savefig(os.path.join(save_dir, 'output.png'))
```

## 文档编写

1. 代码文档：
   - 使用 Google 风格的文档字符串
   - 包含参数说明、返回值说明和示例

2. API 文档：
   - 在 `docs/api/` 目录下添加新文件
   - 使用 Markdown 格式
   - 包含详细的参数说明和示例

3. 用户指南：
   - 在 `docs/guide/` 目录下添加新文件
   - 使用简单明了的语言
   - 提供实际的使用场景

## 提交变更

1. 提交前的检查：
```bash
# 运行所有测试
pytest

# 代码格式化
black .

# 代码检查
flake8

# 类型检查
mypy .
```

2. 提交代码：
```bash
git add .
git commit -m "描述你的改动"
git push origin feature/your-feature-name
```

3. 创建 Pull Request：
   - 提供清晰的描述
   - 列出主要改动
   - 提供测试结果

## 发布新版本

1. 更新版本号：
   - 在 `setup.py` 中
   - 在 `__init__.py` 中
   - 在 `CHANGELOG.md` 中

2. 创建发布标签：
```bash
git tag -a v0.1.0 -m "版本 0.1.0"
git push origin v0.1.0
```

## 最佳实践

1. 代码质量
   - 编写清晰的代码
   - 添加适当的注释
   - 遵循 PEP 8 规范

2. 测试
   - 保持高测试覆盖率
   - 测试边界情况
   - 使用参数化测试

3. 文档
   - 及时更新文档
   - 提供实用的示例
   - 保持文档的一致性

4. 版本控制
   - 使用有意义的提交信息
   - 保持提交历史整洁
   - 及时合并上游更改 