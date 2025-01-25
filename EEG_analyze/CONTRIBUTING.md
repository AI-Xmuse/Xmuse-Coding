# 贡献指南

感谢您对 EEG-Analyze 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 报告问题
- 提交功能建议
- 改进文档
- 提交代码修复
- 添加新功能

## 如何贡献

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的改动 (`git commit -m '添加一些特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 代码风格

- 遵循 PEP 8 规范
- 使用有意义的变量名和函数名
- 添加适当的注释和文档字符串
- 保持代码简洁清晰

## 提交 Pull Request

1. 确保您的代码通过了所有测试
2. 更新相关文档
3. 在 PR 描述中说明您的改动
4. 等待审核和合并

## 报告问题

如果您发现了问题，请：

1. 检查是否已经有相同的问题被报告
2. 提供详细的问题描述
3. 提供复现步骤
4. 说明您的运行环境

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/AI-Xmuse/Xmuse-Coding.git
cd eeg-analyze

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install -e .
```

## 运行测试

```bash
python -m pytest tests/
```

## 文档编写

- 使用 Markdown 格式
- 保持文档的及时更新
- 添加适当的示例代码
- 确保文档的准确性

## 版本发布

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建新的 release tag

## 联系我们

如果您有任何问题，请通过以下方式联系我们：

- 提交 Issue
- 发送邮件至：601625293@qq.com或者support@xmuse.cn

感谢您的贡献！ 