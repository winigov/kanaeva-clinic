"""Готовит картинки для сайта из исходников проекта.

Запуск из папки site/:  python3 tools/prepare_images.py
Нужен Pillow. Исходники берутся из ../assets/images (папка проекта),
результат складывается в docs/assets/img.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

SITE = Path(__file__).resolve().parent.parent
SRC = SITE.parent / "assets" / "images"
REGEN = SRC / "clinic-regenerated"
OUT = SITE / "docs" / "assets" / "img"

GREEN = (0x21, 0x33, 0x25)

DOCTORS = {
    "kanaeva-fatima": "01-Фатима-Канаева",
    "abdurahmanova-aida": "02-Аида-Абдурахманова",
    "abdurahmanov-abdulkarim": "03-Абдулкарим-Абдурахманов",
    "emeeva-raziyat": "04-Разият-Эмеева",
    "ahmedhanova-zarina": "05-Зарина-Ахмедханова",
    "gusejnova-rezeda": "06-Резеда-Гусейнова",
}

INTERIOR = REGEN / "02-Интерьеры-и-кабинеты"
FACADE = REGEN / "05-Фасад-и-вход"
PHOTOS = {
    "consultation": REGEN / "03-Приём-и-работа-врачей" / "02-Консультация-в-кабинете.jpg",
    "work": REGEN / "03-Приём-и-работа-врачей" / "01-Врачи-за-работой.jpg",
    "team": REGEN / "04-Групповое-фото" / "01-Команда-клиники-по-центру.jpg",
    "library": INTERIOR / "Кабинеты" / "01-Кабинет-с-книжными-шкафами.jpg",
    "cabinet-blinds": INTERIOR / "Кабинеты" / "02-Кабинет-с-вертикальными-жалюзи.jpg",
    "workplace": INTERIOR / "Кабинеты" / "03-Рабочее-место-врача.jpg",
    "couch": INTERIOR / "Кабинеты" / "04-Кушетка-и-раковина.jpg",
    "desk": INTERIOR / "Кабинеты" / "06-Стол-и-монитор.jpg",
    "reception": INTERIOR / "Ресепшен" / "02-Стойка-ресепшена.jpg",
    "reception-door": INTERIOR / "Ресепшен" / "01-Вход-в-зону-ресепшена.jpg",
    "corridor-uzi": INTERIOR / "Коридоры-и-ожидание" / "01-Коридор-перед-кабинетом-УЗИ.jpg",
    "corridor-doors": INTERIOR / "Коридоры-и-ожидание" / "02-Коридор-с-серыми-дверями.jpg",
    "staircase": INTERIOR / "Коридоры-и-ожидание" / "03-Лестница-и-информация.jpg",
    "waiting": INTERIOR / "Коридоры-и-ожидание" / "04-Зона-ожидания-у-лестницы.jpg",
    "corridor-light": INTERIOR / "Коридоры-и-ожидание" / "05-Коридор-и-освещение.jpg",
    "entrance-side": FACADE / "04-Вход-боковой-ракурс.jpg",
    "entrance-steps": FACADE / "05-Вход-ступени-и-вывеска.jpg",
    "facade-green": FACADE / "02-Зелёный-фасад.jpg",
    "facade-street": FACADE / "03-Фасад-со-стороны-улицы.jpg",
    "entrance-trees": FACADE / "01-Вход-за-деревьями.jpg",
}


def save_webp(im, path, width, quality=80):
    height = round(im.height * width / im.width)
    im.resize((width, height), Image.LANCZOS).save(path, "WEBP", quality=quality, method=6)


def doctors():
    out = OUT / "doctors"
    out.mkdir(parents=True, exist_ok=True)
    for slug, name in DOCTORS.items():
        tall = Image.open(REGEN / "01-Врачи" / "Портреты-3x4" / f"{name}.jpg").convert("RGB")
        save_webp(tall, out / f"{slug}-lg.webp", 960)
        save_webp(tall, out / f"{slug}-sm.webp", 480)
        square = Image.open(REGEN / "01-Врачи" / "Квадратные-1x1" / f"{name}.jpg").convert("RGB")
        save_webp(square, out / f"{slug}-sq.webp", 160, quality=82)


def photos():
    out = OUT / "photos"
    out.mkdir(parents=True, exist_ok=True)
    for name, src in PHOTOS.items():
        im = Image.open(src).convert("RGB")
        vertical = im.height > im.width
        save_webp(im, out / f"{name}-lg.webp", 1000 if vertical else 1600)
        save_webp(im, out / f"{name}-sm.webp", 600 if vertical else 800)


def logo_alpha():
    """Маска логотипа: белые штрихи на зелёном фоне исходного JPG."""
    im = np.asarray(Image.open(SRC / "site" / "logo.jpg").convert("RGB")).astype(float)
    lum = im.mean(axis=2)
    bg = float(np.mean(GREEN))
    alpha = np.clip((lum - bg) / (255 - bg), 0, 1)
    alpha[alpha < 0.04] = 0
    return (alpha * 255).astype(np.uint8)


def tinted(alpha, color):
    rgba = np.zeros((*alpha.shape, 4), np.uint8)
    rgba[..., :3] = color
    rgba[..., 3] = alpha
    return Image.fromarray(rgba, "RGBA")


def brand():
    out = OUT / "brand"
    out.mkdir(parents=True, exist_ok=True)
    alpha = logo_alpha()
    ys, xs = np.where(alpha > 20)
    full = (xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5)
    cols = (alpha > 20).sum(axis=0)
    gap = next(x for x in range(420, 470) if cols[x] == 0)
    mono = (xs.min() - 4, ys.min() - 4, gap, ys.max() + 5)

    for name, color in (("logo-green", GREEN), ("logo-white", (255, 255, 255))):
        img = tinted(alpha, color).crop(full)
        img.resize((round(img.width * 160 / img.height), 160), Image.LANCZOS).save(out / f"{name}.png", optimize=True)

    mono_green = tinted(alpha, GREEN).crop(mono)
    mono_white = tinted(alpha, (255, 255, 255)).crop(mono)
    mono_green.resize((round(mono_green.width * 200 / mono_green.height), 200), Image.LANCZOS).save(out / "mono-green.png", optimize=True)

    # Иконки: белая монограмма на фирменном зелёном
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")):
        canvas = Image.new("RGBA", (size, size), GREEN + (255,))
        h = round(size * 0.72)
        m = mono_white.resize((round(mono_white.width * h / mono_white.height), h), Image.LANCZOS)
        canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
        canvas.save(out / name, optimize=True)

    # Превью для мессенджеров: логотип на зелёном + фото команды
    og = Image.new("RGB", (1200, 630), GREEN)
    team = Image.open(PHOTOS["team"]).convert("RGB")
    th = 630
    tw = round(team.width * th / team.height)
    team = team.resize((tw, th), Image.LANCZOS)
    left = (tw - 600) // 2
    og.paste(team.crop((left, 0, left + 600, th)), (600, 0))
    logo = tinted(alpha, (255, 255, 255)).crop(full)
    lw = 480
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    og.paste(logo, ((600 - lw) // 2, (630 - logo.height) // 2), logo)
    ImageDraw.Draw(og).rectangle((0, 600, 600, 630), fill=(0xF8, 0xC8, 0x57))
    og.save(out / "og.jpg", quality=86, optimize=True)


if __name__ == "__main__":
    doctors()
    photos()
    brand()
    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"Готово: {sum(1 for p in OUT.rglob('*') if p.is_file())} файлов, {total / 1024 / 1024:.1f} МБ")
