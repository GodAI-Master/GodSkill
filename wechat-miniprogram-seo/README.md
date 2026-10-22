# 微信小程序 SEO

把微信小程序的长尾搜索页面从“想到一个词就加一页”，整理成一套可复用的设计、实现和验收方法。这个 Skill 帮助 Agent 识别真正有公开搜索价值的内容，建立稳定、可直接打开的原生页面，并正确处理页面标题、公开内链、`sitemap.json` 和动态信息的可信度。

## 它解决什么问题

- 按用户的搜索意图组织页面，减少重复、空洞的关键词页。
- 为公开内容提供稳定链接，让页面在没有首页状态、登录状态或上一个页面的情况下也能打开。
- 用清晰标题、真实正文、页面间链接和 sitemap 共同描述可搜索内容。
- 公开内容先展示；收藏、同步等需要身份的操作再要求登录。
- 把“技术上允许被抓取”与“微信实际收录、展示或排名”明确分开。

## 适合场景

- 新建小程序时规划公开内容和搜索落地页。
- 修改已有小程序的公开页面、直达链接、标题、内链或 sitemap。
- 检查页面是否依赖登录、上一页状态或临时缓存，导致无法独立打开。
- 审查重复页面、薄弱内容、孤岛页、过期信息和不应公开收录的页面。
- 发布前区分代码检查、开发者工具验收和真实微信搜索结果。

以下情况不应为了 SEO 扩大范围：纯后台功能、个人数据、账号专属页面、支付或编辑流程，以及没有独立公开搜索价值的普通功能。这个 Skill 也不能保证微信最终收录、展示或排名。

## 核心方法

1. 先检查页面结构、公开数据来源和现有 sitemap。
2. 按真实搜索意图聚类，避免为同义关键词复制页面。
3. 为每个合格主题建立稳定地址、独立标题和真实可见正文。
4. 保证页面可从冷启动直接打开，核心公开内容不依赖登录或前置页面。
5. 用 `navigator` 连接公开入口、分类和详情，避免孤岛页。
6. 只在 sitemap 中开放内容完整、公开且有独立价值的页面。
7. 分别验证代码、微信开发者工具、真机访问和平台实际收录，不混淆证据范围。

## 目录内容

```text
wechat-miniprogram-seo/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── seo-page-standard.md
└── _skillhub_meta.json
```

| 文件 | 作用 |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent 读取的核心工作指引和边界。 |
| [openai.yaml](agents/openai.yaml) | Codex 中展示名称、简介和默认调用提示。 |
| [seo-page-standard.md](references/seo-page-standard.md) | 完整的页面模型、搜索意图、稳定地址、内容、内链、sitemap、维护和验收规范。 |
| [_skillhub_meta.json](_skillhub_meta.json) | 统一仓库使用的 Skill 元数据。 |

## 安装给 Codex

Windows PowerShell：

```powershell
git clone https://github.com/GodAI-Master/GodSkill.git
Set-Location .\GodSkill
$skillPath = Join-Path $env:USERPROFILE ".codex\skills\wechat-miniprogram-seo"
New-Item -ItemType Directory -Path $skillPath -Force | Out-Null
Copy-Item .\wechat-miniprogram-seo\* $skillPath -Recurse -Force
```

这会把完整技能安装到当前 Windows 用户的 Codex 技能目录。若设置了自定义 `CODEX_HOME`，请将目标改为该目录下的 `skills\wechat-miniprogram-seo`。安装后重新打开 Codex；也可以在任务中明确写 `$wechat-miniprogram-seo`。

只想在单个项目内使用时，把完整的 `wechat-miniprogram-seo` 目录复制到项目的 `.agents/skills/` 下。不要只复制 `SKILL.md`，否则完整规范和界面说明会丢失。

## 使用示例

新建小程序时：

> 使用 `$wechat-mini-program-seo`。先检查项目类型、页面结构和公开内容，规划哪些用户需求值得形成独立的搜索落地页，再实现需要的页面。搜索词按意图聚类，不编造营业、价格或地点信息；说明哪些页面具备被收录的技术条件，以及还需要在微信公众平台完成什么设置。

修改已有小程序时：

> 使用 `$wechat-mini-program-seo`，先检查当前 sitemap、公开页面、直达链接和内容来源，再按本项目现有结构改进搜索落地页。保留业务功能，验证冷启动、未登录访问、标题、内链和 sitemap，并明确哪些结论还需要开发者工具、微信公众平台或真机确认。

只做审查时：

> 使用 `$wechat-mini-program-seo` 审查这个小程序的公开搜索页面。列出重复、薄弱、无法冷启动、被登录阻挡、缺少公开入口或不应进入 sitemap 的页面，并区分已确认问题与仍需平台验证的事项。

## 验证

在 GodSkill 仓库根目录运行：

```powershell
py -3 -X utf8 .\no-repeat-skill\scripts\validate_skill.py .\wechat-miniprogram-seo --strict
```

这项检查能确认文件结构、说明入口、内部链接、JSON 和明显的私有路径或密钥问题。它不能证明微信开发者工具、真机访问或微信搜索收录已经成功；这些结果需要分别验证。

## 使用边界

页面具备稳定地址、公开内容、正确标题、内链和 sitemap 配置，只表示它达到了“可索引候选页”的技术条件。微信是否抓取、收录、展示以及排序，由平台决定；小程序后台的页面收录设置、内容质量、审核状态和真实用户体验也会影响结果。发布前应核对微信官方文档的现行要求。

## 官方参考

- [微信小程序搜索优化指南](https://developers.weixin.qq.com/miniprogram/dev/framework/search/seo.html)
- [微信小程序 sitemap 配置](https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/sitemap.html)
- [微信小程序 navigator 组件](https://developers.weixin.qq.com/miniprogram/dev/component/navigator.html)
- [微信官方小程序示例中的 sitemap.json](https://github.com/wechat-miniprogram/miniprogram-demo/blob/master/sitemap.json)

## 迁移来源

本目录完整迁移自独立仓库 [GodAI-Master/wechat-mini-program-seo](https://github.com/GodAI-Master/wechat-mini-program-seo) 的提交 `b4f6493ae71a1fdcec95b14c25029267683f808c`。原有 `SKILL.md`、Codex 界面信息和完整参考规范的内容均已迁入，并按 GodSkill 的统一目录补充了独立说明、元数据和更明确的使用边界。
