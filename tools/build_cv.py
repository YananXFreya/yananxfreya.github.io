"""Generate two public CVs from site.json. Requires reportlab and a CJK TrueType font."""
from pathlib import Path
from html import escape
import json, os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
FONT=os.environ.get('CV_CJK_FONT','C:/Windows/Fonts/msyh.ttc')
if not Path(FONT).exists():
    raise SystemExit('Set CV_CJK_FONT to an installed CJK TrueType .ttf or .ttc font.')
pdfmetrics.registerFont(TTFont('CJK',FONT,subfontIndex=0))
bold_font=Path(FONT).with_name('msyhbd.ttc')
if bold_font.exists():
    pdfmetrics.registerFont(TTFont('CJK-Bold',str(bold_font),subfontIndex=0))
    pdfmetrics.registerFontFamily('CJK',normal='CJK',bold='CJK-Bold',italic='CJK',boldItalic='CJK-Bold')
else:
    pdfmetrics.registerFontFamily('CJK',normal='CJK',bold='CJK',italic='CJK',boldItalic='CJK')
INK=HexColor('#183b3e'); MUTED=HexColor('#526668'); LINE=HexColor('#d9e2de')
STYLES={
 'name':ParagraphStyle('name',fontName='CJK',fontSize=27,leading=36,textColor=INK,spaceAfter=8),
 'section':ParagraphStyle('section',fontName='CJK',fontSize=13,leading=19,textColor=INK,spaceBefore=15,spaceAfter=8,keepWithNext=True),
 'title':ParagraphStyle('title',fontName='CJK',fontSize=10.5,leading=16,textColor=INK,spaceBefore=7,spaceAfter=3,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='CJK',fontSize=9,leading=15,textColor=INK,spaceAfter=6,wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='CJK',fontSize=8,leading=13,textColor=MUTED,spaceAfter=4,wordWrap='CJK'),
 'label':ParagraphStyle('label',fontName='CJK',fontSize=8,leading=13,textColor=MUTED,spaceAfter=6),
}

def local(value,lang):
    value=value[lang] if isinstance(value,dict) else str(value)
    return escape(value.replace('—','-').replace('–','-').replace('’',"'").replace('‑','-'))

def p(text,style='body'):
    return Paragraph(text,STYLES[style])

def line():
    return HRFlowable(width='100%',thickness=.5,color=LINE,spaceBefore=6,spaceAfter=6)

def footer(canv,doc):
    canv.saveState(); w,h=doc.pagesize
    canv.setStrokeColor(LINE); canv.line(43,40,w-43,40)
    canv.setFont('CJK',7); canv.setFillColor(MUTED)
    canv.drawString(43,27,'Yanan Xin  |  yananxfreya.github.io')
    canv.drawRightString(w-43,27,f'{DATA["updated"]}  /  {doc.page}')
    canv.restoreState()

def build(lang):
    zh=lang=='zh'; story=[]
    story+=[p('辛雅楠  /  Yanan Xin' if zh else 'Yanan Xin','name'),p(local(DATA['role'],lang),'label'),p(local(DATA['affiliation'],lang),'small')]
    email=DATA['email']; url=DATA['url']
    story+=[p(f'<link href="mailto:{email}">{email}</link>  |  <link href="{url}">yananxfreya.github.io</link>','small'),line()]
    story+=[p('研究简介' if zh else 'Research profile','section'),p(local(DATA['bio'],lang)),p(local(DATA['bio_more'],lang))]
    story+=[p('教育经历' if zh else 'Education','section')]
    for item in DATA['education']:
        story.append(KeepTogether([p(local(item['date'],lang)+'  |  '+local(item['school'],lang),'title'),p(local(item['degree'],lang)+' · '+local(item['status'],lang),'body')]))
    story+=[p('联合培养与交流' if zh else 'Research visit','section')]
    v=DATA['visits'][0]
    story+=[p(local(v['date'],lang)+'  |  '+local(v['school'],lang),'title'),p(local(v['degree'],lang))]
    story+=[p('项目经历' if zh else 'Project experience','section')]
    project=DATA['projects'][0]
    story+=[p(local(project['title'],lang),'title'),p(local(project['category'],lang)+' · '+local(project['date'],lang),'small'),p(local(project['body'],lang))]
    story+=[PageBreak(),p('代表成果' if zh else 'Selected research outputs','section')]
    for pub in DATA['papers']:
        story+=[p(f'{pub["year"]} / '+local(pub['type'],lang),'label')]
        if zh: story+=[p(local(pub['title_zh'],lang),'title')]
        story+=[p(local(pub['title'],lang),'title')]
        authors=', '.join('<b>'+escape(a)+'</b>' if a=='Yanan Xin' else escape(a) for a in pub['authors'])
        story+=[p(authors,'small'),p(local(pub['venue'],lang)+' · '+local(pub['meta'],lang),'small')]
        if pub['doi']: story+=[p(f'DOI: <link href="https://doi.org/{pub["doi"]}">{pub["doi"]}</link>','small')]
        else:
            story+=[p(f'<link href="{pub["links"][0]["url"]}">'+('会议官方记录 · P-2.23' if zh else 'Official conference record · P-2.23')+'</link>','small')]
        story+=[p(local(pub['method'],lang)),p(local(pub['finding'],lang)),Spacer(1,8)]
    story+=[p('技术能力' if zh else 'Technical skills','section')]
    for skill in DATA['skills']:
        story+=[p(local(skill['title'],lang),'title'),p(local(skill['text'],lang))]
    story+=[p('联系与更多信息' if zh else 'Contact & further information','section')]
    story+=[p(f'<link href="mailto:{email}">{email}</link>','body'),p(f'<link href="{url}">{url}</link>','body'),p(f'<link href="{DATA["github"]}">{DATA["github"]}</link>','body')]
    out=ROOT/'assets/cv'/f'yanan-xin-{lang}.pdf'; out.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=43,rightMargin=43,topMargin=36,bottomMargin=53,title=('辛雅楠 - 公开简历' if zh else 'Yanan Xin - Public CV'),author='Yanan Xin',subject='Education, research, and selected outputs')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(out.name,out.stat().st_size)

if __name__=='__main__':
    build('zh'); build('en')
