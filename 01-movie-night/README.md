# 01 · movie-night

影视主题 · 8 个动态表情，Clawd 主演。眼睛始终是两个小黑方块，不画嘴，戏全靠动作和道具。

![preview](preview.png)

| # | 片名 | 动图 | 小剧情 |
|---|---|---|---|
| 1 | 降临 Arrival | <img src="gif/arrival.gif" width="120"> | 盯着七肢桶的墨圈一笔画完，吓得一蹦 |
| 2 | 星际穿越 Interstellar | <img src="gif/interstellar.gif" width="120"> | 穿着宇航服在卡冈图雅旁边失重翻滚 |
| 3 | 肖申克的救赎 The Shawshank Redemption | <img src="gif/shawshank.gif" width="120"> | 雨中张开双臂，Free |
| 4 | 泰坦尼克号 Titanic | <img src="gif/titanic.gif" width="120"> | Rose 披着披肩在船头张开双臂，Jack 在身后搂着，海风吹动披肩 |
| 5 | 西游记 Journey to the West | <img src="gif/wukong.gif" width="120"> | 戴紧箍、扛金箍棒，踩着筋斗云飞 |
| 6 | 第九区 District 9 | <img src="gif/district9.gif" width="120"> | 母舰滴下的黑液让手变成虾钳，吓得狂甩 |
| 7 | 黑客帝国 The Matrix | <img src="gif/matrix.gif" width="120"> | 黑风衣，代码雨里下腰躲子弹 |
| 8 | 寻梦环游记 Coco | <img src="gif/coco.gif" width="120"> | 万寿菊花瓣和彩旗下弹吉他 |

## 自己生成

```bash
cd src
pip install pillow
python clawd_movies.py          # 生成全部 8 个到 ../gif/
python clawd_movies.py matrix   # 只生成一个
```

肖申克里的 “Free” 用了 [Zpix 像素字体](https://github.com/SolidZORO/zpix-pixel-font)，把 `zpix.ttf` 放到 `src/` 里，或者设置 `ZPIX_FONT` 环境变量。
