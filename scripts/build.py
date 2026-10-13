#!/usr/bin/env python3
"""Generate the research-thread homepage and Markdown views from papers.json."""
from pathlib import Path
import html
import json
import hashlib
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/papers.json').read_text())
STYLE_VERSION = hashlib.sha256((ROOT / 'site-assets/ai-economics.css').read_bytes()).hexdigest()[:12]
E = html.escape
HOME = 'https://yukunzhang1.github.io/'
AGENT = HOME + 'research/ai-agent-economics/'
UPDATED = date.fromisoformat(DATA['updated'])
UPDATED_LABEL = {'en': f'{UPDATED.day} {UPDATED:%B %Y}', 'zh': f'{UPDATED.year}年{UPDATED.month}月{UPDATED.day}日'}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n')


def bilingual(en, zh=None):
    if isinstance(en, dict):
        en, zh = en['en'], en['zh']
    return f'<span data-lang="en">{E(en)}</span><span data-lang="zh" lang="zh-Hans">{E(zh)}</span>'


def link(url, label, cls=''):
    return f'<a class="{cls}" href="{E(url, quote=True)}">{label}</a>'


def abstract(p, lang):
    return p['abstract' if lang == 'en' else 'abstract_zh'].replace(r'\sigma_L > 1 > \sigma_H', 'σ_L > 1 > σ_H')


def resources(p, lang):
    en = lang == 'en'
    links = [('Read paper PDF' if en else '阅读论文 PDF', 'https://arxiv.org/pdf/' + p['id']), ('arXiv', 'https://arxiv.org/abs/' + p['id'])]
    if p.get('doi'):
        links.append(('Published version' if en else '出版版本', 'https://doi.org/' + p['doi']))
    if p.get('proceedings_url'):
        links.append(('Conference proceedings' if en else '会议论文集', p['proceedings_url']))
    return links


def md_resources(p, lang):
    return ' · '.join(f'[{label}]({url})' for label, url in resources(p, lang))


def record_sources(r, lang):
    return [(r['source_label'][lang], r['url'])] + [(s[lang], s['url']) for s in r.get('links', [])]


def records_md(p, lang, detailed=False):
    lines = []
    for r in p['recognition']:
        line = f'- **{r[lang]}** — {r["date_label"][lang]}. '
        if detailed:
            line += r['detail'][lang] + ' '
        line += ' · '.join(f'[{label}]({url})' for label, url in record_sources(r, lang))
        lines.append(line)
    return '\n'.join(lines)


def readme(lang):
    en = lang == 'en'
    text = '# Generative AI Economics\n\n**' + DATA['research_question'][lang] + '**\n\nYukun Zhang · Tianyang Zhang\n\n'
    text += ('[中文](README.zh-CN.md)' if en else '[English](README.md)') + f' · [Academic homepage]({HOME})\n\n'
    text += DATA['description'][lang] + '\n\n'
    text += ('[Research papers](#papers) · [Contact](#contact)' if en else '[系列论文](#papers) · [联系](#contact)') + '\n\n'
    text += '<a id="papers"></a>\n\n## ' + ('Research papers' if en else '系列论文') + '\n\n'
    text += ' · '.join(f'[{g[lang]}](#{g["id"]})' for g in DATA['groups']) + '\n\n'
    for g in DATA['groups']:
        text += f'<a id="{g["id"]}"></a>\n\n### {g[lang]}\n\n'
        for p in DATA['papers']:
            if p['group'] != g['id']:
                continue
            text += f'<a id="{p["slug"]}"></a>\n\n#### {p["number"]:02d}. [{p["title"]}](https://arxiv.org/abs/{p["id"]})\n\n'
            text += '**' + ('Abstract' if en else '摘要（译文）') + '**\n\n' + abstract(p, lang) + '\n\n'
            text += md_resources(p, lang) + '\n\n'
            if p['recognition']:
                text += ' · '.join(f'[{r[lang]}]({r["url"]})' for r in p['recognition']) + '\n\n'
            if p.get('published_title'):
                text += ('Published under the title: ' if en else '出版版本题名：') + '*' + p['published_title'] + '*.\n\n'
    text += '<a id="contact"></a>\n\n## ' + ('Contact' if en else '联系') + '\n\n'
    text += 'Yukun Zhang: [215010026@link.cuhk.edu.cn](mailto:215010026@link.cuhk.edu.cn)\n\nTianyang Zhang: [yc57317@connect.um.edu.mo](mailto:yc57317@connect.um.edu.mo)\n\n'
    text += f'[Academic homepage]({HOME}) · [AI Agent Economics]({AGENT})\n'
    return text


def paper_html(p):
    records = ''
    if p['recognition']:
        records = '<p class="paper-context">' + ' · '.join(link(r['url'], bilingual(r)) for r in p['recognition']) + '</p>'
    links = ''.join(link(url, bilingual(en, zh)) for (en, url), (zh, _) in zip(resources(p, 'en'), resources(p, 'zh')))
    note = ''
    if p.get('published_title'):
        note = '<p class="publication-note">' + bilingual('Published under the title: ', '出版版本题名：') + '<em>' + E(p['published_title']) + '</em>.</p>'
    return f'''<article class="paper" id="{p['slug']}" aria-labelledby="title-{p['slug']}">
  <div class="paper-number" aria-hidden="true">{p['number']:02d}</div>
  <div class="paper-body">
    <h4 id="title-{p['slug']}">{link('https://arxiv.org/abs/' + p['id'], E(p['title']))}</h4>
    <p class="abstract-label">{bilingual('Abstract', '摘要（译文）')}</p>
    <p class="abstract" data-lang="en" lang="en">{E(abstract(p, 'en'))}</p>
    <p class="abstract" data-lang="zh" lang="zh-Hans">{E(abstract(p, 'zh'))}</p>
    <div class="paper-links">{links}</div>
    {records}
    {note}
  </div>
</article>'''


def website():
    sections = []
    for i, g in enumerate(DATA['groups'], 1):
        papers = '\n'.join(paper_html(p) for p in DATA['papers'] if p['group'] == g['id'])
        sections.append(f'<section class="theme" id="{g["id"]}" aria-labelledby="heading-{g["id"]}"><h3 class="theme-heading" id="heading-{g["id"]}"><span aria-hidden="true">{i:02d}</span> {bilingual(g)}</h3>\n{papers}</section>')
    themes = ''.join(link('#' + g['id'], bilingual(g)) for g in DATA['groups'])
    navigation = ''.join(link('#' + target, bilingual(en, zh)) for target, en, zh in [('papers', 'Papers', '论文'), ('contact', 'Contact', '联系')])
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#12313e">
  <title>Generative AI Economics — A Research Series</title>
  <meta name="description" content="{E(DATA['description']['en'], quote=True)}">
  <meta property="og:title" content="Generative AI Economics">
  <meta property="og:description" content="Seven papers on capital, markets, and information, with full abstracts and academic activities.">
  <meta property="og:type" content="website">
  <link rel="stylesheet" href="site-assets/ai-economics.css?v={STYLE_VERSION}">
  <script src="site-assets/ai-economics.js" defer></script>
</head>
<body id="top">
  <a class="skip-link" href="#papers">{bilingual('Skip to papers', '跳至论文')}</a>
  <nav class="masthead" aria-label="Main navigation"><div class="masthead-inner">
    {link(HOME, 'Yukun Zhang', 'author-home')}
    <div class="navigation">{navigation}<button class="language" type="button" aria-label="切换至中文" hidden>中文</button></div>
  </div></nav>
  <header class="series-header reading-column">
    <p class="eyebrow">{bilingual('A research series', '经济学研究系列')}</p>
    <h1>Generative AI <em>Economics</em></h1>
    <p class="deck">{bilingual(DATA['research_question'])}</p>
  </header>
  <div class="metadata-band"><dl class="series-meta reading-column">
    <div><dt>{bilingual('Authors', '作者')}</dt><dd>{link(HOME, 'Yukun Zhang')}<br>Tianyang Zhang</dd></div>
    <div><dt>{bilingual('Research areas', '研究主题')}</dt><dd>{bilingual(DATA['subtitle'])}</dd></div>
    <div><dt>{bilingual('Last updated', '最近更新')}</dt><dd><time datetime="{DATA['updated']}">{bilingual(UPDATED_LABEL)}</time></dd></div>
  </dl></div>
  <main>
    <div class="introduction reading-column"><p>{bilingual(DATA['description'])}</p></div>
    <section class="reading-column papers" id="papers" aria-labelledby="papers-title">
      <h2 id="papers-title">{bilingual('Research papers', '系列论文')}</h2>
      <p class="section-intro">{bilingual('The papers are arranged by research theme. Full abstracts appear below.', '论文按研究主题排列，以下直接展示每篇论文的完整摘要。')}</p>
      <nav class="themes" aria-label="Research themes">{themes}</nav>
      {''.join(sections)}
    </section>
    <section class="reading-column contact" id="contact" aria-labelledby="contact-title">
      <h2 id="contact-title">{bilingual('Discussion & contact', '交流与联系')}</h2>
      <p>{bilingual('For questions and research discussions, contact the authors.', '欢迎就论文内容与研究合作联系作者。')}</p>
      <dl class="contacts"><div><dt>Yukun Zhang</dt><dd>{link('mailto:215010026@link.cuhk.edu.cn', '215010026@link.cuhk.edu.cn')}</dd></div><div><dt>Tianyang Zhang</dt><dd>{link('mailto:yc57317@connect.um.edu.mo', 'yc57317@connect.um.edu.mo')}</dd></div></dl>
    </section>
  </main>
  <footer><div class="reading-column footer-inner"><p>Generative AI Economics</p><div class="footer-links">{link(HOME, bilingual('Academic homepage', '学术主页'))}{link(AGENT, 'AI Agent Economics')}{link(DATA['repo_url'], 'GitHub')}{link('#top', bilingual('Back to top ↑', '返回顶部 ↑'))}</div></div></footer>
</body>
</html>'''


def main():
    write(ROOT / 'README.md', readme('en'))
    write(ROOT / 'README.zh-CN.md', readme('zh'))
    write(ROOT / 'index.html', website())
    for p in DATA['papers']:
        text = '[← Series overview](../README.md)\n\n# ' + p['title'] + '\n\nYukun Zhang · Tianyang Zhang\n\n' + md_resources(p, 'en')
        if p['recognition']:
            text += '\n\n## Awards & academic activities\n\n' + records_md(p, 'en', detailed=True)
        text += '\n\n## Abstract\n\n' + abstract(p, 'en')
        if p.get('published_title'):
            text += '\n\nPublished under the title: *' + p['published_title'] + '*.'
        text += '\n\n## 中文摘要（译文）\n\n' + abstract(p, 'zh')
        if p['recognition']:
            text += '\n\n## 奖项与学术活动\n\n' + records_md(p, 'zh', detailed=True)
        write(ROOT / 'papers' / (p['slug'] + '.md'), text)
    print('Generated research-thread homepage, bilingual READMEs, and seven reading pages.')


if __name__ == '__main__':
    main()
