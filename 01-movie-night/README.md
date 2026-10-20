# 01 · movie-night

影视主题 · 10 个动态表情，Clawd 主演。眼睛始终是两个小黑方块，不画嘴，戏全靠动作和道具。

![preview](preview.png)

| # | 片名 | 动图 | 小剧情 |
|---|---|---|---|
| 1 | 降临克 Arrival | <img src="gif/arrival.gif" width="120"> | 盯着七肢桶的墨圈一笔画完，吓得一蹦 |
| 2 | 星际穿克 Interstellar | <img src="gif/interstellar.gif" width="120"> | 穿着宇航服在卡冈图雅旁边失重翻滚 |
| 3 | 肖申克的救赎 The Shawshank Redemption | <img src="gif/shawshank.gif" width="120"> | 从下水管里一点点挤出来，蹦上管口，雨中张开双臂，Free |
| 4 | 泰坦尼克号 Titanic | <img src="gif/titanic.gif" width="120"> | Rose 踩在 Jack 头上，两只一起在船头张开双臂起飞，海风吹动披肩 |
| 5 | 西游克 Journey to the West | <img src="gif/wukong.gif" width="120"> | 戴紧箍、扛金箍棒，踩着筋斗云飞 |
| 6 | 第九克 District 9 | <img src="gif/district9.gif" width="120"> | 母舰滴下的黑液让手变成虾钳，吓得狂甩 |
| 7 | 黑克帝国 The Matrix | <img src="gif/matrix.gif" width="120"> | 黑风衣，代码雨里下腰躲子弹 |
| 8 | 寻克环游记 Coco | <img src="gif/coco.gif" width="120"> | 万寿菊花瓣和彩旗下弹吉他 |
| 9 | 金刚克 Wolverine | <img src="gif/wolverine.gif" width="120"> | 金刚狼发型，欻欻欻弹出精钢爪 |
| 10 | 电锯惊克 Saw | <img src="gif/saw.gif" width="120"> | 雪花屏后出现在监控屏幕里（REC 闪烁），屏幕上一个字一个字打出 PLAY GAME，凑近、歪头、装深沉，然后信号断开 |

## 自己生成

```bash
cd src
pip install pillow
python clawd_movies.py          # 生成全部 10 个到 ../gif/
python clawd_movies.py matrix   # 只生成一个
```

肖申克里的 “Free” 用了 [Zpix 像素字体](https://github.com/SolidZORO/zpix-pixel-font)，把 `zpix.ttf` 放到 `src/` 里，或者设置 `ZPIX_FONT` 环境变量。
