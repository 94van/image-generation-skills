---
name: 94van-malfoid-studio
description: Compose ready-to-use text-to-image prompts in Chinese, English, Japanese, or Korean by combining subject, scene, action, medium, camera, lighting, palette, and layout. Use for broad visual ideation, Malfoid character art, portraits, products, architecture, nature, fashion, fantasy, posters, and storyboards.
---

# 94van Malfoid Studio

中文 · English · 日本語 · 한국어

## Choose the language

Use the explicitly requested language first; otherwise match the user's message. Accept `language=zh`, `zh-CN`, `en`, `ja`, or `ko`. Produce all four versions when requested. Preserve `Malfoid`, `@PLAyfORGE`, filenames, example IDs, `ar`, and `n` exactly across languages.

Read the selected language guide for the workflow, 24 domain templates, composition recipe, and four complete examples:

| Language | Built-in guide |
| --- | --- |
| 中文 | [中文创作指南](references/languages/zh-CN.md) |
| English | [English creation guide](references/languages/en.md) |
| 日本語 | [日本語制作ガイド](references/languages/ja.md) |
| 한국어 | [한국어 제작 가이드](references/languages/ko.md) |

## Compose the prompt

1. Produce complete text-to-image prompts by default. Generate images when the user asks for images. Infer workable visual choices from a short theme so the user can start with one sentence.
2. Use the subject specified in the user's text. For a character request without another character specification, use Malfoid: a 25-year-old adult woman with long platinum-blonde hair, emerald eyes, black hoop earrings, a white collared shirt, a green-and-silver striped tie, a charcoal knit vest, and a black robe with emerald lining. For product, architecture, nature, or vehicle requests, focus on the requested subject.
3. Choose one primary domain and one dominant visual medium. Combine subject + setting + action or arrangement + viewpoint + lighting + palette + mood + composition. Read the matching domain recipe and the component bank when useful. Create an appropriate combination for subjects beyond the listed domains as well.
4. Turn the selected ingredients into coherent visual prose. Specify concrete positions, material surfaces, focal hierarchy, and spatial relationships. Expand every placeholder. Resolve competing media, light directions, and camera positions into one intentional scene. User-specified details take priority over defaults.
5. Keep the subject's defining features fixed across a series. Within one medium, vary one or two dimensions per prompt. For a combination of styles, choose a distinct primary medium for each prompt and coordinate its setting, lighting, and palette. Make each prompt self-contained. For multiple characters, name each person's position, action, and prop ownership explicitly.
6. Apply the requested language, aspect ratio, count, and lettering. Defaults: `ar=2:3`, `n=1`, one discreet `@PLAyfORGE` signature at the bottom right. User-supplied `n` counts the total standalone images across all concepts unless explicitly stated per concept. For three concepts and `n=3`, allocate one image to each and show `n=1` on each prompt. Panel counts describe the layout within one image. Translations do not increase image count. A completely text-free request also omits the signature.

## Deliver

For each variation, provide a short style title, one complete copy-ready prompt, and its parameters. Match the user's requested output format. When all four languages are requested, preserve identical visual content and parameters across translations.

For image requests, use the available image-generation tool, create the requested standalone images, and inspect subject features, anatomy where applicable, materials, layout, count, and lettering before presenting the results.

## Resources

- [Composition components](references/composition.md): visual media, settings, actions, cameras, lighting, palettes, moods, and layouts.
- [Domain recipes](references/prompt-library.md) · [JSON](references/prompt-library.json): 24 combinable templates and complete examples, searchable by domain `id`. Express their visual ingredients in the selected output language.
- [Example gallery](examples/README.md): four finished visual examples and their prompt links.
- [Example prompts](examples/prompts.json): four standalone style recipes with image paths.
