# 写実素材 — 2026-10-15
Built-in image_genを使用。生成後の画像加工なし。透過画像をSVG内で重ねて回転。

- assets/venue-photo.png: Straight-on product photograph of traditional Japanese shopping-street garapon lottery stall. Blank white scalloped fabric awning, red-and-white vertical striped cloth, real fabric wrinkles, dark green steel A-frame without drum, brass catching tray, dark polished wooden countertop, alternating red/white tissue-paper pompom flowers. Diffuse daylight. No text, people, hands, UI or radial graphics.
- assets/drum-photo.png: Isolated orange octagonal Japanese garapon metal drum on genuinely transparent background. Exactly frontal centered view, orange enamel, subtle scratches, screws, central chrome hub, black outlet at upper right, off-white arrow. No stand, legs, tray, background or text. Product photography.

## 球状ハンドル修正
Built-in image_gen edit of drum-photo.png saved as assets/drum-knob.png. Prompt: Replace only the upper-right black component with a glossy spherical black bakelite handle on a short metal spindle. Rounded ball volume, upper-left highlights and contact shadow. Preserve octagon, hub, paint, arrow, screws, square frame and transparency.

## 2011年版を参考にしたTOPタイトル
Built-in image_gen. assets/title-gold.png: four kanji in a 2x2 layout, 福引 above 会場. Heavy chunky rounded Japanese lettering with warm golden faces and deep bronze extrusion, matching the original 2011 title. Transparent background, no sunburst, rays, buttons or additional text. Reference: user video frame at 00:00.

## 右寄せの会場素材
Built-in imagegen precise-object-edit of venue-photo.png; saved as assets/venue-right.png. Prompt: shift only the green support stand and brass tray slightly right, preserve their dimensions, vertical positions, the awning, curtains, tabletop, flowers and lighting; no drum or text. The edited stand axis is approximately (596,670), tray landing (253,1013); the SVG drum origin, pointer coordinates, ball landing and outlet were updated to match.
