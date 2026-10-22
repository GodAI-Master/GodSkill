---
name: wechat-miniprogram-seo
description: "Apply when a WeChat Mini Program task involves public, search-worthy content, stable landing pages, direct-entry routing, navigator discovery links, sitemap admission, or indexing-readiness review. Do not add SEO scope to private, account-only, or unrelated feature work."
---

# 微信小程序 SEO

在创建、修改、审查或规划微信小程序时，先判断任务是否涉及具备公开搜索价值的内容。若涉及，再把搜索可发现性作为基础架构检查项：查看当前页面结构、公开内容来源和 `sitemap.json`，确认任务是否新增、改变或依赖适合被搜索的公开内容。纯私有、账号专属或与搜索无关的功能，不要为了 SEO 强行扩展页面范围。

涉及 SEO 页面时，遵循以下要求：

- 先聚类搜索意图，再规划页面；不要按同义关键词批量复制内容。
- 每个公开落地页都有稳定、简洁的 URL，并能从新启动的小程序直接打开；核心内容不依赖前页状态、登录或临时缓存。
- 标题和正文要与页面主题一致。正文展示给真实用户，也展示给搜索爬虫；不隐藏关键词、不编造事实。
- 公开内容先展示；收藏、同步等身份相关操作再要求登录。
- 用小程序原生页面承载被搜索的核心内容。发现 SEO 页时优先用 `navigator` 建立公开链接；维持 hub、分类和详情页之间的可遍历关系。
- 将 sitemap 当作收录准入清单，只开放内容完整、公开且有独立价值的页面。检查是否存在登录页、个人信息、编辑、支付、临时结果等非公开页面被放开。
- 数据有时效或核验状态时显示来源、核验时间和待确认状态；过期或冲突的信息不能被写成确定事实。避免创建重复、薄弱或失效的页面。
- 把“页面具备被索引的技术条件”与“微信实际收录、曝光或排名”分开表述。不要承诺收录结果。

执行具体 SEO 设计或实现前，读取 [完整设计与实现规范](references/seo-page-standard.md)。根据当前项目技术栈采用合适的路由和数据来源，不要照搬示例目录。保留既有产品视觉、业务入口和数据边界。

验收时检查：直接冷启动 URL、无登录访问、页面标题与可见正文、链接可达性、孤岛页、重复意图、数据兜底、sitemap JSON 以及项目已有测试。必要时区分代码检查、微信开发者工具验收和真实微信搜索收录；前两者不能证明最终已被收录。
