# Layered ZINE Poster · 上下分层对照式海报

将任意垫图转化为「上半层保真参照 + 下半层高级 ZINE 艺术转译」的海报提示词，或在可用图像工具中生成成品。适配人物、景物、建筑、环境、物品与混合主体。默认 2:3、上下各半、1 个版本；原始用例中的 `n=10` 可按需开启。

下层保留超过 65% 留白、米白纸面、一个高对比亮色几何色块、微弱丝网印刷质感、1–2 行主题文字与极小署名 `PlAyFoRgE`。人物脸部抽象，但妆造、轮廓、服饰纹样、姿态和气质保持辨识度。

## 样板展示

风格编号 **ZINE-001**。查看 [器物样板与生成说明](examples/README.md)。安装整个 ZINE 总入口后可用 `style=ZINE-001`；单独安装本 Skill 后仍用 `$layered-zine-poster`。

## 安装

在本仓库根目录，将 `layered-zine-poster` 文件夹复制到 Agent 的 Skills 目录。Codex 默认示例：

```bash
mkdir -p ~/.codex/skills
cp -R zine-library/styles/layered-zine-poster ~/.codex/skills/
```

自定义 `CODEX_HOME` 时使用相应的 `skills` 目录。其他 Agent 使用其支持的 Skill 发现机制加载 `SKILL.md`。

## 输入与调用

具体任务提供可读取的参考图；历史聊天里仅显示“曾附图”而没有图片内容，不算可用参考图。可提供角色名、重点保留部位、色彩或语言偏好。多张参考图默认逐张处理，需要融合时明确每张图的用途。

```text
使用 $layered-zine-poster，基于附图写一组可复制的海报提示词。
```

```text
使用 $layered-zine-poster，基于这张人物图，face_mode=featureless，
accent_color=钴蓝，n=10。保持发饰、刺绣和姿态，十版上层一致。
```

```text
使用 $layered-zine-poster，将这张寺庙建筑图做成海报，mode=image，
accent_color=朱红，text_language=zh。保留屋檐比例与装饰纹样。
```

```text
使用 $layered-zine-poster，分别处理这三张山景、街道环境和陶瓷器物图，
每张一版，mode=prompt。下层只提取各自主体，不重建整幅背景。
```

```text
使用 $layered-zine-poster，mode=template，给我不绑定具体题材的母提示词。
```

参数默认值、输入规则与输出契约详见 [SKILL.md](SKILL.md#输入与参数)。可以直接使用自然语言，无需记忆参数名。

## 输入 / 输出示例

示例输入（假设附图中可见）：一只象牙白陶瓷瓶，细长瓶颈、圆腹、钴蓝枝叶纹样，置于灰色桌面；请求 `mode=prompt`。

预期输出：一段完整、独立可复制的提示词，明确上层保持陶瓷瓶与桌面原构图；下层仅转译瓶体，保留细颈圆腹及钴蓝纹样，以纸本色块表现陶瓷质感；象牙白底，朱红单一圆形，小主体在中下部，留白 >65%；下层小字可为「一枝蓝，停在器物的呼吸里。」并署名 `PlAyFoRgE`；附完整负面约束。实际文字必须依据真实附图，不能机械套用这个示例。

人物用例应产生弱五官、无具体五官或抽象色块的下层脸部；建筑用例应保留结构比例；环境用例应提取空间骨架而非复制完整背景。

## 母提示词与文件

- [SKILL.md](SKILL.md)：Agent 入口、参数、输入要求、工作流、输出规则、负面约束与验收。
- [references/master-prompt.md](references/master-prompt.md)：可复制母提示词。
- [agents/openai.yaml](agents/openai.yaml)：Codex 界面名称与默认调用语句。

## 依赖与边界

写提示词不依赖额外服务；实际出图需要支持参考图的图像工具。Skill 不绑定模型专属语法，不把 `ar` 或 `n` 当作所有工具都支持的 API 参数，也不自动发布、归档或安装其他插件。

纯生成可能使上半层发生漂移；严格保真成品优先使用保留原图上层的合成或局部编辑能力。成品需检查留白、服饰纹样、文字及署名；只输出提示词不能等同于通过成品视觉验证。
