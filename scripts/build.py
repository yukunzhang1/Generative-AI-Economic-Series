#!/usr/bin/env python3
"""Generate the single-page website and repository reading pages from papers.json."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/papers.json').read_text())
E = html.escape
HOME = 'https://yukunzhang1.github.io/'
AGENT = HOME + 'research/ai-agent-economics/'


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n')


def bilingual(en, zh=None):
    if isinstance(en, dict):
        en, zh = en['en'], en['zh']
    return '<span data-lang="en">' + E(en) + '</span><span data-lang="zh" lang="zh-Hans">' + E(zh) + '</span>'


def abstract(p, lang):
    return p['abstract' if lang == 'en' else 'abstract_zh'].replace(r'\sigma_L > 1 > \sigma_H', 'σ_L > 1 > σ_H')


def resources(p, lang):
    links = [('Paper PDF' if lang == 'en' else '论文 PDF', 'https://arxiv.org/pdf/' + p['id']), ('arXiv', 'https://arxiv.org/abs/' + p['id'])]
    if p.get('doi'):
        links.append(('Published version' if lang == 'en' else '出版版本', 'https://doi.org/' + p['doi']))
    return links


def md_resources(p, lang):
    return ' · '.join(f'[{label}]({url})' for label, url in resources(p, lang))


def records_md(p, lang):
    records = [f'[{r[lang]}]({r["url"]})' for r in p['recognition']]
    return '\n\n' + ' · '.join(records) if records else ''


def readme(lang):
    en = lang == 'en'
    text = '# Generative AI Economics\n\n**' + DATA['subtitle'][lang] + '**\n\nYukun Zhang · Tianyang Zhang\n\n'
    text += ('[中文](README.zh-CN.md)' if en else '[English](README.md)') + f' · [Academic homepage]({HOME})\n\n'
    text += DATA['description'][lang] + '\n\n'
    text += ' · '.join(f'[{g[lang]}](#{g["id"]})' for g in DATA['groups']) + '\n\n'
    for i, g in enumerate(DATA['groups']):
        text += f'<a id="{g["id"]}"></a>\n\n## {i+1}. {g[lang]}\n\n'
        for p in DATA['papers']:
            if p['group'] != g['id']:
                continue
            text += f'### {p["number"]}. [{p["title"]}](https://arxiv.org/abs/{p["id"]})\n\n'
            text += md_resources(p, lang) + '\n\n**' + ('Abstract' if en else '摘要（译文）') + '**\n\n' + abstract(p, lang)
            text += records_md(p, lang)
            if p.get('published_title'):
                text += '\n\n' + ('Published under the title: ' if en else '出版版本题名：') + '*' + p['published_title'] + '*.'
            text += '\n\n'
    text += '---\n\n' + ('**Contact**' if en else '**联系**') + '\n\n'
    text += 'Yukun Zhang: [215010026@link.cuhk.edu.cn](mailto:215010026@link.cuhk.edu.cn)  \nTianyang Zhang: [yc57317@connect.um.edu.mo](mailto:yc57317@connect.um.edu.mo)\n\n'
    text += f'[Academic homepage]({HOME}) · [AI Agent Economics]({AGENT})\n'
    return text


def website():
    body = '<header class="series-header"><div class="topline"><a href="'+HOME+'">Yukun Zhang · '+bilingual('Academic homepage','学术主页')+'</a><button class="language" type="button" aria-label="切换至中文" hidden>中文</button></div><h1>Generative AI Economics</h1><p class="subtitle">'+bilingual(DATA['subtitle'])+'</p><p class="authors">Yukun Zhang <span aria-hidden="true">·</span> Tianyang Zhang</p><p class="introduction">'+bilingual(DATA['description'])+'</p></header>'
    body += '<nav class="themes" aria-label="Research themes">'
    labels=[('Capital & Infrastructure','资本与基础设施'),('Markets & Platforms','市场与平台'),('Information & Incentives','信息与激励')]
    for g, names in zip(DATA['groups'], labels):
        body += '<a href="#'+g['id']+'">'+bilingual(*names)+'</a>'
    body += '</nav><main id="papers">'
    for i, g in enumerate(DATA['groups']):
        body += '<section class="theme" id="'+g['id']+'"><h2><span class="theme-number">'+['I','II','III'][i]+'.</span> '+bilingual(g)+'</h2>'
        for p in DATA['papers']:
            if p['group'] != g['id']:
                continue
            body += '<article class="paper" id="'+p['slug']+'"><h3><a href="https://arxiv.org/abs/'+p['id']+'" target="_blank" rel="noopener noreferrer">'+E(p['title'])+'</a></h3><div class="paper-links">'
            for (en, url), (zh, _) in zip(resources(p, 'en'), resources(p, 'zh')):
                body += '<a href="'+E(url,quote=True)+'" target="_blank" rel="noopener noreferrer">'+bilingual(en,zh)+'</a>'
            body += '</div><p class="abstract-label">'+bilingual('Abstract','摘要（译文）')+'</p><p class="abstract" data-lang="en" lang="en">'+E(abstract(p,'en'))+'</p><p class="abstract" data-lang="zh" lang="zh-Hans">'+E(abstract(p,'zh'))+'</p>'
            for r in p['recognition']:
                body += '<p class="record"><a href="'+E(r['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+bilingual(r)+'</a></p>'
            if p.get('published_title'):
                body += '<p class="publication-note">'+bilingual('Published under the title: ','出版版本题名：')+'<em>'+E(p['published_title'])+'</em>.</p>'
            body += '</article>'
        body += '</section>'
    body += '</main><footer id="contact"><p><strong>'+bilingual('Contact','联系')+'</strong></p><p>Yukun Zhang · <a href="mailto:215010026@link.cuhk.edu.cn">215010026@link.cuhk.edu.cn</a><br>Tianyang Zhang · <a href="mailto:yc57317@connect.um.edu.mo">yc57317@connect.um.edu.mo</a></p><p class="footer-links"><a href="'+HOME+'">'+bilingual('Academic homepage','学术主页')+'</a><a href="'+AGENT+'">AI Agent Economics</a><a href="'+DATA['repo_url']+'">GitHub</a><a href="#top">'+bilingual('Back to top ↑','返回顶部 ↑')+'</a></p></footer>'
    return '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#17354a"><title>Generative AI Economics — Capital, Markets, and Information</title><meta name="description" content="'+E(DATA['description']['en'],quote=True)+'"><meta property="og:title" content="Generative AI Economics"><meta property="og:description" content="Capital, Markets, and Information. Seven research papers by Yukun Zhang and Tianyang Zhang."><meta property="og:type" content="website"><link rel="stylesheet" href="site-assets/ai-economics.css"><script src="site-assets/ai-economics.js" defer></script></head><body id="top"><a class="skip-link" href="#papers">'+bilingual('Skip to papers','跳至论文')+'</a><div class="page">'+body+'</div></body></html>'


def main():
    write(ROOT / 'README.md', readme('en'))
    write(ROOT / 'README.zh-CN.md', readme('zh'))
    write(ROOT / 'index.html', website())
    for p in DATA['papers']:
        text = '[← Series overview](../README.md)\n\n# ' + p['title'] + '\n\nYukun Zhang · Tianyang Zhang\n\n' + md_resources(p,'en') + '\n\n## Abstract\n\n' + abstract(p,'en') + records_md(p,'en')
        if p.get('published_title'):
            text += '\n\nPublished under the title: *' + p['published_title'] + '*.'
        text += '\n\n## 中文摘要（译文）\n\n' + abstract(p,'zh')
        write(ROOT / 'papers' / (p['slug']+'.md'), text)
    print('Generated single-page website, two READMEs, and seven reading pages.')


if __name__ == '__main__':
    main()
