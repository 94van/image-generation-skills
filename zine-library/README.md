# ZINE 风格库

一个持续扩充的 ZINE 创作目录。**先看样板选风格，再调用一个小 Skill。** 每种风格独立维护，新增风格不覆盖已有风格。

## 风格总表

| 编号 | 风格 / 小 Skill | 构图与视觉特征 | 适配题材 | 样板 | 调用 |
| --- | --- | --- | --- | --- | --- |
| ZINE-001 | [原影·纸译](styles/layered-zine-poster/README.md) | 上层保真，下层纸本抽象；>65% 留白、单一亮色块、诗性小字 | 人物、景物、建筑、环境、物品 | [查看器物样板](styles/layered-zine-poster/examples/README.md) | `style=ZINE-001` / `$layered-zine-poster` |

目前已收录 **1** 种风格。后续按 ZINE-002、ZINE-003…递增；编号保留，不因排序变化重编号。这里只列已完成条目，不把未创建的风格当作可用项。

## 样板画廊

### ZINE-001 · 原影·纸译

**上层保真，下层纸本转译的对照式 ZINE。**「原影」保留参考图的主体与氛围；「纸译」将同一主体转成留白充足的纸本艺术。辨识特征是上下对照、下层超过 65% 留白、单一亮色几何色块与细腻印刷颗粒；人物下层弱化五官，保留妆造、服饰、姿态和气质。

<img src="styles/layered-zine-poster/examples/ceramic-vase.png" width="360" alt="ZINE-001 器物风格样板：上层陶瓷瓶照片感，下层象牙白留白与朱红圆形" />

**合成风格样板**：原创生成的陶瓷瓶题材，上下均由图像模型生成。展示布局与视觉方向，不作为真实垫图保真能力的测试结果。[样板说明与完整生成提示词](styles/layered-zine-poster/examples/README.md)

## 怎么调用

安装总入口后，按编号选择，Agent 只读取选中的子 Skill：

```text
使用 $zine-library，style=ZINE-001，基于附图写一组海报提示词。
```

```text
使用 $zine-library，展示风格目录和样板，我先选一种。
```

单独安装小 Skill 后，也可直接调用：

```text
使用 $layered-zine-poster，基于附图生成上下对照 ZINE 提示词，n=3。
```

以后提供新风格时可以直接说：

```text
把下面这套新 ZINE 风格收进我的 ZINE 风格库，建立独立小 Skill，
更新总目录和样板说明，并提交到 GitHub。以下是提示词和参考图：……
```

## 安装方式

在仓库根目录执行。安装整个目录入口及随附风格：

```bash
mkdir -p ~/.codex/skills
cp -R zine-library ~/.codex/skills/
```

这会通过 `$zine-library` 路由读取所选风格，不要求 Agent 自动发现嵌套 Skill。

只想直接调用某个小 Skill，则单独复制它：

```bash
mkdir -p ~/.codex/skills
cp -R zine-library/styles/layered-zine-poster ~/.codex/skills/
```

自定义 `CODEX_HOME` 时改用其 `skills` 目录。安装更新遵循宿主的重新加载方式。此前已安装的小 Skill 可以继续使用；更新它时从新的子目录复制。总库和单独安装的小 Skill 是两个安装副本，更新仓库不会自动同步本机副本。

## 目录结构

```text
zine-library/
├── README.md                       # 风格总表 + 样板画廊
├── SKILL.md                        # 总入口：选风格、按需读取、收录新风格
├── agents/openai.yaml
├── references/add-style.md         # 新风格收录规范
└── styles/
    └── layered-zine-poster/         # ZINE-001，独立可安装
        ├── SKILL.md
        ├── README.md
        ├── agents/openai.yaml
        ├── references/master-prompt.md
        └── examples/               # 样板图、来源说明、生成提示词
```

新风格使用 `styles/<skill-name>/`，保持同样的可独立调用结构。每种风格定义自己的构图、纸张、文字、颜色和负面约束；不要求所有 ZINE 都采用上下分层。[新风格收录规范](references/add-style.md)
