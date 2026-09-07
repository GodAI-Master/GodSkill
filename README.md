# GodSkill

一个由多个独立 Agent Skill 组成的开源仓库。每个 Skill 都有自己的目录、说明文件和安装方式，可以单独使用。

## Skills

| Skill | 用途 | 详细说明 |
| --- | --- | --- |
| `first-principles-decision` | 在购买、技术选型、产品设计、商业策略等复杂决策前，检查真实目标、隐藏假设、信息差和替代方案。 | [查看独立 README](first-principles-decision/README.md) |
| `no-repeat-skill` | 判断重复工作是否值得做成 Skill，并创建、重构、审查和验证可复用的 Agent Skill。 | [查看独立 README](no-repeat-skill/README.md) |

## 目录

```text
GodSkill/
├── README.md
├── first-principles-decision/
│   ├── README.md
│   ├── SKILL.md
│   └── _skillhub_meta.json
└── no-repeat-skill/
    ├── README.md
    ├── SKILL.md
    ├── references/
    ├── assets/
    ├── evals/
    ├── scripts/
    ├── agents/
    └── _skillhub_meta.json
```

## 安装

```bash
git clone https://github.com/GodAI-Master/GodSkill.git
```

克隆后，阅读目标 Skill 目录中的 `README.md`，将对应的完整子目录复制到你使用的 Agent skills 目录。

## 许可

MIT License
