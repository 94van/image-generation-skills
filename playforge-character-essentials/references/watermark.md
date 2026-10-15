# 不可见签名与原始 PNG 追踪

生成阶段不要把 `@PLAyfORGE_` 画进图片。使用 `scripts/invisible_watermark.py` 在最终 PNG 副本中写入机器可提取的签名；原始源图保持不变。该脚本不联网，只依赖 Python 3.10+ 和 Pillow。

## 写入与验证

在 Skill 目录下执行，示例中的路径替换为实际路径；输出目录须已存在：

```bash
python3 scripts/invisible_watermark.py embed source.png final.png
python3 scripts/invisible_watermark.py inspect final.png
```

写入后产生两个独立文件：`final.png` 和 `final.png.watermark.json`。两个目标文件只要有一个已存在，命令就会拒绝覆盖；不提供强制覆盖选项，也不能把源图、输出图和 manifest 指向同一文件。已经含有 PlayForge 水印的图像不会被重复写入，请使用原始未标记图片。

`--owner` 可显式改变默认所有者标识 `@PLAyfORGE_`。`--manifest path.json` 可在两个命令中指定旁车记录路径；`inspect` 未指定时自动检查图片旁的 `图片文件名.png.watermark.json`（若存在）。移动图片和旁车文件时应同时保留二者；图片改名后可用 `--manifest` 显式关联原记录。

脚本只接受位深不超过 8 的静态 PNG，输出仍为 PNG；更高位深会被拒绝，避免静默损失精度。RGB、RGBA、灰度和带调色板透明度的 PNG 可用；后两者会转换为 RGB/RGBA。RGBA 的透明度、红通道和绿通道保持不变，载荷区域每个像素的蓝通道最多变化 1 个数值。透明像素也参与编码，其 alpha 不变。不会增加可见文字、图形或边角标记。

保留源图的 ICC、DPI、EXIF、文本元数据，以及原始 `gAMA`、`sRGB`、`cHRM` 色彩块，避免因丢失这些显示信息改变颜色呈现；色彩块校验和损坏时拒绝写入。其他未支持的私有 PNG 块不承诺保留。

## 实际保存的信息

- `owner`：默认 `@PLAyfORGE_`。
- `artwork_id`：每次成功写入新生成的 UUID。
- `created_utc`：包含微秒的 UTC 写入时间。
- `source_sha256`：未修改源 PNG 文件字节的 SHA256。
- `schema`：载荷格式版本。

像素载荷按行从左到右、从上到下写入蓝通道最低位，采用 `PFWMARK1` magic、32 位长度、32 位 CRC32 和 UTF-8 JSON。magic、长度与 CRC32 用于识别格式及检测意外损坏。相同 JSON 另存于 PNG 文本元数据 `playforge.watermark`，方法名保存在 `playforge.watermark.method`。

旁车 manifest 保存相同载荷、编码信息、图像尺寸，以及**最终输出 PNG 文件的 SHA256**。输出哈希只写在旁车中，避免在图片内存入其自身哈希形成循环。源文件哈希提供追踪线索；只有持有对应源文件并自行计算同一 SHA256，才能进一步确认它是否匹配。

## 检查结果与退出码

所有命令向标准输出写 JSON；只有明确返回 `status=valid` 才表示此次验证通过。

| 退出码 | 状态 | 含义 |
| --- | --- | --- |
| 0 | `embedded` / `valid` | 新文件写入成功，或像素载荷与 PNG 元数据一致，且可用／指定的 manifest 校验通过 |
| 1 | `error` | 参数、文件格式、容量或读写错误；包括拒绝覆盖 |
| 2 | `absent` | 没有识别到水印，也没有对应元数据或旁车记录 |
| 3 | `invalid` | CRC32、JSON、元数据、旁车记录或文件哈希不一致，或指定的 manifest 缺失 |

无旁车文件时，`inspect` 仍可提取并交叉检查像素水印与 PNG 文本元数据；`checks.manifest=null` 明确表示没有进行最终文件哈希比对。不要把这种结果描述成已核验原始文件字节。若元数据被移除但像素载荷保留，仍会返回提取到的 `watermark`，同时返回 `invalid`，指出完整验证未通过。

## 保证边界

仅保证工具输出的**原始无损 PNG**可按上述格式提取和核对。裁剪、缩放、截图、颜色变换、重绘、平台转码和有损重压缩可能破坏载荷；即使像素未变，重新保存或删除元数据也可能让文件哈希或元数据校验不通过。

这是可读取、可修改的明文追踪标记，**不是加密、数字签名、防伪技术或版权认证**。CRC32 检测意外损坏，不防蓄意篡改。SHA256 用于核对文件字节，不独立证明作者身份或拥有权。需要让后续使用者保留原始 PNG 与旁车记录；不能承诺传播后仍可追踪。
