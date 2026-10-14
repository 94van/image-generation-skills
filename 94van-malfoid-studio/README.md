# 94van Malfoid Studio

**中文 · English · 日本語 · 한국어**

全域组合式生图提示词工作室：内置中英日韩四语、24 类题材配方、可自由搭配的画面组件，以及四种风格的成图示例。通过文字组合主体、场景、动作、媒介、镜头、光线、配色与构图。

A multilingual text-to-image prompt studio with 24 domain recipes, combinable visual components, and four visual examples. Compose subjects, scenes, actions, media, cameras, lighting, palettes, and layouts in Chinese, English, Japanese, or Korean.

24分野のレシピ、自由に組み合わせられる画面要素、4種類の作例を備えた画像生成プロンプトスタジオ。中国語・英語・日本語・韓国語で、被写体、場面、動作、画材、カメラ、光、配色、構図を組み立てます。

24개 분야의 구성법, 자유롭게 조합하는 시각 요소, 4가지 완성 예시를 갖춘 이미지 생성 프롬프트 스튜디오입니다. 중국어·영어·일본어·한국어로 대상, 장면, 동작, 매체, 카메라, 조명, 색상, 구도를 구성합니다.

## 样图 · Gallery · 作例 · 갤러리

**暗夜电竞房 · Midnight Gaming Room**

![Midnight gaming room](examples/images/midnight-gaming-room.png)

| 薄荷魔法海报 · Aqua Magic | 冷光表情特写 · Emerald Close-up | 真人手绘本 · Cosplay & Sketchbook |
| --- | --- | --- |
| ![Aqua magic poster](examples/images/aqua-magic-poster.png) | ![Emerald close-up](examples/images/emerald-closeup.png) | ![Cosplay and sketchbook](examples/images/cosplay-sketchbook.png) |

[查看大图与提示词 · Images & prompts · 画像とプロンプト · 이미지와 프롬프트](examples/README.md)

## 四语内置 · Built-in languages

每种语言均包含组合流程、24 类题材模板和四条完整示例提示词。指定 `language=zh/en/ja/ko` 即可切换；未指定时跟随当前输入语言，也支持一次输出四语版本。

| Language | Guide | Example invocation |
| --- | --- | --- |
| 中文 | [中文创作指南](references/languages/zh-CN.md) | 使用 $94van-malfoid-studio，为 Malfoid 生成暗夜电竞房提示词，language=zh。 |
| English | [English guide](references/languages/en.md) | Use $94van-malfoid-studio to create an aqua magic poster prompt for Malfoid, language=en. |
| 日本語 | [日本語ガイド](references/languages/ja.md) | $94van-malfoid-studio で、Malfoid の冷たい光のアニメ顔アップのプロンプトを作成してください。language=ja。 |
| 한국어 | [한국어 가이드](references/languages/ko.md) | $94van-malfoid-studio로 Malfoid의 코스프레와 스케치북 사진 프롬프트를 작성해 주세요. language=ko. |

## 组合方式 · Compose

```text
主体 + 题材领域 + 主要媒介 + 场景 + 动作或摆放
+ 镜头 + 光线 + 配色 + 情绪 + 构图 + 输出参数
```

从人像、服装、城市、植物、奇幻、科幻、产品、建筑、交通工具到多人叙事与分镜，选一组题材配方，再自由搭配画面组件。指定自己的主体即可使用；人物创作也可直接调用 Malfoid 的默认形象。

```text
使用 $94van-malfoid-studio，围绕“雨夜车站”组合四套生图提示词：
赛璐璐动画、水彩、版画、电影摄影。每套使用不同动作、镜头和配色。
language=zh，ar=2:3，n=4。
```

```text
使用 $94van-malfoid-studio，为一瓶翠绿色香水组合三套产品广告提示词：
苔藓石台、玻璃展台、沙丘日落。language=zh，ar=4:5，n=3。
```

## 安装 · Install

```bash
git clone https://github.com/94van/image-generation-skills.git
mkdir -p ~/.codex/skills
cp -R image-generation-skills/94van-malfoid-studio ~/.codex/skills/
```

```text
使用 $94van-malfoid-studio，生成成年 Malfoid 的四张独立作品：
暗夜电竞房（16:9）、薄荷魔法海报（4:7）、冷光表情特写（4:7）、真人手绘本（9:16）。
保留铂金长发、碧绿眼睛与绿银配色；耳饰、衣装与署名按各示例设置。
每种风格一张。提示词用中文、英文、日文、韩文各输出一版。
```

## 资源 · Resources

- [SKILL.md](SKILL.md)：调用入口与语言选择。
- [题材配方](references/prompt-library.md) · [JSON](references/prompt-library.json)：24 组可组合模板与完整示例。
- [画面组件](references/composition.md)：媒介、场景、动作、镜头、光线、配色、情绪与构图。
- [样图提示词](examples/prompts.json)：四种风格的独立完整提示词。
