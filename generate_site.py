#!/usr/bin/env python3
"""
AIHOT Topics · Site Generator
从精选的选题 JSON 生成完整的 GitHub Pages 站点。
用法：cat curated.json | python3 generate_site.py
"""

import sys
import json
import os
import re
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(REPO_ROOT, "archive")


def slugify(text):
    """将中文标题转为 URL-friendly 的 slug"""
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return s[:60]


def render_topics(data):
    """生成今日选题的 HTML 卡片"""
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    topics = data.get("topics", [])

    if not topics:
        return f'''
<div class="empty-state" id="emptyState">
  <div class="icon">⏳</div>
  <h3>今日暂无选题</h3>
  <p>AIHOT Topics 每日 13:00 自动抓取并策展，请稍后再来看看。</p>
  <div class="hint">⏰ 下次更新：今天 13:00</div>
</div>
''', "——", date_str

    blocks = []
    for i, topic in enumerate(topics, 1):
        tag_class = "tag-hot" if "热点" in topic.get("type", "") else "tag-tool"
        tag_label = topic.get("type", "热点解读型")

        context = topic.get("context", "")
        insight = topic.get("core_insight", "")
        signals = topic.get("hidden_signals", "")
        outline = topic.get("outline", [])
        controversy = topic.get("controversy", "")
        links = topic.get("links", [])
        oneliner = topic.get("oneliner", "")

        # Outline list
        outline_html = ""
        if outline:
            items = "".join(f"<li>{o}</li>" for o in outline)
            outline_html = f'<ol class="outline-list">{items}</ol>'

        # Links
        links_html = ""
        if links:
            items = "".join(
                f'<a href="{l}" target="_blank" rel="noopener">🔗 原文</a>'
                if not l.startswith("http") or True else
                f'<a href="{l}" target="_blank" rel="noopener">🔗 原文</a>'
                for l in links
            )
            links_html = f'<div class="links-box">{items}</div>'

        # Controversy
        controversy_html = ""
        if controversy:
            controversy_html = f'''
<div class="topic-section">
  <div class="label"><span class="emoji">⚠️</span>争议点</div>
  <div class="controversy-box">{controversy}</div>
</div>'''

        # Hidden signals
        signals_html = ""
        if signals:
            signals_html = f'''
<div class="topic-section">
  <div class="label"><span class="emoji">📡</span>隐藏信号</div>
  <div class="signal-box">{signals}</div>
</div>'''

        block = f'''
<div class="topic-card">
  <div class="topic-header">
    <div class="topic-index">{i}</div>
    <div class="topic-meta">
      <h3>{topic["title"]}</h3>
      <div class="topic-tags">
        <span class="tag {tag_class}">{tag_label}</span>
      </div>
    </div>
  </div>

  {f'<div class="oneliner">{oneliner}</div>' if oneliner else ''}

  <div class="topic-section">
    <div class="label"><span class="emoji">📖</span>来龙去脉</div>
    <div class="context-box">{context}</div>
  </div>

  <div class="topic-section">
    <div class="label"><span class="emoji">🔬</span>核心洞察</div>
    <div class="insight-box">{insight}</div>
  </div>

  {signals_html}

  {f'<div class="topic-section"><div class="label"><span class="emoji">📄</span>文章大纲</div>{outline_html}</div>' if outline_html else ''}

  {controversy_html}

  {f'<div class="topic-section"><div class="label"><span class="emoji">🔗</span>参考链接</div>{links_html}</div>' if links_html else ''}
</div>'''
        blocks.append(block)

    topics_html = "\n".join(blocks)
    count = len(topics)
    return topics_html, f"{count} 个选题", date_str


def render_archive_page(data):
    """生成存档页面 archive/YYYY-MM-DD.html"""
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    topics_html, count_text, _ = render_topics(data)

    # Format date for display
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = dt.strftime("%Y 年 %m 月 %d 日")
    except ValueError:
        display_date = date_str

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIHOT Topics · {date_str} 选题</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><text y='52' font-size='48'>🔥</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* [CSS 嵌入 — 使用与 index.html 相同的样式] */
:root {{
  --paper:        #F7F4EE;
  --paper-light:  #FBFAF7;
  --ink:          #1A1A2E;
  --ink-60:       #5A5A6A;
  --ink-40:       #8A8A9A;
  --ink-20:       #BABAC6;
  --accent:       #CC785C;
  --accent-light: #E8C4B0;
  --accent-deep:  #A85D42;
  --accent-dim:   rgba(204, 120, 92, 0.12);
  --accent-glow:  rgba(204, 120, 92, 0.08);
  --border:       #E8E4DC;
  --border-light: #F0ECE4;
  --green:        #5A9E6F;
  --green-dim:    rgba(90, 158, 111, 0.12);
  --gold:         #D4A853;
  --gold-dim:     rgba(212, 168, 83, 0.12);
  --font-serif:   'Noto Serif SC', Georgia, 'Times New Roman', serif;
  --font-sans:    'Inter', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-mono:    'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-2xl:  1.5rem;
  --text-3xl:  1.875rem;
  --space-3:  0.75rem;
  --space-4:  1rem;
  --space-5:  1.25rem;
  --space-6:  1.5rem;
  --space-7:  1.75rem;
  --space-8:  2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-14: 3.5rem;
  --space-20: 5rem;
  --radius-md:  8px;
  --radius-lg:  12px;
  --shadow-lg:  0 8px 30px rgba(26, 26, 46, 0.08);
}}
/* ─── 复用 index.html 完整样式 ─── */
/* 注意：完整 CSS 会由 generate_site.py 内嵌 */
/* 以下为核心样式精简版，与 index.html 一致 */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-sans);background:var(--paper);color:var(--ink);line-height:1.7;-webkit-font-smoothing:antialiased}}
a{{color:var(--accent-deep);text-decoration:none;transition:color .15s}}
a:hover{{color:var(--accent);text-decoration:underline}}

.workspace-topbar{{background:rgba(204,120,92,.08);border-bottom:1px solid var(--border);padding:6px 24px;font-size:.8rem;text-align:center}}
.workspace-topbar a{{color:var(--accent-deep);font-weight:600;text-decoration:none}}
.workspace-topbar a:hover{{text-decoration:underline}}
.workspace-topbar .sep{{color:var(--ink-20);margin:0 8px}}
.workspace-topbar .current{{color:var(--ink-60)}}

.hero{{background:linear-gradient(135deg,var(--paper-light) 0%,var(--paper) 100%);border-bottom:1px solid var(--border);padding:var(--space-12) var(--space-8) var(--space-8);position:relative;overflow:hidden}}
.hero::before{{content:"";position:absolute;inset:auto -180px -180px auto;width:480px;height:480px;border-radius:50%;background:radial-gradient(circle,rgba(204,120,92,.15) 0%,rgba(204,120,92,0) 68%);pointer-events:none}}
.hero .inner{{max-width:960px;margin:0 auto;position:relative;z-index:1}}
.hero h1{{font-family:var(--font-serif);font-size:var(--text-3xl);font-weight:900;letter-spacing:-.03em;margin:0 0 var(--space-2)}}
.hero h1 .accent{{color:var(--accent)}}
.hero .subtitle{{font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-60);max-width:600px;margin-bottom:var(--space-4)}}
.hero .meta span{{display:inline-flex;align-items:center;gap:var(--space-2);padding:0.3rem 0.7rem;background:var(--accent-dim);color:var(--accent-deep);border-radius:999px;font-size:var(--text-xs);font-weight:600}}

.page{{max-width:960px;margin:0 auto;padding:0 24px}}
.section{{padding:var(--space-8) 0}}
.back-link{{margin-bottom:var(--space-5)}}
.back-link a{{display:inline-flex;align-items:center;gap:var(--space-2);font-size:var(--text-sm);color:var(--ink-40)}}
.back-link a:hover{{color:var(--accent-deep)}}

/* 复用 topic-card 样式 */
.topic-card{{background:var(--paper-light);border:1px solid var(--border);border-radius:var(--radius-lg);padding:var(--space-7);margin-bottom:var(--space-5);transition:box-shadow .2s}}
.topic-card:hover{{box-shadow:var(--shadow-lg)}}
.topic-card .topic-header{{display:flex;align-items:flex-start;gap:var(--space-4);margin-bottom:var(--space-4)}}
.topic-card .topic-index{{flex-shrink:0;width:38px;height:38px;display:flex;align-items:center;justify-content:center;background:var(--accent-dim);color:var(--accent-deep);border-radius:var(--radius-md);font-family:var(--font-serif);font-weight:700;font-size:var(--text-base)}}
.topic-card .topic-meta{{flex:1;min-width:0}}
.topic-card .topic-meta h3{{font-family:var(--font-serif);font-size:var(--text-lg);font-weight:700;margin:0 0 var(--space-2)}}
.topic-card .topic-tags .tag{{padding:0.15rem 0.6rem;border-radius:999px;font-size:var(--text-xs);font-weight:600}}
.topic-card .tag-hot{{background:var(--accent-dim);color:var(--accent-deep)}}
.topic-card .tag-tool{{background:var(--green-dim);color:var(--green)}}
.topic-card .oneliner{{font-size:var(--text-sm);color:var(--ink-60);margin-bottom:var(--space-4);padding-left:var(--space-5);border-left:2px solid var(--accent-light)}}
.topic-card .topic-section{{margin-bottom:var(--space-3)}}
.topic-card .topic-section .label{{font-size:var(--text-xs);font-weight:600;letter-spacing:.05em;color:var(--ink-40);margin-bottom:var(--space-1)}}
.topic-card .topic-section .label .emoji{{margin-right:var(--space-1)}}
.topic-card .context-box{{font-size:var(--text-sm);color:var(--ink-60);line-height:1.7;padding:var(--space-3) var(--space-4);background:var(--accent-glow);border-radius:var(--radius-md);border-left:3px solid var(--accent-light)}}
.topic-card .insight-box{{font-size:var(--text-sm);color:#3A3A4A;line-height:1.7;padding:var(--space-3) var(--space-4);background:var(--green-dim);border-radius:var(--radius-md);border-left:3px solid var(--green)}}
.topic-card .outline-list{{list-style:none;padding:0;counter-reset:outline-step}}
.topic-card .outline-list li{{counter-increment:outline-step;padding:var(--space-2) 0 var(--space-2) var(--space-6);position:relative;font-size:var(--text-sm);color:var(--ink-60);border-bottom:1px solid var(--border-light)}}
.topic-card .outline-list li:last-child{{border-bottom:none}}
.topic-card .outline-list li::before{{content:counter(outline-step);position:absolute;left:0;top:var(--space-2);width:18px;height:18px;line-height:18px;text-align:center;background:var(--accent-dim);color:var(--accent-deep);border-radius:999px;font-size:.6rem;font-weight:700}}
.topic-card .controversy-box{{font-size:var(--text-sm);line-height:1.6;padding:var(--space-3) var(--space-4);background:#FFF8E8;border-radius:var(--radius-md);border-left:3px solid var(--gold);color:#7A6A3A}}
.topic-card .links-box{{display:flex;flex-wrap:wrap;gap:var(--space-2)}}
.topic-card .links-box a{{display:inline-flex;align-items:center;gap:var(--space-1);padding:0.25rem 0.6rem;background:var(--accent-glow);border-radius:var(--radius-md);font-size:var(--text-xs);color:var(--accent-deep);border:1px solid var(--border-light);transition:all .15s}}
.topic-card .links-box a:hover{{background:var(--accent-dim);border-color:var(--accent-light);text-decoration:none}}

.footer{{border-top:1px solid var(--border);padding:var(--space-8) 0;text-align:center}}
.footer .inner{{max-width:960px;margin:0 auto;padding:0 var(--space-8)}}
.footer p{{color:var(--ink-40);font-size:var(--text-sm);margin-bottom:var(--space-1)}}
.footer .source{{color:var(--ink-20);font-size:var(--text-xs);font-family:var(--font-mono)}}

@media (max-width:768px){{.hero{{padding:var(--space-8) var(--space-4) var(--space-6)}}.page{{padding:0 16px}}.topic-card{{padding:var(--space-5)}}.topic-card .topic-header{{flex-direction:column;gap:var(--space-2)}}.workspace-topbar{{font-size:.7rem;padding:4px 16px}}}}
</style>
</head>
<body>
<div class="workspace-topbar">
  <a href="https://zhangs1r.github.io/lessonworkspace/">📚 LessonWorkspace</a>
  <span class="sep">/</span>
  <a href="https://zhangs1r.github.io/aihot-topics/">AIHOT Topics</a>
  <span class="sep">/</span>
  <span class="current">{date_str}</span>
</div>

<div class="hero">
  <div class="inner">
    <h1>AIHOT <span class="accent">Topics</span> <span style="font-size:.5em;color:var(--ink-40);font-family:var(--font-mono)">· {date_str}</span></h1>
    <p class="subtitle">{display_date} · {count_text}</p>
    <div class="meta">
      <span>📦 存档</span>
      <span>📅 {date_str}</span>
    </div>
  </div>
</div>

<div class="section">
  <div class="page">
    <div class="back-link">
      <a href="https://zhangs1r.github.io/aihot-topics/">← 返回最新选题</a>
    </div>
    {topics_html}
  </div>
</div>

<div class="footer">
  <div class="inner">
    <p>AIHOT Topics · 基于 <a href="https://aihot.virxact.com" target="_blank">AI HOT</a> 的公众号选题自动策展</p>
    <p class="source">zhangs1r/aihot-topics · GitHub Pages</p>
  </div>
</div>
</body>
</html>'''
    return html


def get_existing_archives():
    """扫描 archive/ 目录获取已存档的日期列表"""
    if not os.path.isdir(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        return []
    archives = []
    for f in os.listdir(ARCHIVE_DIR):
        if f.endswith(".html") and len(f) == 15:  # YYYY-MM-DD.html
            date_str = f[:-5]
            archives.append(date_str)
    return sorted(archives, reverse=True)


def render_archive_grid(archives, current_date=None):
    """生成存档卡片网格的 HTML"""
    if not archives:
        return '<div style="color:var(--ink-40);font-size:var(--text-sm);text-align:center;padding:var(--space-4)">暂无存档记录</div>'

    cards = []
    for date_str in archives:
        if current_date and date_str == current_date:
            continue  # 当天不显示在存档里（已在今日选题区）
        # Parse date for display
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day = dt.strftime("%-d")
        except ValueError:
            day = date_str

        cards.append(f'''
<a class="archive-card" href="archive/{date_str}.html">
  <span class="day">{day}</span>
  <span class="date">{date_str}</span>
</a>''')
    return "\n".join(cards)


def update_index_html(today_data, all_archives):
    """更新 index.html 中的今日选题区 + 存档区"""
    index_path = os.path.join(REPO_ROOT, "index.html")
    topics_html, count_text, _ = render_topics(today_data)

    # 更新时间戳
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    updated_text = f"最近更新：{now}"

    # 存档卡片
    archive_html = render_archive_grid(all_archives, today_data.get("date"))

    # 读取 index.html
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替换今日选题区
    import re as _re
    content = _re.sub(
        r'<div id="topicsContent">.*?</div>\s*\n\s*<!-- ═══ 存档区 ═══ -->',
        f'<div id="topicsContent">\n{topics_html}\n</div>\n\n    <!-- ═══ 存档区 ═══ -->',
        content,
        flags=_re.DOTALL
    )

    # 替换 count
    content = _re.sub(
        r'<span class="count">——</span>',
        f'<span class="count">{count_text}</span>',
        content
    )

    # 替换更新时间
    content = _re.sub(
        r'<span id="updateTime">.*?</span>',
        f'<span id="updateTime">{updated_text}</span>',
        content
    )

    # 替换存档区
    content = _re.sub(
        r'<div class="archive-grid" id="archiveGrid">.*?</div>',
        f'<div class="archive-grid" id="archiveGrid">\n{archive_html}\n</div>',
        content,
        flags=_re.DOTALL
    )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ index.html 已更新 · {count_text}")


def main():
    # 读取标准输入
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))

    # 1. 确保 archive 目录存在
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # 2. 生成存档页
    archive_html = render_archive_page(data)
    archive_path = os.path.join(ARCHIVE_DIR, f"{date_str}.html")
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(archive_html)
    print(f"✅ 存档页已生成: archive/{date_str}.html")

    # 3. 获取现有存档列表
    all_archives = get_existing_archives()
    if date_str not in all_archives:
        all_archives.append(date_str)
        all_archives.sort(reverse=True)

    # 4. 更新 index.html
    update_index_html(data, all_archives)


if __name__ == "__main__":
    main()
