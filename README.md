# 个人生图 Skills

94van 的个人生图 Skill 收藏库。按创作系列组织，每个系列有总目录，每种风格有独立可调用的 Skill、提示词和样板。后续新系列与 ZINE 并列收录。

## 系列总目录

| 系列 | 内容 | 入口 |
| --- | --- | --- |
| ZINE 风格库 | 风格目录、样板画廊、独立风格 Skill；目前收录 ZINE-001「原影·纸译」：上层保真、下层纸本转译 | [浏览目录与样板](zine-library/README.md) |

## 目录结构

```text
image-generation-skills/
├── README.md
└── zine-library/
    ├── README.md                  # ZINE 总目录与样板画廊
    ├── SKILL.md                   # 系列路由入口
    └── styles/
        └── layered-zine-poster/   # ZINE-001 独立小 Skill
```

## 安装与使用

```bash
git clone https://github.com/94van/image-generation-skills.git
cd image-generation-skills
mkdir -p ~/.codex/skills
cp -R zine-library ~/.codex/skills/
```

安装后通过总入口选择风格：

```text
使用 $zine-library，调用 ZINE-001，基于附图生成海报提示词。
```

也可只安装一个小 Skill：

```bash
cp -R zine-library/styles/layered-zine-poster ~/.codex/skills/
```

```text
使用 $layered-zine-poster，基于附图生成上下分层对照式 ZINE 海报提示词。
```

自定义 CODEX_HOME 时使用其 skills 目录。仓库内容不会自动安装到本机；安装或更新后按 Agent 的方式重新加载。

## 后续收录

新 ZINE 风格放在 `zine-library/styles/<skill-name>/`，更新系列目录和样板；新的生图系列放在仓库根目录的独立系列文件夹，再登记到本页。每个小 Skill 保留自己的规则，避免不同风格互相覆盖。

每个风格包含有效的 SKILL.md、使用说明、可复制母提示词及样板说明。真实参考图转译与合成展示样板分别标注，不把展示图当作保真测试结果。
