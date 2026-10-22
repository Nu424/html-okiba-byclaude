"""生成画像(1024px)から、タイル付きの正方形アイコンPNGを作る。

使い方: python tools/make_icon.py <生成画像> <出力PNG>
被写体(暗色・彩度のある画素)だけを切り出し、淡色の角丸タイルの中央に再配置する。
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SIZE = 256          # 出力サイズ
TILE = "#faf5ee"    # タイル色(クリーム)
SUBJECT_RATIO = 0.64  # 被写体がタイルに占める最大比率
RADIUS_RATIO = 0.22   # 角丸の半径比


def subject_bbox(img: Image.Image):
    a = np.asarray(img.convert("RGB")).astype(int)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    mask = (lum < 150) | (sat > 90)
    ys, xs = np.where(mask)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def main(src: str, dst: str) -> None:
    img = Image.open(src).convert("RGB")
    x0, y0, x1, y1 = subject_bbox(img)
    crop = img.crop((x0, y0, x1, y1))
    # 被写体の周囲の淡色(背景・影)を透過にしてタイル色になじませる
    arr = np.asarray(crop).astype(int)
    dist = 255 - arr.min(axis=2)
    alpha = np.clip((dist - 45) * 6, 0, 255).astype(np.uint8)
    crop_rgba = crop.convert("RGBA")
    crop_rgba.putalpha(Image.fromarray(alpha))
    scale = SIZE * SUBJECT_RATIO / max(crop.size)
    new = (round(crop.width * scale), round(crop.height * scale))
    crop_rgba = crop_rgba.resize(new, Image.LANCZOS)

    tile = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    mask = Image.new("L", (SIZE * 4, SIZE * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, SIZE * 4 - 1, SIZE * 4 - 1), radius=int(SIZE * 4 * RADIUS_RATIO), fill=255)
    mask = mask.resize((SIZE, SIZE), Image.LANCZOS)
    tile.paste(Image.new("RGBA", (SIZE, SIZE), TILE), (0, 0), mask)
    tile.alpha_composite(crop_rgba, ((SIZE - new[0]) // 2, (SIZE - new[1]) // 2))
    # 角丸の外側を再度透過
    tile.putalpha(mask)
    tile.save(dst, optimize=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
