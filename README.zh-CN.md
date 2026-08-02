# API Platform Skills

[English](README.md) | **中文**

<p align="center">
  <strong>别再让 Agent 默默改坏线上接口。</strong><br/>
  <em>设计容易，演进很难。</em>
</p>

---

## 先做这两步（约 1 分钟）

### 1. 安装（Claude Code）

```powershell
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
.\scripts\install.ps1 -Claude
```

```bash
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
chmod +x scripts/install.sh && ./scripts/install.sh --claude
```

重启 Claude Code。技能目录：`~/.claude/skills/`。

### 2. 立刻试这条提示词

```text
对比 examples/toy-orders-api/openapi.v1.yaml 和 openapi.v2-bad.yaml，
按 breaking-change-review 出合并 verdict。
```

**正常结果：** `request-changes` / 不应合并——鉴权被删、状态码乱改、金额单位变更、字段删除等。

Demo 动图见英文首页 [README.md](README.md) 顶部 GIF。

---

## 解决什么问题

| 没有这套 skill | 有了之后 |
|----------------|----------|
| Agent 改字段名「反正能编译」 | **破坏性变更审查** + 迁移说明 |
| 删接口还叫「弃用」 | **弃用剧本**（日期、双轨、回滚） |
| 客户端超时重试导致双下单 | **幂等与重试**设计 |
| 合作方问「到底改了啥」 | **API changelog** 可直接发 |

**不是**又一个 REST 命名教程。  
命名/风格已有很多包；本仓库做 **演进层**：兼容、break、弃用、可靠投递、表面安全。

---

## 你得到什么（10 个 skill）

| 场景 | 用 |
|------|-----|
| 先写 OpenAPI 再写代码 | `contract-first-openapi` |
| 改一处谁会挂 | `compatibility-matrix` |
| 审 API PR | `breaking-change-review` |
| 下线 v1 | `deprecation-playbook` |
| 消费者契约 | `consumer-driven-contract` |
| 支付/下单类接口 | `idempotency-and-retries` |
| Webhook | `webhook-design` |
| 越权 / 过量返回 | `secure-api-surface` |
| 给调用方写发布说明 | `api-changelog` |
| 不知道用哪个 | `using-api-platform-skills` |

每个 skill 都有：**触发条件 · 步骤 · 完成标准 · 反模式 · 报告模板**。

### 机器辅助 diff

```bash
python scripts/openapi_breaking_diff.py old.yaml new.yaml
# 退出码 0 = 未检出硬 break；2 = 有硬/语义 break
```

---

## 安装方式一览

| 方式 | 做法 |
|------|------|
| **推荐：Claude 全局** | `.\scripts\install.ps1 -Claude` |
| 多 harness | `-All` |
| 仅当前仓库 | `-Project` |
| 插件 | `/plugin marketplace add Wanbinyu/api-platform-skills` |
| **只要一个 skill** | 例如 https://github.com/Wanbinyu/skill-breaking-change-review |

---

## 姊妹包

| 包 | 对象 |
|----|------|
| **本包** | HTTP / OpenAPI → 人与 SDK |
| [ai-surface-skills](https://github.com/Wanbinyu/ai-surface-skills) | Tool / MCP → **Agent** |

19 个独立 skill 仓库：https://github.com/Wanbinyu?tab=repositories&q=skill-

---

## 明确不做

- REST 资源命名课  
- 完整 SDLC `/spec/plan/build` 大礼包  
- 红队 exploit  

详见：[docs/NOT-ANOTHER-API-DESIGN-PACK.md](docs/NOT-ANOTHER-API-DESIGN-PACK.md)

## 许可证

MIT · [Wanbinyu](https://github.com/Wanbinyu)
