# 分层配置

所有 PNG 为同尺寸 RGBA 画布，size 默认为 512；路径相对 rig.json。输入已去除眼睛的脸部底图，并通过独立眼睛图层叠回。不要用包含原眼睛的图片作为 body/head，否则眨眼时仍能看到原眼睛。

```json
{
  "size": 512, "frames": 400, "duration_ms": 20,
  "background": "#f7f3eb", "mode": "hop", "cycles": 8,
  "body": "body.png", "head": "head.png",
  "head_pivot": [256, 315], "ground": 392,
  "eyes": [{"path":"eyes.png", "center":[256,220]}],
  "feet": [], "overlay": "type.png", "camera": true,
  "blink_times": [0.55,2.48,4.42,4.73,6.53]
}
```

head、eyes、feet、overlay 可省略；省略的层不应出现对应动作。head_pivot 为局部头部旋转中心。eyes 可以每只眼一个层，也可同高双眼共用一个层；center 是闭眼垂直压缩的中心。feet 项为 `{ "path":"left.png", "pivot":[225,340], "phase":0 }`，phase 单位弧度。两脚通常相差 π，多足按支撑序列设置。

mode 为 expression/hop/walk/crawl，cycles 必须正整数以便首尾循环。overlay 层固定在画框内，用于环绕打字机字体。camera 为二维整体推近再回到起点，不是三维镜头。

渲染器接收 10ms 整数倍帧延时，默认 20ms=50fps。内存随尺寸和帧数增长；512×512×400 的 RGB 原始帧约 300MiB。不要直接用超大尺寸长片段；分段或流式实现需单独开发。基础脚摆角不等于足底锁定，专业行走必须按接地窗口校正脚世界位置。


仓库渲染器要求 walk 至少两只独立脚层，crawl 至少三只；单支撑使用 hop。没有 head 时不旋转眼睛来冒充局部点头。
