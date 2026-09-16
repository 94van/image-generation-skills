---
name: 94van-ip-gif-studio
description: Create distinct minimal IP mascots and turn explicit 2D character layers into real looping GIFs with blinking, small nods, and structure-aware hopping, walking or crawling. Use for PlayForge、灵动造物、极简机器人 IP、角色标志动效、50fps GIF and layered mascot animation; not for ZINE posters or automatic 3D rig recovery.
---

# 灵动造物｜极简 IP 动画工坊

从静态极简角色到真实可播放的 GIF：角色轮廓有辨识度，眼睛完整友善，眨眼是眼部局部动作，点头是头部动作，移动方式由已有肢体结构决定。PlayForge 机器人为默认示例；品牌、主体、数量与动作按用户需求调整。

## 输入与参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `mode` | 按请求推断 | `design` 原创造型/提示词；`animate` 已有角色动画；`demo` 验证管线；`full` 从设计到交付 |
| `brand` | `PlayForge` | 底部文字；可替换为用户品牌 |
| `subject` | 极简 AI robot | 可替换角色；保留已有角色身份与结构 |
| `n` | `1` | 独立设计与文件数，各款轮廓应清楚可辨 |
| `size` | `512` | 正方形输出边长，脚本支持 32–2048；高尺寸高帧数需考虑内存 |
| `frames` | `400` | 默认 8 秒；总时长 = frames × duration_ms |
| `duration_ms` | `20` | 10ms 的正整数倍；20ms 对应标称 50fps，按延时计算实际规格 |
| `motion` | 按结构选择 | `expression / hop / walk / crawl`，无腿轻跳、双足步行、多足爬行 |
| `cycles` | `8` | 正整数，周期动作在片长内闭合 |
| `camera` | `true` | 二维缓推再回到起点，形成循环跟随效果 |
| `background` | `#f7f3eb` | GIF 默认先合成到纯色底，不承诺完整半透明 |

`animate` 需可访问的原图或已分层 PNG + rig.json；素材不全时补齐后制作。`demo` 可直接运行随附几何角色示例。

## 工作流程

1. **设计。** 阅读 [references/master-prompt.md](references/master-prompt.md)，按请求输出提示词或使用可用图像工具创造静态角色。大量留白、少量色彩、清晰轮廓与负空间，底部小而纤细的复古打字机字体；64px 缩略下仍可辨认。用户指定 n 时逐款独立交付。详见 [references/tutorial.md](references/tutorial.md) 的设计方向表，根据主体选择视觉语言。
2. **分层。** 按 [references/rig.md](references/rig.md) 准备同尺寸 RGBA body/head/eyes/feet/overlay。先修复脸底原眼及 alpha，再叠眼层；清除旧阴影与旧文字。人工核对轮廓、枢轴、足底及关节重叠区，浅色身体采用可靠的轮廓蒙版。图像编辑使用当前环境可用且符合其规则的工具。渲染脚本接收预先准备的二维图层。
3. **表情。** 眨眼约 70ms 合、40ms 闭、130ms 开，局部最小眼高约 4%；双眼同步或极轻微时差。点头 2–4°，眼睛随头部一起动；局部点头需独立 head，眨眼需独立 eyes。缺少相应图层时先补充分层。
4. **移动。** 默认不挥手、不新增肢体。无腿按底部锚点预压—腾空—落地恢复，阴影联动；单支撑用轻跳；双足相差半周期；多足错相维持支撑。渲染器 walk 至少两脚，crawl 至少三脚。基础脚本只做关节摆角，未实现脚底世界坐标锁定；要求自然步态时需进一步修正接地轨迹。
5. **镜头与循环。** 文字固定画框，地标反向滚动表达跟随。前 6 秒缓推、后 2 秒回归是默认 8 秒镜头的折中。严格单向长推与无缝回到固定起始构图冲突时，说明取舍，可按用户选择做非循环视频或转场。最后一帧为 (N−1)×dt，不重复首帧。
6. **渲染。** 使用 [scripts/render_gif.py](scripts/render_gif.py)，共用采样调色板，默认关闭抖动，20ms 帧延时、无限循环、原子写入，再重新逐帧解码。内存随尺寸与帧数增长，默认 RGB 帧约 300MiB，实际峰值更高；多角色串行渲染，不同时囤积多套帧。
7. **验收。** 使用 [scripts/validate_gif.py](scripts/validate_gif.py) 检查格式、尺寸、帧数、逐帧时长、总时长、无限循环、不同帧、大小和 SHA256。首尾差只用于排查，不能替代观看。查看闭眼、抬头/低头、起跳/落地、首尾衔接关键帧；有播放工具时观看动画。检查残眼、文字、肢体、黑边、滑步、穿地与闪烁，如实说明缺陷及未完成的视觉验证。

## 执行与交付

依赖 [requirements.txt](requirements.txt)，Python 3 + Pillow。从本 Skill 目录运行：

```bash
python scripts/make_demo.py ./work/demo
python scripts/render_gif.py ./work/demo/rig.json ./work/demo/demo.gif
python scripts/validate_gif.py ./work/demo/demo.gif --size 512 --frames 400 --duration-ms 20
```

[scripts/make_demo.py](scripts/make_demo.py) 生成几何机器人图层与 rig 配置，用于快速体验工作流。制作新角色时，按设计需求准备原画与分层，再配置表情和移动轨道。

实际动画交付独立 GIF、所用参数与分层/rig、校验报告和预览；多款按需要打包合集。只要设计提示词时无需渲染。交付前核对实际格式与规格，明确已完成内容及待补充项。样板与校验报告见 [examples/README.md](examples/README.md)。
