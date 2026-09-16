# 灵动造物｜极简 IP 动画工坊

从有辨识度的极简角色，到眨眼、点头和按身体结构移动的真实 GIF。独立于 ZINE 系列；适合机器人标志、品牌吉祥物、头像动效与循环贴图。

调用名：`94van-ip-gif-studio`。源自用户提供的《PlayForge：从极简 IP 标志到 50fps GIF 的完整教程》。默认 PlayForge 品牌可以替换，默认 512px、400 帧、20ms/帧、8 秒，无限循环。

## 样板

![原创几何机器人管线演示](examples/demo.gif)

此图为随附脚本生成的几何机器人演示，不是历史十款成品或图像模型新设计的高档 IP。[演示说明与实测报告](examples/README.md)

## 安装

在个人生图仓库根目录执行：

```bash
mkdir -p ~/.codex/skills
cp -R 94van-ip-gif-studio ~/.codex/skills/
```

使用自定义 CODEX_HOME 时改用其 skills 目录。Python 动画依赖建议安装到独立环境：

```bash
cd 94van-ip-gif-studio
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/make_demo.py ./work/demo
.venv/bin/python scripts/render_gif.py ./work/demo/rig.json ./work/demo/demo.gif
.venv/bin/python scripts/validate_gif.py ./work/demo/demo.gif --size 512 --frames 400 --duration-ms 20
```

## 调用示例

```text
使用 $94van-ip-gif-studio，为 PlayForge 设计 3 款不同轮廓的极简机器人，先只给静态设计提示词。
```

```text
使用 $94van-ip-gif-studio，将附图角色制作成 512px、50fps、8 秒 GIF。
自然眨眼和小幅点头，不挥手；按原有肢体决定轻跳、走动或爬行，底部固定品牌文字。
```

```text
使用 $94van-ip-gif-studio，运行 demo 并检查帧数、逐帧延时、不同帧和循环。
```

## 文件与边界

- [SKILL.md](SKILL.md)：输入参数、工作流、输出与验收。
- [母提示词](references/master-prompt.md)、[原教程与来源说明](references/tutorial.md)、[rig 配置](references/rig.md)。
- [make_demo.py](scripts/make_demo.py)：原创几何测试图层。
- [render_gif.py](scripts/render_gif.py)：明确图层的二维动画渲染。
- [validate_gif.py](scripts/validate_gif.py)：逐帧解码与规格验证。

脚本不自动抠图，不恢复三维骨骼，不生成十种风格，也未实现足底锁定。walk/crawl 是基础摆角演示；高质量步态需额外修正。实际播放速度受设备影响；GIF 帧延时以 10ms 为单位。历史十款文件未附入本仓库，其教程记载未独立复核。
