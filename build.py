"""Собирает статический сайт в папку docs/.

Запуск:  python3 build.py
Страницы генерируются из content.py; стили, скрипты, шрифты и картинки
лежат в docs/assets и не перезаписываются.
"""
import html
import json
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

from content import CLINIC, DEMO, DIR, DIRECTIONS, DOC, DOCTORS, FAQ_GENERAL, GALLERY, SITE_URL, TAGS

DOCS = Path(__file__).resolve().parent / "docs"
IMG = DOCS / "assets" / "img"
BASE_PATH = urlparse(SITE_URL).path  # /kanaeva-clinic/


def e(s):
    return html.escape(str(s), quote=True)


# ---------- Иконки (Lucide, ISC) ----------
ICONS = {
    "msg": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "up-right": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
    "parking": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>',
    "bus": '<path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01"/><path d="M15 9h.01"/>',
    "sprout": '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>',
    "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "stethoscope": '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
    "wind": '<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "hand": '<path d="M18 11V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v2"/><path d="M10 10.5V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
    "apple": '<path d="M12 20.94c1.5 0 2.75 1.06 4 1.06 3 0 6-8 6-12.22A4.91 4.91 0 0 0 17 5c-2.22 0-4 1.44-5 2-1-.56-2.78-2-5-2a4.9 4.9 0 0 0-5 4.78C2 14 5 22 8 22c1.25 0 2.5-1.06 4-1.06Z"/><path d="M10 2c1 .5 2 2 2 5"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
}


def icon(name, size=20, sw=1.75):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def tbd(text="уточняется"):
    return f'<span class="tbd" title="Данные нужно получить от клиники">{text}</span>'


def plural(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


# ---------- Картинки ----------
_sizes = {}


def img_size(rel):
    if rel not in _sizes:
        with Image.open(IMG / rel) as im:
            _sizes[rel] = im.size
    return _sizes[rel]


def photo(r, name, alt, sizes="(max-width: 760px) 100vw, 50vw", pos=None, eager=False, cls=""):
    lg, sm = f"photos/{name}-lg.webp", f"photos/{name}-sm.webp"
    w, h = img_size(lg)
    ws, _ = img_size(sm)
    style = f' style="object-position: {pos}"' if pos else ""
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{r}assets/img/{lg}" srcset="{r}assets/img/{sm} {ws}w, {r}assets/img/{lg} {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {loading} decoding="async"{style}>')


def doc_photo(r, d, size="sm", eager=False, sizes="(max-width: 760px) 80vw, 25vw"):
    if not d["photo"]:
        return f'<div class="initials" role="img" aria-label="{e(d["name"])}, фото будет добавлено">{d["initials"]}</div>'
    slug = d["slug"]
    lg, sm = f"doctors/{slug}-lg.webp", f"doctors/{slug}-sm.webp"
    w, h = img_size(lg if size == "lg" else sm)
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{r}assets/img/{lg if size == "lg" else sm}" srcset="{r}assets/img/{sm} 480w, {r}assets/img/{lg} 960w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{e(d["name"])}" {loading} decoding="async">')


def avatar(r, d):
    if d["photo"]:
        return f'<img src="{r}assets/img/doctors/{d["slug"]}-sq.webp" width="80" height="80" alt="" loading="lazy">'
    return ""


# ---------- Общие блоки ----------
NAV = [
    ("napravleniya/", "Направления", "dir"),
    ("vrachi/", "Врачи", "doc"),
    ("ceny/", "Цены", "price"),
    ("pacientam/", "Пациентам", "pat"),
    ("o-klinike/", "О клинике", "about"),
    ("kontakty/", "Контакты", "contacts"),
]


def book_btn(r, label="Записаться", cls="btn btn-primary", doctor="", direction="", title="", extra=""):
    attrs = ' data-book'
    if doctor:
        attrs += f' data-doctor="{doctor}"'
    if direction:
        attrs += f' data-direction="{direction}"'
    if title:
        attrs += f' data-book-title="{e(title)}"'
    return f'<a href="{r}kontakty/#zapis" class="{cls}"{attrs}>{extra}{label}</a>'


def wa_link(cls, label="Написать в WhatsApp", size=18):
    return f'<a href="{CLINIC["whatsapp"]}" target="_blank" rel="noopener" class="{cls}">{icon("msg", size)}{label}</a>'


def header(r, active):
    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{r}{href}"{current if key == active else ""}>{label}</a>' for href, label, key in NAV
    )
    mlinks = "".join(f'<a href="{r}{href}">{label}</a>' for href, label, _ in NAV)
    return f'''
<header class="header">
<div class="wrap">
<a class="logo" href="{r or './'}" aria-label="Центр Канаевой — на главную"><img src="{r}assets/img/brand/logo-green.png" width="349" height="160" alt="Kanaeva — центр аллергологии и интегративной медицины"></a>
<nav class="nav" aria-label="Основное меню">{links}</nav>
<div class="header-actions">
<a class="header-phone" href="{CLINIC["phone_href"]}"><b>{CLINIC["phone"]}</b><span>{CLINIC["hours_short"]}</span></a>
<a class="icon-btn" href="{CLINIC["whatsapp"]}" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">{icon("msg")}</a>
{book_btn(r, cls="btn btn-primary btn-sm")}
<a class="header-call" href="{CLINIC["phone_href"]}" aria-label="Позвонить">{icon("phone", 22)}</a>
<button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mobile-nav">{icon("menu", 26)}</button>
</div>
</div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="Меню">
{mlinks}
{book_btn(r, "Записаться на приём", "btn btn-primary btn-block")}
<div class="contacts">{CLINIC["address_short"]}<br>{CLINIC["hours_full"]}</div>
</nav>'''


def footer(r):
    dirs = "".join(f'<a href="{r}napravleniya/{d["slug"]}/">{short_dir(d)}</a>' for d in DIRECTIONS)
    L = CLINIC["legal"]
    return f'''
<footer class="wrap footer">
<div class="footer-grid">
<div class="footer-brand">
<img src="{r}assets/img/brand/logo-green.png" width="349" height="160" alt="Kanaeva" loading="lazy">
<p>{CLINIC["name"]}. Махачкала, с {CLINIC["since"]} года.</p>
</div>
<div class="footer-col"><b>Направления</b>{dirs}</div>
<div class="footer-col"><b>Пациентам</b>
<a href="{r}vrachi/">Врачи</a><a href="{r}ceny/">Цены</a><a href="{r}pacientam/">Первый визит и вопросы</a><a href="{r}o-klinike/">О клинике</a><a href="{r}kontakty/">Контакты</a>
</div>
<div class="footer-col"><b>Контакты</b>
<span>{CLINIC["address_short"]}</span>
<a class="ph" href="{CLINIC["phone_href"]}">{CLINIC["phone"]}</a>
<a href="{CLINIC["whatsapp"]}" target="_blank" rel="noopener">WhatsApp</a>
<span>{CLINIC["hours_full"]}</span>
</div>
</div>
<div class="footer-legal">
<span>{L["entity"]} · ОГРНИП {L["ogrnip"]} · ИНН {L["inn"]}<br>Лицензия {L["license"]}, выдана Росздравнадзором</span>
<nav aria-label="Документы"><a href="{r}svedeniya/">Сведения о медицинской организации</a><a href="{r}politika/">Политика обработки персональных данных</a></nav>
</div>
<div class="warning">Имеются противопоказания. Необходима консультация специалиста</div>
</footer>'''


def short_dir(d):
    return {"allergologiya": "Аллергология", "integrativnaya-medicina": "Интегративная медицина", "terapiya": "Терапевт"}.get(d["slug"], d["title"])


def mobile_bar(r):
    return f'''
<div class="mobile-bar">
<a class="icon-btn" href="{CLINIC["phone_href"]}" aria-label="Позвонить">{icon("phone", 22)}</a>
<a class="icon-btn" href="{CLINIC["whatsapp"]}" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">{icon("msg", 22)}</a>
{book_btn(r, "Записаться на приём", "btn btn-primary")}
</div>'''


def field_name():
    return '<label class="field">Имя<input type="text" name="name" autocomplete="name" placeholder="Как к вам обращаться" required><span class="error">Введите имя</span></label>'


def field_phone():
    return '<label class="field">Телефон<input type="tel" name="phone" autocomplete="tel" inputmode="tel" placeholder="+7 (___) ___-__-__" required><span class="error">Введите номер полностью</span></label>'


def select_direction(selected=""):
    opts = "".join(f'<option value="{d["slug"]}"{" selected" if d["slug"] == selected else ""}>{d["title"]}</option>' for d in DIRECTIONS)
    return f'<label class="field">Направление<select name="direction"><option value="">Не знаю — нужна помощь</option>{opts}</select></label>'


def select_doctor(selected=""):
    opts = "".join(f'<option value="{d["slug"]}"{" selected" if d["slug"] == selected else ""}>{d["short"]} — {d["role"].split(",")[0]}</option>' for d in DOCTORS)
    return f'<label class="field">Врач<select name="doctor"><option value="">Любой врач</option>{opts}</select></label>'


def time_chips():
    items = [("morning", "Утро · 9–12"), ("day", "День · 12–15"), ("evening", "Вечер · 15–18")]
    chips = "".join(
        f'<label><input type="radio" name="time" value="{v}"{" checked" if i == 0 else ""}><span>{t}</span></label>'
        for i, (v, t) in enumerate(items)
    )
    return f'<div class="field" role="radiogroup" aria-label="Удобное время"><span>Удобное время</span><div class="time-chips">{chips}</div></div>'


def consent(r):
    return (f'<label class="consent"><input type="checkbox" name="consent" required><span>Даю <a href="{r}politika/">согласие на обработку персональных данных</a> '
            f'и принимаю <a href="{r}politika/">политику конфиденциальности</a></span></label>')


def dialog(r):
    return f'''
<dialog class="modal" id="booking" aria-labelledby="booking-title">
<form class="form-card" data-booking>
<div class="modal-head"><div><b id="booking-title" data-title>Запись на приём</b><p>Перезвоним в рабочее время и подберём удобный день</p></div>
<button type="button" class="modal-close" data-close aria-label="Закрыть">{icon("x", 20)}</button></div>
<div class="form-body">
<div class="form-grid">{field_name()}{field_phone()}</div>
<div class="form-grid">{select_direction()}{select_doctor()}</div>
{time_chips()}
{consent(r)}
<button class="btn btn-primary btn-block" type="submit">Отправить заявку</button>
</div>
</form>
</dialog>'''


def inline_form(r, title, note, doctor=""):
    hidden = f'<input type="hidden" name="doctor" value="{doctor}">' if doctor else ""
    return f'''<form class="form-card" data-booking>{hidden}
<div class="form-body">
<div class="form-head"><b>{title}</b><span>{note}</span></div>
<div class="form-row">{field_name()}{field_phone()}<button class="btn btn-primary" type="submit">Записаться</button></div>
<p class="form-note">Нажимая «Записаться», вы соглашаетесь с <a href="{r}politika/">обработкой персональных данных</a></p>
</div>
</form>'''


def cta(r, title, text="Позвоните, напишите в WhatsApp или оставьте заявку — подберём удобное время.", doctor="", direction=""):
    return f'''
<section class="bg-green">
<div class="wrap cta">
<div class="t"><h2>{title}</h2><p>{text}</p></div>
<div class="r">
<a class="big-phone" href="{CLINIC["phone_href"]}">{CLINIC["phone"]}</a>
<div class="btn-row">{book_btn(r, "Записаться", "btn btn-accent", doctor=doctor, direction=direction)}{wa_link("btn btn-outline-light", "WhatsApp")}</div>
</div>
</div>
</section>'''


def crumbs(r, items):
    parts = [f'<a href="{r or "./"}">Главная</a>']
    for href, label in items[:-1]:
        parts.append(f'<span aria-hidden="true">/</span><a href="{r}{href}">{label}</a>')
    parts.append(f'<span aria-hidden="true">/</span><span aria-current="page">{items[-1][1]}</span>')
    return f'<nav class="crumbs" aria-label="Навигационная цепочка">{"".join(parts)}</nav>'


def section_head(title, text="", link=""):
    right = ""
    if text or link:
        right = f'<div class="stack">{f"<p>{text}</p>" if text else ""}{link}</div>'
    return f'<div class="section-head"><h2>{title}</h2>{right}</div>'


def doc_card(r, d):
    tags = " ".join(d["tags"])
    exp = f'<span class="chip">{e(d["exp"])}</span>' if d["exp"] else "<span></span>"
    return f'''<article class="doc-card" data-tags="{tags}">
<a class="ph" href="{r}vrachi/{d["slug"]}/" tabindex="-1" aria-hidden="true">{doc_photo(r, d)}</a>
<div class="body">
<a class="name" href="{r}vrachi/{d["slug"]}/">{d["name"]}</a>
<span class="role">{d["role"]}</span>
<div class="meta">{exp}{book_btn(r, "Записаться →", "", doctor=d["slug"], title=f"Запись к врачу: {d['short']}")}</div>
</div>
</article>'''


def filters(target, bg=""):
    btns = '<button type="button" data-value="all" aria-pressed="true">Все</button>' + "".join(
        f'<button type="button" data-value="{k}" aria-pressed="false">{v}</button>' for k, v in TAGS.items()
    )
    return f'<div class="filters" data-filter="{target}" role="group" aria-label="Фильтр по специальности">{btns}</div>'


def dir_card(r, d):
    return f'''<a class="dir-card" href="{r}napravleniya/{d["slug"]}/">
<div class="top"><span class="icon-circle">{icon(d["icon"], 26)}</span><span class="muted" aria-hidden="true">{icon("up-right", 22)}</span></div>
<b>{d["title"]}</b><span class="desc">{d["card"]}</span>
</a>'''


def diag_card(r):
    return f'''<a class="dir-card dir-card--accent" href="{r}napravleniya/allergologiya/#diagnostika">
<span class="chip chip-dark" style="align-self:flex-start">Первыми в Дагестане</span>
<b>Ускоренная диагностика аллергии</b>
<span class="desc">IgE-зависимые реакции — быстрее стандартных методик</span>
<span class="more">Подробнее {icon("arrow", 18, 2)}</span>
</a>'''


# ---------- Каркас страницы ----------
def page(path, title, description, body, active="", home=False, r=None):
    depth = path.count("/")
    if r is None:
        r = "../" * depth
    full_title = f"{title} — {CLINIC['short']}" if not home else f"{CLINIC['name']} — Махачкала"
    robots = '<meta name="robots" content="noindex, nofollow">' if DEMO else ""
    demo = ('<div class="demo-bar"><b>Демо-версия</b> нового сайта центра. Цены и часть данных уточняются, '
            'заявки с форм никуда не отправляются.</div>') if DEMO else ""
    ld = ""
    if home:
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org",
            "@type": "MedicalClinic",
            "name": CLINIC["name"],
            "url": SITE_URL,
            "telephone": "+79288062417",
            "image": SITE_URL + "assets/img/brand/og.jpg",
            "address": {"@type": "PostalAddress", "streetAddress": "ул. Нурадилова, 58", "addressLocality": "Махачкала",
                        "addressRegion": "Республика Дагестан", "postalCode": CLINIC["zip"], "addressCountry": "RU"},
            "geo": {"@type": "GeoCoordinates", "latitude": CLINIC["lat"], "longitude": CLINIC["lon"]},
            "openingHours": "Mo-Fr 09:00-18:00",
            "foundingDate": str(CLINIC["since"]),
        }, ensure_ascii=False) + "</script>"
    out = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
{robots}
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="{e(CLINIC['short'])}">
<meta property="og:title" content="{e(title if not home else CLINIC['name'])}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:image" content="{SITE_URL}assets/img/brand/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#213325">
<link rel="icon" type="image/png" sizes="32x32" href="{r}assets/img/brand/favicon-32.png">
<link rel="apple-touch-icon" href="{r}assets/img/brand/apple-touch-icon.png">
<link rel="preload" href="{r}assets/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/fonts/onest.css">
<link rel="stylesheet" href="{r}assets/css/site.css">
{ld}
</head>
<body>
<a class="sr-only" href="#main">Перейти к содержимому</a>
{demo}
{header(r, active)}
<main id="main">
{body}
</main>
{footer(r)}
{mobile_bar(r)}
{dialog(r)}
<script src="{r}assets/js/site.js" defer></script>
</body>
</html>
'''
    target = DOCS / path / "index.html" if not path.endswith(".html") else DOCS / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


# ---------- Главная ----------
def home():
    r = ""
    fatima = DOC["kanaeva-fatima"]
    avatars = "".join(avatar(r, DOC[s]) for s in ("abdurahmanov-abdulkarim", "abdurahmanova-aida", "gusejnova-rezeda"))
    doc_cards = "".join(doc_card(r, d) for d in DOCTORS)
    steps = "".join(
        f'<div class="step"><span class="num">{i}</span><div><b>{t}</b><span>{s}</span></div></div>'
        for i, (t, s) in enumerate([
            ("Запишитесь", "По телефону, в WhatsApp или через форму на сайте. Перезвоним и подберём удобное время."),
            ("Возьмите с собой", "Паспорт, результаты анализов и обследований, выписки и список лекарств, которые принимаете."),
            ("На приёме", "Врач подробно расспросит об истории болезни, осмотрит и составит план обследования и лечения."),
        ], 1)
    )
    body = f'''
<section class="bg-warm">
<div class="wrap hero">
<div class="hero-text">
<span class="pill"><span class="dot"></span>Центр аллергологии и интегративной медицины · с {CLINIC["since"]} года</span>
<h1>Лечим не симптомы, а&nbsp;причину</h1>
<p class="lead">Центр доктора Канаевой в Махачкале: аллергология и иммунология, УЗИ, эндокринология, кардиология и интегративная медицина — для взрослых и детей.</p>
{inline_form(r, "Запись на приём", "Перезвоним и подберём удобное время")}
{wa_link("link-arrow", "Или напишите нам в WhatsApp →", 20)}
</div>
<div class="hero-media">
<div class="hero-photo">{doc_photo(r, fatima, "lg", eager=True, sizes="(max-width: 960px) 100vw, 440px")}</div>
<div class="badge-round"><small>с</small><b>{CLINIC["since"]}</b><small>года</small></div>
<div class="float-card"><b>{fatima["name"]}</b><span>Главный врач · 45 лет стажа</span></div>
<a class="team-pill" href="vrachi/"><span class="avatars">{avatars}</span>{len(DOCTORS)} врачей в команде</a>
</div>
</div>
</section>

<section class="section bg-white">
<div class="wrap">
{section_head("Направления", "Аллергология — наша основная специализация. Рядом — диагностика и врачи смежных специальностей, чтобы обследоваться в одном месте.", f'<a class="link-arrow" href="napravleniya/">Все направления и цены {icon("arrow", 18, 2)}</a>')}
<div class="dir-grid">{"".join(dir_card(r, d) for d in DIRECTIONS)}{diag_card(r)}</div>
</div>
</section>

<section class="section section--tight-top bg-white">
<div class="wrap about">
<div><div class="about-photo">{photo(r, "team", "Команда центра: Абдурахманов А. Г., Канаева Ф. А., Абдурахманова А. М., Эмеева Р. М.", "(max-width: 960px) 100vw, 60vw")}</div>
<p class="figcap">Слева направо: Абдурахманов А. Г., Канаева Ф. А., Абдурахманова А. М., Эмеева Р. М.</p></div>
<div class="about-text">
<span class="chip" style="background:var(--yellow);align-self:flex-start">С {CLINIC["since"]} года</span>
<h2>«Свой» медицинский центр в&nbsp;Махачкале</h2>
<p class="lead">Сюда приходят за точной диагностикой и внимательным отношением. В команде — опытные врачи, которым доверяют годами.</p>
<div class="stats"><div><b>45 лет</b><span>стаж главного врача</span></div><div><b>{len(DOCTORS)}</b><span>врачей в команде</span></div><div><b>{CLINIC["patients"]}</b><span>пациентов</span></div></div>
<a class="link-arrow" href="o-klinike/">Подробнее о центре {icon("arrow", 18, 2)}</a>
</div>
</div>
</section>

<section class="section bg-warm">
<div class="wrap">
<div class="section-head">
<div class="stack" style="gap:24px"><h2>Врачи центра</h2>{filters("home-docs")}</div>
<div class="arrows"><button type="button" data-scroll="prev" data-target="home-docs" aria-label="Предыдущие врачи">{icon("arrow-left", 20, 2)}</button><button type="button" data-scroll="next" data-target="home-docs" aria-label="Следующие врачи">{icon("arrow", 20, 2)}</button></div>
</div>
<div class="doc-scroller" id="home-docs">{doc_cards}</div>
</div>
</section>

<section class="section bg-white">
<div class="wrap">
{section_head("Центр изнутри", "Светлые кабинеты, отдельный кабинет УЗИ и зона ожидания с детским уголком — всё в одном здании на ул. Нурадилова, 58.", f'<a class="link-arrow" href="o-klinike/">Больше фото {icon("arrow", 18, 2)}</a>')}
<div class="bento">
<figure class="b1">{photo(r, "consultation", "Приём в кабинете", "(max-width: 960px) 100vw, 50vw", "35% center")}<figcaption class="cap">Приём в кабинете</figcaption></figure>
<figure class="b2">{photo(r, "corridor-uzi", "Коридор у кабинета УЗИ", "(max-width: 960px) 50vw, 25vw")}<figcaption class="cap">Кабинет УЗИ</figcaption></figure>
<figure class="b3">{photo(r, "reception", "Стойка ресепшена", "(max-width: 960px) 50vw, 25vw")}<figcaption class="cap">Ресепшен</figcaption></figure>
<figure class="b4">{photo(r, "waiting", "Зона ожидания у лестницы с детским уголком", "(max-width: 960px) 100vw, 50vw", "center 60%")}<figcaption class="cap">Зона ожидания с детским уголком</figcaption></figure>
</div>
</div>
</section>

<section class="section bg-warm">
<div class="wrap two-col">
<div class="col-intro"><h2>Первый визит</h2><p>Коротко о том, как записаться и что взять с собой, чтобы приём прошёл с пользой.</p>
<a class="link-arrow" href="pacientam/">Подготовка и частые вопросы {icon("arrow", 18, 2)}</a></div>
<div class="steps">{steps}</div>
</div>
</section>

{contacts_band(r)}
'''
    page("", CLINIC["name"], "Центр аллергологии и интегративной медицины доктора Канаевой в Махачкале: аллергология, УЗИ, эндокринология, кардиология. Работаем с 1999 года.", body, home=True)


def contacts_band(r):
    return f'''
<section class="section bg-green">
<div class="wrap contacts-band">
<div class="info">
<h2>Контакты</h2>
<a class="big-phone" href="{CLINIC["phone_href"]}">{CLINIC["phone"]}</a>
<div class="info-rows">
<div>{icon("pin", 22)}<span>{CLINIC["address"]}</span></div>
<div>{icon("clock", 22)}<span>Пн–Пт 9:00–18:00 · Сб–Вс — выходные</span></div>
</div>
<div class="btn-row">{book_btn(r, "Записаться онлайн", "btn btn-accent")}{wa_link("btn btn-outline-light")}</div>
</div>
<figure class="entrance">{photo(r, "entrance-side", "Вход в центр: лестница и зелёный фасад", "(max-width: 960px) 100vw, 50vw")}
<figcaption><span><b>Зелёное здание с белыми наличниками</b><span>Вход — по широкой лестнице</span></span>
<a class="btn btn-primary btn-sm" href="{r}kontakty/">{icon("pin", 18)}Как добраться</a></figcaption></figure>
</div>
</section>'''


# ---------- Врачи ----------
def doctors_index():
    r = "../"
    cards = "".join(doc_card(r, d) for d in DOCTORS)
    body = f'''
<section class="bg-warm">
<div class="wrap">
{crumbs(r, [("vrachi/", "Врачи")])}
<div style="padding:32px 0 40px;display:flex;flex-direction:column;gap:20px">
<h1>Врачи центра</h1>
<p class="lead">{len(DOCTORS)} врачей: аллергология, гомеопатия, УЗИ-диагностика, эндокринология, кардиология и терапия. Сложные случаи ведём вместе.</p>
{filters("all-docs")}
</div>
<div class="doc-grid" id="all-docs" style="padding-bottom:100px">{cards}</div>
</div>
</section>
{cta(r, "Не знаете, к какому врачу записаться?", "Позвоните или напишите в WhatsApp — администратор подскажет, какой специалист нужен.")}
'''
    page("vrachi/", "Врачи", "Врачи центра доктора Канаевой в Махачкале: аллерголог, гомеопаты, УЗИ-диагностика, эндокринолог, кардиолог.", body, "doc")


def doctor_page(d):
    r = "../../"
    idx = DOCTORS.index(d)
    others = [DOCTORS[(idx + k) % len(DOCTORS)] for k in (1, 2, 3)]
    facts = "".join(f'<div><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in d["facts"])
    facts += f'<div><b>{tbd()}</b><span>стоимость приёма</span></div>'
    tags = "".join(f'<span class="tag">{t}</span>' for t in d["areas"])
    sections = []
    if d["conditions"]:
        conds = "".join(
            f'<div class="cond"><span class="ck">{icon("check", 18, 2)}</span><div><b>{t}</b>{f"<span>{s}</span>" if s else ""}</div></div>'
            for t, s in d["conditions"]
        )
        sections.append(f'<div class="wrap">{section_head(d["cond_title"], d["cond_intro"])}<div class="cond-grid">{conds}</div></div>')
    if d["about"]:
        ph_name, ph_cap = d["about_photo"]
        paras = "".join(f"<p>{p}</p>" for p in d["about"])
        note = f'<div class="note-card">{d["note"]}</div>' if d["note"] else ""
        sections.append(f'''<div class="wrap split">
<figure style="margin:0"><div class="ph">{photo(r, ph_name, ph_cap, "(max-width: 960px) 100vw, 50vw", "55% center")}</div><figcaption class="figcap">{ph_cap}</figcaption></figure>
<div class="text"><h2>{d["about_title"]}</h2>{paras}{note}</div>
</div>''')
    edu = "".join(f'<div class="row"><b>{t}</b><span class="chip">{p}</span></div>' for t, p in d["education"])
    comm = ""
    if d["communities"]:
        comm = '<h3>Профессиональные сообщества</h3>' + "".join(
            f'<div class="community"><span class="ic">{icon("award", 20)}</span>{c}</div>' for c in d["communities"]
        )
    docs_ph = "".join(f'<div>{icon("file", 24, 1.5)}{t}</div>' for t in ("диплом", "сертификат", "сертификат", "аккредитация"))
    extra_note = f'<div class="note-card">{d["note"]}</div>' if d["note"] and not d["about"] else ""
    sections.append(f'''<div class="wrap two-col--even two-col">
<div class="rows"><h3 style="margin-bottom:16px">{d["edu_title"]}</h3>{edu}</div>
<div class="stack">{comm}{extra_note}
<h3 style="margin-top:{'28px' if comm or extra_note else '0'}">Дипломы и сертификаты</h3>
<p class="muted" style="font-size:15px">Сканы документов появятся после согласования с клиникой.</p>
<div class="docs-ph">{docs_ph}</div>
</div>
</div>''')
    bgs = ["bg-white", "bg-warm"]
    body_sections = "".join(f'<section class="section {bgs[i % 2]}">{s}</section>' for i, s in enumerate(sections))
    last_bg = bgs[len(sections) % 2]
    minis = "".join(f'''<a class="mini-doc" href="{r}vrachi/{o["slug"]}/"><span class="ph">{doc_photo(r, o) if o["photo"] else f'<span class="initials initials--sm">{o["initials"]}</span>'}</span>
<span class="t"><b>{o["name"]}</b><span>{o["role"]}</span>{f'<span class="chip">{o["exp"]}</span>' if o["exp"] else ""}</span></a>''' for o in others)
    badge = f'<span class="cap">{d["badge"]}</span>' if d["badge"] else ""
    body = f'''
<section class="bg-warm">
<div class="wrap">
{crumbs(r, [("vrachi/", "Врачи"), ("", d["name"])])}
<div class="doc-hero">
<div class="ph">{doc_photo(r, d, "lg", eager=True, sizes="(max-width: 960px) 100vw, 460px")}{badge}</div>
<div class="text">
<div class="tag-list">{tags}</div>
<div><h1 style="font-size:clamp(36px,4.4vw,60px)">{d["name"]}</h1><p class="role">{d["role"]}</p></div>
<p class="intro">{d["lead"]}</p>
<div class="facts">{facts}</div>
{inline_form(r, f"Запись к {d['call']}", "Перезвоним и подберём время", d["slug"])}
<div class="btn-row">{wa_link("link-arrow", "Написать в WhatsApp", 18)}<a class="link-arrow" href="{CLINIC["phone_href"]}">{icon("phone", 18)}{CLINIC["phone"]}</a></div>
</div>
</div>
</div>
</section>
{body_sections}
<section class="section {last_bg}">
<div class="wrap">
{section_head("Другие врачи центра", "", f'<a class="link-arrow" href="{r}vrachi/">Все {len(DOCTORS)} врачей {icon("arrow", 18, 2)}</a>')}
<div class="mini-docs">{minis}</div>
</div>
</section>
{cta(r, f"Запишитесь на приём к {d['call']}", doctor=d["slug"])}
'''
    page(f'vrachi/{d["slug"]}/', d["name"], f'{d["name"]} — {d["role"].lower()}. {d["lead"]}', body, "doc")


# ---------- Направления ----------
def directions_index():
    r = "../"
    body = f'''
<section class="bg-warm">
<div class="wrap">
{crumbs(r, [("napravleniya/", "Направления")])}
<div style="padding:32px 0 40px;display:flex;flex-direction:column;gap:20px">
<h1>Направления</h1>
<p class="lead">Аллергология — основная специализация центра. Рядом — УЗИ-диагностика и врачи смежных специальностей: всё в одном здании.</p>
</div>
<div class="dir-grid" style="padding-bottom:100px">{"".join(dir_card(r, d) for d in DIRECTIONS)}{diag_card(r)}</div>
</div>
</section>
{cta(r, "Поможем выбрать врача", "Опишите, что беспокоит, — администратор подскажет, к какому специалисту записаться.")}
'''
    page("napravleniya/", "Направления", "Направления центра доктора Канаевой: аллергология и иммунология, детям, интегративная медицина, УЗИ, эндокринология, кардиология, терапия.", body, "dir")


def direction_page(d):
    r = "../../"
    docs = [DOC[s] for s in d["doctors"]]
    n = len(docs)
    avatars = "".join(avatar(r, x) for x in docs if x["photo"])
    groups = "".join(
        f'<div class="complaint"><span class="icon-circle">{icon(ic, 24)}</span><b>{t}</b><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>'
        for ic, t, items in d["groups"]
    )
    gcls = {1: "complaints--1", 2: "complaints--2", 3: "complaints--3"}.get(len(d["groups"]), "")
    steps = "".join(
        f'<div class="step-card"><span class="num num--md">{i}</span><b>{t}</b><span>{s}</span></div>'
        for i, (t, s) in enumerate(d["steps"], 1)
    )
    scls = "" if len(d["steps"]) == 4 else "step-cards--3"
    cards = "".join(doc_card(r, x) for x in docs)
    prices = "".join(f'<div class="price-row"><span>{p}</span><span class="v">{tbd()}</span></div>' for p in d["prices"])
    faq_items = d["faq"] or FAQ_GENERAL[:4]
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}<span class="pm">{icon("plus", 20, 2)}</span></summary><p>{a or "Уточните у администратора по телефону " + CLINIC["phone"] + " или в WhatsApp."}</p></details>'
        for i, (q, a) in enumerate(faq_items)
    )
    diag = ""
    if d.get("diagnostics"):
        ab = DOC["abdurahmanov-abdulkarim"]
        diag = f'''
<section class="section bg-white" id="diagnostika" style="padding-bottom:0">
<div class="wrap">
<div class="diag">
<div class="text">
<span class="chip chip-dark" style="align-self:flex-start">Первыми в Дагестане</span>
<h2>Ускоренная диагностика аллергии</h2>
<p>Выявляем IgE-зависимые аллергические реакции быстрее, чем при стандартных методиках: точный результат и лечение пациент получает раньше.</p>
<div class="diag-facts"><div><small>Результат</small><b>{tbd()}</b></div><div><small>Стоимость</small><b>{tbd()}</b></div><div><small>Проводит</small><b>{ab["short"]}</b></div></div>
{book_btn(r, "Записаться на диагностику", "btn btn-primary", doctor=ab["slug"], direction=d["slug"], title="Запись на ускоренную диагностику аллергии")}
</div>
<div class="ph">{doc_photo(r, ab, "sm", sizes="(max-width: 960px) 80vw, 340px")}</div>
</div>
</div>
</section>'''
    body = f'''
<section class="bg-warm">
<div class="wrap">
{crumbs(r, [("napravleniya/", "Направления"), ("", d["title"])])}
<div class="dir-hero">
<div class="text">
<span class="pill"><span class="dot"></span>{d["pill"]}</span>
<h1>{d["title"]}</h1>
<p class="lead">{d["lead"]}</p>
<div class="btn-row">{book_btn(r, "Записаться на приём", "btn btn-primary", direction=d["slug"], title=f"Запись: {d['title']}")}{wa_link("btn btn-outline")}</div>
<div class="quick">
<div><small>Первичный приём</small><b>{tbd()}</b></div>
<div><small>Длительность</small><b>{tbd()}</b></div>
<div><small>Ведут приём</small><b style="display:flex;align-items:center;gap:10px"><span class="avatars">{avatars}</span>{n} {plural(n, "врач", "врача", "врачей")}</b></div>
</div>
</div>
<div class="ph">{photo(r, d["photo"], d["title"], "(max-width: 960px) 100vw, 540px", d["photo_pos"], eager=True)}</div>
</div>
</div>
</section>
{diag}
<section class="section bg-white">
<div class="wrap">
{section_head(d["groups_title"], d["groups_intro"])}
<div class="complaints {gcls}">{groups}</div>
</div>
</section>

<section class="section bg-warm">
<div class="wrap">
<div class="section-head"><h2>Как проходит приём</h2></div>
<div class="step-cards {scls}">{steps}</div>
</div>
</section>

<section class="section bg-white">
<div class="wrap">
{section_head("Врачи направления", "", f'<a class="link-arrow" href="{r}vrachi/">Все врачи центра {icon("arrow", 18, 2)}</a>')}
<div class="doc-grid doc-grid--3">{cards}</div>
</div>
</section>

<section class="section bg-warm">
<div class="wrap two-col two-col--even">
<div class="stack" style="gap:24px"><h2 style="font-size:clamp(28px,3vw,40px)">Цены</h2>
<div class="price-card">{prices}</div>
<div class="price-foot"><span class="small">Цены уточняются. Не является публичной офертой.</span><a class="link-arrow" href="{r}ceny/">Все цены {icon("arrow", 18, 2)}</a></div>
</div>
<div class="stack"><h2 style="font-size:clamp(28px,3vw,40px);margin-bottom:12px">Частые вопросы</h2>
<div class="faq">{faq}</div>
</div>
</div>
</section>
{cta(r, "Запишитесь на приём", "Позвоните, напишите в WhatsApp или оставьте заявку — подберём врача и удобное время.", direction=d["slug"])}
'''
    page(f'napravleniya/{d["slug"]}/', d["title"], f'{d["title"]} в центре доктора Канаевой, Махачкала. {d["lead"]}', body, "dir")


# ---------- Контакты ----------
def contacts():
    r = "../"
    L = CLINIC["legal"]
    hours = "".join(
        f'<div class="hours-row"><span>{dname}</span>{f"<b>{h}</b>" if ":" in h else f"<em>{h}</em>"}</div>' for dname, h in CLINIC["hours"]
    )
    howto = "".join(
        f'<div><div class="ph">{photo(r, ph, alt, "(max-width: 960px) 100vw, 33vw", pos)}</div><div class="t"><span class="num num--sm">{i}</span><span><b>{t}</b><span>{s}</span></span></div></div>'
        for i, (ph, alt, pos, t, s) in enumerate([
            ("facade-street", "Зелёный фасад здания со стороны улицы", "center 40%", "Ищите зелёное здание", "Ярко-зелёный фасад с белыми наличниками на ул. Нурадилова, 58."),
            ("entrance-steps", "Вход в центр: широкая лестница и зелёная дверь", None, "Поднимитесь по лестнице", "Вход — по широкой лестнице с узорными перилами, через зелёную двустворчатую дверь."),
            ("reception", "Стойка ресепшена", None, "Подойдите к ресепшену", "Администратор подскажет, где кабинет врача."),
        ], 1)
    )
    orgs = "".join(
        f'<div class="org-card"><b>{o}</b><span>Адрес и телефон: {tbd()}</span></div>'
        for o in ("Министерство здравоохранения Республики Дагестан",
                  "Территориальный орган Росздравнадзора по Республике Дагестан",
                  "Управление Роспотребнадзора по Республике Дагестан")
    )
    req = "".join(
        f'<div class="req-row"><span>{k}</span><span>{v}</span></div>'
        for k, v in [("Исполнитель", L["entity"]), ("ОГРНИП", L["ogrnip"]), ("ИНН", L["inn"]), ("Лицензия", L["license"]),
                     ("Кем выдана", L["license_body"]), ("Адрес деятельности", L["license_address"])]
    )
    lat, lon = CLINIC["lat"], CLINIC["lon"]
    body = f'''
<section class="bg-warm">
<div class="wrap" style="padding-bottom:64px">
{crumbs(r, [("kontakty/", "Контакты")])}
<h1 style="margin-top:32px">Контакты</h1>
<p class="lead" style="margin-top:16px">{CLINIC["name"]} — в Махачкале, на ул. Нурадилова, 58.</p>
<div class="info-cards">
<div class="info-card"><span class="icon-circle">{icon("pin", 22)}</span><small>Адрес</small><span class="v">{CLINIC["address"]}</span><span class="small">Индекс {CLINIC["zip"]}</span>
<a class="link-arrow bottom" href="{CLINIC["yandex_route"]}" target="_blank" rel="noopener">Построить маршрут {icon("arrow", 18, 2)}</a></div>
<div class="info-card"><span class="icon-circle">{icon("phone", 22)}</span><small>Телефон и WhatsApp</small><a class="v-phone" href="{CLINIC["phone_href"]}">{CLINIC["phone"]}</a><span class="small">Звонки и сообщения — в часы работы центра</span>
<div class="btn-row bottom"><a class="btn btn-primary btn-sm" href="{CLINIC["phone_href"]}">Позвонить</a>{wa_link("btn btn-outline btn-sm", "WhatsApp", 16)}</div></div>
<div class="info-card"><span class="icon-circle">{icon("clock", 22)}</span><small>Часы работы</small><div>{hours}</div></div>
</div>
</div>
</section>

<section class="section bg-white" style="padding-top:80px;padding-bottom:0">
<div class="wrap">
<div class="map">
<iframe src="https://yandex.ru/map-widget/v1/?ll={lon}%2C{lat}&amp;z=16&amp;pt={lon}%2C{lat}%2Cpm2dgl" title="Центр Канаевой на Яндекс Картах" loading="lazy" allowfullscreen></iframe>
<div class="map-card">
<img src="{r}assets/img/brand/logo-green.png" width="349" height="160" alt="Kanaeva">
<b>ул. Нурадилова, 58</b><span class="small">{CLINIC["hours_short"]}</span>
<div class="btn-row"><a class="btn btn-primary btn-sm" href="{CLINIC["yandex"]}" target="_blank" rel="noopener">Яндекс Карты</a><a class="btn btn-outline btn-sm" href="{CLINIC["gis"]}" target="_blank" rel="noopener">2ГИС</a></div>
</div>
</div>
</div>
</section>

<section class="section bg-white">
<div class="wrap">
{section_head("Как найти вход", "Центр — в ярко-зелёном здании с белыми наличниками, его хорошо видно с улицы.")}
<div class="howto">{howto}</div>
<div class="soft-chips"><span>{icon("parking", 16)}Парковка: {tbd()}</span><span>{icon("bus", 16)}Ближайшая остановка: {tbd()}</span></div>
</div>
</section>

<section class="section bg-warm" id="zapis">
<div class="wrap booking">
<div class="stack" style="gap:20px">
<h2>Запись и вопросы</h2>
<p class="lead">Оставьте заявку — администратор перезвонит в рабочее время, подберёт врача и удобный день.</p>
<a class="contact-link" href="{CLINIC["whatsapp"]}" target="_blank" rel="noopener"><span class="icon-circle">{icon("msg", 20)}</span><span><b>Написать в WhatsApp</b><span>Удобно, если не получается дозвониться</span></span></a>
<a class="contact-link" href="{CLINIC["phone_href"]}"><span class="icon-circle">{icon("phone", 20)}</span><span><b>{CLINIC["phone"]}</b><span>{CLINIC["hours_short"]}</span></span></a>
<figure class="photo-card" style="height:280px;margin-top:12px">{photo(r, "waiting", "Зона ожидания у лестницы с детским уголком", "(max-width: 960px) 100vw, 40vw", "center 60%")}<figcaption class="cap">Зона ожидания с детским уголком</figcaption></figure>
</div>
<form class="form-card form-card--lg" data-booking>
<div class="form-body">
<h3>Заявка на приём</h3>
<div class="form-grid">{field_name()}{field_phone()}</div>
<div class="form-grid">{select_direction()}{select_doctor()}</div>
{time_chips()}
<label class="field">Комментарий<textarea name="comment" placeholder="Коротко опишите, что беспокоит (необязательно)"></textarea></label>
{consent(r)}
<button class="btn btn-primary btn-block" type="submit">Отправить заявку</button>
</div>
</form>
</div>
</section>

<section class="section bg-white">
<div class="wrap two-col two-col--even">
<div class="rows"><h3 style="margin-bottom:16px">Реквизиты и лицензия</h3>{req}
<div class="doc-links"><a href="{L["registry"]}" target="_blank" rel="noopener">{icon("file", 16)}Реестр лицензий Росздравнадзора</a><a href="{r}svedeniya/">Сведения о медицинской организации</a><a href="{r}politika/">Политика обработки персональных данных</a></div></div>
<div class="stack"><h3>Контролирующие органы</h3>{orgs}</div>
</div>
</section>
'''
    page("kontakty/", "Контакты", f"Адрес, телефон и часы работы центра доктора Канаевой: {CLINIC['address']}, {CLINIC['phone']}.", body, "contacts")


# ---------- О клинике ----------
def about():
    r = "../"
    gal = "".join(
        f'<figure class="{"wide" if i == 0 else ""}">{photo(r, n, c, "(max-width: 960px) 50vw, 25vw")}<figcaption class="cap">{c}</figcaption></figure>'
        for i, (n, c) in enumerate(GALLERY)
    )
    approach = "".join(
        f'<div class="step-card"><span class="num num--md">{i}</span><b>{t}</b><span>{s}</span></div>'
        for i, (t, s) in enumerate([
            ("Подробный приём", "Разбираем историю болезни, образ жизни и то, что предшествовало появлению симптомов."),
            ("Точная диагностика", "Аллергодиагностика и УЗИ в одном центре — без поездок по разным клиникам."),
            ("Индивидуальный план", "Сочетаем классическую медицину и интегративные методы с учётом особенностей пациента."),
            ("Сопровождение", "Наблюдаем в динамике и корректируем лечение на повторных приёмах."),
        ], 1)
    )
    body = f'''
<section class="bg-warm">
<div class="wrap" style="padding-bottom:64px">
{crumbs(r, [("o-klinike/", "О клинике")])}
<h1 style="margin-top:32px">О центре</h1>
<p class="lead" style="margin-top:16px">Работаем с {CLINIC["since"]} года и остаёмся тем самым «своим» медицинским центром, куда приходят за точной диагностикой и внимательным отношением.</p>
</div>
</section>

<section class="section bg-white">
<div class="wrap about">
<div><div class="about-photo">{photo(r, "team", "Команда центра", "(max-width: 960px) 100vw, 60vw", eager=True)}</div>
<p class="figcap">Слева направо: Абдурахманов А. Г., Канаева Ф. А., Абдурахманова А. М., Эмеева Р. М.</p></div>
<div class="about-text">
<p class="lead" style="color:var(--text)">Ежедневно принимаем пациентов, проводим современные исследования и помогаем разобраться в любых вопросах о здоровье.</p>
<p class="lead">В команде — опытные врачи, которым доверяют годами. Мы за честную, понятную и качественную медицину, где комфорт пациента всегда на первом месте.</p>
<div class="stats"><div><b>{CLINIC["since"]}</b><span>год основания</span></div><div><b>{len(DOCTORS)}</b><span>врачей в команде</span></div><div><b>{CLINIC["patients"]}</b><span>пациентов</span></div></div>
<a class="link-arrow" href="{r}vrachi/">Познакомиться с врачами {icon("arrow", 18, 2)}</a>
</div>
</div>
</section>

<section class="section bg-warm">
<div class="wrap">
<div class="section-head"><h2>Как мы работаем</h2><p>Лечение начинается с понимания причины: внимательно разбираем историю болезни и строим план под конкретного человека.</p></div>
<div class="step-cards">{approach}</div>
</div>
</section>

<section class="section bg-white">
<div class="wrap">
{section_head("Центр изнутри", "Зелёное здание на ул. Нурадилова, 58: кабинеты врачей, кабинет УЗИ, ресепшен и зона ожидания с детским уголком.")}
<div class="gallery">{gal}</div>
</div>
</section>
{cta(r, "Приходите на приём", "Позвоните, напишите в WhatsApp или оставьте заявку — подберём врача и удобное время.")}
'''
    page("o-klinike/", "О клинике", "Центр доктора Канаевой в Махачкале работает с 1999 года: команда, подход к лечению, фото центра.", body, "about")


# ---------- Пациентам ----------
def patients():
    r = "../"
    steps = "".join(
        f'<div class="step"><span class="num">{i}</span><div><b>{t}</b><span>{s}</span></div></div>'
        for i, (t, s) in enumerate([
            ("Запишитесь", "По телефону, в WhatsApp или через форму на сайте. Администратор перезвонит в рабочее время и подберёт удобный день."),
            ("Подготовьтесь", "Соберите документы и результаты обследований. Если идёте на УЗИ или аллергодиагностику — уточните у администратора, нужна ли подготовка."),
            ("Приходите на приём", "Центр — в зелёном здании на ул. Нурадилова, 58, вход по широкой лестнице. На ресепшене подскажут, куда пройти."),
        ], 1)
    )
    bring = "".join(
        f'<div class="cond"><span class="ck">{icon("check", 18, 2)}</span><div><b>{t}</b><span>{s}</span></div></div>'
        for t, s in [("Паспорт", "и полис, если есть"), ("Результаты анализов", "и обследований за последнее время"),
                     ("Выписки", "из больниц и заключения других врачей"), ("Список лекарств", "которые вы принимаете сейчас")]
    )
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}<span class="pm">{icon("plus", 20, 2)}</span></summary><p>{a or "Уточните у администратора по телефону " + CLINIC["phone"] + " или в WhatsApp."}</p></details>'
        for i, (q, a) in enumerate(FAQ_GENERAL)
    )
    body = f'''
<section class="bg-warm">
<div class="wrap" style="padding-bottom:64px">
{crumbs(r, [("pacientam/", "Пациентам")])}
<h1 style="margin-top:32px">Пациентам</h1>
<p class="lead" style="margin-top:16px">Как записаться, что взять с собой и ответы на частые вопросы.</p>
</div>
</section>

<section class="section bg-white">
<div class="wrap two-col">
<div class="col-intro"><h2>Первый визит</h2><p>Три шага, чтобы приём прошёл спокойно и с пользой.</p>{book_btn(r, "Записаться на приём", "btn btn-primary")}</div>
<div class="steps">{steps}</div>
</div>
</section>

<section class="section bg-warm">
<div class="wrap">
{section_head("Что взять с собой", "Всё, что поможет врачу быстрее разобраться в ситуации.")}
<div class="cond-grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{bring}</div>
<div class="note-card" style="margin-top:24px;background:var(--white)">Памятки по подготовке к УЗИ и аллергодиагностике появятся после согласования с клиникой.</div>
</div>
</section>

<section class="section bg-white">
<div class="wrap two-col">
<div class="col-intro"><h2>Частые вопросы</h2><p>Не нашли ответ — позвоните или напишите в WhatsApp.</p>{wa_link("btn btn-outline")}</div>
<div class="faq">{faq}</div>
</div>
</section>
{cta(r, "Остались вопросы?", "Позвоните или напишите в WhatsApp — администратор ответит в рабочее время.")}
'''
    page("pacientam/", "Пациентам", "Как записаться в центр доктора Канаевой, что взять на первый приём и ответы на частые вопросы.", body, "pat")


# ---------- Цены ----------
def prices():
    r = "../"
    blocks = "".join(
        f'''<div class="stack" style="gap:16px"><h3><a href="{r}napravleniya/{d["slug"]}/">{d["title"]}</a></h3>
<div class="price-card" style="background:var(--white)">{"".join(f'<div class="price-row"><span>{p}</span><span class="v">{tbd()}</span></div>' for p in d["prices"])}</div></div>'''
        for d in DIRECTIONS
    )
    body = f'''
<section class="bg-warm">
<div class="wrap" style="padding-bottom:100px">
{crumbs(r, [("ceny/", "Цены")])}
<h1 style="margin-top:32px">Цены</h1>
<p class="lead" style="margin-top:16px">Стоимость приёмов и исследований уточняется — актуальные цены сообщит администратор по телефону {CLINIC["phone"]}.</p>
<div class="two-col two-col--even" style="margin-top:48px;row-gap:40px">{blocks}</div>
<p class="small" style="margin-top:32px">Информация о ценах не является публичной офертой.</p>
</div>
</section>
{cta(r, "Узнать стоимость и записаться", "Позвоните или напишите в WhatsApp — администратор назовёт цену и подберёт время.")}
'''
    page("ceny/", "Цены", "Цены на приёмы и исследования в центре доктора Канаевой, Махачкала.", body, "price")


# ---------- Документы ----------
def legal_info():
    r = "../"
    L = CLINIC["legal"]
    staff = "".join(f'<div class="req-row"><span>{d["role"]}</span><span><a href="{r}vrachi/{d["slug"]}/" style="text-decoration:underline">{d["name"]}</a></span></div>' for d in DOCTORS)
    body = f'''
<section class="bg-warm">
<div class="wrap" style="padding-bottom:64px">
{crumbs(r, [("svedeniya/", "Сведения о медицинской организации")])}
<h1 style="margin-top:32px;font-size:clamp(32px,4vw,56px)">Сведения о медицинской организации</h1>
</div>
</section>
<section class="section bg-white">
<div class="wrap two-col two-col--even">
<div class="rows"><h3 style="margin-bottom:16px">Организация и лицензия</h3>
<div class="req-row"><span>Исполнитель</span><span>{L["entity"]}</span></div>
<div class="req-row"><span>ОГРНИП</span><span>{L["ogrnip"]}</span></div>
<div class="req-row"><span>ИНН</span><span>{L["inn"]}</span></div>
<div class="req-row"><span>Адрес</span><span>{L["license_address"]}</span></div>
<div class="req-row"><span>Режим работы</span><span>{CLINIC["hours_full"]}</span></div>
<div class="req-row"><span>Лицензия</span><span>{L["license"]}</span></div>
<div class="req-row"><span>Кем выдана</span><span>{L["license_body"]}</span></div>
<div class="doc-links"><a href="{L["registry"]}" target="_blank" rel="noopener">{icon("file", 16)}Проверить в реестре лицензий</a></div>
</div>
<div class="rows"><h3 style="margin-bottom:16px">Медицинские работники</h3>{staff}
<p class="small" style="margin-top:16px">Сведения об образовании и квалификации — на страницах врачей.</p></div>
</div>
</section>
<section class="section bg-warm">
<div class="wrap">
<div class="section-head"><h2>Контролирующие органы</h2></div>
<div class="info-cards" style="margin-top:0">
<div class="org-card" style="background:var(--white)"><b>Министерство здравоохранения Республики Дагестан</b><span>Адрес и телефон: {tbd()}</span></div>
<div class="org-card" style="background:var(--white)"><b>Территориальный орган Росздравнадзора по Республике Дагестан</b><span>Адрес и телефон: {tbd()}</span></div>
<div class="org-card" style="background:var(--white)"><b>Управление Роспотребнадзора по Республике Дагестан</b><span>Адрес и телефон: {tbd()}</span></div>
</div>
</div>
</section>
'''
    page("svedeniya/", "Сведения о медицинской организации", "Реквизиты, лицензия и контролирующие органы центра доктора Канаевой.", body)


def policy():
    r = "../"
    L = CLINIC["legal"]
    body = f'''
<section class="bg-warm">
<div class="wrap" style="padding-bottom:64px">
{crumbs(r, [("politika/", "Политика обработки персональных данных")])}
<h1 style="margin-top:32px;font-size:clamp(32px,4vw,56px)">Политика обработки персональных данных</h1>
</div>
</section>
<section class="section bg-white">
<div class="wrap prose">
<p><b>Оператор:</b> {L["entity"]}, ОГРНИП {L["ogrnip"]}, ИНН {L["inn"]}, адрес: {L["license_address"]}.</p>
<p>Полный текст политики обработки персональных данных и форма согласия на обработку персональных данных будут размещены на этой странице после согласования с клиникой.</p>
<p class="muted">В демо-версии сайта данные из форм никуда не передаются и не сохраняются.</p>
</div>
</section>
'''
    page("politika/", "Политика обработки персональных данных", "Политика обработки персональных данных центра доктора Канаевой.", body)


def not_found():
    r = BASE_PATH
    body = f'''
<section class="bg-warm">
<div class="wrap notfound">
<span class="pill"><span class="dot"></span>Ошибка 404</span>
<h1>Такой страницы нет</h1>
<p class="lead">Возможно, она переехала. Начните с главной или посмотрите направления и врачей центра.</p>
<div class="btn-row"><a class="btn btn-primary" href="{r}">На главную</a><a class="btn btn-outline" href="{r}vrachi/">Врачи</a><a class="btn btn-outline" href="{r}napravleniya/">Направления</a></div>
</div>
</section>'''
    page("404.html", "Страница не найдена", "Страница не найдена.", body, r=r)


def extras():
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    robots = "User-agent: *\nDisallow: /\n" if DEMO else f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n"
    (DOCS / "robots.txt").write_text(robots, encoding="utf-8")


if __name__ == "__main__":
    home()
    doctors_index()
    for d in DOCTORS:
        doctor_page(d)
    directions_index()
    for d in DIRECTIONS:
        direction_page(d)
    contacts()
    about()
    patients()
    prices()
    legal_info()
    policy()
    not_found()
    extras()
    pages = sorted(p.relative_to(DOCS) for p in DOCS.rglob("*.html"))
    print(f"Собрано страниц: {len(pages)}")
    for p in pages:
        print("  ", p)
