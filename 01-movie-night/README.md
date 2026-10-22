# 01 · movie-night

影视主题 · 20 个动态表情，Clawd 主演。眼睛是两个小黑方块（偶尔眯成 ^ ^ 或 > <），不画嘴，戏全靠动作和道具。

![preview](preview.png)

| # | 片名 | 动图 | 小剧情 |
|---|---|---|---|
| 1 | 降临克 Arrival | <img src="gif/arrival.gif" width="120"> | 盯着七肢桶的墨圈一笔画完，吓得一蹦 |
| 2 | 星克穿越 Interstellar | <img src="gif/interstellar.gif" width="120"> | 穿着宇航服在卡冈图雅旁边失重翻滚 |
| 3 | 肖申克的救赎 The Shawshank Redemption | <img src="gif/shawshank.gif" width="120"> | 从下水管里一点点挤出来，蹦上管口，雨中张开双臂，Free |
| 4 | 泰坦尼克号 Titanic | <img src="gif/titanic.gif" width="120"> | Rose 踩在 Jack 头上，两只一起在船头张开双臂起飞，海风吹动披肩 |
| 5 | 西游克 Journey to the West | <img src="gif/wukong.gif" width="120"> | 戴紧箍、扛金箍棒，踩着筋斗云飞 |
| 6 | 第九克 District 9 | <img src="gif/district9.gif" width="120"> | 母舰滴下的黑液让手变成虾钳，吓得狂甩 |
| 7 | 黑克帝国 The Matrix | <img src="gif/matrix.gif" width="120"> | 黑风衣，代码雨里下腰躲子弹 |
| 8 | 寻克环游记 Coco | <img src="gif/coco.gif" width="120"> | 万寿菊花瓣和彩旗下弹吉他 |
| 9 | 金刚克 Wolverine | <img src="gif/wolverine.gif" width="120"> | 金刚狼发型，欻欻欻弹出精钢爪 |
| 10 | 电锯惊克 Saw | <img src="gif/saw.gif" width="120"> | 雪花屏后出现在监控屏幕里（REC 闪烁），屏幕上一个字一个字打出 PLAY GAME，凑近、歪头、装深沉，然后信号断开 |
| 11 | 阿克正传 Forrest Gump | <img src="gif/forrest.gif" width="120"> | 腿上的铁支架崩飞，从慢跑到越跑越快 |
| 12 | 蜘蛛克 Spider-Man | <img src="gif/spider.gif" width="120"> | 红蓝战衣，倒挂在细细的蛛丝上挥手 |
| 13 | 哈利波克 Harry Potter | <img src="gif/harry.gif" width="120"> | 大巫师帽、圆眼镜、小闪电，挥魔杖冒出一串小爱心 |
| 14 | 星克大战 Star Wars | <img src="gif/starwars.gif" width="120"> | 死星下，蓝色绝地和红色西斯两只小克光剑对决 |
| 15 | 行克走克 The Walking Dead | <img src="gif/walkingdead.gif" width="120"> | 警长帽、左轮，> < 眼螃蟹式小碎步被丧尸一路追着跑 |
| 16 | 克门的世界 The Truman Show | <img src="gif/truman.gif" width="120"> | 推开天幕墙上的门：早安、午安、晚安 |
| 17 | 侏罗克公园 Jurassic Park | <img src="gif/jurassic.gif" width="120"> | 骑着霸王龙 ^ ^ 欢呼，脚下跑过一群美颌龙 |
| 18 | 痴克 Obsession | <img src="gif/obsession.gif" width="120"> | 折断许愿柳枝，token 金币哗哗往下掉 |
| 19 | 钢铁克 Iron Man | <img src="gif/ironman.gif" width="120"> | > < 眼焊初代机甲，方舟反应堆亮起来，开心蹦两下 |
| 20 | 魔女宅克 Kiki's Delivery Service | <img src="gif/kiki.gif" width="120"> | 顶着大红蝴蝶结骑扫把飞，黑猫吉吉坐在扫把头，尾巴垂下来轻轻晃 |

## 下载 / 在微信里用

- `gif/`：原尺寸 276×288，透明背景
- `wechat/`：240×240、每张 ≤100KB 的小尺寸版，透明背景

想在微信里用：把 `wechat/` 里的 GIF 发到「文件传输助手」，点开长按 →「添加到表情」就好啦。

## 自己生成

```bash
cd src
pip install pillow
python clawd_movies.py          # 生成前 10 个到 ../gif/
python clawd_movies.py matrix   # 只生成一个
python clawd_movies_more.py ../gif   # 生成后 10 个（第 11–20）
python clawd_movies_more.py ../gif ironman   # 只生成一个
```

肖申克里的 “Free”、电锯惊克的 PLAY GAME、克门的早安午安晚安用了 [Zpix 像素字体](https://github.com/SolidZORO/zpix-pixel-font)，把 `zpix.ttf` 放到 `src/` 里，或者设置 `ZPIX_FONT` 环境变量。
