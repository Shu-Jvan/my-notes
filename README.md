# My Study Notes

I will share my learning insights and study notes here. Welcome to browse my [blog](https://www.cnblogs.com/myInception)

---

## Git 常用操作速查

### 1. 安装 Git

| 场景 | 命令 | 说明 |
| :--- | :--- | :--- |
| 验证安装 | `git --version` | 查看 Git 版本，确认安装成功 |
| 首次配置用户名 | `git config --global user.name "用户名"` | 设置提交记录中的作者名 |
| 首次配置邮箱 | `git config --global user.email "邮箱"` | 设置提交记录中的作者邮箱 |
| 查看已有配置 | `git config --global --list` | 列出所有全局配置 |

### 2. 存档：工作区、暂存区、提交历史

| 场景            | 命令                   | 说明                  |
| :------------ | :------------------- | :------------------ |
| 初始化仓库         | `git init`           | 在当前目录创建 `.git` 仓库   |
| 查看当前状态        | `git status`         | 检查新增 / 修改 / 删除的笔记文件 |
| 添加单个文件        | `git add 文件名`        | 仅暂存指定文件             |
| 添加整个文件夹       | `git add 目录名/`       | 批量暂存文件夹内改动          |
| 添加所有改动（含新建文件） | `git add .`          | 暂存当前目录全部改动          |
| 添加所有改动（含删除）   | `git add -A`         | 比 `.` 更彻底，包含删除操作    |
| 提交到本地         | `git commit -m "说明"` | 生成一个带说明的提交快照        |
| 查看提交历史        | `git log --oneline`  | 简洁地一行显示一条提交         |
| 查看改动详情        | `git diff`           | 显示未暂存文件的具体改动内容      |
| 查看暂存区改动详情     | `git diff --staged`  | 显示已暂存但未提交的改动        |

### 3. 回滚：三种情况的撤销方法

| 场景             | 命令                         | 说明                                 |
| :------------- | :------------------------- | :--------------------------------- |
| 撤销工作区修改（未 add） | `git restore 文件名`          | 丢弃工作区改动（旧版：`git checkout -- 文件名`）  |
| 撤销全部工作区修改      | `git restore .`            | 丢弃所有未暂存改动                          |
| 撤回暂存区（保留改动）    | `git restore --staged 文件名` | 取消暂存但修改仍在（旧版：`git reset HEAD 文件名`） |
| 撤销提交，改动保留在工作区  | `git reset --soft HEAD~1`  | 最安全，改动回到工作区                        |
| 撤销提交，改动保留在暂存区  | `git reset --mixed HEAD~1` | 默认行为                               |
| 撤销提交并彻底丢弃改动    | `git reset --hard HEAD~1`  | ⚠️ 危险，改动无法恢复                       |
| 反向撤销指定提交       | `git revert 提交哈希`          | 新建反向提交，保留历史记录                      |
| 修改上一次提交        | `git commit --amend`       | 把新改动并入上一次提交并重写说明                   |

> 💡 建议：不确定时先用 `--soft`，修改不会丢失；`--hard` 操作前务必确认。

### 4. 用 .gitignore 忽略文件

| 场景 | 命令 | 说明 |
| :--- | :--- | :--- |
| 停止追踪单个文件 | `git rm --cached 文件名` | 从 Git 移除追踪，本地文件保留 |
| 停止追踪整个目录 | `git rm -r --cached 目录名` | 批量停止追踪 |
| 提交忽略变更 | `git commit -m "停止追踪某些文件"` | 使忽略规则生效 |

### 5. 分支：创建、合并与冲突

| 场景 | 命令 | 说明 |
| :--- | :--- | :--- |
| 查看所有分支 | `git branch` | 列出分支，`*` 标记当前分支 |
| 创建新分支 | `git branch 分支名` | 新建分支（不切换） |
| 切换分支 | `git switch 分支名` | 切换分支（旧版：`git checkout 分支名`） |
| 创建并切换 | `git switch -c 分支名` | 一步完成（旧版：`git checkout -b 分支名`） |
| 合并分支 | `git merge 分支名` | 把指定分支合入当前分支 |
| 放弃本次合并 | `git merge --abort` | 冲突时取消合并，回到合并前 |
| 删除已合并分支 | `git branch -d 分支名` | 安全删除 |
| 强制删除未合并分支 | `git branch -D 分支名` | 强制删除，改动一并丢弃 |

### 6. 进阶：Rebase、Stash、Worktree

| 场景 | 命令 | 说明 |
| :--- | :--- | :--- |
| 变基 | `git rebase main` | 把当前分支提交搬运到 main 顶端 |
| 交互式变基 | `git rebase -i HEAD~3` | 整理最近 3 条提交（pick / squash / reword / drop） |
| 临时保存改动 | `git stash` | 保存工作区改动，工作区恢复干净 |
| 带说明暂存 | `git stash save "说明"` | 给暂存加备注，便于识别 |
| 查看暂存列表 | `git stash list` | 列出所有 stash 记录 |
| 恢复暂存（保留记录） | `git stash apply` | 恢复最近一次，stash 仍在 |
| 恢复并删除记录 | `git stash pop` | 恢复最近一次并移除记录 |
| 删除指定暂存 | `git stash drop stash@{0}` | 删除某一条暂存 |
| 添加工作树 | `git worktree add 路径 分支名` | 同一仓库同时检出多个分支 |
| 查看工作树 | `git worktree list` | 列出所有工作树 |

> ⚠️ 黄金法则：不要对已经推送到远程的提交执行 rebase！

### 7. GitHub：配置与协作

| 场景 | 命令 | 说明 |
| :--- | :--- | :--- |
| 生成 SSH 密钥 | `ssh-keygen -t ed25519 -C "邮箱"` | 生成密钥用于免密码推送 |
| 查看公钥 | `cat ~/.ssh/id_ed25519.pub` | 复制内容到 GitHub → Settings → SSH keys |
| 关联远程仓库 | `git remote add origin 仓库地址` | 关联远程（HTTPS 或 SSH 均可） |
| 查看远程仓库 | `git remote -v` | 查看已关联的远程地址 |
| 重命名主分支 | `git branch -M main` | 确保本地与远程主分支名一致 |
| 首次推送 | `git push -u origin main` | 建立跟踪关系并推送 |
| 克隆远程仓库 | `git clone 仓库地址` | 下载远程仓库到本地 |
| 拉取并合并 | `git pull` | 同步远程最新改动（多设备前先拉取） |
| 推送本地提交 | `git push` | 上传本地所有提交到远程 |
| 仅获取不合并 | `git fetch` | 只下载远程更新，不自动合并 |

### 8. 高频速查

| 场景         | 命令                                | 说明             |
| :--------- | :-------------------------------- | :------------- |
| 查看状态       | `git status`                      | 高频使用，随时确认当前改动  |
| 查看历史       | `git log --oneline`               | 快速浏览提交记录       |
| 图形化历史      | `git log --graph --oneline --all` | 用线条直观展示分支走向    |
| 查看某条提交详情   | `git show 提交哈希`                   | 查看该提交的改动内容与元数据 |
| 删除文件       | `git rm 文件名`                      | 删除文件并暂存删除操作    |
| 重命名 / 移动文件 | `git mv 旧名 新名`                    | 重命名并暂存         |

### 9. 补充

| 场景 | 命令 | 说明 |
| :--- | :--- | :--- |
| 打标签 | `git tag v1.0` | 给重要版本打轻量标签 |
| 带说明打标签 | `git tag -a v1.0 -m "说明"` | 创建带注释的标签 |
| 安全强制推送 | `git push --force-with-lease` | 覆盖远程历史（比 `--force` 安全，仍须慎用） |
| 配置命令别名 | `git config --global alias.st status` | 之后可用 `git st` 代替 `git status` |
| 从追踪中移除并保留本地 | `git rm --cached 文件名` | 与 .gitignore 配合清理误提交的文件 |
| 查看某文件提交历史 | `git log -- 文件名` | 只看该文件被修改过哪些提交 |
| 查看某行改动来源 | `git blame 文件名` | 逐行显示最后一次修改的提交与作者 |
