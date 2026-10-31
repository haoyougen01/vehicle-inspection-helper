# 发布到 GitHub 操作指南

> 本文档针对本仓库（`车辆年检助手-开源版`）的实际环境编写。
> 当前状态：本地 git 仓库已初始化（`main` 分支），15 个文件已暂存，**只差 提交 + 建远程仓库 + 推送**。

---

## 0. 环境现状（2026-10-31 实测）

| 项目 | 状态 |
| --- | --- |
| git | 已安装 `2.55.0.windows.3` |
| Git Credential Manager | 已存在（便携版 Git 自带），HTTPS 推送可弹浏览器登录 |
| GitHub CLI (`gh`) | **未安装** |
| SSH 密钥 | **不存在**（`~/.ssh` 无内容） |
| 全局 `user.name` / `user.email` | **未配置**（必须先配，否则 commit 失败） |
| 本地仓库 | 已 `git init -b main`，`git add -A` 完成 |

---

## 1. 补齐作者信息（只需一次）

```bash
git config --global user.name  "你的名字或 GitHub 昵称"
git config --global user.email "你的邮箱@example.com"
```

> 建议 `user.email` 用 GitHub 账号绑定的邮箱；若不想暴露真实邮箱，可用
> `Settings → Emails → Keep my email addresses private` 提供的
> `12345678+用户名@users.noreply.github.com`。

顺手关掉中文转义，否则中文文件名会显示成 `\346\226\207\346\241\243`：

```bash
git config --global core.quotepath false
```

---

## 2. 首次提交

```bash
cd vehicle-inspection-helper    # 进入本仓库目录（或在此目录右键 Git Bash Here）
git commit -m "feat: 车辆年检助手开源版首次提交

- WebView2 苹果风界面，临时车辆查询 + 存量车跟踪管理双模块
- 内置 2022 年免检新政、20 年节点、处置期计算
- Excel 批量导入、导出、年检提醒、查询历史
- 含虚构演示数据与完整开发文档"
```

多行提交信息：

- **cmd / PowerShell**：用多个 `-m` 分段，不要直接换行
  ```powershell
  git commit -m "feat: 首次提交" -m "- 双模块界面" -m "- 内置年检规则"
  ```
- **Git Bash**：可直接用上面的多行写法。

提交后核对：

```bash
git log --stat -1
```

> 如果提交后发现作者信息写错：`git commit --amend --reset-author`（仅在**未推送**前可用）。

---

## 3. 在 GitHub 网页创建**空**仓库

1. 打开 <https://github.com/new>
2. **Repository name**：`vehicle-inspection-helper`（建议英文；中文名也能用，但 URL 会变成百分号编码）
3. **Visibility**：`Public`（开源）
4. **不要勾选** `Add a README file` / `Add .gitignore` / `Choose a license`
   —— 本地已有这三个文件，勾了会造成远程已有提交、首次 push 被拒
5. 点 **Create repository**

---

## 4. 关联远程并推送

```bash
cd vehicle-inspection-helper    # 进入本仓库目录（或在此目录右键 Git Bash Here）
git remote add origin https://github.com/<你的用户名>/vehicle-inspection-helper.git
git push -u origin main
```

首次推送会**弹出 Git Credential Manager 窗口**：

1. 选 `Sign in with your browser`（或 `Token`）
2. 浏览器里用 GitHub 账号登录并点 `Authorize`
3. 回到终端，看到 `branch 'main' -> 'main'` 即成功

之后同一台机器再推送**不再需要认证**（凭据已存 Windows 凭据管理器）。

---

## 5. 三种认证方式对比

| 方式 | 准备工作 | 适用场景 | 备注 |
| --- | --- | --- | --- |
| **HTTPS + GCM 浏览器登录**（推荐） | 无 | 一次性搞定，最省事 | 首次 push 弹窗授权，凭据自动保存 |
| **HTTPS + PAT** | 网页生成 Token（勾 `repo`） | 无图形环境 / CI | 密码框里**粘 Token**，不是账号密码 |
| **SSH 密钥** | `ssh-keygen` + 贴公钥 | 长期多仓库、免输凭据 | 内网/代理环境常配 `ssh.github.com:443` |

### 5.1 PAT 方式补充

GitHub → 头像 → `Settings` → `Developer settings` → `Personal access tokens`
→ `Tokens (classic)` → `Generate new token (classic)` → 勾 **`repo`** → 复制 `ghp_xxx`。

推送时：
- Username：你的 GitHub 用户名
- Password：**粘贴 Token**（`ghp_...`）

细粒度 Token（Fine-grained）也可以，但需显式授予该仓库 `Contents: Read and write` 权限。

### 5.2 SSH 方式补充

```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"     # 一路回车（密码可留空）
cat ~/.ssh/id_ed25519.pub                            # 复制整行
```

粘贴到：GitHub → `Settings` → `SSH and GPG keys` → `New SSH key`。

```bash
git remote set-url origin git@github.com:<用户名>/<仓库名>.git
ssh -T git@github.com          # 出现 "Hi 用户名!" 即通
git push -u origin main
```

---

## 6. 国内网络处理

推送卡住 / `Connection timed out` 时，临时走本地代理（按自己代理端口改）：

```bash
git config --global http.proxy  http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

> 只给 GitHub 走代理、不影响公司内网 Git 的写法：
> ```bash
> git config --global http.https://github.com.proxy http://127.0.0.1:7890
> ```

SSH 被 22 端口封时，改用 443：

```
# 编辑 ~/.ssh/config，新增：
Host github.com
    HostName ssh.github.com
    Port 443
    User git
```

---

## 7. 常见报错对照表

| 报错 | 原因 | 解决 |
| --- | --- | --- |
| `Support for password authentication was removed` | 密码框里输了账号密码 | 改用 **PAT** 当密码 |
| `remote: Repository not found` | 仓库名/用户名拼错，或 Token 无该仓库权限 | 核对 URL；重新生成带 `repo` 的 Token |
| `error: remote origin already exists` | 已配过 remote | `git remote set-url origin <新地址>` |
| `Updates were rejected because the remote contains work...` | 建仓库时勾了 README/License | `git pull --rebase origin main` 后再 push |
| `fatal: author identity unknown` | 没配 `user.name/email` | 见第 1 节 |
| `RPC failed; HTTP 413` / push 极慢 | 传了大文件（exe/压缩包） | exe 已由 `.gitignore` 排除，改用 **Releases** 分发 |
| 中文文件名变成 `\346\226\207...` | git 默认转义非 ASCII | `git config --global core.quotepath false` |
| `SSL certificate problem: unable to get local issuer certificate` | 代理/杀软做了证书替换 | 换网络；或临时 `git config http.sslVerify false`（**仅临时，用完删掉**） |
| 提交后提示 `CRLF will be replaced by LF` | 行尾转换警告 | 本仓库已用 `.gitattributes` 固定，可忽略 |

---

## 8. 推送后建议做的事

1. **仓库Topics**：`aardio` `windows` `vehicle` `inspection` `webview2` `desktop-app`
2. **Releases 分发 exe**：`Releases → Draft a new release → 上传 工程/dist/车辆年检助手.exe`
   —— exe 不进版本库（`.gitignore` 已忽略），走 Release 附件最规范
3. **README 顶部加下载徽章**，指向最新 Release
4. **设置 About 描述**：一句话说明用途

---

## 9. 后续日常提交流程

```bash
cd vehicle-inspection-helper    # 进入本仓库目录（或在此目录右键 Git Bash Here）
git status                      # 看改动
git add -A
git commit -m "fix: 说明改了什么"
git push
```

> 维护"自用版"与"开源版"两份时：改完 `车辆年检助手/工程/` 后，把
> `main.aardio`、`ui/index.html` 同步到开源版目录，再提交推送。
> **切勿把真实 `车辆跟踪库.csv` 带进开源版仓库。**

---

## 10. 一键核对脚本

推送前跑一遍，确认没有敏感信息混进版本库：

```bash
cd vehicle-inspection-helper    # 进入本仓库目录（或在此目录右键 Git Bash Here）
git grep --cached -nE "迅雷|pr0039|ghp_[A-Za-z0-9]{20,}"      # 不应有输出
git grep --cached -nE "津[A-Z0-9]{2}[0-9A-Z]{3,}"             # 不应有输出（真实车牌）
git ls-files | grep -iE "\.exe$|\.dll$|init_dump|调试日志"     # 不应有输出
```

三条都无输出即可放心推送。
