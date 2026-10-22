<div align="center">

# ⚡ GodSkill

### 别只让 Agent 回答问题，让它带着方法工作。

**Think clearly · Build once · Be discovered**

GodSkill 是一组可独立安装的 Agent Skills。它把判断方法、工作流程和验收边界封装成可复用能力，让 Agent 不只是“这次答对”，而是在下一次遇到同类问题时，依然知道该如何思考、执行和检查。

<p>
  <img alt="Skills: 3" src="https://img.shields.io/badge/Skills-3-7C3AED?style=for-the-badge">
  <img alt="Install independently" src="https://img.shields.io/badge/Install-Independent-0284C7?style=for-the-badge">
  <img alt="Chinese documentation" src="https://img.shields.io/badge/Docs-Chinese-059669?style=for-the-badge">
</p>

</div>

> 复杂问题看不清、同样工作反复解释、好内容难被发现——GodSkill 给 Agent 的不是一段“万能提示词”，而是一套能反复执行、按需读取并明确验证边界的方法。

```text
复杂问题看不清             同样工作反复解释             好内容难被发现
       ↓                           ↓                           ↓
First Principles              No Repeat Skill             WeChat SEO
找到真正目标                 沉淀可复用能力               建立可发现页面
```

## 30 秒找到适合你的 Skill

| 如果你正在…… | 从这里开始 | 它会帮你…… |
| --- | --- | --- |
| 在几个方案间犹豫，担心一开始就选错方向 | [`first-principles-decision`](first-principles-decision/README.md) | 拆开真实目标、隐藏假设、信息差和替代路径，给出明确建议 |
| 每周重复解释同一套流程，想把经验交给 Agent | [`no-repeat-skill`](no-repeat-skill/README.md) | 判断应该做成 Skill、脚本还是模板，并完成最小实现与验证 |
| 为微信小程序建设公开搜索页，又不想堆砌关键词 | [`wechat-miniprogram-seo`](wechat-miniprogram-seo/README.md) | 规划真实内容、稳定页面、公开内链和 sitemap，并守住收录证据边界 |

选择一个真实问题，安装对应 Skill，然后直接把任务交给 Agent。每个 Skill 都有自己的目录、说明文件和安装方式，不需要一次安装全部内容。

## 它们怎样工作：6 个示例任务

以下都是能力示例，用来展示各 Skill 的处理方式和预期输出，不代表虚构的客户成绩或平台结果。

<details open>
<summary><strong>🧭 first-principles-decision：重要决策先看清真正目标</strong></summary>

### 示例 1：系统变慢，要不要马上拆微服务？

**你原本会问：**

> 订单系统越来越慢，我们是不是应该马上拆成微服务？

**Skill 会怎么处理：**

先把目标还原为性能、稳定性与迭代效率，检查“系统慢就是架构不够复杂”的假设；再比较数据库优化、缓存、异步任务、模块化单体和微服务，最后从失败成本与团队维护能力反向复核。

**你会得到：**

明确的继续、调整或放弃结论，以及推荐路线、实施顺序、切换条件和主要风险，而不是一张只有优缺点的选型表。

### 示例 2：两万元预算，是否值得买本地 AI 主机？

**你原本会问：**

> 我想花两万元买一台机器长期运行 AI Agent，这是不是最划算的方案？

**Skill 会怎么处理：**

根据真实任务、使用频率、隐私要求和维护能力重新定义需求，核实会变化的硬件与云服务信息，再比较本地、云端和混合方案的总成本与扩展性。

**你会得到：**

一条有条件的购买建议、替代方案、配置重点和停止条件，避免先买设备再寻找使用理由。

</details>

<details>
<summary><strong>🔁 no-repeat-skill：把反复解释变成可复用能力</strong></summary>

### 示例 3：每周客户周报总要重新解释

**你原本会说：**

> 我每周都要告诉 Agent 怎么整理客户周报，帮我做成一个 Skill。

**Skill 会怎么处理：**

先判断真正重复的是数据整理、固定格式，还是需要语境判断的总结；再在模板、脚本、自动化和 Skill 中选择最小组合，不默认制造复杂目录。

**你会得到：**

一个足够小、能够安装和验证的能力包；如果模板或脚本更合适，也会明确建议不做 Skill。

### 示例 4：现有 Skill 经常误触发

**你原本会说：**

> 这个 Skill 有时不触发，有时普通问题也会触发，帮我修好。

**Skill 会怎么处理：**

检查说明是否过宽、入口是否塞入太多内容、参考文件是否能够找到；补充应该触发、明确不触发和容易混淆的近邻场景，再运行结构与回归检查。

**你会得到：**

更准确的触发边界、必要的最小修改、可重复运行的检查，以及“已经证明什么、还没有证明什么”的清晰说明。

</details>

<details>
<summary><strong>🔍 wechat-miniprogram-seo：让公开内容具备被发现的条件</strong></summary>

### 示例 5：给城市活动做微信搜索落地页

**你原本会说：**

> 给现有小程序增加城市活动搜索页，希望用户能从微信搜索直接进入。

**Skill 会怎么处理：**

按活动类型、时间和地点聚类真实搜索需求，设计稳定地址与独立标题，保证页面冷启动、未登录也能看到公开内容，并用 `navigator` 建立公开入口，只把合格页面加入 sitemap。

**你会得到：**

可执行的页面体系、内容与链接要求、异常处理方式和验收清单，同时明确“具备可索引条件”不等于“已经被微信收录”。

### 示例 6：sitemap 全部放开，为什么仍没有曝光？

**你原本会问：**

> 我的 sitemap 已经允许所有页面，为什么微信搜索还是找不到？

**Skill 会怎么处理：**

检查公开页面是否被登录阻挡、是否依赖上一页状态、标题与正文是否薄弱、是否存在重复页或孤岛页；同时排除个人资料、编辑、支付和临时结果等不应公开的页面。

**你会得到：**

一份按优先级整理的问题清单、建议开放的页面范围和验证步骤；不会把 sitemap 配置成功误报为平台已经抓取或排名提升。

</details>

## 60 秒开始使用

### 1. 克隆仓库

```bash
git clone https://github.com/GodAI-Master/GodSkill.git
cd GodSkill
```

### 2. 只安装你需要的 Skill

Windows PowerShell 示例：

```powershell
$skillName = "first-principles-decision"
$target = Join-Path $env:USERPROFILE ".codex\skills\$skillName"
New-Item -ItemType Directory -Path $target -Force | Out-Null
Copy-Item ".\$skillName\*" $target -Recurse -Force
```

macOS / Linux 示例：

```bash
skill_name="first-principles-decision"
mkdir -p "$HOME/.codex/skills/$skill_name"
cp -R "$skill_name"/. "$HOME/.codex/skills/$skill_name"/
```

把技能名替换为下面任意一个：

```text
first-principles-decision
no-repeat-skill
wechat-miniprogram-seo
```

请复制完整子目录，不要只复制 `SKILL.md`；否则参考资料、模板、检查脚本或界面信息可能丢失。若使用自定义 `CODEX_HOME`，将目标路径改为该目录下的 `skills/<skill-name>`。

### 3. 直接调用

```text
使用 $first-principles-decision 分析：我们是否应该把现有系统拆成微服务？
```

```text
使用 $no-repeat-skill，把每周客户周报流程整理成最小、可验证的可复用能力。
```

```text
使用 $wechat-miniprogram-seo，检查这个小程序的公开页面、直达访问、内链和 sitemap。
```

如果客户端没有自动刷新 Skill 列表，请重新打开 Codex。更详细的安装、边界和示例请阅读对应目录中的独立 README。

## GodSkill 的设计原则

- **一个 Skill，一个目录**：按需安装、独立阅读、独立维护。
- **先解决真实问题**：不为了看起来完整而堆文件、模板和流程。
- **方法与资料分层**：核心入口保持精简，详细规范和工具按需读取。
- **验证不夸大**：结构检查、真实行为和外部平台结果分别说明。
- **保留用户选择**：Skill 帮助 Agent 做出更好的判断，不替用户扩大任务范围。

## 仓库结构

```text
GodSkill/
├── README.md
├── first-principles-decision/
│   ├── README.md
│   ├── SKILL.md
│   └── _skillhub_meta.json
├── no-repeat-skill/
│   ├── README.md
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   ├── evals/
│   ├── references/
│   ├── scripts/
│   └── _skillhub_meta.json
└── wechat-miniprogram-seo/
    ├── README.md
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── _skillhub_meta.json
```

## 验证与证据边界

仓库中的 `no-repeat-skill/scripts/validate_skill.py` 可以检查 Skill 名称、说明入口、内部链接、JSON、参考资源和明显的发布残留。

Windows PowerShell：

```powershell
py -3 -X utf8 .\no-repeat-skill\scripts\validate_skill.py .\no-repeat-skill --strict
```

macOS / Linux：

```bash
python3 no-repeat-skill/scripts/validate_skill.py no-repeat-skill --strict
```

静态检查通过，只能证明基础结构和文件关系没有发现问题，不能自动证明 Agent 在所有真实任务中都会正确触发，也不能替代外部平台验收。特别是微信小程序的 sitemap、页面结构和本地检查通过，不代表微信已经抓取、收录、展示或提升排名。

## 许可

仓库当前在 README 中声明为 MIT License，但尚未包含独立的 `LICENSE` 文件。如需公开再分发或用于正式项目，请先确认适用的许可条件。

---

<div align="center">

**从一个真实问题开始，选择一个 Skill，让 Agent 不再每次从零开始。**

</div>
