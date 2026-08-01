# Use with Claude / Claude Code

These skills use the standard **`SKILL.md`** format Claude Code understands.
Descriptions include **English + Chinese** trigger phrases so both languages auto-match.

You can install them three ways.

---

## Option A — Personal skills（最常用，全局生效）

复制到本机 Claude 技能目录：

### Windows (PowerShell)

```powershell
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
.\scripts\install.ps1 -Claude
```

会写入：`%USERPROFILE%\.claude\skills\<skill-name>\`

### macOS / Linux

```bash
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
./scripts/install.sh --claude
```

写入：`~/.claude/skills/<skill-name>/`

然后 **重启 Claude Code**（或新开会话）。  
在对话里直接说：

```text
Review this OpenAPI diff for breaking changes.
```

Claude 会根据 skill 的 `description` 自动选用 `breaking-change-review` 等技能。

也可显式点名：

```text
Use the breaking-change-review skill on examples/toy-orders-api.
```

---

## Option B — Project skills（只对当前仓库）

在**你的业务项目**根目录：

```powershell
# 从本仓库拷 skills 到「当前项目」
cd path\to\your-app
# 假设 api-platform-skills 已 clone 到 G:\skill\api-platform-skills
Copy-Item -Recurse G:\skill\api-platform-skills\skills\* .\.claude\skills\
```

或在本仓库内：

```powershell
cd G:\skill\api-platform-skills
.\scripts\install.ps1 -Project
```

路径：`.claude/skills/`（可提交进 git，团队共享）。

---

## Option C — Claude Code Plugin / Marketplace（一键装整包）

本仓库已带：

- `.claude-plugin/plugin.json` — 插件清单  
- `.claude-plugin/marketplace.json` — 可作为 marketplace 源  

在 **Claude Code** 里：

```text
/plugin marketplace add Wanbinyu/api-platform-skills
```

然后：

```text
/plugin install api-platform-skills@api-platform-skills
```

若提示找不到 marketplace，可先：

```text
/plugin marketplace add https://github.com/Wanbinyu/api-platform-skills
```

装完后：

```text
/reload-plugins
```

本地开发调试也可用：

```bash
claude --plugin-dir /path/to/api-platform-skills
```

---

## Option D — 手动复制单个 skill

只要把文件夹拷进 skills 目录即可，例如只要破坏性变更审查：

```powershell
$src = "G:\skill\api-platform-skills\skills\breaking-change-review"
$dst = "$env:USERPROFILE\.claude\skills\breaking-change-review"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse $src $dst -Force
```

每个 skill 是独立的：

```text
~/.claude/skills/breaking-change-review/SKILL.md
~/.claude/skills/breaking-change-review/references/   # 如有
```

---

## 和 claude.ai 网页版 Skills 的关系

| 环境 | 用法 |
|------|------|
| **Claude Code（终端/IDE）** | 上列 A/B/C，原生 `~/.claude/skills` / plugin |
| **claude.ai 自定义 Skills** | 可上传/粘贴单个 `SKILL.md` 内容（视产品入口而定）；推荐仍用 Claude Code 获得完整多 skill 包 |

格式都是 YAML frontmatter + Markdown，**无需改写成另一种语言**。

---

## 装好后怎么验证

1. 打开 Claude Code  
2. 发送：

```text
List installed skills related to API or breaking changes.
Then compare examples/toy-orders-api/openapi.v1.yaml and openapi.v2-bad.yaml
using breaking-change-review.
```

3. 期望：出现 **request-changes / MERGE 类结论**，并列出 auth 删除、201→200 等 delta  

（若在别的项目里测，把 toy yaml 路径改成绝对路径，或先 `cd` 到本仓库。）

---

## Slash 命令

`commands/` 下提供了 `/api-break`、`/api-ship-check` 等说明文件。  
作为 **plugin** 安装时，Claude Code 会从插件的 `commands/` 加载。  
仅复制 `skills/` 到 `~/.claude/skills` 时，主要靠 **自然语言触发**（`description` 里的短语），这是 Skills 的标准用法。

---

## 故障排除

| 现象 | 处理 |
|------|------|
| 完全不触发 skill | 确认目录名与 `name:` 一致；重启会话 |
| 只有 name、行为不对 | 打开对应 `SKILL.md` 看 Exit criteria 是否被跳过，可说 “follow exit criteria strictly” |
| plugin 装不上 | 用 Option A 复制到 `~/.claude/skills`（最稳） |
| 和别的 api-design skill 冲突 | 本包装的是演进层；路由 skill 会声明不负责 REST 命名 |
