"""Build the bilingual static site from content/site.json (Python standard library)."""
from pathlib import Path
from html import escape as e
from datetime import date
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
PAGES = ['home', 'education', 'publications', 'projects', 'contact']
LABELS = {
 'zh': ['首页', '教育与经历', '论文与成果', '研究与项目', '简历与联系'],
 'en': ['Home', 'Education', 'Publications', 'Research', 'CV & Contact']
}
TEXT = {
 'zh': {'skip':'跳至正文','menu':'展开导航','intro':'个人简介','interests':'研究方向','selected':'代表成果','all':'查看全部成果','cv':'下载中文简历','contact':'联系我','details':'了解研究','education':'学位教育','visits':'联合培养与交流','methods':'方法与工具','problem':'研究问题','method':'研究方法','finding':'主要发现','figures':'代表性图表','image':'查看原尺寸图片','related':'查看对应成果','email':'电子邮箱','profile':'GitHub 账号','publiccv':'公开简历','cvintro':'简历汇总教育背景、研究经历、代表成果和技术能力。中文与英文版内容一致。','downloadzh':'中文简历 · PDF','downloaden':'英文简历 · PDF','talk':'欢迎交流','talktext':'欢迎就智能反射面、毫米波通信、波束成形与接收端信号处理开展学术交流，也欢迎联系通信研发与系统仿真相关机会。','updated':'更新于','based':'基于','license':'许可证','focus':'研究概览','figuretitle':'从传播环境到接收端','figuretext':'联合考虑反射路径、波束设计与信号量化。','work':'无线通信 · 系统建模 · 算法仿真','pubintro':'围绕智能反射面辅助通信的代表性合作研究，涵盖宽带混合波束成形与模 ADC 接收端设计。','eduintro':'从通信工程基础，到无线通信系统建模与优化研究。','projintro':'围绕传播建模、波束优化和接收端量化开展研究，以系统仿真连接算法与性能分析。','coauthor':'研究简介介绍与合作者共同完成的工作。','contactintro':'公开简历与学术交流入口。','sitecredit':'个人主页','figurecredit':'论文图表归原作者及相应权利人所有。','back':'返回首页'},
 'en': {'skip':'Skip to content','menu':'Open navigation','intro':'About me','interests':'Research interests','selected':'Selected work','all':'All publications','cv':'Download English CV','contact':'Get in touch','details':'Explore the work','education':'Degree education','visits':'Research visits & exchange','methods':'Methods & tools','problem':'The question','method':'The approach','finding':'Key findings','figures':'Selected figures','image':'View full-size figure','related':'View related publication','email':'Email','profile':'GitHub profile','publiccv':'Public CV','cvintro':'Education, research experience, selected outputs, and technical skills. The Chinese and English versions contain the same information.','downloadzh':'Chinese CV · PDF','downloaden':'English CV · PDF','talk':'Let’s connect','talktext':'I welcome academic discussions on intelligent reflecting surfaces, millimeter-wave communication, beamforming, and receiver signal processing, as well as opportunities in communication R&D and system simulation.','updated':'Updated','based':'Adapted from','license':'License','focus':'Research overview','figuretitle':'From propagation to reception','figuretext':'Considering reflected paths, beamforming, and signal quantization together.','work':'Wireless communication · Modeling · Simulation','pubintro':'Selected collaborative work on IRS-assisted communication, from wideband hybrid beamforming to modulo-ADC receiver design.','eduintro':'From communication engineering fundamentals to wireless-system modeling and optimization.','projintro':'Research in propagation modeling, beamforming optimization, and receiver quantization, connecting algorithms with performance through system simulation.','coauthor':'Research summaries describe work carried out with coauthors.','contactintro':'Public CVs and ways to connect.','sitecredit':'Personal website','figurecredit':'Research figures remain the property of their authors and respective rights holders.','back':'Back to home'}
}

def loc(obj, lang):
    return e(obj[lang] if isinstance(obj, dict) else str(obj))

def path(lang, page='home'):
    return f'/{lang}/' if page == 'home' else f'/{lang}/{page}/'

def arrow():
    return '<span aria-hidden="true">↗</span>'

def button(url, label, primary=False, download=False):
    return f'<a class="button{" primary" if primary else ""}" href="{e(url, quote=True)}"{ " download" if download else ""}>{label}{arrow()}</a>'

def authors(p):
    return ', '.join('<strong>Yanan Xin</strong>' if a == 'Yanan Xin' else e(a) for a in p['authors'])

def paper_card(p, lang):
    title = p['title_zh'] if lang == 'zh' else p['title']
    return f'''<article class="citation">
      <a class="citation-image" href="{path(lang, 'publications')}#{p['id']}" tabindex="-1" aria-hidden="true"><img src="/assets/images/{p['image']}" alt="" loading="lazy" width="900" height="470"></a>
      <div class="citation-text"><div class="eyebrow">{p['year']} <span> / </span> {loc(p['type'],lang)}</div>
      <h3 class="citation-title"><a href="{path(lang,'publications')}#{p['id']}">{e(title)}</a></h3>
      <div class="citation-authors">{authors(p)}</div><div class="citation-details">{e(p['venue'])}</div>
      <p class="citation-description">{loc(p['teaser'],lang)}</p>
      <a class="text-link" href="{path(lang,'publications')}#{p['id']}">{TEXT[lang]['details']} {arrow()}</a></div></article>'''

def page_heading(lang, page, intro):
    num = PAGES.index(page)
    return f'<section class="page-heading"><div class="eyebrow">{num:02d} / {TEXT[lang]["sitecredit"]}</div><h1>{LABELS[lang][num]}</h1><p class="lead">{intro}</p></section>'

def home(lang):
    t = TEXT[lang]
    intro = f'''<section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="status-dot"></span>{loc(DATA['role'],lang)}</div>
      <h1>{loc(DATA['name'],lang)}</h1><p class="name-sub">{'Yanan Xin' if lang=='zh' else 'Wireless communications researcher'}</p>
      <p class="tagline">{loc(DATA['tagline'],lang)}</p><p class="affiliation">{loc(DATA['affiliation'],lang)}</p>
      <div class="actions">{button(path(lang,'publications'),t['selected'],True)}{button('/assets/cv/yanan-xin-'+lang+'.pdf',t['cv'],download=True)}</div>
      <a class="hero-email" href="mailto:{DATA['email']}">{DATA['email']} {arrow()}</a></div>
      <div class="research-panel"><div class="panel-top"><span>{t['focus']}</span><span>IRS × MIMO</span></div>
      <figure><img src="/assets/images/modulo-system.webp" alt="{loc(DATA['papers'][0]['figures'][0]['alt'],lang)}" width="1600" height="830" fetchpriority="high"><figcaption>{t['figuretitle']}</figcaption></figure>
      <p>{t['figuretext']}</p><div class="panel-bottom">{t['work']}</div></div></section>'''
    bio = f'<section class="about section-split"><div><span class="eyebrow">01 /</span><h2>{t["intro"]}</h2></div><div class="prose"><p class="large-text">{loc(DATA["bio"],lang)}</p><p>{loc(DATA["bio_more"],lang)}</p><a class="text-link" href="{path(lang,"education")}">{LABELS[lang][1]} {arrow()}</a></div></section>'
    interests = '<section class="interests"><div class="section-title"><h2>'+t['interests']+'</h2><span class="eyebrow">02 /</span></div><div class="grid interest-grid">'
    for i, item in enumerate(DATA['interests'],1):
        interests += f'<article class="interest"><span class="index">0{i}</span><h3>{loc(item["title"],lang)}</h3><p>{loc(item["text"],lang)}</p><span class="topic-tag">{item["tag"]}</span></article>'
    interests += '</div></section>'
    selected = f'<section><div class="section-title"><h2>{t["selected"]}</h2><a class="text-link" href="{path(lang,"publications")}">{t["all"]} {arrow()}</a></div><div class="citation-container">'+''.join(paper_card(p,lang) for p in DATA['papers'])+'</div></section>'
    return intro+bio+interests+selected

def education(lang):
    t=TEXT[lang]
    result=page_heading(lang,'education',t['eduintro'])+f'<section class="section-split"><h2>{t["education"]}</h2><div class="timeline">'
    for item in DATA['education']:
        result += f'<article class="timeline-item"><div class="timeline-date">{loc(item["date"],lang)}</div><h3>{loc(item["school"],lang)}</h3><p class="degree">{loc(item["degree"],lang)}</p><p>{loc(item["detail"],lang)}</p><span class="topic-tag">{loc(item["status"],lang)}</span></article>'
    result += f'</div></section><section class="section-split"><h2>{t["visits"]}</h2><div>'
    for item in DATA['visits']:
        result += f'<article class="visit"><div class="timeline-date">{loc(item["date"],lang)}</div><h3>{loc(item["school"],lang)}</h3><p class="degree">{loc(item["degree"],lang)}</p><p>{loc(item["detail"],lang)}</p></article>'
    return result+'</div></section>'+skill_section(lang)

def skill_section(lang):
    return f'<section class="section-split"><h2>{TEXT[lang]["methods"]}</h2><div class="skill-list">'+''.join(f'<article><h3>{loc(s["title"],lang)}</h3><p>{loc(s["text"],lang)}</p></article>' for s in DATA['skills'])+'</div></section>'

def publications(lang):
    t=TEXT[lang]
    result=page_heading(lang,'publications',t['pubintro'])
    result+='<nav class="paper-nav" aria-label="'+t['selected']+'">'+''.join(f'<a href="#{p["id"]}">{p["year"]} / {"ICC" if p["id"]=="modulo-adc" else "EuCNC"} {arrow()}</a>' for p in DATA['papers'])+'</nav>'
    for p in DATA['papers']:
        result+=f'<article class="publication" id="{p["id"]}"><header class="publication-header"><div class="eyebrow">{p["year"]} / {loc(p["type"],lang)}</div><h2>{e(p["title_zh"] if lang=="zh" else p["title"])}</h2>'
        if lang=='zh': result+=f'<p class="original-title" lang="en">{e(p["title"])}</p>'
        result+=f'<p class="authors">{authors(p)}</p><p class="venue">{e(p["venue"])}</p><p class="muted">{loc(p["meta"],lang)}</p>'
        if p['doi']: result+=f'<p class="doi">DOI: <a href="https://doi.org/{p["doi"]}">{p["doi"]}</a></p>'
        result+='<div class="actions">'+''.join(button(l['url'],loc(l['label'],lang)) for l in p['links'])+'</div></header>'
        result+='<div class="research-summary">'+''.join(f'<section><h3>{t[key]}</h3><p>{loc(p[key],lang)}</p></section>' for key in ['problem','method','finding'])+'</div>'
        result+=f'<h3 class="figure-heading">{t["figures"]}</h3><div class="figure-grid">'
        for fig in p['figures']:
            result+=f'<figure><a href="/assets/images/{fig["file"]}" aria-label="{t["image"]}: {loc(fig["alt"],lang)}"><img src="/assets/images/{fig["file"]}" alt="{loc(fig["alt"],lang)}" loading="lazy" width="1600" height="1250"></a><figcaption>{loc(fig["caption"],lang)}</figcaption></figure>'
        result+='</div></article>'
    return result+f'<p class="editorial-note">{t["coauthor"]}</p>'

def projects(lang):
    t=TEXT[lang]
    result=page_heading(lang,'projects',t['projintro'])+'<section class="projects">'
    for i,p in enumerate(DATA['projects'],1):
        result+=f'<article class="project" id="{p["id"]}"><div class="project-number">0{i}</div><div><div class="eyebrow">{loc(p["date"],lang)}</div><h2>{loc(p["title"],lang)}</h2><p class="project-category">{loc(p["category"],lang)}</p><p>{loc(p["body"],lang)}</p><p class="project-outcome">{loc(p["outcome"],lang)}</p>'
        if p['paper']: result+=f'<a class="text-link" href="{path(lang,"publications")}#{p["paper"]}">{t["related"]} {arrow()}</a>'
        result+='</div></article>'
    return result+'</section>'+skill_section(lang)

def contact(lang):
    t=TEXT[lang]
    result=page_heading(lang,'contact',t['contactintro'])+f'<section class="contact-grid"><div class="cv-panel"><span class="eyebrow">CURRICULUM VITAE</span><h2>{t["publiccv"]}</h2><p>{t["cvintro"]}</p><div class="cv-mark" aria-hidden="true">YX<span>CV</span></div><div class="cv-downloads">{button("/assets/cv/yanan-xin-zh.pdf",t["downloadzh"],True,True)}{button("/assets/cv/yanan-xin-en.pdf",t["downloaden"],False,True)}</div></div><div class="contact-info"><h2>{t["talk"]}</h2><p>{t["talktext"]}</p><dl><dt>{t["email"]}</dt><dd><a href="mailto:{DATA["email"]}">{DATA["email"]} {arrow()}</a></dd><dt>{t["profile"]}</dt><dd><a href="{DATA["github"]}">YananXFreya {arrow()}</a></dd></dl><p class="affiliation">{loc(DATA["affiliation"],lang)}</p></div></section>'
    return result.replace('CURRICULUM VITAE', '个人履历') if lang == 'zh' else result

RENDERERS={'home':home,'education':education,'publications':publications,'projects':projects,'contact':contact}

def document(lang,page,is_root=False,not_found=False):
    t=TEXT[lang]; label=LABELS[lang][PAGES.index(page)]
    title=f'{loc(DATA["name"],lang)} · {label}'
    nav=''.join(f'<a href="{path(lang,p)}"{" aria-current=\"page\"" if p==page else ""}>{LABELS[lang][i]}</a>' for i,p in enumerate(PAGES))
    language=''.join(f'<a class="lang-link" href="{path(l,page)}" lang="{l}" hreflang="{l}" data-lang="{l}"{" aria-current=\"true\"" if l==lang else ""}>{"中文" if l=="zh" else "English"}</a>' for l in ['zh','en'])
    canonical=DATA['url']+('/' if is_root else path(lang,page))
    content=RENDERERS[page](lang) if not not_found else f'<section class="page-heading"><div class="eyebrow">404</div><h1>页面未找到 / Page not found</h1><p><a href="/zh/">返回中文首页</a> · <a href="/en/">English home</a></p></section>'
    structured={'@context':'https://schema.org','@type':'Person','name':'Yanan Xin','alternateName':'辛雅楠','url':DATA['url'],'sameAs':[DATA['github']],'affiliation':{'@type':'CollegeOrUniversity','name':'Chongqing University of Posts and Telecommunications'}}
    return f'''<!doctype html>
<html lang="{'zh-CN' if lang=='zh' else 'en'}" data-dark="false"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{loc(DATA['bio'],lang)}"><meta name="theme-color" content="#153f40"><link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="zh-CN" href="{DATA['url']}{path('zh',page)}"><link rel="alternate" hreflang="en" href="{DATA['url']}{path('en',page)}"><link rel="alternate" hreflang="x-default" href="{DATA['url']}{path('zh',page)}">
<meta property="og:title" content="{title}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:description" content="{loc(DATA['tagline'],lang)}"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="stylesheet" href="/assets/template.css"><link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script><script type="application/ld+json">{json.dumps(structured,ensure_ascii=False)}</script></head>
<body data-language="{lang}" data-page="{page}" data-root="{str(is_root).lower()}"><a class="skip-link" href="#main">{t['skip']}</a>
<header class="site-header"><div class="header-inner"><a href="{path(lang)}" class="brand" aria-label="{loc(DATA['name'],lang)} · {LABELS[lang][0]}"><span class="monogram" aria-hidden="true">YX<span></span></span><span>{loc(DATA['name'],lang)}</span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="{t['menu']}"><span></span><span></span></button><nav id="site-nav" class="site-nav" aria-label="{ '主导航' if lang=='zh' else 'Main navigation'}">{nav}</nav><div class="language-switch" aria-label="{'语言' if lang=='zh' else 'Language'}">{language}</div></div></header>
<main id="main">{content}</main><footer class="site-footer"><div class="footer-main"><div><a class="footer-name" href="{path(lang)}">{loc(DATA['name'],lang)}</a><p>{t['work']}</p></div><a href="mailto:{DATA['email']}">{DATA['email']} {arrow()}</a></div><div class="footer-meta"><span>© {DATA['updated'][:4]} Yanan Xin · {t['updated']} {DATA['updated']}</span><span>{t['based']} <a href="https://github.com/greenelab/lab-website-template">Lab Website Template</a> · <a href="/LICENSE.md">{t['license']}</a></span></div><p class="rights">{t['figurecredit']}</p></footer></body></html>'''

def main():
    for lang in ['zh','en']:
        for page in PAGES:
            target=ROOT/path(lang,page).lstrip('/')/'index.html'
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(document(lang,page),encoding='utf-8')
    (ROOT/'index.html').write_text(document('zh','home',True),encoding='utf-8')
    (ROOT/'404.html').write_text(document('zh','home',not_found=True),encoding='utf-8')
    sitemap=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for lang in ['zh','en']:
        for page in PAGES:
            item=ET.SubElement(sitemap,'url'); ET.SubElement(item,'loc').text=DATA['url']+path(lang,page)
            ET.SubElement(item,'lastmod').text=DATA['updated']
    ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+DATA['url']+'/sitemap.xml\n',encoding='utf-8')
    print('Built 10 bilingual pages, Chinese root page, 404, and sitemap.')

if __name__=='__main__': main()
