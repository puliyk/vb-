#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 matplotlib 直接生成论文插图 PNG（绕过 SVG/cairo 依赖）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import numpy as np
import os

# 注册中文字体
for fp in ['C:/Windows/Fonts/msyhl.ttc', 'C:/Windows/Fonts/simsun.ttc']:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

OUT = r'c:\Users\16137\Desktop\vb期末\diagrams'
DPI = 200

def draw_box(ax, x, y, w, h, color='#FFFFFF', edge='#CBD5E1', lw=1.2, zorder=2):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=3",
                                    facecolor=color, edgecolor=edge, linewidth=lw, zorder=zorder)
    ax.add_patch(rect)

def draw_accent_box(ax, x, y, w, h, zorder=2):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=3",
                                    facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2, zorder=zorder)
    ax.add_patch(rect)

def text(ax, x, y, s, size=9, bold=False, color='#0F172A', ha='center', va='center'):
    ax.text(x, y, s, fontsize=size, fontweight='bold' if bold else 'normal',
            color=color, ha=ha, va=va, zorder=10)

def arrow(ax, x1, y1, x2, y2, color='#94A3B8', lw=1.5, zorder=1):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw), zorder=zorder)

# ═══════════════════════════════════════════
# 图1: 三层架构图
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(0, 1200); ax.set_ylim(0, 820)
ax.set_aspect('equal'); ax.axis('off')
ax.set_facecolor('#F8FAFC')

draw_box(ax, 20, 60, 1160, 740, edge='#94A3B8', lw=2)
text(ax, 600, 810, '系统三层架构图', size=14, bold=True)

# ── 表现层 ──
draw_accent_box(ax, 30, 530, 1140, 260)
text(ax, 50, 780, '【表现层】Presentation Layer', size=11, bold=True, color='#1E40AF', ha='left')

mods = [
    (50, 570, '仪表盘\nDashboard', '统计卡片 · 日历热力\n趋势图 · 排行榜'),
    (250, 570, '说明书\nDoc Panel', '技术版 · 小白版\n语义解释 · 代码输入'),
    (450, 570, '练习\nPractice', '对比评估 · 每日挑战\nPyodide · 学习笔记'),
    (650, 570, '历史\nHistory', '搜索筛选 · 分页浏览\n批量选择 · 重命名'),
    (850, 570, '成就\nBadges', '徽章墙 · 进度条\n解锁弹窗 · 里程碑'),
]
for x, y, title, desc in mods:
    draw_box(ax, x, y, 180, 100)
    text(ax, x+90, y+80, title, size=10, bold=True)
    text(ax, x+90, y+50, desc, size=7.5, color='#64748B')

# AI 文档横条
draw_box(ax, 70, 548, 1060, 18, edge='#93C5FD')
text(ax, 600, 557, 'AI 文档面板 (PPT / Word / TTS) — PptxGenJS · JSZip · html2canvas · Web Speech API', size=8, color='#64748B')

arrow(ax, 600, 548, 600, 533)

# ── 业务逻辑层 ──
draw_accent_box(ax, 30, 260, 1140, 268)
text(ax, 50, 518, '【业务逻辑层】Business Logic Layer', size=11, bold=True, color='#1E40AF', ha='left')

biz1 = [
    (50, 380, '解析引擎', 'parseJava()\nparsePython()\n正则提取'),
    (250, 380, '比喻匹配器', 'matchMetaphorEntry()\n38条概念域\n加权评分'),
    (450, 380, '模式检测器', 'detectPatterns()\n12种模式\n递归·排序·缓存'),
    (650, 380, '健康度评估', 'calculateHealthScore()\n5维评分\n参数·行数·嵌套'),
]
for x, y, title, desc in biz1:
    draw_box(ax, x, y, 180, 80)
    text(ax, x+90, y+65, title, size=9, bold=True)
    text(ax, x+90, y+30, desc, size=7, color='#64748B')

biz2 = [
    (120, 295, 'PPT 生成器', '·7页PPT模板\n·PptxGenJS'),
    (380, 295, 'Word 导出器', '·周期筛选\n·HTML→Blob'),
    (640, 295, '叙事生成器', 'renderTechDoc() 技术版\nrenderBeginnerDoc() 小白版'),
]
for x, y, title, desc in biz2:
    draw_box(ax, x, y, 190, 58)
    text(ax, x+95, y+42, title, size=9, bold=True)
    text(ax, x+95, y+18, desc, size=7, color='#64748B')

arrow(ax, 600, 268, 600, 253)

# ── 数据持久层 ──
draw_accent_box(ax, 30, 60, 1140, 188)
text(ax, 50, 243, '【数据持久层】Data Layer', size=11, bold=True, color='#1E40AF', ha='left')

draw_box(ax, 50, 75, 1100, 150)
text(ax, 600, 215, 'localStorage: appStats', size=10, bold=True)

data_items = [
    (70, 110, 180, 'total · javaCount\npythonCount · avgTime'),
    (270, 110, 180, 'patternStats\n"递归":5 · "排序":3'),
    (470, 110, 180, 'metaphorHits\n"sort":12 · "filter":7'),
    (670, 110, 180, 'history [50条]\ncode · lang · funcName'),
    (870, 110, 180, 'badgeState\nfirst_blood · java_master'),
]
for x, y, w, desc in data_items:
    draw_box(ax, x, y, w, 65)
    text(ax, x+w/2, y+33, desc, size=7, color='#64748B')

draw_box(ax, 70, 80, 1060, 16, edge='#CBD5E1')
text(ax, 600, 88, 'favorites [收藏]  ·  notes [笔记]  ·  settings (主题/动画)  ·  practiceHistory', size=7, color='#64748B')

plt.tight_layout(pad=0.5)
fig.savefig(os.path.join(OUT, 'fig1_architecture.png'), dpi=DPI, bbox_inches='tight', facecolor='white')
plt.close()
print('[OK] fig1_architecture.png')

# ═══════════════════════════════════════════
# 图3: 比喻匹配流程图
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 13))
ax.set_xlim(0, 750); ax.set_ylim(0, 900)
ax.set_aspect('equal'); ax.axis('off')
ax.set_facecolor('#F8FAFC')

text(ax, 375, 880, '比喻匹配加权评分算法流程图', size=13, bold=True)

# 节点
nodes = [
    (275, 830, 200, 32, '输入: code, parsed, patterns', '#EFF6FF'),
    (275, 775, 200, 32, 'bestScore=0, bestEntry=null', '#FFFFFF'),
    (275, 720, 200, 32, 'for each in METAPHOR_LIBRARY (38条)', '#FFFFFF'),
    (215, 650, 320, 55, 'Step 1: 函数名匹配\n关键词∈函数名→+8  概念词∈函数名→+6', '#FFFFFF'),
    (215, 575, 320, 55, 'Step 2: 代码体匹配\n泛型词(if/for/return)→+1  领域词(sort/cache/api)→+3', '#FFFFFF'),
    (215, 500, 320, 55, 'Step 3: 模式交叉验证\n概念词 ∩ 检测模式? → +7', '#FFFFFF'),
]

for x, y, w, h, label, color in nodes:
    draw_box(ax, x, y, w, h, color=color)
    parts = label.split('\n')
    for i, p in enumerate(parts):
        text(ax, x+w/2, y+h - 12 - i*14, p, size=8, bold=(i==0))

# 菱形判断
cx, cy = 375, 435
draw_box(ax, cx-65, cy-22, 130, 44, color='#FFF7ED', edge='#F59E0B')
text(ax, cx, cy, 'score > bestScore?', size=9, bold=True)

# YES / NO
draw_accent_box(ax, 460, 385, 160, 22)
text(ax, 540, 396, 'YES → 更新 best', size=8, bold=True)
draw_accent_box(ax, 90, 385, 140, 22)
text(ax, 160, 396, 'NO → 下一条', size=8, bold=True)

# 质量判定
draw_box(ax, 275, 340, 200, 36, color='#FFFFFF')
text(ax, 375, 365, '判定匹配质量:', size=8, bold=True)
text(ax, 375, 350, '≥8→strong  ≥1→moderate  0→fallback', size=7.5, color='#64748B')

# 输出
draw_accent_box(ax, 275, 290, 200, 36)
text(ax, 375, 315, '输出: { entry, matchQuality }', size=8, bold=True)

# 箭头
arrows = [
    (375, 830, 375, 807), (375, 775, 375, 752), (375, 720, 375, 705),
    (375, 650, 375, 630), (375, 575, 375, 555), (375, 500, 375, 479),
    (375, 435, 375, 376), (375, 340, 375, 326),
]
for x1, y1, x2, y2 in arrows:
    arrow(ax, x1, y1, x2, y2)

# 分支箭头
arrow(ax, 310, 435, 160, 410)    # NO
arrow(ax, 440, 435, 540, 410)    # YES
arrow(ax, 160, 385, 160, 740)    # loop back (dashed)
arrow(ax, 160, 740, 275, 740)     # loop back
arrow(ax, 540, 385, 540, 370)    # YES goes down
arrow(ax, 540, 370, 375, 370)    # YES merge

# 图例
draw_box(ax, 560, 280, 160, 70, color='#F8FAFC')
text(ax, 640, 340, '权重原则', size=8, bold=True)
text(ax, 640, 325, '函数名 > 概念词 > 模式', size=7, color='#64748B')
text(ax, 640, 312, '> 领域词 > 泛型词', size=7, color='#64748B')
text(ax, 640, 299, '泛型词降权防止噪声', size=7, color='#64748B')

plt.tight_layout(pad=0.5)
fig.savefig(os.path.join(OUT, 'fig3_metaphor_match.png'), dpi=DPI, bbox_inches='tight', facecolor='white')
plt.close()
print('[OK] fig3_metaphor_match.png')

# ═══════════════════════════════════════════
# 图2: 核心数据流图
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 16))
ax.set_xlim(0, 900); ax.set_ylim(0, 1150)
ax.set_aspect('equal'); ax.axis('off')
ax.set_facecolor('#F8FAFC')

text(ax, 450, 1135, '核心数据流图', size=13, bold=True)

# 用户输入
draw_accent_box(ax, 300, 1080, 300, 30)
text(ax, 450, 1095, '用户粘贴代码 (Java / Python)', size=9, bold=True)
arrow(ax, 450, 1080, 450, 1060)

# 解析引擎
draw_box(ax, 230, 990, 440, 65)
text(ax, 450, 1040, 'parseJava() / parsePython()', size=9, bold=True)
text(ax, 450, 1020, '输出: ParsedFunction { methodName, parameters[],', size=7, color='#64748B')
text(ax, 450, 1005, '  returnType, dependencies[], hasTryCatch, rawCode }', size=7, color='#64748B')

# 三分支
arrow(ax, 320, 990, 180, 940)
arrow(ax, 450, 990, 450, 940)
arrow(ax, 580, 990, 720, 940)

for x, y, title, desc in [
    (70, 920, 'matchMetaphorEntry()', '38条比喻库\n加权评分'),
    (350, 920, 'detectPatterns()', '12种模式检测\n正则匹配'),
    (630, 920, 'generateStatement\nExplanation()', '逐行翻译\nif/for/return'),
]:
    draw_box(ax, x, y, 200, 45)
    text(ax, x+100, y+30, title, size=8, bold=True)
    text(ax, x+100, y+12, desc, size=7, color='#64748B')

# 中间结果
for x, label in [(80, 855), (370, 855), (640, 855)]:
    draw_accent_box(ax, x, 855, 180, 22)
    text(ax, x+90, 866, label, size=7.5, color='#64748B')

# 汇聚
arrow(ax, 170, 855, 170, 830)
arrow(ax, 170, 830, 450, 830)
arrow(ax, 460, 855, 460, 830)
arrow(ax, 730, 855, 730, 830)
arrow(ax, 730, 830, 450, 830)
arrow(ax, 450, 830, 450, 805)

# 渲染器
for x, y_val, title, desc in [
    (50, 770, 'renderTechDoc()', '技术版\n·函数签名 ·参数表格'),
    (330, 770, 'renderBeginnerDoc()', '小白版\n·比喻叙事 ·模式补充'),
    (610, 770, 'renderSemanticDoc()', '语义版\n·算法逻辑 ·数据流'),
]:
    draw_box(ax, x, y_val, 240, 35)
    text(ax, x+120, y_val+20, title, size=8, bold=True)
    text(ax, x+120, y_val+8, desc, size=7, color='#64748B')

# 汇聚到面板
arrow(ax, 170, 770, 170, 745)
arrow(ax, 170, 745, 450, 745)
arrow(ax, 450, 770, 450, 745)
arrow(ax, 730, 770, 730, 745)
arrow(ax, 730, 745, 450, 745)
arrow(ax, 450, 745, 450, 725)

draw_accent_box(ax, 280, 700, 340, 25)
text(ax, 450, 712, '右侧面板（三标签页显示）', size=9, bold=True)
arrow(ax, 450, 700, 450, 685)

# recordParse
draw_box(ax, 230, 610, 440, 72)
text(ax, 450, 672, 'recordParse()', size=9, bold=True)
text(ax, 450, 652, 'appStats.total++  ·  patternStats["递归"]++', size=7, color='#64748B')
text(ax, 450, 638, 'metaphorHits["sort"]++  ·  history.unshift({...})', size=7, color='#64748B')
text(ax, 450, 624, 'parseDays[today]++  →  checkBadges()  →  saveStats()  →  renderAllUI()', size=7, color='#64748B')

arrow(ax, 450, 610, 450, 595)
draw_accent_box(ax, 300, 575, 300, 20)
text(ax, 450, 585, 'localStorage 持久化 + 全部仪表板刷新', size=8, bold=True)

plt.tight_layout(pad=0.5)
fig.savefig(os.path.join(OUT, 'fig2_dataflow.png'), dpi=DPI, bbox_inches='tight', facecolor='white')
plt.close()
print('[OK] fig2_dataflow.png')

# ═══════════════════════════════════════════
# 图5: 系统功能模块图
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 950); ax.set_ylim(0, 600)
ax.set_aspect('equal'); ax.axis('off')
ax.set_facecolor('#F8FAFC')

text(ax, 475, 585, '系统功能模块图 v4.5', size=13, bold=True)

draw_accent_box(ax, 200, 550, 550, 25)
text(ax, 475, 562, '代码智能说明书与文档自动化系统 v4.5', size=10, bold=True)

# 6大模块
mods = [
    (30, 500, '仪表盘', ['统计卡片', '日历热力', '趋势图', '排行榜', '里程碑']),
    (185, 500, '说明书', ['技术版', '小白版', '语义版', 'JSON导出', 'PNG导出']),
    (340, 500, '练习', ['对比练习', '每日挑战', 'Pyodide', 'AI评估', '笔记']),
    (495, 500, '历史', ['搜索筛选', '分页', '批量勾选', '重命名', '清空']),
    (650, 500, '成就', ['8种徽章', '进度追踪', '隐藏成就', '里程碑', '']),
    (805, 500, 'AI文档', ['PPT导出', 'Word报告', 'TTS讲解', '批量ZIP', 'API配置']),
]
for x, y_val, title, items in mods:
    draw_accent_box(ax, x, y_val, 140, 36)
    text(ax, x+70, y_val+25, title, size=9, bold=True)
    text(ax, x+70, y_val+10, ' · '.join([i for i in items if i]), size=6, color='#64748B')

    for j, it in enumerate(items):
        if it:
            draw_box(ax, x, y_val - 70 + j*30, 140, 22)
            text(ax, x+70, y_val - 59 + j*30, it, size=7, color='#64748B')

arrow(ax, 475, 550, 475, 536)

# PPT 7页结构
draw_box(ax, 30, 200, 890, 200, edge='#93C5FD')
text(ax, 475, 390, 'PPT 7页结构', size=10, bold=True)

ppt = [
    (45, 220, '第1页\n暗色封面', '函数名·语言\n健康度·比喻'),
    (170, 220, '第2页\n签名+参数', '原始代码\n解析签名'),
    (295, 220, '第3页\n函数元信息', '返回值·异常\n依赖·健康度'),
    (420, 220, '第4页\n逻辑解读', '算法描述\n模式·比喻'),
    (545, 220, '第5页\n示例调用', '测试场景\n实践提示'),
    (670, 220, '第6页\n代码优劣', '优点列表\n改进空间'),
    (795, 220, '第7页\n最佳实践', '统计快照\n热门模式'),
]
for x, y, title, desc in ppt:
    draw_box(ax, x, y, 110, 100, color='#FFFFFF')
    text(ax, x+55, y+85, title, size=8, bold=True)
    text(ax, x+55, y+45, desc, size=7, color='#64748B')

# 底部统计
draw_accent_box(ax, 30, 175, 890, 22)
text(ax, 475, 186, '统计快照: 总解析次数 · Java/Python分布 · 平均耗时 · 比喻命中率 · 成就解锁数 · 连续天数',
     size=7.5, color='#64748B')

plt.tight_layout(pad=0.5)
fig.savefig(os.path.join(OUT, 'fig5_modules.png'), dpi=DPI, bbox_inches='tight', facecolor='white')
plt.close()
print('[OK] fig5_modules.png')

# ═══════════════════════════════════════════
# 雷达图（修复中文版）
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 6), subplot_kw=dict(polar=True))
categories = ['参数数量\n(扣8/个)', '代码行数\n(扣6/4行)', '嵌套深度\n(扣8/层)', '圈复杂度\n(扣5/分支)', '线性冗余\n(扣3/行)']
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

values_good = [5, 4, 3, 4, 5]; values_good += values_good[:1]
values_poor = [2, 2, 1, 1, 2]; values_poor += values_poor[:1]

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10)
ax.set_rlabel_position(30)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8, color='grey')
ax.set_ylim(0, 5)

ax.fill(angles, values_good, alpha=0.15, color='#10B981')
ax.plot(angles, values_good, 'o-', linewidth=2, color='#10B981', label='健康函数 (85分)')
ax.fill(angles, values_poor, alpha=0.15, color='#EF4444')
ax.plot(angles, values_poor, 'o-', linewidth=2, color='#EF4444', label='需优化函数 (35分)')

ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
ax.set_title('健康度评分五维雷达图', fontsize=14, fontweight='bold', pad=20)
fig.text(0.5, 0.02, '评分区间:  80-100 健康  |  50-79 一般  |  0-49 需优化', ha='center', fontsize=10)

plt.tight_layout()
fig.savefig(os.path.join(OUT, 'fig_radar.png'), dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('[OK] fig_radar.png')

print(f'\n[DONE] All PNGs saved to {OUT}')
for f in sorted(os.listdir(OUT)):
    if f.endswith('.png'):
        size_kb = os.path.getsize(os.path.join(OUT, f)) / 1024
        print(f'  {f} ({size_kb:.0f} KB)')
