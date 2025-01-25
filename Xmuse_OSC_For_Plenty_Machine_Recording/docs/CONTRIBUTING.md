# 贡献指南

## 提交 Pull Request

### 1. Fork 仓库
- 访问 GitHub 仓库页面
- 点击 "Fork" 按钮创建副本
- 克隆你的 fork 到本地

```bash
git clone https://github.com/AI-Xmuse/Xmuse-Coding.git
cd osc-data-receiver
```

### 2. 创建分支
```bash
# 创建并切换到新分支
git checkout -b feature/amazing-feature

# 或者
git branch feature/amazing-feature
git checkout feature/amazing-feature
```

### 3. 提交代码
```bash
# 添加更改
git add .

# 提交更改
git commit -m "feat: add amazing feature"
```

提交信息格式：
- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- style: 代码格式
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

### 4. 更新文档
- 更新 API 文档
- 添加新功能说明
- 更新使用示例
- 更新测试文档

### 5. 提交 PR
- 推送到你的 fork
```bash
git push origin feature/amazing-feature
```
- 访问原仓库创建 Pull Request
- 填写 PR 描述
- 等待审查和合并

## 代码审查

### 1. 代码质量
- 遵循项目代码规范
- 代码可读性和可维护性
- 适当的注释和文档
- 避免重复代码

### 2. 测试覆盖
- 添加单元测试
- 更新集成测试
- 确保测试通过
- 维持代码覆盖率

### 3. 文档完整性
- API 文档更新
- README 更新
- 示例代码
- 更新日志

### 4. 性能考虑
- 资源使用效率
- 并发处理
- 内存管理
- 错误处理

## 开发流程

### 1. 选择任务
- 查看 Issues
- 认领未分配的任务
- 创建新的 Issue

### 2. 开发
- 遵循开发指南
- 经常同步上游更改
- 保持提交历史清晰

### 3. 测试
- 运行测试套件
- 添加新测试
- 性能测试
- 手动测试

### 4. 提交
- 清晰的提交信息
- 相关的 Issue 引用
- 代码审查修改

## 沟通

### 1. Issue 讨论
- 描述清晰的问题
- 提供复现步骤
- 相关的日志和截图

### 2. PR 讨论
- 详细的变更说明
- 回应审查意见
- 保持积极沟通

### 3. 文档贡献
- 修复文档错误
- 改进文档结构
- 添加使用示例

## 行为准则

1. 尊重所有贡献者
2. 保持专业和友善
3. 接受建设性批评
4. 遵循项目规范 