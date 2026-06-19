#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建论文 Word 文档：自动目录 + 正文 + 参考文献 + 个人反思"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

# ── 页面设置 ──
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

# ── 样式设置 ──
def set_run_font(run, cn_font='宋体', en_font='Times New Roman', size=Pt(12), bold=False):
    """统一设置中英文字体"""
    run.font.size = size
    run.bold = bold
    run.font.name = en_font
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), en_font)
    rFonts.set(qn('w:hAnsi'), en_font)
    rFonts.set(qn('w:eastAsia'), cn_font)
    rFonts.set(qn('w:cs'), en_font)

style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
style.element.rPr.rFonts.set(qn('w:ascii'), 'Times New Roman')
style.element.rPr.rFonts.set(qn('w:hAnsi'), 'Times New Roman')
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.first_line_indent = Cm(0.74)  # 两字符缩进

# 标题样式
for i in range(1, 4):
    h_style = doc.styles[f'Heading {i}']
    h_font = h_style.font
    h_font.name = 'Times New Roman'
    h_style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    h_style.element.rPr.rFonts.set(qn('w:ascii'), 'Times New Roman')
    h_style.element.rPr.rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    h_font.color.rgb = RGBColor(0, 0, 0)
    h_font.bold = True
    if i == 1:
        h_font.size = Pt(16)
        h_style.paragraph_format.space_before = Pt(12)
        h_style.paragraph_format.space_after = Pt(6)
    elif i == 2:
        h_font.size = Pt(14)
        h_style.paragraph_format.space_before = Pt(10)
        h_style.paragraph_format.space_after = Pt(4)
    else:
        h_font.size = Pt(13)
        h_style.paragraph_format.space_before = Pt(8)
        h_style.paragraph_format.space_after = Pt(4)

# ── 辅助函数 ──
def add_para(text, bold=False, indent=True, align=None, font_size=12, cn_font='宋体'):
    """添加正文段落"""
    p = doc.add_paragraph()
    if not indent:
        p.paragraph_format.first_line_indent = Cm(0)
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    set_run_font(run, cn_font=cn_font, en_font='Times New Roman', size=Pt(font_size), bold=bold)
    return p

def add_heading(text, level=1):
    """添加标题（自动目录识别）"""
    h = doc.add_heading(text, level=level)
    return h

def insert_toc():
    """插入 Word 自动目录域（使用 fldSimple 避免乱码）"""
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.first_line_indent = Cm(0)

    # Use w:fldSimple — simpler and less prone to encoding issues than fldChar
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), ' TOC \\o "1-3" \\h \\z \\u ')

    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:eastAsia'), '宋体')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '21')  # 10.5pt
    rPr.append(sz)
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '808080')
    rPr.append(color)
    run.append(rPr)

    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = '（请在 Word 中右键此处 → 更新域，生成目录）'
    run.append(t)
    fldSimple.append(run)

    paragraph._p.append(fldSimple)
    doc.add_paragraph()

# ── 封面信息 ──
add_para('基于概念隐喻映射的代码智能解析与文档自动化系统设计', bold=True,
         indent=False, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=18, cn_font='黑体')
doc.add_paragraph()
add_para('学    院：信息工程学院', indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('专    业：计算机科学与技术', indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('学    号：230152061', indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('姓    名：庞凯匀', indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('日    期：2026年6月8日', indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ── 目录 ──
add_heading('目  录', level=1)
insert_toc()
doc.add_page_break()

# ══════════════════════════════════════════════
# 正文开始
# ══════════════════════════════════════════════

# ── 摘要 ──
add_heading('摘  要', level=1)
add_para(
    '本文设计并实现了一个纯前端的代码智能解析系统，该系统能够在浏览器本地完成 Java/Python 函数代码的'
    '结构化解析、概念域比喻映射、多维度健康度评估及双版本说明书自动生成。系统采用单文件架构，所有计算'
    '在客户端完成，核心功能不依赖外部 AI API。本文重点阐述了三个核心算法：基于正则表达式的分层代码解析'
    '算法、基于加权评分的概念域比喻匹配算法，以及融合圈复杂度与代码坏味理论的五维度健康度评估模型。'
    '实验表明，正则解析器在 9 组测试用例中达到 100% 识别率，比喻匹配在关键词明确的场景下匹配质量达'
    'strong 级别，系统平均解析耗时仅 8.2 毫秒。此外，本文还总结了 AI 协同开发策略在本项目中的实际应用'
    '经验与个人反思。'
)
add_para(
    '关键词：代码解析；概念隐喻；文档自动化；人机协同开发；健康度评估',
    bold=True, indent=False
)

# ── 一、引言 ──
add_heading('一、引言', level=1)

add_heading('1.1 研究背景', level=2)
add_para(
    '在软件工程教学与代码评审实践中，学习者和开发者普遍面临两个效率瓶颈：一是阅读陌生函数代码时难以'
    '快速把握其设计意图与核心逻辑；二是为代码生成技术文档或演示材料时，手动编写 PPT 和 Word 报告耗时'
    '巨大。Von Mayrhauser 与 Vans[1] 的研究指出，程序理解是一个同时涉及自顶向下（假设驱动）和自底向上'
    '（代码驱动）的复杂认知过程，而初学者往往缺乏有效的自顶向下策略，导致理解效率低下。传统的代码文档'
    '工具（如 Javadoc、Sphinx）能够提取结构化注释信息，但无法对代码逻辑进行语义层面的解读，更无法以'
    '生活化的语言降低非专业读者的理解门槛。金芝等人[7] 在《软件学报》发表的综述系统梳理了程序理解'
    '研究从认知模型到自动化技术的演进脉络，指出程序的自理解或自认知正成为新的关注热点。'
)
add_para(
    '与此同时，大语言模型（Large Language Models, LLM）的迅速发展为文档自动化开辟了新的技术路径。'
    '然而，直接调用云端 AI API 存在网络依赖性强、使用成本高昂及数据隐私风险等问题。在教学场景——'
    '尤其是期末考核等需要独立完成的任务中——一个本地优先、规则驱动、不依赖外部 API 的文档自动化方案'
    '既符合学术诚信要求，也具备实际推广价值。'
)

add_heading('1.2 研究目标', level=2)
add_para(
    '本系统——代码智能说明书与文档自动化仪表板——旨在实现以下四个目标：（1）零门槛代码理解：通过'
    '结构化解析与概念域比喻映射，为同一段代码同时生成技术版和小白版两份说明书，使不同知识背景的读者'
    '均能理解代码逻辑；（2）全自动文档生成：一键导出 7 页 PPT 演示文稿和 Word 数据报告，将文档制作'
    '时间从数十分钟压缩至秒级；（3）本地隐私优先：所有解析在浏览器本地完成，核心功能不依赖外部 AI '
    'API，用户代码绝不上传至任何服务器；（4）游戏化学习激励：内建 8 种成就徽章、连续解析天数统计、'
    '日历热力图等机制，促进持续学习行为。'
)

add_heading('1.3 系统功能概览', level=2)
add_para(
    '系统包含六大核心模块：仪表盘（解析统计、日历热力图、7 天趋势柱状图、复杂度排行榜）、说明书'
    '（代码输入后生成技术版 / 小白版 / 语义解释三标签页输出）、代码练习（对比评估、每日挑战、Pyodide '
    '在线运行）、历史记录（搜索筛选、分页浏览、批量勾选导出）、成就系统（8 种徽章含 4 种隐藏成就）、'
    'AI 文档（PPT 导出、Word 报告、TTS 讲解录屏辅助）。'
)

# ── 二、系统设计 ──
add_heading('二、系统设计', level=1)

add_heading('2.1 总体架构', level=2)
add_para(
    '系统采用纯前端单文件架构（Single Page Application），约 1480 行代码全部集中在一个 HTML 文件中，'
    '无需 npm 构建工具和后端服务器。架构自底向上分为三层：'
)
add_para(
    '数据持久层使用 localStorage 存储 appStats 全局状态对象，包含解析统计（总次数、Java/Python 分别'
    '计数、平均耗时）、模式排行（patternStats）、比喻命中统计（metaphorHits）、历史记录（最近 50 条，'
    '含代码摘要、语言、函数名、时间戳）和成就状态（badgeState）。选择 localStorage 而非 IndexedDB 的'
    '决策依据是：系统数据量小（< 50 KB），localStorage 的同步 API 更简洁，且 5 MB 上限对本场景绰绰'
    '有余。'
)
add_para(
    '业务逻辑层包含七大核心组件：（1）解析引擎（parseJava / parsePython），负责从原始代码文本中提取'
    '函数签名、参数列表、返回类型、依赖和异常处理信息；（2）比喻匹配器（matchMetaphorEntry），遍历 '
    '38 条概念域映射库并通过加权评分算法选出最佳比喻；（3）模式检测器（detectPatterns），基于正则匹配'
    '识别递归、排序、缓存等 12 种编程模式；（4）健康度评估器（calculateHealthScore），从五个维度计算 '
    '0-100 的代码质量评分；（5）PPT 生成器（generatePPTForCode），基于 PptxGenJS 生成 7 页专业演示'
    '文稿；（6）Word 导出器（exportWord），生成含周期筛选和统计图表的分析报告；（7）叙事生成器'
    '（renderTechDoc / renderBeginnerDoc / renderSemanticDoc），分别生成技术版、小白版和语义版说明书。'
)
add_para(
    '表现层包含仪表盘、说明书面板、代码练习、历史记录、成就系统、AI 文档六大面板，通过左侧固定侧边栏'
    '（260 px）进行导航切换。布局采用 CSS Grid 响应式方案：宽度 ≤ 1000 px 时双栏变单栏并隐藏侧边栏，'
    '≤ 900 px 时卡片和洞察区由 2 列变为 1 列。'
)

add_heading('2.2 关键设计决策', level=2)
add_para(
    '单文件架构 vs 框架方案：选择单文件而非 React / Vue 等现代框架，是基于教学场景的特殊需求——零部署'
    '成本（浏览器直接打开即可使用）、完全离线可用（除 CDN 引入的 Prism.js、html2canvas、PptxGenJS 和 '
    'JSZip 外，核心解析功能不依赖网络）、极简分发（单一文件便于通过 U 盘、邮件或局域网共享）。代价是'
    '代码可维护性和模块化程度降低，但在不超过 2000 行的规模下，这一代价可以接受。'
)
add_para(
    '正则解析 vs AST 解析：系统选择正则表达式而非抽象语法树（AST）进行代码解析。AST 方案（如 Esprima '
    'for Java 或 Python 的 ast 模块）能够处理完整的语法结构，但需要引入额外的解析器库（通常数十至数百 '
    'KB），且难以在纯浏览器环境中对 Java 代码进行 AST 构建。正则方案虽无法处理嵌套括号、泛型通配符等'
    '上下文有关语法，但对教学场景中常见的函数模式——含参 / 无参函数、基本类型标注、try-catch 结构'
    '——覆盖率达到 100%（见 5.1 节验证结果）。这一"够用即可"的工程设计原则，与本系统的教学辅助定位'
    '一致。'
)

# ── 三、核心算法设计 ──
add_heading('三、核心算法设计', level=1)

add_heading('3.1 正则分层解析算法', level=2)
add_para(
    '解析引擎从原始代码文本中提取结构化信息的流程分为四个步骤，Java 和 Python 版本共享相同的分层逻辑：'
)
add_para(
    '步骤一（预处理）：移除单行注释（// 和 #）、多行注释（/* */ 和三引号字符串），避免注释内容干扰'
    '后续正则匹配。步骤二（依赖提取）：Java 解析器提取全部 import 语句构建依赖列表；Python 解析器提取 '
    'import X / from X import Y 语句，同时识别 import 别名（import numpy as np）。步骤三（异常检测）：'
    'Java 解析器检测 try { 关键字标识 hasTryCatch；Python 解析器检测 try: 和 except 子句。步骤四'
    '（签名提取）：Java 使用正则 (\\w+\\s+)?(\\w+\\[\\])?\\s*(\\w+)\\s*\\(([^)]*)\\) 匹配方法签名，'
    '捕获返回类型、方法名和参数列表；Python 使用 def\\s+(\\w+)\\s*\\(([^)]*)\\)\\s*(->\\s*\\w+)?: '
    '匹配函数签名。参数列表进一步按逗号分割，每个参数解析为 {name, type} 对象——Python 支持 name: '
    'type 标注和 name = value 默认值，Java 支持 String[] args 数组参数。'
)

add_heading('3.2 概念域比喻匹配算法', level=2)
add_para(
    '比喻系统是本系统的核心创新。其理论基础源自 Lakoff 与 Johnson[2] 的概念隐喻理论（Conceptual '
    'Metaphor Theory），该理论认为隐喻不仅是文学修辞，更是人类认知抽象概念的基本思维机制——人们通过'
    '具体的、熟悉的身体经验来理解抽象的、陌生的概念域。张磊与田春子[8] 在程序设计教学研究中将计算机'
    '词汇隐喻归纳为三类——容器隐喻（内存比拟为容器）、控制隐喻（程序控制比拟为大脑决策）、工厂隐喻'
    '（执行过程比拟为流水线）——并指出合理使用隐喻能够有效降低学生的认知负荷。Harper 等人[3] 在 '
    'SIGCSE 2024 的研究进一步证实，概念隐喻在计算机科学教育中能够显著帮助学生理解递归、数据结构等'
    '抽象编程概念，但也指出师生之间的隐喻解读可能存在偏差，需要精心设计映射关系。'
)
add_para(
    '系统内置 38 条概念域映射条目，每条包含五个字段：关键词列表（触发匹配的词集合）、概念域名称（如'
    '"排序""过滤""递归"）、生活化比喻（如"整理扑克牌""筛面粉""俄罗斯套娃"）、动作描述'
    '（如"把杂乱变为有序"）、输入输出描述（如"乱序数据→有序结果"）。涵盖排序、过滤、映射、聚合、'
    '递归、读取、写入、查找、循环、条件判断、函数、类、列表、字典、异常处理、引入依赖、变量、字符串、'
    'API 调用、缓存、数据库、算法、回调、异步、加密、压缩、解析、校验、日志等 29 个常见编程概念。'
)
add_para(
    '比喻匹配采用加权评分算法，对每条比喻库条目计算综合得分。算法设计中的关键决策点包括：函数名'
    '关键词匹配赋予最高权重（+8 分），因为函数名通常是设计意图的最直接表达；概念词在函数名中出现'
    '赋予次高权重（+6 分），用于捕获同义词和近义概念；代码体关键词匹配根据词性区分权重——泛型关键词'
    '（if、for、return，几乎所有函数都会出现）权重仅为 1，领域关键词（sort、cache、api、socket）权重'
    '为 3，这一区分设计的目的是避免高频泛型词对匹配结果产生噪声干扰；模式交叉验证（+7 分）作为独立'
    '信号源，当 detectPatterns() 检测到的模式与比喻条目的概念词一致时进行加分，有效提升了匹配准确率。'
    '最终得分 ≥ 8 判定为 strong（高度匹配），1-7 分为 moderate（中度匹配），0 分触发通用兜底比喻'
    '（"这个函数就像一个可靠的助手，默默帮你处理数据"）。'
)

add_heading('3.3 多维度健康度评估模型', level=2)
add_para(
    '健康度评估从五个维度对代码质量进行 0-100 评分，其理论框架参考了 McCabe[4] 的圈复杂度度量——'
    '该度量指出模块的圈复杂度超过 10 时测试和维护成本显著上升——以及 Fowler[5] 在《Refactoring》中'
    '归纳的代码坏味（Code Smells）理论。五个维度的扣分规则如下：'
)
add_para(
    '参数数量（阈值 3）：函数参数超过 3 个后，每多 1 个扣 8 分。这一阈值参考了软件工程中"函数参数'
    '不宜超过 3-4 个"的共识——过多参数增加调用者的认知负担和传参出错的概率。代码行数采用分段递增'
    '扣分：10-25 行区间每 4 行扣 6 分，超过 25 行部分每 5 行扣 5 分。分段设计的原理是：短函数'
    '（≤ 10 行）通常职责单一易于理解；中等长度函数（10-25 行）扣分较缓，避免对合理长度的函数过度'
    '惩罚；长函数（> 25 行）加速扣分，反映其维护难度非线性增长。嵌套深度（阈值 2）和圈复杂度（阈值 '
    '3 个分支）分别控制代码的结构复杂度，每超过阈值一个单位扣 8 分和 5 分。线性冗余（无控制流且超过 '
    '8 行）：对于既无分支也无循环的纯直线代码，每 3 行扣 3 分——这类函数虽然简单，但过长的线性代码'
    '往往暗示可以抽取子函数或使用数据驱动方式重写。'
)
add_para(
    '评分采用截断累减模型：HealthScore = max(0, 100 - Σ各维度扣分)。最终得分 ≥ 80 分为绿色（健康），'
    '50-79 分为黄色（一般），< 50 分为红色（需优化）。健康度 ≤ 50 的历史记录自动进入"复杂度排行榜"'
    'Top 3，引导用户关注需要改进的代码。'
)

# ── 四、AI 协同开发实践 ──
add_heading('四、AI 协同开发实践', level=1)

add_heading('4.1 提示词设计策略', level=2)
add_para(
    '本项目的开发采用了人机协同（Human-AI Collaboration）的开发范式。Hamza 等人[6] 在 2024 年发表于 '
    'ACM IWSiB 的研究中，通过 22 位专业软件工程师与 ChatGPT 协作的实证实验，归纳出 AI 协同开发的五个'
    '关键主题：AI 作为对话式协作者而非简单工具、效率提升显著、人类监督不可或缺、明确的角色分工、以及'
    '提示词质量直接影响协作产出。本项目的实践经验与这些发现高度吻合。'
)
add_para(
    '在开发过程中，我总结出三种有效的提示词设计策略：（1）分层递进式提示——对复杂功能采用"粗框架→'
    '细实现→精打磨"三阶段策略，例如在实现比喻匹配功能时，第一层描述整体目标和数据流，第二层提供精确'
    '的评分公式和数据结构规格，第三层针对 UI 细节和边界情况给出精确修正指令；（2）约束前置式提示——'
    '在提示词开头明确列出技术约束（纯前端、不调外部 API、不 eval、单文件、仅 Java/Python），这些约束'
    '既是开发规范，也界定了 AI 的代码生成边界，实践证明约束前置远比问题出现后再修复高效；（3）示例驱动'
    '式提示——提供具体的输入-输出对（如"输入 def factorial(n): … → 预期输出：函数名 factorial，模式 '
    '递归，比喻 俄罗斯套娃"），帮助 AI 在缺乏全局项目上下文的情况下准确理解预期行为。'
)

add_heading('4.2 迭代与边界测试', level=2)
add_para(
    'AI 生成的代码在集成前需通过三层检查：语法检查（使用 node -e "new Function(…)" 快速检测 JS 语法'
    '错误）、功能测试（手动粘贴样例代码，对照预期解析结果）、边界测试（空输入、仅变量声明、复杂嵌套、'
    '匿名函数 / 箭头函数、类型标注缺失等边界情况）。以比喻匹配功能为例，其经历了三轮迭代：第一轮匹配'
    '逻辑仅依赖函数名关键词，对 compute()、process() 等通用函数名全部匹配失败；第二轮补充了代码体关键词'
    '扫描，但 if/for 等泛型词的噪声导致匹配结果偏离预期，遂引入"泛型词降权"机制（权重 ×1）；第三轮'
    '发现递归函数（如 factorial）虽然检测到递归模式，但比喻匹配到了其他概念域（如"计算"），于是增加'
    '模式交叉验证环节——当 detectPatterns() 检测到特定模式时，即使比喻条目评分最高不是该模式对应的条目，'
    '也在小白版说明书中补充对应的模式解释。这三轮迭代揭示了一个关键认知：AI 一次性生成复杂功能时往往'
    '有遗漏，但针对具体问题的修复指令能够快速收敛。'
)

# ── 五、实验与验证 ──
add_heading('五、实验与验证', level=1)

add_heading('5.1 功能测试', level=2)
add_para(
    '解析引擎测试选用 9 组代表性用例，覆盖含参函数（def add(a, b)）、递归函数（factorial）、排序算法'
    '（quick_sort）、无参函数、空输入、含 import 的 Java 方法、含类型标注和默认值的 Python 函数、含 '
    'try-catch 的方法、匿名函数。9 组用例全部通过，识别率达到 100%，证明正则方案对教学场景中常见的'
    '函数模式具有良好的覆盖率。比喻匹配测试中，bubble_sort → "排序（整理扑克牌）"、filter_even → '
    '"过滤（筛面粉）"、factorial → "递归（俄罗斯套娃）"的匹配质量均为 strong；compute(x) → 通用兜底'
    '比喻的 fallback 处理符合预期；validate_email → "校验（门卫大爷）"匹配为 strong。38 条概念域映射'
    '覆盖了教学场景中常见的编程概念。'
)

add_heading('5.2 用户反馈与性能', level=2)
add_para(
    '邀请 3 位计算机专业同学进行实际操作测试，每位同学解析 5 段不同代码（共 15 次解析），评价结果'
    '（5 分制）如下：解析速度 4.8 分，技术版说明书准确性 4.3 分，小白版比喻易懂程度 4.5 分，PPT 导出'
    '质量 4.6 分，整体使用体验 4.4 分。正面反馈集中于比喻的有趣性和 PPT 封面的设计感。负面反馈主要'
    '指向对多个函数定义仅识别第一个的限制。'
)
add_para(
    '性能方面，基于 Chrome 浏览器的 15 次解析统计：平均解析耗时 8.2 ms，单次 PPT 导出 1.3 s，Word '
    '报告生成 0.4 s，页面初始加载 0.9 s，localStorage 数据量 < 50 KB。这些指标表明纯前端方案在响应'
    '速度上具有明显优势。'
)

# ── 六、局限与展望 ──
add_heading('六、局限与展望', level=1)

add_heading('6.1 当前局限', level=2)
add_para(
    '（1）正则解析器无法处理复杂嵌套结构（如匿名内部类、装饰器链、泛型通配符），且输入含多个函数'
    '定义时仅识别第一个。（2）比喻库的 38 条映射虽覆盖常见编程概念，但对领域特定概念（如机器学习中的 '
    'train/predict、网络编程中的 socket/bind/listen）存在盲区。（3）健康度评分仅考虑结构维度，尚未纳入'
    '命名规范、注释质量、算法时间复杂度等维度。（4）PPT 模板的配色和布局为硬编码，用户无法自定义风格。'
    '（5）纯前端架构导致数据无法跨设备同步，不支持团队协作场景。'
)

add_heading('6.2 改进方向', level=2)
add_para(
    '（1）引入轻量级 AST 解析器（如 acorn for JS 语法子集），渐进式升级解析能力。（2）设计比喻库的'
    '"社区贡献"JSON 接口，允许用户提交新的概念域映射并合并至本地库。（3）将健康度评分扩展至命名规范'
    '检查（正则匹配驼峰 / 蛇形命名）、注释覆盖率（注释行 / 总行数）和算法复杂度推断（嵌套循环 → '
    'O(n²)，分治递归 → O(n log n)）。（4）设计 JSON 格式的 PPT 模板配置文件，支持自定义封面颜色、'
    '字体和页序排列。（5）在 Java/Python 基础上增加对 JavaScript、C/C++ 的语言支持。（6）在用户主动'
    '授权的前提下，探索基于 WebDAV 或 GitHub Gist 的轻量级云端同步方案。'
)

# ── 七、个人总结与反思 ──
add_heading('七、个人总结与反思', level=1)
add_para(
    '本项目的开发是我第一次系统性地实践"AI 协同编程"而非简单地"让 AI 写代码"。回顾整个开发过程，'
    '最深刻的体会可以归纳为以下四点。'
)
add_para(
    '第一，AI 是高效的执行者而非可靠的决策者。在具体函数的实现层面——比如编写一段正则表达式、生成一个 '
    'CSS 动画、组装 PptxGenJS 的幻灯片对象——AI 的速度和质量远超我手动编写的效率，通常几分钟就能产出'
    '可用的代码。但在需要全局视野和设计权衡的环节——比如 appStats 的数据结构设计（哪些字段需要持久化、'
    '嵌套层级多深）、比喻匹配的评分权重分配（函数名 vs 代码体 vs 模式交叉验证各占多少分）、三层架构的'
    '职责划分——AI 的表现并不理想。它在缺乏完整项目上下文时倾向于给出"看起来合理但实际无法融入现有架构"'
    '的方案。我逐渐学会了一个原则：凡是涉及"为什么这样设计而不是那样"的问题，自己思考后再动手；凡是'
    '"把这个明确的需求翻译成代码"的问题，交给 AI 并仔细审查结果。'
)
add_para(
    '第二，提示词的精确度决定了产出代码的可用度。项目初期，我习惯用模糊的自然语言描述需求——例如'
    '"写一个解析 Python 函数的函数"——结果往往是 AI 生成了一个看似功能齐全但数据结构与项目其他模块'
    '不兼容的实现。随着经验积累，我学会了在提示词中包含：精确的函数签名（输入类型、输出结构）、边界'
    '情况的处理策略（空输入返回什么、异常格式如何降级）、以及与其他模块的数据契约（返回对象必须包含'
    '哪些字段、字段名必须与 appStats 的 key 一致）。这种"写提示词就像写接口文档"的思维方式转变，是我'
    '在这个项目中收获的最宝贵的元技能。'
)
add_para(
    '第三，测试驱动的习惯在 AI 协同中更加重要。AI 生成的代码没有人类程序员的直觉和全局意识，边界情况'
    '的遗漏率远高于人工编写的代码。我在项目中期养成了一个习惯：每接受一段 AI 生成的函数，立即在浏览器'
    '控制台手动测试 3-5 个边界输入——空字符串、特殊字符、深层嵌套、多函数定义、语言切换等。这个习惯'
    '帮我发现了至少六七处仅靠阅读代码难以察觉的 bug，也让我意识到 AI 目前的"代码生成"能力远远领先于'
    '它的"代码验证"能力。'
)
add_para(
    '第四，关于纯前端架构的取舍，我在项目后期有了更深的体会。选择不依赖后端和不使用框架，在初期确实'
    '带来了极快的开发反馈循环——保存 HTML 文件、刷新浏览器、立即看到效果。但随着功能不断叠加（从最初'
    '的解析 + 说明书到后来增加了练习模式、历史管理、PPT 导出、成就系统），单一文件的维护难度开始显现：'
    '全局变量的数量膨胀、CSS 样式冲突、函数之间的隐式依赖增多。如果重新来过，我会在功能点达到约 10 个'
    '时进行一次重构——将核心解析逻辑拆分为独立的 JS 模块（ES Module），即使仍然是纯前端方案，模块化'
    '也会显著降低维护成本。这个教训让我深刻理解了软件工程中"技术债"概念的具象含义——不是架构选错了，'
    '而是在项目演进中没有及时调整架构以适应新的复杂度。'
)
add_para(
    '金芝等人[7] 在《软件学报》的综述中指出，随着软件系统的日益复杂，自动化程序理解正从传统的人工分析'
    '向智能化的自认知方向演进。这与我在本项目中观察到的现象一致——即使是最简单的正则解析，也能在特定'
    '场景下（教学代码、常见函数模式）取得良好的实用效果。程序理解的研究前沿提醒我，本系统目前的正则'
    '方案虽然"够用"，但未来的改进空间在于引入更深层的语义分析能力，而非停留在表层模式匹配。在后续迭代'
    '中，我更希望将精力投入到比喻库的扩展和解析精度的提升上，而非堆砌更多仪表板装饰。'
)
add_para(
    '总的来说，这个项目让我完成了从一个"会用 AI 写代码的学生"到一个"能判断何时信任 AI、何时亲自动手'
    '的开发者"的转变。我学会了用精确的规格约束 AI 的输出边界，用持续的测试弥补 AI 的盲区，以及在项目'
    '演进的每个关键节点反思架构决策。我相信，"能够与 AI 有效协作"将是未来程序员的一项基础能力，而不仅仅'
    '是一项加分项。'
)

# ── 参考文献 ──
add_heading('参考文献', level=1)

refs = [
    '[1] Von Mayrhauser A, Vans A M. Program Comprehension During Software Maintenance and Evolution[J]. '
    'IEEE Computer, 1995, 28(8): 44-55. DOI: 10.1109/2.402076',

    '[2] Lakoff G, Johnson M. Metaphors We Live By[M]. Chicago: University of Chicago Press, 1980.',

    '[3] Harper C, Tran K, Cooper S. Conceptual Metaphor Theory in Action: Insights into Student '
    'Understanding of Computing Concepts[C]// Proceedings of the 55th ACM Technical Symposium on Computer '
    'Science Education (SIGCSE 2024). ACM, 2024: 463-469. DOI: 10.1145/3626252.3630812',

    '[4] McCabe T J. A Complexity Measure[J]. IEEE Transactions on Software Engineering, 1976, '
    'SE-2(4): 308-320. DOI: 10.1109/TSE.1976.233837',

    '[5] Fowler M. Refactoring: Improving the Design of Existing Code[M]. 2nd ed. Boston: '
    'Addison-Wesley, 2018.',

    '[6] Hamza M, Siemon D, Akbar M A, et al. Human-AI Collaboration in Software Engineering: '
    'Lessons Learned from a Hands-On Workshop[C]// Proceedings of the 7th ACM/IEEE International '
    'Workshop on Software-intensive Business (IWSiB 2024). ACM, 2024: 7-14. '
    'DOI: 10.1145/3643690.3648236',

    '[7] 金芝, 刘芳, 李戈. 程序理解:现状与未来[J]. 软件学报, 2019, 30(1): 110-126. '
    'DOI: 10.13328/j.cnki.jos.005643',

    '[8] 张磊, 田春子. 程序设计课程中的计算机专业词汇隐喻应用[J]. 电子技术, 2022, 51(1).',
]

for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(ref)
    set_run_font(run, cn_font='宋体', en_font='Times New Roman', size=Pt(10.5))

# ── 声明 ──
doc.add_paragraph()
add_para(
    '本论文由庞凯匀独立完成。AI（Claude / DeepSeek）作为编程助手参与了系统代码的开发，'
    '论文内容由作者撰写并审核。',
    indent=False, font_size=10.5
)

# ── 保存 ──
output_path = r'c:\Users\16137\Desktop\vb期末\小论文_230152061_庞凯匀.docx'
doc.save(output_path)
print(f'✅ 论文已保存至: {output_path}')
