# 贡献指南

感谢您考虑为亚马逊广告智能投放平台做出贡献！

---

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request流程](#pull-request流程)

---

## 行为准则

本项目采用贡献者公约作为行为准则。参与本项目即表示您同意遵守其条款。请阅读 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 了解详情。

---

## 如何贡献

### 报告Bug

如果您发现了bug，请创建一个Issue并包含：

1. **清晰的标题** - 简明扼要地描述问题
2. **详细描述** - 包括预期行为和实际行为
3. **复现步骤** - 逐步说明如何重现问题
4. **环境信息**：
   ```bash
   Python版本: 
   操作系统:
   项目版本:
   ```
5. **相关日志或截图** - 如果有的话

### 建议新功能

如果您有新功能建议，请创建一个Issue并包含：

1. **功能描述** - 详细说明您希望的功能
2. **使用场景** - 这个功能解决什么问题
3. **实现建议** - 如果您有实现想法

### 改进文档

文档改进包括：

- 修正拼写或语法错误
- 添加缺失的文档
- 改进现有文档的清晰度
- 添加更多示例

---

## 开发流程

### 1. Fork仓库

点击GitHub页面右上角的"Fork"按钮

### 2. 克隆您的Fork

```bash
git clone https://github.com/YOUR_USERNAME/amzongtest-advertisement.git
cd amzongtest-advertisement
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

分支命名规范：
- `feature/` - 新功能
- `fix/` - Bug修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关

### 4. 设置开发环境

#### 后端环境

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install cryptography
```

#### 前端环境

```bash
cd frontend
npm install
```

### 5. 进行开发

确保遵循[代码规范](#代码规范)

### 6. 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

**所有测试必须通过才能提交PR**

### 7. 提交更改

遵循[提交规范](#提交规范)

### 8. 推送到您的Fork

```bash
git push origin feature/your-feature-name
```

### 9. 创建Pull Request

遵循[Pull Request流程](#pull-request流程)

---

## 代码规范

### Python代码规范

使用以下工具确保代码质量：

```bash
# 代码格式化
black app/
isort app/

# 代码检查
flake8 app/

# 类型检查
mypy app/
```

#### Python规范要点

- **类型注解**：所有函数必须有类型注解
  ```python
  def calculate_acos(spend: Decimal, sales: Decimal) -> float:
      ...
  ```

- **文档字符串**：使用Google风格
  ```python
  def execute_bidding(keyword_id: str, strategy: str) -> dict:
      """执行竞价策略
      
      Args:
          keyword_id: 关键词ID
          strategy: 策略名称
          
      Returns:
          包含调整结果的字典
          
      Raises:
          ValueError: 当策略名称无效时
      """
      ...
  ```

- **导入顺序**：标准库 → 第三方库 → 本地模块
  ```python
  import os
  from typing import Dict, List
  
  from fastapi import HTTPException
  from sqlalchemy.orm import Session
  
  from app.core.config import settings
  from app.models.models import Keyword
  ```

### TypeScript代码规范

```bash
# 代码格式化
npm run format

# 代码检查
npm run lint

# 类型检查
npm run type-check
```

#### TypeScript规范要点

- **组件命名**：使用PascalCase
  ```typescript
  const DashboardMetrics: React.FC<DashboardProps> = ({ data }) => {
    ...
  }
  ```

- **接口定义**：所有API响应必须有类型定义
  ```typescript
  interface CampaignMetricResponse {
    entity_id: string;
    entity_name: string;
    ...
  }
  ```

- **使用const**：优先使用const，必要时使用let
  ```typescript
  const handleClick = () => { ... };
  let count = 0;
  ```

### 通用规范

- **最大行长度**：100字符
- **缩进**：2空格（TypeScript）或4空格（Python）
- **文件编码**：UTF-8
- **换行符**：LF（Unix风格）

---

## 提交规范

我们遵循[Conventional Commits](https://www.conventionalcommits.org/)规范：

### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建或辅助工具变动
- `ci`: CI配置变动

### Scope范围

- `api`: API相关
- `frontend`: 前端相关
- `backend`: 后端相关
- `models`: 数据模型
- `services`: 业务服务
- `docs`: 文档

### 示例

```bash
# 新功能
git commit -m "feat(api): 添加关键词推荐API"

# Bug修复
git commit -m "fix(bidding): 修复竞价历史记录错误"

# 文档更新
git commit -m "docs: 更新API使用说明"

# 多行提交
git commit -m "feat(dashboard): 实现性能趋势图表

- 添加ACoS趋势线
- 添加ROAS趋势线
- 支持时间范围选择

Closes #123"
```

---

## Pull Request流程

### 创建PR前的检查清单

- [ ] 代码遵循项目代码规范
- [ ] 所有测试通过
- [ ] 新功能有对应的测试
- [ ] 文档已更新（如需要）
- [ ] 提交消息符合规范
- [ ] 分支从最新的main创建

### PR标题格式

```
<type>(<scope>): <description>
```

示例：
- `feat(dashboard): 添加实时数据图表`
- `fix(api): 修复SQL注入风险`

### PR描述模板

```markdown
## 变更类型
- [ ] 新功能
- [ ] Bug修复
- [ ] 重构
- [ ] 文档更新

## 变更说明
<!-- 描述您的变更内容 -->

## 测试说明
<!-- 描述如何测试这些变更 -->

## 相关Issue
<!-- 关联的Issue编号，如 Closes #123 -->

## 截图
<!-- 如果有UI变更，请提供截图 -->
```

### 代码审查

所有PR都需要至少一位维护者审查后才能合并。

审查要点：
1. 代码质量
2. 测试覆盖
3. 文档完整性
4. 性能影响
5. 安全风险

### 合并要求

- 至少1位审查者批准
- 所有CI检查通过
- 无合并冲突
- 分支与main同步

---

## 开发技巧

### 调试技巧

#### 后端调试

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

#### 前端调试

```typescript
console.log('调试信息:', data);
debugger; // 断点
```

### 保持同步

定期同步上游仓库：

```bash
git remote add upstream https://github.com/Nuility/amzongtest-advertisement.git
git fetch upstream
git checkout main
git merge upstream/main
```

---

## 获取帮助

- **文档**: 查看 [README.md](README.md) 和 [docs/](docs/)
- **Issues**: 在Issue中提问
- **讨论**: 使用GitHub Discussions

---

## 许可证

通过贡献代码，您同意您的代码将根据MIT许可证授权。

---

感谢您的贡献！🎉

**Amazon Ads Platform Team**  
**Powered by 华为云 CodeArts**
