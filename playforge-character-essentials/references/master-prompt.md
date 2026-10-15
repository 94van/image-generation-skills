# 94｜PLAyfORGE CHARACTER ESSENTIALS GENERATOR

通用角色衣橱图鉴｜双路径自适应母提示词

本模板将原始角色图鉴的构图逻辑通用化：人物、穿搭、配色和物品均由输入确定。`{{...}}` 是有意保留的模板变量；交付具体提示词或调用图像工具前必须全部展开。输入有图片时，实际检查图片，再按 [拆解规则](adaptation.md) 建立蓝图。仅提示词文本不能代替传入参照图。

## 任务参数

```text
MODE = AUTO | REFERENCE | CHARACTER | HYBRID
CHARACTER = 目标角色名称或原创人物描述
WORK = 所属作品、世界观或 AUTO
REFERENCE_IMAGES = 实际附件与各图用途；没有则为空
THEME = AUTO | 衣橱与服饰 | 装备与武器 | 生活用品与收藏 | 综合 Essentials
ASPECT_RATIO = 4:7
N = 1
STYLE = 精致日系二维角色设定集 × 柔和复古水彩
SIGNATURE = @PLAyfORGE_
WATERMARK = invisible
OUTPUT = 提示词 | 图片
```

`N` 控制任务的独立成品总数，不能在一张画布里铺成 N 格。`SIGNATURE` 只是生成后暗水印的作者数据，不能要求模型把它画到图片上；实际嵌入与核验按 [暗水印说明](watermark.md) 执行。先解析模式并确定每张蓝图，随后为每张使用以下单张模板。参数值可由自然语言推导，缺省值不是强制限制用户的选择。

## 单张完整模板

### 01｜画幅与目标

生成一张独立完整的 {{ASPECT_RATIO}} {{CANVAS_ORIENTATION}} {{CHARACTER_TITLE}} CHARACTER ESSENTIALS 角色图鉴。只出现一名中央全身角色，周围是分离陈列的服饰、配件和专属物品。它是一幅完整插画，不是分镜、拼图、角色多视图或照片拼接。

本张使用 {{RESOLVED_MODE}} 模式：{{SOURCE_RULES}}。固定 {{IDENTITY_LOCKS}}；本张主题为 {{THEME}}。所有衣橱和道具属于同一角色与世界观，设计细节有统一的色彩、材质和符号逻辑。

### 02｜核心视觉风格

{{STYLE_DESCRIPTION}}。

默认风格：精致日系角色漫画插画 × Anime Fashion Essentials Character Sheet × 角色衣橱与专属物品图鉴 × 柔和复古水彩 × 高级角色设定集。极细且干净的浅棕／灰色轮廓线，轻柔赛璐璐阴影，半透明水彩晕染，柔和奶油色高光。服装褶皱、针织、缝线、蕾丝或刺绣仅在所选衣物需要时准确呈现；金属、皮革、纸张与玻璃具有不同表面质感。

配合角色保留自然肤色和体型，不强制瓷白皮肤或纤瘦女性化身材。画面细腻、清晰、克制，统一人物与物品的绘制精度。若已明确选用其他画风，用具体风格描述替换本段默认风格，不将冲突的媒介要求叠加。

### 03｜中央人物自动设定

人物是 {{CHARACTER_IDENTITY_AND_VERSION}}，外观与识别点为 {{FACE_HAIR_EYES_SKIN_BODY}}，年龄表现和气质为 {{AGE_AND_TEMPERAMENT}}。保留 {{CANONICAL_OR_REFERENCE_MARKERS}}，不要替换为来源示例中的人物。

正面或轻微四分之三站姿，{{POSE_AND_EXPRESSION}}。重心合理，双手结构清楚、动作简洁，不遮挡脸与核心服装。头顶、发梢、手部和脚部／鞋底都在画内；脚下留空，不裁切任何身体部位。角色只出现一次。

### 04｜中央穿搭与细节

人物穿着 {{CENTRAL_OUTFIT}}，包括 {{OUTFIT_LAYERS_AND_FASTENINGS}}。轮廓、裁片、开合、领口、袖型和衣褶符合穿着逻辑。使用 {{CENTRAL_OUTFIT_MATERIALS_AND_PALETTE}}，标志细节为 {{CENTRAL_OUTFIT_SYMBOLS}}。

中央穿搭应符合角色身份、年龄和指定版本；默认不透明的完整服装或得体基础搭配。周围陈列单品与中央穿搭相互呼应，但不需要为了展示衣橱而让人物脱衣。{{FOOTWEAR_OR_BAREFOOT_DETAIL}}。若画出人类赤足，脚趾结构自然、没有多余或融合；穿鞋时保持鞋型和左右脚透视正确。

### 05｜构图与左右物品排布

Composition: One central full-body character surrounded by individually floating wardrobe essentials, in a balanced, symmetrical yet organic fashion flat-lay arrangement. One continuous canvas, one character, no panels.

默认竖版中，中央人物宽度约占画面 40%，高度约占 84%；以完整全身、顶部标题与底部留白和物品清晰度为优先，可适度调整比例。方形或横版需重新安排人物占比与物品密度。较大的衣物放在两侧上中部，长物沿侧边展开，小饰品穿插于空隙，较重的书本或包袋稳定下部视觉。左右视觉重量平衡，不要求逐件镜像。

画面左侧从上到下：
{{LEFT_ITEMS_NUMBERED_WITH_SHAPE_COLOR_MATERIAL_DETAILS}}

画面右侧从上到下：
{{RIGHT_ITEMS_NUMBERED_WITH_SHAPE_COLOR_MATERIAL_DETAILS}}

每件物品都完整、单独悬浮、具有清晰轮廓与呼吸间距。物品不切边、不融合、不互相遮挡，不覆盖人物脸部、手脚或标题。空衣服中没有人头、手臂、腿或人体模型。成对鞋袜保留各自结构。优先展示有身份关联的物件，避免装饰堆满背景。

### 06｜背景与角色自适应配色

背景为 {{BACKGROUND}}，默认纯净奶油白纸张与极轻微暖白纹理。角色主色 {{PRIMARY_COLORS}}，辅色 {{SECONDARY_COLORS}}，金属／点缀色 {{ACCENT_COLORS}}；不同深浅的同类颜色用于建立层次，不污染角色的代表配色。

使用极少量 {{CHARACTER_RELEVANT_ORNAMENTS}} 点缀空白，装饰符号仅来自当前角色的身份或用户指定改编。背景高亮、低干扰，服饰道具质感清楚，保持疏密有序与足够负空间。

### 07｜画内标题与无可见水印

{{LETTERING_INSTRUCTIONS}}

默认顶部居中第一行精确写「{{ENGLISH_CHARACTER_TITLE}}」，第二行精确写「E S S E N T I A L S」。标题字体根据世界观调整：古典衬线、简洁现代、机械几何或其他契合的字形；保持克制、清晰、层级分明，不默认套用魔法学院字体。

底部与画面任何位置都不要绘制作者签名、用户名、Logo、品牌文字或低透明度水印。脚下保持干净留白。暗水印是生成后的文件处理，不是要画出的图案或文字。

只有用户需要的文字进入画面；默认不添加额外说明、物品编号、乱码、中文或日文标签。用户提供其他语言标题时按原文使用。用户要求完全无文字时，删除本节的标题和全部字母标签；不可见暗水印不属于画内文字，仍在生成后按配置处理。

### 08｜画质与完整性

Premium character essentials illustration, delicate clean line art, coherent character identity, sophisticated outfit breakdown, carefully rendered fabric and material textures, readable floating accessories, elegant visual hierarchy, balanced negative space, complete full-body composition, high-resolution finish.

{{STYLE_SPECIFIC_QUALITY_TERMS}}。所有独立服饰道具形状可辨、材质统一，角色面部、手部、脚部和服装结构清楚自然。全幅完成度一致，不只精细刻画脸部而让周围物品模糊。

### 09｜排除与最终确认

不要拼图、九宫格、漫画分镜、分割画框、照片拼接、多个完整人物、重复角色、头像小窗、背面人物或独立人体局部。不要裁切头顶、发梢、手脚、鞋底、衣服或道具。不要多余肢体、多余手掌、重复脚掌、错接关节、融合手指、异常脚趾、身体部件附着在悬浮衣物上。非人类角色遵守已经明确的物种结构。

不要无关世界观符号、错误角色配色、拥挤背景、不可辨认的服饰、文字乱码或可见作者签名。{{STYLE_SPECIFIC_EXCLUSIONS}}。

最终产物：一张 {{ASPECT_RATIO}} 的 {{CHARACTER_TITLE}} ESSENTIALS 独立完整图鉴；中央只有一个全身角色，左右物品分离悬浮、完整可辨；{{FINAL_LETTERING_STATE}}，无可见作者签名或水印。本次渲染只生成这一张，不画多格合成。

## 展开规则

- `SOURCE_RULES`：REFERENCE 写明保留哪些实际图中特征；CHARACTER 写明作品／OC 与版本；HYBRID 明确身份来自目标、哪些视觉层面来自哪张参考图。不要在最终提示词中留待选择的模式列表。
- `CANVAS_ORIENTATION` 由宽高比决定：宽小于高为竖版，相等为方形，宽大于高为横版；默认 `4:7` 为竖版，不产生「16:9 竖版」等矛盾表述。
- `LEFT_ITEMS…` 与 `RIGHT_ITEMS…`：替换成已设计好的逐项清单，含材质、颜色、形状和标志细节。不能保留「AI 自动设计 N 件」作为清单。
- 没有合适的英文角色名时，优先用户名字或可靠的转写；原创描述可使用简短身份标题，不捏造“官方英文名”。
- 默认风格的 `STYLE_SPECIFIC_EXCLUSIONS` 为厚重黑描边、三维渲染、写实摄影、油画、粗糙草图与低质量平涂。用户选了这些媒介之一时，替换不适用的排除项，不能一边要求一边禁止。
- `signature=NONE` 或 `watermark=off` 关闭生成后的暗水印步骤；「完全无文字」只删除标题、书脊字样与标签，默认保留暗水印。`ar`、标题、水印状态的各处表述必须一致。无论是否嵌入暗水印，都不能默认绘制作者标识。
- 默认在画外说明补全来源、批次编号和总张数；用户只要提示词时省略额外说明，来源区分保留在内部蓝图。图像工具可用的尺寸、参考图参数及一次输出数量，以工具真实能力为准，不编造 API 字段。
