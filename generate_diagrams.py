#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成论文用 SVG 矢量图 — 三层架构图、数据流图、比喻匹配流程图"""
import os

OUT = r'c:\Users\16137\Desktop\vb期末\diagrams'
os.makedirs(OUT, exist_ok=True)

def svg(w, h):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<style>
  text {{ font-family: "Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif; }}
  .title {{ font-size:15px; font-weight:700; fill:#1E293B; }}
  .subtitle {{ font-size:11px; fill:#64748B; }}
  .box {{ fill:#FFFFFF; stroke:#CBD5E1; stroke-width:1.2; rx:6; }}
  .box-accent {{ fill:#EFF6FF; stroke:#93C5FD; stroke-width:1.2; rx:6; }}
  .layer-label {{ font-size:13px; font-weight:700; fill:#1E40AF; }}
  .module-name {{ font-size:11px; font-weight:600; fill:#0F172A; }}
  .module-desc {{ font-size:9px; fill:#64748B; }}
  .badge {{ font-size:10px; font-weight:600; }}
  .arrow {{ stroke:#94A3B8; stroke-width:1.5; fill:none; marker-end:url(#arrowhead); }}
  .arrow-thin {{ stroke:#CBD5E1; stroke-width:1; fill:none; }}
  .dashed {{ stroke-dasharray: 4 3; }}
</style>
<defs>
  <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#94A3B8"/>
  </marker>
</defs>
<rect width="{w}" height="{h}" fill="#F8FAFC" rx="4"/>
'''

def rect(x, y, w, h, cls='box'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}"/>'

def text(x, y, content, cls='module-name', anchor='middle'):
    lines = content.split('\n')
    out = []
    for i, line in enumerate(lines):
        out.append(f'<text x="{x}" y="{y + i*15}" class="{cls}" text-anchor="{anchor}">{line}</text>')
    return '\n'.join(out)

def badge(x, y, txt, color):
    return f'<rect x="{x}" y="{y}" width="28" height="14" rx="3" fill="{color}" opacity="0.12"/><text x="{x+14}" y="{y+10}" class="badge" fill="{color}" text-anchor="middle">{txt}</text>'

# ═══════════════════════════════════════════
# 图1: 三层架构图 (1200 x 820)
# ═══════════════════════════════════════════
w, h = 1200, 820
s = svg(w, h)

# 背景层框
s += rect(20, 40, 1160, 720, 'box')
s += f'<text x="600" y="22" class="title" text-anchor="middle">系统三层架构图</text>'

# ── 表现层 ──
s += rect(40, 55, 1120, 240, 'box-accent')
s += text(60, 72, '【表现层】Presentation Layer', 'layer-label', 'start')

# 5个模块卡片
modules_p = [
    ('📊 仪表盘\nDashboard', '·统计卡片 ·日历热力\n·趋势图 ·排行榜', 80),
    ('📝 说明书\nDoc Panel', '·技术版 ·小白版\n·语义解释 ·代码输入', 280),
    ('🏋️ 练习\nPractice', '·对比评估 ·每日挑战\n·Pyodide ·学习笔记', 480),
    ('🕐 历史\nHistory', '·搜索筛选 ·分页浏览\n·批量选择 ·重命名', 680),
    ('🏆 成就\nBadges', '·徽章墙 ·进度条\n·解锁弹窗 ·里程碑', 880),
]
for label, desc, x in modules_p:
    s += rect(x, 90, 180, 80, 'box')
    s += text(x + 90, 108, label, 'module-name')
    s += text(x + 90, 135, desc, 'module-desc')

# AI 文档面板 (下方横条)
s += rect(80, 185, 1040, 50, 'box')
s += text(600, 205, '📄 AI 文档面板 (PPT / Word / TTS) — 一键导出 7页PPT + Word分析报告 + 语音讲解', 'module-name')
s += text(600, 222, 'PptxGenJS · JSZip · html2canvas · Web Speech API', 'module-desc')

# ── 箭头 表现层→业务逻辑层 ──
s += f'<line x1="600" y1="295" x2="600" y2="315" class="arrow"/>'

# ── 业务逻辑层 ──
s += rect(40, 320, 1120, 190, 'box-accent')
s += text(60, 338, '【业务逻辑层】Business Logic Layer', 'layer-label', 'start')

# 第一行 4个组件
biz_row1 = [
    ('解析引擎', 'parseJava()\nparsePython()\n正则提取: 函数名\n参数列表·返回类型\n依赖/异常', 80),
    ('比喻匹配器', 'matchMeta-\nphorEntry()\n38条概念域映射\n加权打分:\n函数名+8 概念+6\n代码体+3 模式+7', 280),
    ('模式检测器', 'detectPatterns()\n12种模式:\n·递归·排序·缓存\n·工厂·I/O·校验\n·循环·分支·聚合', 500),
    ('健康度评估器', 'calculateHealth\nScore()\n5维评分:\n·参数·行数·嵌套\n·圈复杂度·冗余', 730),
]
for label, desc, x in biz_row1:
    s += rect(x, 355, 200, 105, 'box')
    s += text(x + 100, 373, label, 'module-name')
    s += text(x + 100, 393, desc, 'module-desc')

# 第二行 3个组件
biz_row2 = [
    ('PPT 生成器', 'generatePPTForCode()\n·7页PPT模板\n·PptxGenJS\n·批量ZIP打包', 160),
    ('Word 导出器', 'exportWord()\n·周期筛选\n·HTML→Blob\n·.docx下载', 440),
    ('叙事生成器', 'renderTechDoc() 技术版\nrenderBeginnerDoc() 小白版\nrenderSemanticDoc() 语义版\n·推论标记(inferred)\n·生活化比喻叙事', 720),
]
for label, desc, x in biz_row2:
    s += rect(x, 470, 260, 40, 'box')
    s += text(x + 130, 488, label, 'module-name')
    s += text(x + 130, 503, desc, 'module-desc')

# ── 箭头 业务→持久 ──
s += f'<line x1="600" y1="510" x2="600" y2="530" class="arrow"/>'

# ── 数据持久层 ──
s += rect(40, 535, 1120, 195, 'box-accent')
s += text(60, 553, '【数据持久层】Data Layer', 'layer-label', 'start')

s += rect(80, 570, 1040, 140, 'box')
s += text(600, 590, 'localStorage: appStats', 'module-name')

data_items = [
    ('total · javaCount\npythonCount · avgTime', 150),
    ('patternStats\n"递归":5,"排序":3', 350),
    ('metaphorHits\n"sort":12,"filter":7', 550),
    ('history [50条]\n{code, lang, funcName,\ntimestamp, score}', 750),
    ('badgeState\nfirst_blood:✓\njava_master:✓', 950),
]
for desc, x in data_items:
    s += rect(x, 610, 180, 80, 'box')
    s += text(x + 90, 635, desc, 'module-desc')

# 扩展存储
s += rect(80, 700, 1040, 22, 'box')
s += text(600, 716, 'favorites [收藏列表]  ·  notes [学习笔记]  ·  settings (主题/动画)  ·  practiceHistory', 'module-desc')

s += '</svg>'

with open(os.path.join(OUT, 'fig1_architecture.svg'), 'w', encoding='utf-8') as f:
    f.write(s)
print('[OK] fig1_architecture.svg')

# ═══════════════════════════════════════════
# 图2: 核心数据流图 (900 x 1100)
# ═══════════════════════════════════════════
w2, h2 = 900, 1100
s2 = svg(w2, h2)
s2 += f'<text x="450" y="22" class="title" text-anchor="middle">核心数据流图</text>'

# 用户输入
s2 += rect(300, 40, 300, 36, 'box-accent')
s2 += text(450, 63, '用户粘贴代码 (Java / Python)', 'module-name')

s2 += f'<line x1="450" y1="76" x2="450" y2="100" class="arrow"/>'

# 解析引擎
s2 += rect(250, 105, 400, 80, 'box')
s2 += text(450, 123, 'parseJava() / parsePython()', 'module-name')
s2 += text(450, 148, '输出: ParsedFunction { methodName, parameters[],', 'module-desc')
s2 += text(450, 163, '  returnType, dependencies[], hasTryCatch, rawCode }', 'module-desc')

# 三分支
s2 += f'<line x1="250" y1="145" x2="140" y2="200" class="arrow-thin"/>'
s2 += f'<line x1="450" y1="185" x2="450" y2="210" class="arrow"/>'
s2 += f'<line x1="650" y1="145" x2="760" y2="200" class="arrow-thin"/>'

for x, label, desc in [
    (30, 'matchMetaphorEntry()', '38条比喻库\n加权评分'),
    (340, 'detectPatterns()', '12种模式检测\n正则匹配'),
    (650, 'generateStatement\nExplanation()', '逐行翻译\nif/for/return'),
]:
    s2 += rect(x, 215, 200, 55, 'box')
    s2 += text(x + 100, 233, label, 'module-name')
    s2 += text(x + 100, 255, desc, 'module-desc')

# 汇聚箭头
for x in [130, 450, 750]:
    s2 += f'<line x1="{x}" y1="270" x2="{x}" y2="300" class="arrow-thin"/>'

# 中间结果
for x, label in [(80, '{entry, matchQuality}'), (370, "['递归','排序',...]"), (640, '[逐行解释]')]:
    s2 += rect(x, 305, 180, 28, 'box-accent')
    s2 += text(x + 90, 324, label, 'module-desc')

# 汇聚
s2 += f'<line x1="170" y1="333" x2="170" y2="380" class="arrow-thin"/>'
s2 += f'<line x1="170" y1="380" x2="450" y2="380" class="arrow-thin"/>'
s2 += f'<line x1="460" y1="333" x2="460" y2="380" class="arrow-thin"/>'
s2 += f'<line x1="730" y1="333" x2="730" y2="380" class="arrow-thin"/>'
s2 += f'<line x1="730" y1="380" x2="450" y2="380" class="arrow-thin"/>'
s2 += f'<line x1="450" y1="380" x2="450" y2="410" class="arrow"/>'

# 三个渲染器
for x, label, desc in [
    (30, 'renderTechDoc()', '技术版\n·函数签名 ·参数表格\n·健康度评分'),
    (330, 'renderBeginnerDoc()', '小白版\n·比喻叙事 ·模式补充\n·推论标记'),
    (630, 'renderSemanticDoc()', '语义版\n·算法逻辑 ·数据流\n·推论标记'),
]:
    s2 += rect(x, 415, 240, 65, 'box')
    s2 += text(x + 120, 433, label, 'module-name')
    s2 += text(x + 120, 458, desc, 'module-desc')

# 汇聚到右侧面板
for x in [150, 450, 750]:
    s2 += f'<line x1="{x}" y1="480" x2="{x}" y2="520" class="arrow-thin"/>'
    s2 += f'<line x1="{x}" y1="520" x2="450" y2="520" class="arrow-thin"/>'
s2 += f'<line x1="450" y1="520" x2="450" y2="545" class="arrow"/>'

s2 += rect(280, 550, 340, 36, 'box-accent')
s2 += text(450, 573, '右侧面板（三标签页显示）', 'module-name')

s2 += f'<line x1="450" y1="586" x2="450" y2="610" class="arrow"/>'

# recordParse
s2 += rect(250, 615, 400, 100, 'box')
s2 += text(450, 633, 'recordParse()', 'module-name')
s2 += text(450, 655, 'appStats.total++  ·  patternStats["递归"]++', 'module-desc')
s2 += text(450, 672, 'metaphorHits["sort"]++  ·  history.unshift({...})', 'module-desc')
s2 += text(450, 689, 'parseDays[today]++  →  checkBadges()  →  saveStats()', 'module-desc')

# 底部
s2 += f'<line x1="450" y1="715" x2="450" y2="740" class="arrow"/>'
s2 += rect(300, 745, 300, 36, 'box-accent')
s2 += text(450, 768, 'localStorage 持久化 + renderAllUI() 刷新', 'module-name')

# 底部箭头 + 循环
s2 += f'<line x1="150" y1="763" x2="150" y2="800" class="arrow-thin dashed"/>'
s2 += f'<line x1="150" y1="800" x2="150" y2="800" class="arrow-thin dashed"/>'

s2 += '</svg>'

with open(os.path.join(OUT, 'fig2_dataflow.svg'), 'w', encoding='utf-8') as f:
    f.write(s2)
print('[OK] fig2_dataflow.svg')

# ═══════════════════════════════════════════
# 图3: 比喻匹配加权评分算法流程图 (750 x 900)
# ═══════════════════════════════════════════
w3, h3 = 750, 900
s3 = svg(w3, h3)
s3 += f'<text x="375" y="22" class="title" text-anchor="middle">比喻匹配加权评分算法流程图</text>'

nodes = [
    # (x, y, w, h, text, type)
    (275, 45, 200, 36, '输入: code, parsed, patterns', 'accent'),
    (275, 105, 200, 36, '初始化 bestScore=0, bestEntry=null', 'normal'),
    (275, 165, 200, 36, 'for each in METAPHOR_LIBRARY (38条)', 'normal'),
    (215, 230, 320, 50, 'Step 1: 函数名匹配\n关键词∈函数名→+8  概念词∈函数名→+6', 'normal'),
    (215, 305, 320, 50, 'Step 2: 代码体匹配\n泛型词(if/for/return)→+1  领域词(sort/cache/api)→+3', 'normal'),
    (215, 380, 320, 50, 'Step 3: 模式交叉验证\n概念词 ∩ 检测模式? → +7', 'normal'),
    (275, 460, 200, 36, 'score > bestScore?', 'diamond'),
    # yes → 更新
    (450, 525, 180, 28, 'YES → 更新 best', 'accent'),
    # no → 继续下一条
    (95, 525, 140, 28, 'NO → 继续下一条', 'accent'),
    (275, 590, 200, 40, '判定匹配质量:\n≥8→strong  ≥1→moderate  0→fallback', 'normal'),
    (275, 660, 200, 36, '输出: { entry, matchQuality,\n  firstKeyword, inferReason }', 'accent'),
]

for i, (x, y, w_, h_, txt, typ) in enumerate(nodes):
    cls = 'box-accent' if typ == 'accent' else 'box'
    if typ == 'diamond':
        # draw diamond using polygon
        cx, cy = x + w_/2, y + h_/2
        pts = f'{cx},{y} {x+w_},{cy} {cx},{y+h_} {x},{cy}'
        s3 += f'<polygon points="{pts}" class="box" stroke="#F59E0B" stroke-width="1.5"/>'
        s3 += text(cx, cy + 4, txt, 'module-name')
    else:
        s3 += rect(x, y, w_, h_, cls)
        lines = txt.split('\n')
        lines_total = len(lines)
        for li, line in enumerate(lines):
            s3 += text(x + w_/2, y + 14 + li * 16, line, 'module-name')

# Arrows
arrows = [
    (375, 81, 375, 105), (375, 141, 375, 165), (375, 201, 375, 230),
    (375, 280, 375, 305), (375, 355, 375, 380), (375, 430, 375, 460),
    (375, 496, 375, 590),  # main flow (from diamond bottom)
    (375, 630, 375, 660),
]
for x1, y1, x2, y2 in arrows:
    s3 += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="arrow"/>'

# Diamond branches
s3 += f'<line x1="275" y1="478" x2="165" y2="525" class="arrow-thin"/>'  # NO left
s3 += f'<line x1="475" y1="478" x2="540" y2="525" class="arrow-thin"/>'  # YES right
s3 += f'<line x1="165" y1="553" x2="165" y2="183" class="arrow-thin dashed"/>'  # loop back
s3 += f'<line x1="165" y1="183" x2="275" y2="183" class="arrow-thin dashed"/>'  # loop back
s3 += f'<line x1="540" y1="553" x2="540" y2="608" class="arrow-thin"/>'  # YES down
s3 += f'<line x1="540" y1="608" x2="375" y2="608" class="arrow-thin"/>'  # YES merge

# Legend
s3 += rect(550, 720, 170, 80, 'box')
s3 += text(635, 740, '权重设计原则', 'module-name')
s3 += text(635, 760, '函数名 > 概念词 > 模式', 'module-desc')
s3 += text(635, 775, '> 领域词 > 泛型词', 'module-desc')
s3 += text(635, 792, '泛型词降权防止噪声', 'module-desc')

s3 += '</svg>'

with open(os.path.join(OUT, 'fig3_metaphor_match.svg'), 'w', encoding='utf-8') as f:
    f.write(s3)
print('[OK] fig3_metaphor_match.svg')

# ═══════════════════════════════════════════
# 图4: 健康度评分雷达图五维 (700 x 600) — 用 matplotlib 渲染
# ═══════════════════════════════════════════
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(7, 6), subplot_kw=dict(polar=True))
    categories = ['参数数量\n(扣8/个)', '代码行数\n(扣6/4行)', '嵌套深度\n(扣8/层)', '圈复杂度\n(扣5/分支)', '线性冗余\n(扣3/行)']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # 示例数据：一个健康函数的评分
    values_good = [5, 4, 3, 4, 5]
    values_good += values_good[:1]
    values_poor = [2, 2, 1, 1, 2]
    values_poor += values_poor[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, fontfamily='sans-serif')

    ax.set_rlabel_position(30)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8, color='grey')
    ax.set_ylim(0, 5)

    ax.fill(angles, values_good, alpha=0.15, color='#10B981')
    ax.plot(angles, values_good, 'o-', linewidth=2, color='#10B981', label='健康函数 (85分)')
    ax.fill(angles, values_poor, alpha=0.15, color='#EF4444')
    ax.plot(angles, values_poor, 'o-', linewidth=2, color='#EF4444', label='需优化函数 (35分)')

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
    ax.set_title('健康度评分五维雷达图', fontsize=14, fontweight='bold', pad=20, fontfamily='sans-serif')

    # 评分区间说明
    fig.text(0.5, 0.02, '评分区间: 🟢 80-100 健康  |  🟡 50-79 一般  |  🔴 0-49 需优化',
             ha='center', fontsize=10, fontfamily='sans-serif')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig_radar.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print('[OK] fig_radar.png (health score radar chart)')
except Exception as e:
    print(f'[WARN] radar chart failed: {e}')

# ═══════════════════════════════════════════
# 图5: 系统功能模块图 (900 x 600)
# ═══════════════════════════════════════════
w5, h5 = 950, 580
s5 = svg(w5, h5)
s5 += f'<text x="475" y="22" class="title" text-anchor="middle">系统功能模块图</text>'

# 顶部标题
s5 += rect(200, 40, 550, 36, 'box-accent')
s5 += text(475, 63, '代码智能说明书与文档自动化系统 v4.5', 'module-name')

# 6大模块
mods = [
    ('📊 仪表盘', ['统计卡片', '日历热力', '趋势图', '排行榜', '里程碑']),
    ('📝 说明书', ['技术版', '小白版', '语义版', 'JSON导出', 'PNG导出']),
    ('🏋️ 练习', ['对比练习', '每日挑战', 'Pyodide', 'AI评估', '笔记']),
    ('🕐 历史', ['搜索筛选', '分页', '批量勾选', '重命名', '清空']),
    ('🏆 成就', ['8种徽章', '进度追踪', '隐藏成就', '里程碑', '']),
    ('📄 AI文档', ['PPT导出', 'Word报告', 'TTS讲解', '批量ZIP', 'API配置']),
]
for i, (title, items) in enumerate(mods):
    x = 30 + i * 152
    s5 += rect(x, 100, 140, 50, 'box-accent')
    s5 += text(x + 70, 116, title, 'module-name')
    s5 += text(x + 70, 136, '·'.join([it for it in items if it]), 'module-desc')

# 分隔线
s5 += f'<line x1="475" y1="90" x2="475" y2="100" class="arrow"/>'

# 展开子项
all_items = []
for i, (title, items) in enumerate(mods):
    x = 30 + i * 152
    for j, it in enumerate(items):
        if it:
            all_items.append((x, 160 + j * 32, it))

for x, y, it in all_items:
    s5 += rect(x, y, 140, 24, 'box')
    s5 += text(x + 70, y + 16, it, 'module-desc')

# 底部可视化
s5 += rect(30, 340, 890, 200, 'box')
s5 += text(475, 360, 'PPT 7页结构', 'module-name')
ppt_pages = [
    ('第1页', '暗色封面\n函数名·语言\n健康度·比喻'),
    ('第2页', '签名+参数\n原始代码\n解析签名'),
    ('第3页', '函数元信息\n返回值·异常\n依赖·健康度'),
    ('第4页', '逻辑解读\n算法描述\n模式·比喻'),
    ('第5页', '示例调用\n测试场景\n实践提示'),
    ('第6页', '代码优劣\n优点·改进\n优先级'),
    ('第7页', '最佳实践\n统计快照\n热门模式'),
]
for i, (label, desc) in enumerate(ppt_pages):
    x = 50 + i * 125
    s5 += rect(x, 380, 115, 100, 'box')
    s5 += text(x + 57, 398, label, 'module-name')
    s5 += text(x + 57, 420, desc, 'module-desc')

# 底部统计
s5 += rect(30, 500, 890, 30, 'box-accent')
s5 += text(475, 520, '统计快照: 总解析次数 · Java/Python分布 · 平均耗时 · 比喻命中率 · 成就解锁数 · 连续天数',
          'module-desc')

s5 += '</svg>'

with open(os.path.join(OUT, 'fig5_modules.svg'), 'w', encoding='utf-8') as f:
    f.write(s5)
print('[OK] fig5_modules.svg')

print(f'\n[DONE] All diagrams saved to: {OUT}')
print('SVG files can be opened in browser, then screenshot for Word.')
print('Or convert with: inkscape fig.svg --export-type=png --export-dpi=300')
