# 六层端点与字段

本文件记录每一层的真实调用方式、可解析字段与已知失败模式。所有接口行为在 2026-11 做过实测，市场数据会变化，结论需带观测时间。

## L1 官方内置

客户端自带，无需安装。多版本目录会同时存在，必须按技能名去重后取最高版本。

```text
<客户端资源目录>/plugins/cache/<vendor>/builtin/<plugin>/<version>/SKILL.md
<客户端资源目录>/plugins/cache/<vendor>/builtin/<plugin>/<version>/skills/<name>/SKILL.md
```

可解析字段只有 frontmatter 的 `name`、`description`（部分含 `display_name_zh`、`description_en`、`version`）。

**已知失败模式**

- 同一技能存在多个版本目录（例如同时存在 5.9.3 与 5.11.3），不去重会把同一能力数成两条。
- 插件目录名与技能名不一致，按目录名匹配会漏召回，必须读 frontmatter。
- 内置技能没有下载量与安全报告，采用度维度应给中性分而非零分。

## L2 本地已安装

```text
~/.workbuddy/skills/<name>/SKILL.md
<workspace>/.workbuddy/skills/<name>/SKILL.md
~/.workbuddy/skills-marketplace/skills/<name>/
```

**已知失败模式**

- 只列目录名做匹配是最常见的错误。目录名与能力经常不一致，必须读 frontmatter 的 description。
- 一些技能只是副产物提及关键词（例如内容创作技能在产出格式里写了 xlsx），属于假命中，需按"是否为专用能力"二次过滤。
- 项目级目录可能不存在，缺失不等于零命中，应记为"无项目级技能"。

## L3 SkillHub

```bash
curl -s "https://lightmake.site/api/v1/search?q=<URL 编码关键词>&limit=10"
curl -s "https://lightmake.site/api/v1/skills/<slug>"
```

检索结果字段：`score`、`installs`、`stars`、`downloads`、`namespace.canonicalName`、`homepage`、`description_zh`、`source`、`labels.requires_api_key`、`publisher.verified`、`securityReports`。

详情接口返回 `skill`、`latestVersion`、`namespace`、`securityReports`，其中 `securityReports.keen.status` 与 `securityReports.sanbu.status` 为安全结论（例如 `benign`）。

**已知失败模式**

- `score` 低于 0.05 的结果基本是语义漂移，应过滤。
- `source` 字段会出现 `clawhub` 值，说明该市场对 ClawHub 做了联邦索引，跨市场去重时必须识别。
- 同一技能常被不同账号以不同名称重复上架，描述几乎一致，仅靠名称去重无效。
- 详情接口对 slug 大小写与特殊字符敏感，取不到时不要臆测能力。

## L4 虾评

```bash
curl -s "https://xiaping.coze.com/api/skills/search?q=<URL 编码关键词>&limit=10"
curl -s "https://xiaping.coze.com/api/skills/<skill-id>"
curl -s "https://xiaping.coze.com/api/skills/<skill-id>/download"
```

字段：`name`、`description`、`trigger`、`category`、`tags`、`downloads`、`star_count`、`comment_count`、`status`、`security_status`、`current_version`、`owner_name`、`is_featured`。

`status` 为 `official` 表示官方上架，`security_status` 为 `safe` 表示通过安全检查。

**已知失败模式**

- 域名是 `coze.com`，写成 `coze.site` 会直接失败。
- 下载链接接口需要按其指南技能约定的方式调用，直接请求可能被拒。
- 中文场景相关性通常高于英文市场，英文关键词检索效果差，应优先用中文词。

## L5 ClawHub

```bash
curl -sL "https://clawhub.ai/api/v1/search?q=<关键词>"
```

结果字段：`displayName`、`downloads`、`featured`、`canonicalUrl`、`install.kind`、`install.reference`、`install.sourceUrl`、`description`。

`install.kind` 常见值为 `clawhub` 与 `skills-sh`。后者代表该条目实际托管在 skills.sh，`install.reference` 形如 `skills-sh:<owner>/<repo>/<path>`，可直接换算为 GitHub 源码位置。

**已知失败模式**

- 搜索路由是 `api/v1/search`。写成 `api/v1/skills/search` 会被当作 slug 解析并返回 404，容易被误判为"接口不存在"。
- 裸域请求可能超时或被重定向，需带 `-L` 跟随跳转，并优先用带 `www` 或不带 `www` 中可用的那一个。
- 下载量口径与聚合市场不同。同一技能在 ClawHub 与 SkillHub 的计数可能相差三倍以上，跨市场比较无意义。

## L6 GitHub

```bash
curl -s "https://api.github.com/search/repositories?q=<关键词>+in:name,description&sort=stars&per_page=10"
```

**已知失败模式**

- 代码级搜索（`search/code`）需要令牌。无令牌时只能做仓库级搜索，会漏掉未建仓或仅有单个 SKILL.md 的散落技能，必须在输出中声明这一覆盖缺口。
- 匿名调用有每小时次数上限，多关键词批量检索容易触顶，需控制请求数。
- 仓库搜索结果必须人工判断是否为有效技能：检查是否存在 SKILL.md，而不是只看仓库描述。
- 仓库星数与技能可用性弱相关，高星仓库可能只是文档集合。

## 跨层比较的注意事项

- 不要把不同市场的下载量放在同一列做排名，口径不同。
- 同一技能在不同市场名称可能不同（英文名与中文名），去重靠 canonicalName 与描述指纹，不靠名称。
- 内置层与本地层没有市场热度指标，四维排序时采用度按中性分处理，避免系统性地低估零安装成本的能力。
