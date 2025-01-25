# 安装说明

## 系统要求

- Python >= 3.7
- 操作系统：Windows/Linux/macOS



## 依赖包

主要依赖包及其版本要求：

- numpy >= 1.21.0
- scipy >= 1.7.0
- pandas >= 1.3.0
- matplotlib >= 3.4.0
- mne >= 1.0.0


## 可能遇到的问题

### 1. 安装 MNE 失败

如果安装 MNE 包时遇到问题，可以尝试：

```bash
pip install --upgrade pip
pip install mne --no-deps
pip install -r requirements.txt
```

### 2. 中文显示问题

如果可视化结果中的中文显示为方框，需要确保：

1. Windows 系统：
   - 安装了微软雅黑字体
   - 在代码中设置 `plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']`

2. Linux 系统：
   - 安装文泉驿微米黑字体
   - 在代码中设置 `plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']`

3. macOS 系统：
   - 使用系统自带的华文黑体
   - 在代码中设置 `plt.rcParams['font.sans-serif'] = ['STHeiti']`
