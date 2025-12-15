# Moments 项目贡献指南

为了确保协作过程顺畅高效，我们制定了以下贡献流程和规范，请在提交贡献前仔细阅读。

## GitHub 协作开发流程

### 1. 贡献方式

本项目采用 Fork + Pull Request 的开发模式。

#### 1.1. Fork 仓库
1. 访问项目的 GitHub 主页：`https://github.com/nightwalkerkkk123/Moments.git`
2. 点击右上角的 "Fork" 按钮，将项目复制到你自己的 GitHub 账号下。

现在，你账号下的 Moments 仓库就是原始仓库的一个副本。

#### 1.2. 克隆 (Clone) 到本地
将你 Fork 后的仓库克隆到你的本地开发环境：

```bash
git clone https://github.com/你的用户名/Moments.git
cd Moments
```

#### 1.3. 配置远程上游 (Upstream) 仓库
为了能及时同步原始仓库的最新代码，需要配置一个 upstream remote：

```bash
git remote add upstream https://github.com/nightwalkerkkk123/Moments.git
```

你可以通过 `git remote -v` 查看配置是否成功。

### 2. 开发新功能或修复 Bug

在开始编码前，请确保你的本地仓库是最新的。

#### 2.1. 同步最新代码
```bash
# 切换到开发分支
git checkout develop

# 从 upstream 拉取最新代码
git pull upstream develop
```

#### 2.2. 创建新分支 (Branch)
为每一个新功能、Bug 修复或文档更新创建一个独立的分支。这能保持主分支的干净和稳定。

分支命名规范：
- 功能开发：`feature/功能名称` 或 `feature/简短描述` (例如：`feature/user-authentication`)
- Bug 修复：`fix/问题描述` (例如：`fix/login-error`)
- 文档更新：`docs/文档名称` (例如：`docs/api-reference`)

```bash
# 创建并切换到新分支
git checkout -b feature/your-feature-name
```

#### 2.3. 进行开发
在你的新分支上进行编码。请遵循项目的代码规范。

### 3. 提交 Pull Request (PR)

当你完成开发并测试通过后，就可以向原始仓库提交 PR 了。

#### 3.1. 提交 (Commit) 你的更改
在提交前，请确保你已经将所有修改的文件添加到暂存区。

```bash
# 查看更改
git status
git diff

# 添加文件
git add .

# 提交
git commit -m "feat: add user login functionality"
```

**Commit Message 规范：**
建议遵循 Conventional Commits 规范，例如：
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码风格调整（不影响代码逻辑）
- `refactor:` 代码重构
- `test:` 添加或修改测试
- `chore:` 构建过程或辅助工具的变动

#### 3.2. 推送到你的 Fork 仓库
```bash
git push origin feature/your-feature-name
```

#### 3.3. 创建 Pull Request
1. 访问你 Fork 的仓库在 GitHub 上的页面。
2. 你会看到一个提示，问你是否要为刚刚推送的分支创建一个 Pull Request，点击 "Compare & pull request"。
3. 如果没有自动提示，可以手动进入 "Pull requests" 标签页，然后点击 "New pull request"。
4. **重要：**在 "base repository" 选择 `nightwalkerkkk123/Moments` 和 `develop` 分支。在 "head repository" 选择你的 Fork 和你刚刚推送的分支。
5. 填写 PR 的标题和描述：
   - **标题：**清晰、简洁地描述你的更改。
   - **描述：**详细说明你解决了什么问题、实现了什么功能、以及任何需要 reviewer 特别注意的地方。
6. 点击 "Create pull request"。

### 4. 代码规范

为了保证代码质量和风格一致性，请遵守以下规范：

- **代码风格：**请遵循项目中已有的代码风格。如果项目使用了 ESLint、Prettier 等工具，请确保在提交前运行相关命令并修复所有错误和警告。
- **类型检查：**如果项目使用 TypeScript，请确保类型定义完整且正确。
- **测试：**
  - 新增功能时，请为其编写相应的单元测试或集成测试。
  - 修复 Bug 时，请添加一个测试用例来防止该 Bug 再次出现。
  - 确保所有现有测试在你的更改后仍然通过。
- **文档：**
  - 新增功能或修改 API 时，请同步更新相关的文档（如 README.md、API.md 等）。

### 5. 审核 (Review) 流程

1. 提交 PR 后，项目管理者（或指定的审核者）会收到通知。
2. 审核者会对你的代码进行审查，可能会提出一些修改意见。
3. 你需要根据审核意见在同一个分支上进行修改，并再次 `git push`。PR 会自动更新。
4. 这个过程可能会重复几次，直到审核者认为代码质量达标。

### 6. 合并 (Merge)

- 只有当 PR 经过至少一名项目管理者审核通过后，并且所有自动化检查（如 CI 测试、代码风格检查）都通过时，才能被合并。
- 通常由项目管理者执行合并操作。
- 合并方式一般推荐使用 "Squash and merge"，这样可以将 PR 中的所有 commits 压缩成一个，使主分支的提交历史更加清晰整洁。合并时，请确保填写一个清晰的合并信息。

### 7. 后续操作

PR 被合并后，你可以：

1. 在 GitHub 上删除你用于此 PR 的分支。
2. 在你的本地仓库中，同步上游仓库的最新代码，并删除你的本地分支：

```bash
# 切换到 develop 分支
git checkout develop

# 从 upstream 拉取最新代码（包含你刚刚合并的更改）
git pull upstream develop

# 删除已合并的本地分支
git branch -d feature/your-feature-name
```

## 开发环境配置

### 后端开发环境

1. **安装 Python 依赖**
   ```bash
   cd DjangoProject
   pip install -r requirements.txt
   ```

2. **运行 Django 开发服务器**
   ```bash
   python manage.py runserver
   ```

### 前端开发环境

1. **安装前端依赖**
   ```bash
   cd frontend/uni-preset-vue-vite
   npm install
   ```

2. **运行前端开发服务器**
   ```bash
   npm run dev
   ```

## 项目结构说明

```
Moments/
├── DjangoProject/          # Django 后端项目
│   ├── api/               # API 应用
│   ├── DjangoProject/     # Django 项目配置
│   └── requirements.txt   # Python 依赖
├── frontend/              # 前端项目
│   └── uni-preset-vue-vite/ # Vue + Vite 项目
├── README.md              # 项目说明
└── CONTRIBUTING.md        # 贡献指南
```

## 联系方式

如有任何问题或建议，欢迎通过以下方式联系：
- 提交 Issue
- 发送 Pull Request
- 联系项目维护者

感谢你对 Moments 项目的贡献！