#!/usr/bin/env python3
"""Build repository reading pages and optionally export the academic website."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / 'data/papers.json').read_text())
BASE = D['site_url']
REPO = D['repo_url']
ESC = html.escape

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n')

def citation(p):
    return ('@misc{zhang' + str(p['year']) + p['slug'].replace('-', '') + ',\n'
            '  title = {{' + p['title'] + '}},\n'
            '  author = {Zhang, Yukun and Zhang, Tianyang},\n'
            '  year = {' + str(p['year']) + '},\n'
            '  eprint = {' + p['id'] + '},\n'
            '  archivePrefix = {arXiv},\n'
            '  url = {https://arxiv.org/abs/' + p['id'] + '}\n}')

def poster(p):
    return REPO + '/blob/main/' + quote(p['poster'])

def bi(en, zh=None):
    if isinstance(en, dict):
        en, zh = en['en'], en['zh']
    return '<span data-ge-lang="en">' + ESC(en) + '</span><span data-ge-lang="zh">' + ESC(zh) + '</span>'

def link(url, label, internal=False, cls=''):
    attrs = 'target="_self"' if internal else 'target="_blank" rel="noopener noreferrer"'
    return f'<a class="{cls}" href="{ESC(url, quote=True)}" {attrs}>{label}</a>'

def links(p, detail=False):
    parts = []
    if not detail:
        parts.append(link('/research/ai-economics/' + p['slug'] + '/', bi('Read overview', '阅读介绍'), True))
    parts += [link('https://arxiv.org/abs/' + p['id'], 'arXiv'), link(poster(p), bi('Poster', '海报'))]
    if p.get('doi'):
        parts.append(link('https://doi.org/' + p['doi'], bi('Published version', '出版版本')))
    if detail:
        parts.append(link('#citation', 'BibTeX', True))
    return '<div class="ge-links">' + ''.join(parts) + '</div>'

def recognition(p):
    return ''.join('<p class="ge-recognition">' + link(r['url'], bi(r)) + '</p>' for r in p['recognition'])

def frame(title, excerpt, path, body):
    return ('---\nlayout: default\ntitle: ' + json.dumps(title) + '\nexcerpt: ' + json.dumps(excerpt) + '\n'
            'permalink: ' + path + '\nauthor_profile: true\nresearch_styles: true\n---\n'
            '<div class="ge-series" lang="en" data-ge-language="en">\n'
            '<div class="ge-toolbar">' + link('/#ai-economics', bi('← All research', '← 返回学术主页'), True) +
            '<button class="ge-language" type="button" aria-label="Switch language / 切换语言" hidden>中文</button></div>\n' + body +
            '\n</div>\n<script src="{{ \'/assets/js/ai-economics.js\' | relative_url }}" defer></script>\n')

def overview():
    body = '<header class="ge-hero"><p class="ge-eyebrow">' + bi('Research series · Seven papers', '研究系列 · 七篇论文') + '</p>'
    body += '<h1>Generative AI Economics</h1><p class="ge-subtitle">' + bi(D['subtitle']) + '</p><p class="ge-lead">' + bi(D['description']) + '</p>'
    body += '<div class="ge-links">' + link('#papers', bi('Explore the papers', '阅读系列论文'), True) + link(REPO, bi('Repository & materials', '仓库与材料')) + '</div></header>'
    body += '<nav class="ge-themes" aria-label="Research themes">'
    for g in D['groups']:
        body += link('#' + g['id'], '<strong>' + bi(g) + '</strong><span>' + bi(g['question']) + '</span>', True)
    body += '</nav><div id="papers">'
    for g in D['groups']:
        body += '<section class="ge-group" id="' + g['id'] + '"><h2>' + bi(g) + '</h2>'
        for p in D['papers']:
            body += '<article class="ge-paper"><span class="ge-number">' + str(p['number']).zfill(2) + '</span><div><h3>'
            body += link('/research/ai-economics/' + p['slug'] + '/', ESC(p['title']), True) + '</h3>'
            body += '<p>' + bi(p['summary']) + '</p>' + recognition(p) + links(p) + '</div></article>'
        body += '</section>'
    body += '</div><section class="ge-footer"><h2>' + bi('Recognition & presentations', '学术认可与会议展示') + '</h2><ul>'
    for p in D['papers']:
        for r in p['recognition']:
            body += '<li>' + link(r['url'], bi(r)) + '<br><span class="ge-muted">' + ESC(p['title'].split(':')[0]) + '</span></li>'
    body += '</ul><h2>' + bi('About the series', '关于系列') + '</h2><p>' + bi('The papers share questions about costs, incentives, and welfare. Each develops its own model or computational setting; the thematic order is a reading guide rather than a single sequence of formal deductions.', '各篇共享有关成本、激励和福利的问题，但分别采用独立的模型或计算设定。主题顺序用于引导阅读，并不表示七篇构成一条统一的形式推导链。') + '</p>'
    body += '<p>Yukun Zhang · Tianyang Zhang</p><div class="ge-links">' + link('mailto:215010026@link.cuhk.edu.cn', bi('Contact', '联系')) + link('/research/ai-agent-economics/', 'AI Agent Economics', True) + link('/files/ai-economics/CITATION.bib', bi('Download citations', '下载引用'), True) + '</div></section>'
    return frame('Generative AI Economics', D['description']['en'], '/research/ai-economics/', body)

def detail(p):
    body = '<nav class="ge-breadcrumb" aria-label="Breadcrumb">' + link('/research/ai-economics/', bi('Generative AI Economics', '生成式 AI 经济学'), True) + ' / ' + str(p['number']).zfill(2) + '</nav>'
    body += '<header class="ge-hero"><p class="ge-eyebrow">' + bi('Paper ' + str(p['number']) + ' of 7', '系列论文 ' + str(p['number']) + ' / 7') + '</p><h1 class="ge-detail-title">' + ESC(p['title']) + '</h1>'
    body += '<p class="ge-muted">Yukun Zhang · Tianyang Zhang</p>' + recognition(p) + links(p, True) + '</header>'
    for field, en, zh in [('question', 'Research question', '研究问题'), ('contribution', 'Main contribution', '主要贡献'), ('scope', 'Scope of the results', '结论范围')]:
        body += '<section class="ge-prose"><h2>' + bi(en, zh) + '</h2><p>' + bi(p[field]) + '</p></section>'
    # Preserve the original English abstract, with the one mathematical expression typeset.
    abstract = ESC(p['abstract']).replace(r'\sigma_L &gt; 1 &gt; \sigma_H', 'σ<sub>L</sub> &gt; 1 &gt; σ<sub>H</sub>')
    body += '<details class="ge-abstract"><summary>' + bi('Read the original English abstract', '阅读英文原始摘要') + '</summary><p lang="en">' + abstract + '</p>'
    body += '<p class="ge-muted">' + link('https://arxiv.org/abs/' + p['id'], 'arXiv:' + p['id']) + ' · ' + bi('Metadata checked 13 October 2026', '元数据核对于 2026 年 10 月 13 日') + '</p></details>'
    if p.get('published_title'):
        body += '<p class="ge-publication-note">' + bi('The publication record uses the title: ', '出版版本使用以下题名：') + '<em>' + ESC(p['published_title']) + '</em>.</p>'
    body += '<section id="citation" class="ge-citation"><h2>' + bi('Cite this paper', '引用论文') + '</h2><p class="ge-muted">' + bi('BibTeX for the arXiv version. Use the publisher’s citation for the published version.', '以下为 arXiv 版本引用；引用出版版本时，请使用出版方提供的书目信息。') + '</p>'
    body += '<pre><code>' + ESC(citation(p)) + '</code></pre><button class="ge-copy" type="button" hidden>' + bi('Copy BibTeX', '复制 BibTeX') + '</button><span class="ge-copy-status" aria-live="polite"></span></section>'
    body += '<nav class="ge-pagination" aria-label="Other papers">'
    idx = p['number'] - 1
    if idx > 0:
        prev = D['papers'][idx - 1]
        body += link('/research/ai-economics/' + prev['slug'] + '/', bi('← Previous paper', '← 上一篇'), True)
    body += link('/research/ai-economics/', bi('All seven papers', '全部七篇论文'), True)
    if idx < 6:
        nxt = D['papers'][idx + 1]
        body += link('/research/ai-economics/' + nxt['slug'] + '/', bi('Next paper →', '下一篇 →'), True)
    body += '</nav>'
    return frame(p['title'], p['summary']['en'], '/research/ai-economics/' + p['slug'] + '/', body)

def build_repo():
    bib = '\n\n'.join(citation(p) for p in D['papers']) + '\n'
    write(ROOT / 'CITATION.bib', bib)
    intro = '# Generative AI Economics\n\n**Capital, Markets, and Information**\n\n' + D['description']['en'] + '\n\n'
    intro += f'**[Explore the academic website]({BASE})** · [中文简介](README.zh-CN.md) · [BibTeX](CITATION.bib) · [Author homepage](https://yukunzhang1.github.io/)\n\n'
    intro += '## Research themes\n\n'
    intro += '\n'.join('- **' + g['en'] + '.** ' + g['question']['en'] for g in D['groups']) + '\n\n'
    intro += 'The papers offer complementary perspectives. Each uses its own assumptions and methods; their thematic order is a reading guide, not a single chain of formal deductions.\n\n## Papers\n\n'
    for g in D['groups']:
        intro += '### ' + g['en'] + '\n\n'
        for p in D['papers']:
            intro += f'**{p["number"]}. [{p["title"]}](papers/{p["slug"]}.md)**  \n{p["summary"]["en"]}\n\n'
            intro += f'[arXiv](https://arxiv.org/abs/{p["id"]}) · [Poster]({quote(p["poster"])}) · [Overview]({BASE}{p["slug"]}/)'
            if p.get('doi'):
                intro += f' · [Published version](https://doi.org/{p["doi"]})'
            intro += '\n\n'
    intro += '## Recognition & presentations\n\n'
    for p in D['papers']:
        for rec in p['recognition']:
            intro += '- **' + p['title'].split(':')[0] + '** — [' + rec['en'] + '](' + rec['url'] + ').\n'
    intro += '\n## Materials & citation\n\nThe repository contains seven poster PDFs, per-paper reading pages, and a [BibTeX file](CITATION.bib) for the arXiv versions. Published versions are linked separately where available. Simulation code and replication datasets are not currently included.\n\nPlease cite the individual paper relevant to your work. Full abstracts, research questions, scope notes, and citation entries are available on each paper’s reading page.\n\n'
    intro += '## Authors & contact\n\n**Yukun Zhang · Tianyang Zhang**\n\n[215010026@link.cuhk.edu.cn](mailto:215010026@link.cuhk.edu.cn) · [yc57317@connect.um.edu.mo](mailto:yc57317@connect.um.edu.mo)\n\nRelated series: [AI Agent Economics](https://yukunzhang1.github.io/research/ai-agent-economics/).\n\nMetadata checked: 13 October 2026. [Maintenance guide](MAINTAINING.md).\n'
    write(ROOT / 'README.md', intro)
    zh = '# 生成式 AI 经济学\n\n**资本、市场与信息**\n\n' + D['description']['zh'] + f'\n\n[访问学术专题主页]({BASE}) · [English](README.md) · [下载 BibTeX](CITATION.bib)\n\n'
    for g in D['groups']:
        zh += '## ' + g['zh'] + '\n\n' + g['question']['zh'] + '\n\n'
        for p in D['papers']:
            zh += f'**{p["number"]}. [{p["title"]}](papers/{p["slug"]}.md)**\n\n{p["summary"]["zh"]}\n\n[论文](https://arxiv.org/abs/{p["id"]}) · [海报]({quote(p["poster"])}) · [中英文介绍]({BASE}{p["slug"]}/)\n\n'
    zh += '## 学术认可与会议展示\n\n'
    for p in D['papers']:
        for rec in p['recognition']:
            zh += '- [' + rec['zh'] + '](' + rec['url'] + ') — ' + p['title'].split(':')[0] + '\n'
    zh += '\n## 关于系列\n\n各篇采用独立的模型或计算设定。主题顺序用于引导阅读，并不表示七篇构成一条统一的形式推导链。仓库目前提供论文介绍、海报和 arXiv 版本引用文件，尚未包含模拟代码与复现数据。\n\n**Yukun Zhang · Tianyang Zhang**\n\n[个人学术主页](https://yukunzhang1.github.io/) · [AI Agent Economics](https://yukunzhang1.github.io/research/ai-agent-economics/)\n'
    write(ROOT / 'README.zh-CN.md', zh)
    for p in D['papers']:
        text = '[← Series overview](../README.md) · [Academic website](' + BASE + p['slug'] + '/)\n\n# ' + p['title'] + '\n\nYukun Zhang · Tianyang Zhang\n\n'
        text += f'[arXiv](https://arxiv.org/abs/{p["id"]}) · [Poster](../{quote(p["poster"])})'
        if p.get('doi'):
            text += f' · [Published version](https://doi.org/{p["doi"]})'
        text += '\n\n'
        for field, heading in [('question', 'Research question'), ('contribution', 'Main contribution'), ('scope', 'Scope of the results')]:
            text += '## ' + heading + '\n\n' + p[field]['en'] + '\n\n'
        text += '## Original abstract\n\n' + p['abstract'].replace(r'\sigma_L > 1 > \sigma_H', r'$\sigma_L > 1 > \sigma_H$') + '\n\n'
        if p['recognition']:
            text += '## Recognition & publication\n\n' + '\n'.join('[' + rec['en'] + '](' + rec['url'] + ')' for rec in p['recognition']) + '\n\n'
        if p.get('published_title'):
            text += 'The publication record uses the title *' + p['published_title'] + '*.\n\n'
        text += '## Citation\n\nBibTeX for the arXiv version; use the publisher’s citation for the published version.\n\n```bibtex\n' + citation(p) + '\n```\n\n'
        text += 'Metadata source: [arXiv](https://arxiv.org/abs/' + p['id'] + '), checked 13 October 2026.\n'
        write(ROOT / 'papers' / (p['slug'] + '.md'), text)
    return bib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-root', type=Path, help='Local checkout of yukunzhang1.github.io')
    args = parser.parse_args()
    bib = build_repo()
    if args.site_root:
        site = args.site_root
        write(site / '_pages/ai-economics.html', overview())
        for p in D['papers']:
            write(site / '_pages/ai-economics' / (p['slug'] + '.html'), detail(p))
        write(site / 'files/ai-economics/CITATION.bib', bib)
        for name in ['ai-economics.css', 'ai-economics.js']:
            folder = 'css' if name.endswith('css') else 'js'
            write(site / 'assets' / folder / name, (ROOT / 'site-assets' / name).read_text())
    print('Built seven reading pages, bilingual README files, and BibTeX.' + (' Exported eight website pages.' if args.site_root else ''))

if __name__ == '__main__':
    main()
