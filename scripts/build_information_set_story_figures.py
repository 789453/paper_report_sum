"""Create figures for the Markdown presentation manuscript."""

from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper/information-set-argument-v2/manuscript/story-figures"
OUT.mkdir(exist_ok=True)
RED = "#971f30"
INK = "#252126"
GRAY = "#635e65"
BLUE = "#365e75"
PALE = "#f4e8ea"
FONT = Path("C:/Windows/Fonts")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT / ("msyhbd.ttc" if bold else "msyh.ttc")), size)


def canvas(width=1480, height=470):
    im = Image.new("RGB", (width, height), "white")
    return im, ImageDraw.Draw(im)


def label(draw, at, text, size=32, color=INK, bold=False, anchor="lm"):
    draw.text(at, text, fill=color, font=font(size, bold), anchor=anchor)


def arrow(draw, x1, x2, y, color=GRAY):
    draw.line((x1, y, x2 - 14, y), fill=color, width=4)
    draw.polygon([(x2 - 15, y - 8), (x2, y), (x2 - 15, y + 8)], fill=color)


def acquisition():
    im, d = canvas(height=350)
    items = [
        ("可得资料", "价格、公告、分析师资料"),
        ("在线信息获取", "网页、内容、时点"),
        ("形成判断", "收益预期与风险认识"),
        ("作出交易", "可辨识的订单事件"),
    ]
    for i, (title, detail) in enumerate(items):
        x = 20 + i * 370
        emphasis = i == 1
        d.rounded_rectangle((x, 50, x + 320, 214), radius=14,
                            fill=PALE if emphasis else "#f5f4f4",
                            outline=RED if emphasis else "#d5d1d3", width=3)
        label(d, (x + 160, 103), title, 37, RED if emphasis else INK, True, "mm")
        label(d, (x + 160, 166), detail, 25, GRAY, anchor="mm")
        if i < len(items) - 1:
            arrow(d, x + 326, x + 363, 132)
    label(d, (390, 260), "论文主要测量这一环，并将活动与交易时点相连。", 30, RED, True)
    label(d, (20, 325), "概念示意 · 依据 Laarits 与 Wurgler 2026-04-27，pp. 2–3、10–11", 22, GRAY)
    im.save(OUT / "acquisition.png")


def trade_assignment():
    im, d = canvas(height=385)
    events = [(145, "周一买入"), (685, "周三卖出"), (1160, "周五买入")]
    arrow(d, 95, 1420, 142)
    for x, title in events:
        d.line((x, 106, x, 155), fill=INK, width=4)
        label(d, (x, 75), title, 31, INK, True, "mm")
    for a, b, title in [(168, 675, "周二看同股盈利"), (712, 1150, "周四看同股价格"), (1185, 1398, "周末看同股资料")]:
        arrow(d, a, b, 218, RED if b < 1200 else BLUE)
        label(d, ((a + b) // 2, 187), title, 24, INK, anchor="mm")
    label(d, (424, 265), "计入周三交易前", 28, RED, True, "mm")
    label(d, (930, 265), "计入周五交易前", 28, RED, True, "mm")
    label(d, (1294, 265), "计入末笔交易后", 26, BLUE, True, "mm")
    label(d, (95, 341), "规则示意 · 同一家庭、同一股票 · 样本内周五后没有同股交易 · 论文 p. 37", 25, GRAY)
    im.save(OUT / "trade-assignment.png")


def url_decoding():
    im, d = canvas(height=375)
    address = [("http://finance.yahoo.com", BLUE), ("/q/", INK), ("ao", RED), ("?", INK), ("s=IMCL", RED)]
    x = 40
    positions = {}
    for part, color in address:
        label(d, (x, 65), part, 45, color, True)
        width = d.textlength(part, font=font(45, True))
        positions[part] = round(x + width / 2)
        x += width
    for part, title, color in [("http://finance.yahoo.com", "来源网站", BLUE),
                               ("ao", "分析师意见", RED), ("s=IMCL", "股票代码", RED)]:
        x0 = positions[part]
        x_label = x0 + (36 if part == "s=IMCL" else 0)
        d.line((x0, 101, x0, 131, x_label, 154), fill=color, width=3)
        label(d, (x_label, 182), title, 28, color, True, "mm")
    d.rounded_rectangle((40, 231, 1430, 298), radius=10, fill=PALE)
    label(d, (68, 265), "研究记录    IMCL  ｜  分析师意见  ｜  访问时点  ｜  页面活动时间", 32, INK)
    label(d, (40, 343), "原文地址及字段示意 · 历史网页核验 ao · 附录 Step 3，Table IA1 第13行", 24, GRAY)
    im.save(OUT / "url-decoding.png")


def composite_url():
    im, d = canvas(height=480)
    for y, address, meaning in [
        (60, "…/stocks/earnings/update_earningsChart.asp?", "盈利图表"),
        (117, "duration=1095 & daysforward=545", "约3年历史、约1.5年前瞻"),
        (174, "indicator=volume,1,13,EMA,13", "成交量及移动平均"),
    ]:
        label(d, (32, y), address, 33, RED, True)
        arrow(d, 825, 925, y)
        label(d, (950, y), meaning, 31)
    d.rounded_rectangle((32, 235, 1444, 365), radius=12, fill=PALE)
    label(d, (55, 266), "股票归属  |  相邻记录补出 IMCL", 31, INK, True)
    label(d, (55, 326), "各内容的时间分配加总，仍为原页面活动时长", 31, INK)
    label(d, (32, 429), "原文URL选段与通用拆分规则示意 · p. 10、附录 Step 4、Table IA1 第6–7行", 23, GRAY)
    im.save(OUT / "composite-url.png")


def research_minutes():
    im, d = canvas(height=565)
    x0, scale = 478, 5.7
    label(d, (x0, 43), "分钟／交易（先按家庭计算，再跨家庭汇总）", 31, INK, True)
    for x in (0, 30, 60, 90, 120, 150):
        px = int(x0 + x * scale)
        d.line((px, 95, px, 435), fill="#e4e0e1", width=2)
        label(d, (px, 463), str(x), 23, GRAY, anchor="mm")
    rows = [("484户 · 宽口径研究", 144.2, 36.4),
            ("50户 · 宽口径研究", 96.8, 51.7),
            ("同一50户 · 已交易股票", 29.1, 5.7)]
    for i, (name, mean, median) in enumerate(rows):
        y = 144 + 112 * i
        label(d, (20, y + 12), name, 30, INK, True)
        for dy, value, color in [(-18, mean, BLUE), (25, median, RED)]:
            x1 = int(x0 + value * scale)
            d.rectangle((x0, y + dy, x1, y + dy + 27), fill=color)
            label(d, (x1 + 10, y + dy + 13), f"{value:.1f}", 24, color, True)
    for x, name, color in [(480, "均值", BLUE), (665, "中位数", RED)]:
        d.rectangle((x, 508, x + 27, 535), fill=color)
        label(d, (x + 39, 521), name, 25, color)
    label(d, (925, 521), "据 2026-04-27 稿 Table 2，p. 47 重绘", 22, GRAY)
    im.save(OUT / "research-minutes.png")


def pc_loadings():
    im, d = canvas(height=570)
    labels = ["讨论板", "投机标的倾向", "综合行情", "价格图", "分析师", "技术分析", "其他基本面", "盈利", "分红"]
    pc1 = [0.16, 0.01, 0.32, 0.31, 0.32, 0.27, 0.28, 0.29, 0.10]
    pc2 = [0.46, 0.43, 0.30, 0.19, 0.00, -0.11, -0.29, -0.34, -0.47]
    for center, values, title in [(585, pc1, "PC1 · 26.81%"), (1110, pc2, "PC2 · 8.77%")]:
        label(d, (center, 31), title, 34, INK, True, "mm")
        d.line((center, 62, center, 492), fill="#aca4a9", width=2)
        for i, value in enumerate(values):
            y = 85 + i * 48
            end = round(center + value * 440)
            color = RED if value > 0 else BLUE if value < 0 else GRAY
            if abs(value) >= 0.01:
                d.rectangle((min(center, end), y - 9, max(center, end), y + 9), fill=color)
            label(d, (end + (9 if value >= 0 else -9), y), f"{value:+.2f}" if value else "0.00",
                  22, color, True, "lm" if value >= 0 else "rm")
    for i, name in enumerate(labels):
        label(d, (24, 85 + i * 48), name, 29, INK, name == "投机标的倾向")
    label(d, (24, 531), "按原表符号选绘9项载荷 · 两图同尺度 · 2026-04-27 稿 Table 5，p. 51", 25, GRAY)
    im.save(OUT / "pc-loadings.png")


def paper_panel(doc, page, crop, name):
    doc[page - 1].get_pixmap(matrix=pymupdf.Matrix(3.5, 3.5),
                            clip=pymupdf.Rect(*crop), alpha=False).save(OUT / name)


acquisition()
url_decoding()
composite_url()
trade_assignment()
research_minutes()
pc_loadings()
with pymupdf.open(ROOT / "On the Information Set of Individual Investors.pdf") as paper:
    paper_panel(paper, 52, (125, 129, 493, 390), "lookback-all.png")
    paper_panel(paper, 52, (125, 398, 493, 658), "lookback-opt-in.png")
    paper_panel(paper, 54, (75, 172, 540, 505), "trade-timing.png")
    paper_panel(paper, 55, (72, 195, 502, 485), "research-paths.png")
    paper_panel(paper, 56, (118, 126, 675, 316), "paths-by-direction.png")
