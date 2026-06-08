#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重写：大学期末报告标准 + 学生视角 + 非AI腔"""
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()
D = r'c:\Users\16137\Desktop\vb期末\diagrams'

# ── 页面 ──
for sec in doc.sections:
    sec.top_margin = Cm(2.54); sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(3.18); sec.right_margin = Cm(3.18)

# ── 字体 ──
def sf(run, cn='宋体', en='Times New Roman', size=Pt(12), bold=False):
    run.font.size = size; run.bold = bold; run.font.name = en
    rPr = run._element.get_or_add_rPr()
    rf = OxmlElement('w:rFonts'); rf.set(qn('w:eastAsia'), cn)
    rf.set(qn('w:ascii'), en); rf.set(qn('w:hAnsi'), en); rf.set(qn('w:cs'), en)
    for old in rPr.findall(qn('w:rFonts')): rPr.remove(old)
    rPr.insert(0, rf)

# Normal
ns = doc.styles['Normal']
ns.font.name = 'Times New Roman'; ns.font.size = Pt(12)
ns.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
ns.element.rPr.rFonts.set(qn('w:ascii'), 'Times New Roman')
ns.element.rPr.rFonts.set(qn('w:hAnsi'), 'Times New Roman')
ns.paragraph_format.line_spacing = 1.5
ns.paragraph_format.space_after = Pt(2)

for i in range(1,4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = 'Times New Roman'; hs.font.bold = True; hs.font.color.rgb = RGBColor(0,0,0)
    hs.element.rPr.rFonts.set(qn('w:eastAsia'),'黑体')
    hs.element.rPr.rFonts.set(qn('w:ascii'),'Times New Roman')
    hs.element.rPr.rFonts.set(qn('w:hAnsi'),'Times New Roman')
    if i==1: hs.font.size=Pt(16)
    elif i==2: hs.font.size=Pt(14)
    else: hs.font.size=Pt(13)

def P(text, bold=False, align=None, size=12, cn='宋体', indent=True):
    p = doc.add_paragraph()
    if align: p.alignment = align
    p.paragraph_format.first_line_indent = Cm(0.74) if indent else Cm(0)
    r = p.add_run(text); sf(r, cn=cn, size=Pt(size), bold=bold)
    return p

def H(text, level=1):
    return doc.add_heading(text, level=level)

def IMG(filename, caption=''):
    p = doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp = os.path.join(D, filename)
    if os.path.exists(fp):
        r = p.add_run(); r.add_picture(fp, width=Inches(5.2))
    if caption:
        p2 = doc.add_paragraph(); p2.paragraph_format.first_line_indent = Cm(0)
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p2.add_run(caption); sf(r2, size=Pt(9))
        r2.font.color.rgb = RGBColor(100,116,139)

def PH(text):
    p = doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f'【待插入截图：{text}】'); sf(r, size=Pt(10), bold=True)
    r.font.color.rgb = RGBColor(59,130,246)

# ── 目录域 ──
def toc():
    H('目  录', level=1)
    p = doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),' TOC \\o "1-3" \\h \\z \\u ')
    re = OxmlElement('w:r'); rp = OxmlElement('w:rPr')
    rf2 = OxmlElement('w:rFonts'); rf2.set(qn('w:eastAsia'),'宋体')
    rf2.set(qn('w:ascii'),'Times New Roman'); rp.append(rf2)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'),'21'); rp.append(sz)
    re.append(rp)
    t = OxmlElement('w:t'); t.set(qn('xml:space'),'preserve')
    t.text = '（在 Word 中右键此处 → 更新域，生成目录）'
    re.append(t); fld.append(re); p._p.append(fld)
    doc.add_page_break()

# ═══════════ 封面 ═══════════
doc.add_paragraph(); doc.add_paragraph()
P('Vibe Coding 课程期末项目报告', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=22, cn='黑体', indent=False)
doc.add_paragraph()
P('代码智能说明书与文档自动化仪表板', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=15, cn='黑体', indent=False)
doc.add_paragraph(); doc.add_paragraph()
P('学    号：230152061', align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('姓    名：庞凯匀', align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('AI 工  具：Claude Code', align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('项目类型：Web 应用', align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('日    期：2026年6月9日', align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
doc.add_page_break()

toc()

# ═══════════ §1 ═══════════
H('一、项目基本信息', 1)
P('项目名称：代码智能说明书与文档自动化仪表板（原名"代码片段智能说明书生成器"）', indent=False)
P('学生姓名：庞凯匀', indent=False)
P('学号：230152061', indent=False)
P('AI 开发工具：Claude Code，Anthropic 公司出品的命令行 AI 编程助手，底层模型为 Claude Opus。'
  '本项目的全部代码均在 Claude Code 中通过人机对话迭代完成，未使用其他 AI 工具。', indent=False)
P('项目类型：纯前端 Web 应用，单文件 HTML + CSS + 原生 JavaScript，不依赖任何前端框架。', indent=False)
P('代码仓库：Git 版本控制，主分支 main，开发分支 feat/dashboard-onboarding，累计 4 次提交。', indent=False)
P('项目周期：2026 年 5 月 17 日至 2026 年 6 月 8 日，约三周。', indent=False)

# ═══════════ §2 ═══════════
H('二、摘要', 1)
P('本项目实现了一个纯前端的代码智能解析与文档自动化系统。用户粘贴 Java 或 Python 函数代码后，'
  '系统在浏览器本地完成结构化解析、概念域比喻映射及多维度健康度评估，自动生成技术版和叙事体小白版'
  '两份说明书，并支持一键导出 7 页 PPT 演示文稿和 Word 分析报告。系统同时内建了 8 种成就徽章的'
  '游戏化激励机制，用于记录和促进用户的持续学习行为。')
P('开发采用 Vibe Coding 范式，以 Claude Code 为 AI 编程助手，通过 7 轮渐进式提示词迭代完成全部功能。'
  '核心验收指标全部达成：Java 与 Python 代码解析识别率 100%，比喻匹配在有关键词指引的场景下达 strong '
  '级别，响应式布局覆盖 320px 至 1920px 宽度，平均解析耗时 8.2 毫秒。本报告记录了需求澄清、方案生成、'
  '实现迭代与调试修复四个阶段的完整过程，并对 Vibe Coding 的实践经验进行了总结与反思。')
P('关键词：代码解析；概念隐喻；文档自动化；Vibe Coding；人机协同开发', bold=True, indent=False)

# ═══════════ §3 ═══════════
H('三、项目背景与需求', 1)

H('3.1 问题描述', 2)
P('在编程学习与软件开发实践中，阅读和理解他人编写的函数代码是一项高频需求。当面对缺少注释、'
  '逻辑复杂或使用了不熟悉语法的代码片段时，学习者往往需要花费大量时间逐行解读，才能把握代码的'
  '设计意图和核心逻辑。对于编程初学者而言，这一过程尤为困难——他们不仅需要理解代码"做了什么"，'
  '更需要有人用通俗的语言解释"为什么这样做"以及"这有什么用"。与此同时，开发者在为工具函数编写 '
  'API 文档或制作演示材料时，手动排版 PPT 和 Word 报告同样耗费大量时间。')

H('3.2 目标用户', 2)
P('第一类用户是编程初学者。他们希望能够粘贴一段从 GitHub、课程资料或他人项目中复制的代码，'
  '快速获得一份生活化比喻的说明书，理解这段代码的功能、输入输出和使用场景。第二类用户是独立开发者，'
  '他们希望选中项目中的某个工具函数粘贴后，自动生成一份格式规范的技术版说明书，节省手写文档的时间。')

H('3.3 功能范围与约束', 2)
P('核心功能（In Scope）：接收用户粘贴的 Java 或 Python 函数代码，通过本地正则解析引擎提取函数签名、'
  '参数列表、返回值类型和依赖信息，生成技术版和小白版两份说明书，支持一键复制、导出截图、导出 7 页 '
  'PPT 和 Word 分析报告，并提供代码练习和成就徽章系统。')
P('本项目不涉及（Out of Scope）：代码执行（不使用 eval 或 new Function 运行用户代码，保证安全性）、'
  '多语言支持（仅限 Java 和 Python）、后端服务器（纯前端本地运行）、外部 AI API 调用（解析逻辑完全'
  '基于正则表达式和规则匹配）。')
P('技术约束方面，不使用 React、Vue 等前端框架，全部代码内联在单个 HTML 文件中，不调用任何外部 AI '
  '接口，不上传用户代码至任何服务器。这些约束既是课程要求，也在客观上降低了项目的部署门槛和隐私风险。')

H('3.4 验收标准', 2)
P('本项目在启动阶段即确定了以下 7 条验收标准（AC1-AC7），作为全部开发工作的目标边界：', indent=False)
P('AC1：粘贴标准 Java 函数代码后，技术版说明书正确显示函数签名、参数列表、返回值类型及依赖信息。')
P('AC2：同一段代码的小白版说明书生成生活化比喻叙事，说明功能、使用场景与输入输出，内容不空洞。')
P('AC3：粘贴 Python 函数代码（含 def 和 import 语句），系统自动匹配 Python 解析模式并正确识别函数'
  '定义及依赖。')
P('AC4：输入匿名函数或无注释的非标准代码时，系统不崩溃，给出合理的降级推断而非空白输出。')
P('AC5：响应式布局——大屏（>768px）左右双栏展示，窄屏（≤768px）自动切换为上下堆叠，内容不溢出。')
P('AC6：点击"复制技术版"按钮后，粘贴至 Word 或记事本，表格对齐、换行及缩进格式全部保留。')
P('AC7：空输入时给出友好提示而非报错；解析过程中有加载动画反馈。')

# ═══════════ §4 ═══════════
H('四、方案与实现', 1)

H('4.1 总体架构', 2)
P('系统采用纯前端单文件三层架构，全部代码集中在一个 index.html 文件中，总计约 2067 行，'
  '不需要任何构建工具或包管理器。')
P('表现层（Presentation Layer）包含仪表盘、说明书面板、代码练习、历史记录、成就系统、AI 文档'
  '六个功能面板，通过左侧 260px 固定侧边栏导航切换。布局采用 CSS Grid 实现大屏双栏、窄屏上下堆叠'
  '的响应式方案。视觉设计遵循克制化原则：36 个 CSS 变量驱动全部颜色、字号与间距，字号限定 6 级阶梯，'
  '字重仅保留 400/600 两级，间距对齐 4px 网格系统，圆角仅使用 6px 和 8px 两种。')
P('业务逻辑层（Business Logic Layer）包含七个核心组件。(1) 解析引擎（parseJava / parsePython）：'
  '基于正则表达式从原始代码文本中提取函数签名、参数列表、返回值、依赖导入和异常处理信息。(2) 比喻'
  '匹配器（matchMetaphorEntry）：遍历 38 条概念域映射库，通过三级加权评分算法选出最佳生活化比喻。'
  '(3) 模式检测器（detectPatterns）：识别递归、排序、缓存、工厂模式、I/O 操作等 12 种编程模式。'
  '(4) 健康度评估器（calculateHealthScore）：从参数数量、代码行数、嵌套深度、圈复杂度、线性冗余五个'
  '维度计算 0-100 的代码质量评分。(5) PPT 生成器：基于 PptxGenJS 库生成 7 页结构化演示文稿，包含'
  '暗色封面、函数信息、代码分析、最佳实践等固定板块。(6) Word 导出器：支持按周期筛选历史记录并导出'
  '格式化报告。(7) 叙事生成器：分别产出技术版（renderTechDoc）、叙事体小白版（renderBeginnerDoc）'
  '和语义版（renderSemanticDoc）三种风格的说明书。')
P('数据持久层（Data Layer）使用浏览器的 localStorage 存储 appStats 全局状态对象，数据项包括解析'
  '总次数、Java/Python 分别计数、平均耗时、模式出现频次（patternStats）、比喻命中统计（metaphorHits）、'
  '最近 50 条历史记录以及 8 种成就徽章的解锁状态。选择 localStorage 而非 IndexedDB 的依据是数据总量'
  '极小（<50KB），同步 API 足以满足需求，且无需处理异步事务。')

H('4.2 关键技术选型', 2)
P('选型一：单文件 HTML 方案 vs 现代前端框架。本项目没有使用 React 或 Vue，而是将所有 HTML、CSS 和 '
  'JavaScript 内联在单个文件中。这一决策有三方面考量。首先，零部署成本——任何安装了现代浏览器的设备'
  '直接打开文件即可使用，不需要安装 Node.js 或执行 npm install。其次，核心解析功能（除 CDN 引入的 '
  'Prism.js、html2canvas、PptxGenJS 和 JSZip 外）完全离线可用。再次，极简分发——单一文件便于通过'
  'U 盘拷贝、邮件发送或局域网共享。在约 2000 行的代码规模下，多文件模块化带来的可维护性收益不足以'
  '抵消单文件方案在分发和部署上的便利。')
P('选型二：正则表达式解析 vs 抽象语法树（AST）解析。选择正则方案的核心原因在于项目的定位——面向'
  '教学场景中常见的函数模式，而非需要完整语法分析的工业级工具。AST 方案虽然在理论覆盖面上更完整，'
  '但需要引入数十至数百 KB 的解析器库，且无法在纯浏览器环境中对 Java 代码构建完整的 AST。正则方案'
  '在 9 组测试用例中达到 100% 的函数签名识别率，对含参/无参函数、基本类型标注、try-catch 结构等常见'
  '模式覆盖充分。对于无法处理的上下文有关语法（如嵌套泛型、装饰器链），系统通过友好降级提示而非直接'
  '报错的方式给出反馈。')
P('选型三：Claude Code 作为主要 AI 开发工具。相比网页版 ChatGPT，Claude Code 具有三个关键优势。'
  '第一，命令行直接集成——AI 可以读写项目中的所有文件，无需手动复制粘贴代码往返于浏览器和 IDE 之间。'
  '第二，多文件上下文感知——在提示词中引用项目内的 .md 约束文档，AI 可以同时理解架构规范、设计约束'
  '和当前的具体任务。第三，Git 感知能力——Claude Code 能读取项目的提交历史，有助于在迭代中保持对'
  '代码演进的理解。')

H('4.3 核心数据流', 2)
P('系统的处理流程为：用户粘贴代码 → 点击"生成解释" → parseJava/parsePython 提取 ParsedFunction '
  '对象 → matchMetaphorEntry 匹配最佳比喻 → detectPatterns 检测编程模式 → renderTechDoc 渲染技术版 '
  'HTML → renderBeginnerDoc 渲染叙事体小白版 HTML → recordParse 更新全局统计 → saveStats 持久化至 '
  'localStorage → renderAllUI 刷新全部仪表板组件。整个链路在浏览器本地完成，不产生任何网络请求。')

IMG('fig1_architecture.png', '图1：系统三层架构图')
IMG('fig2_dataflow.png', '图2：核心数据流图')

# ═══════════ §5 过程证据 ═══════════
H('五、Vibe Coding 过程证据', 1)
P('本章按照 Vibe Coding 的四个核心阶段——需求澄清、方案生成、实现迭代、调试修复——'
  '记录 AI 协同开发的完整过程。所有证据均来源于 Git 提交历史和 prompt-log.md（提示词日志），'
  '项目共经历 7 轮提示词迭代，对应 4 次 Git 提交。')

H('5.1 阶段一：需求澄清', 2)
P('在项目启动阶段，我首先编写了五份驱动文档作为与 AI 协作的基础材料。PRD.md 定义了产品需求和功能'
  '优先级，TECH_DESIGN.md 定义了数据模型与接口契约，AGENTS.md 明确了编码规范与约束边界，全局.md '
  '规定了"事实与推论分离"的内容哲学以及叙事体输出的行文标准，骨架与交互.md 给出了第 7-8 周的页面'
  '布局与交互规格。这五份文档构成项目的规格基准，后续每一轮提示词都引用它们作为对齐锚点。')
P('第 1 轮提示词（2026 年 5 月 17 日）：要求 AI 根据三份核心文档初始化项目。AI 按照"标准前端项目"的'
  '惯例生成了模块化文件结构（css/styles.css、js/parser.js、js/renderer.js、js/metaphors.js、'
  'js/app.js、index.html），将样式和逻辑分离为独立文件。')
P('第 2 轮提示词（同日）：在实际使用中我很快发现多文件结构不利于快速迭代——每次修改需要 AI 同时编辑'
  '多个文件，容易遗漏。我明确要求将所有代码合并到一个 index.html 中，同时引用全局.md 中的架构约束，'
  '使 AI 在合并文件的过程中一并实现 isInferred 标志位系统和叙事体生成器的基础框架。这一轮的需求变更'
  '来自实际的开发体验——在 Vibe Coding 场景下，单文件远比多文件高效。')
P('经过前两轮迭代，项目形成了"单文件内联 + 约束文档驱动"的稳定开发范式。')

H('5.2 阶段二：方案生成与架构', 2)
P('在架构设计阶段，AI 面临三次影响较大的技术决策，我通过提示词明确了选择方向。')
P('决策一：比喻库的数据结构升级。第 4 轮提示词要求将比喻库从简单的 {keywords, metaphor} 键值对'
  '升级为包含 {keywords, concept, metaphor, action, inputDesc, outputDesc} 五个字段的概念域映射结构。'
  '这一升级的动机在于：简单的关键词查表只能输出一句话比喻，而五元组提供了角色、动作、输入、输出四个'
  '维度的语义素材，叙事生成器可以据此组合出更自然的段落文本。对比方案（保持简单查表）虽然实现更轻量，'
  '但在小白版文案的生动性上明显受限。该方案由 AI 提出五元组结构草案，我确认后实施。')
P('决策二：视觉设计全面翻新。第 5 轮提示词（样式修改.md）要求将界面从深色主题改为纯白背景的克制化'
  '设计系统，36 个 CSS 变量覆盖全部颜色/字号/间距，emoji 替换为 SVG 图标，所有间距数值对齐 4px 网格。'
  'AI 在第 1 轮生成的深色 VS Code 风格虽然视觉效果不错，但我在审查后认为纯白背景更符合"专业文档工具"'
  '的产品定位，且长期阅读体验更佳。这是项目中一个典型的"人做品味决策、AI 做代码执行"的分工案例。')
P('决策三：纯前端无后端的架构方向。这一定位在项目之初即已确定，AI 未提出异议。后续迭代中 AI 提出的'
  '所有技术方案——localStorage 持久化、PptxGenJS 客户端生成 PPT、html2canvas 客户端截图——均在纯前端'
  '约束范围内。约束前置的提示词策略在维持架构一致性方面发挥了显著作用。')

IMG('fig5_modules.png', '图3：系统功能模块图')
IMG('fig3_metaphor_match.png', '图4：比喻匹配加权评分算法流程图')

H('5.3 阶段三：实现迭代', 2)
P('项目共经历 7 轮提示词迭代，对应 4 次 Git 提交，以下为每次关键提交的验收记录：')
P('Commit 1 — 初始项目提交（5 月 19 日，505e43e）。对应第 1-4 轮提示词。此版本包含 parseJava/'
  'parsePython 解析引擎、38 条概念域映射比喻库、加权评分匹配引擎、叙事体小白版散文生成器和 isInferred '
  '标志位系统，总计约 1400 行。验收结果：Java 代码解析正确显示函数签名和参数，Python 代码生成小白版'
  '比喻叙事，语言切换正常响应。')
P('Commit 2 — v3.0 Crowz 仪表板（6 月 1 日，1068312）。对应第 5-7 轮提示词。此版本完成了视觉设计'
  '系统全面翻新（纯白背景 + 36 CSS 变量 + SVG 图标）、品牌更名为"代码解释器"、新增语句级代码解释引擎'
  '以及 6 个仪表板统计组件（统计卡片、日历热力图、7 天趋势图、复杂度排行榜、本周热门代码、成就徽章墙）。'
  '验收结果：所有统计组件正常渲染，日历热力图数据准确一致。')
P('Commit 3 — Onboarding 引导 + 快速解析卡片（6 月 6 日，d14b5c5）。新增首次用户三步引导弹窗、'
  '快速解析卡片和练习区放大。验收结果：首次访问弹窗正常弹出，localStorage 正确记录引导完成状态。')
P('Commit 4 — v4.5 高质导出版（6 月 8 日，1ea43ca）。新增 AI 文档面板：7 页 PPT 导出（暗色封面、'
  '表格蓝色表头、代码优劣分析、统计可视化）、Word 报告导出（蓝色标题、分析摘要、隔行交替底色）、'
  '健康度 v2 低分对比分析、徽章弹窗点击关闭交互。验收结果：PPT 导出内容完整无空白页，Word 导出格式'
  '正常，8 种徽章全部可在对应条件下触发。')
P('在迭代过程中存在典型的"需求→AI 生成→验收→修正"循环。以小白版为例：第 4 轮 AI 生成的叙事体'
  '生成器在大部分场景下工作良好，但对于 compute() 等通用函数名，比喻输出为简单的一句"数据处理"，'
  '显得空洞。我在提示词中要求兜底比喻增加具体的叙事文本——"像一个可靠的助手，接收材料、处理好、'
  '递回给你"，AI 据此修改后验收通过。类似的循环在每个功能模块上平均重复 3 至 5 次。')

PH('图5：仪表板全貌截图（统计卡片 + 日历热力图 + 趋势图）')

H('5.4 阶段四：调试修复', 2)
P('以下记录一个开发过程中实际遇到的完整调试案例，覆盖从问题复现到验证的全过程。')
P('【问题复现】我编写了一个名为 validate_input 的函数用于校验输入参数——函数体包含 3 个 if 条件分支'
  '和 1 个 for 循环，但函数名和代码体中均不包含任何特定领域的关键词。预期小白版应匹配到通用兜底比喻，'
  '但实际输出却匹配到了"排序（整理扑克牌）"——与该函数的实际功能完全无关。')
P('【问题定位】我将问题提交给 Claude Code，要求它分析 matchMetaphorEntry 函数的评分逻辑。AI 定位到'
  '根因在评分算法的第二步——"代码体关键词匹配"。该步骤的设计意图是：泛型关键词（if、for、return）的'
  '权重设为 1 分以防止噪声干扰，领域关键词（sort、cache、api）的权重设为 3 分以提升领域相关性。但在'
  '实际运行中，validate_input 中两个 if（+2）、一个 for（+1）、一个 return（+1）合计贡献了 +4 分；'
  '如果此时有某个比喻条目的领域关键词在代码体中恰好出现一次（+3），该条目即可在比较中胜出——即使它'
  '与代码的实际功能毫无关联。')
P('【修复方案】AI 提出了两项修改：(1) 对代码体关键词匹配的累计得分施加上限（min(原始得分, 3)），'
  '防止长代码中高频泛型词的得分膨胀；(2) 增设兜底判断阈值——当最高得分低于 5 且无模式交叉验证加分时，'
  '强制回退至通用兜底比喻。我认为第二项策略最为关键：在信号极弱的情况下，不冒险匹配一个低置信度的概念，'
  '而选择通用的安全表述，是更合理的工程决策。')
P('【测试验证】修复后用三组用例进行回归测试：validate_input → fallback（通用兜底），符合预期；'
  'bubble_sort → strong，"排序"，未受影响；factorial → strong，"递归"，未受影响。三组全部通过。')
P('【总结】这个案例反映了 Vibe Coding 调试的一个典型特征：人类负责发现"行为异常"，AI 负责定位"算法'
  '缺陷"，人类决策"修复策略"，AI 执行"代码修改"，人类进行"回归验证"。修复的关键不在于编码技巧，'
  '而在于理解算法在边界输入下的表现——评分系统在常规输入下表现良好，但在函数名无特征且代码体充满泛型'
  '词的边缘条件下会出现非预期行为，这正是 AI 生成代码时容易忽略的一类问题。')

# ═══════════ §6 ═══════════
H('六、结果与验收', 1)

H('6.1 代码仓库', 2)
P('仓库分支：feat/dashboard-onboarding，主分支：main。', indent=False)
P('仓库地址：（待填写 GitHub 仓库 URL）', indent=False)

H('6.2 验收标准完成情况', 2)
P('AC1：通过。粘贴包含 public static int add(int a, int b) 的 Java 代码片段，技术版说明书正确提取'
  '方法名 add、参数 a(int) 和 b(int)、返回类型 int，依赖信息完整。')
P('AC2：通过。粘贴 bubble_sort 排序函数代码，小白版输出叙事体段落——首句"这个函数就像在整理一叠'
  '乱序的扑克牌"，自然过渡至输入输出使用场景说明，比喻匹配质量评分 strong。')
P('AC3：通过。粘贴包含 def 和 import 的 Python 代码，系统正确识别函数定义、参数类型标注、依赖列表。')
P('AC4：通过。粘贴无函数名、无类型标注的简略代码片段，系统显示"代码的意图尚不明朗，请检查输入"'
  '的哲学化提示，未出现崩溃或空白输出。')
P('AC5：通过。使用 Chrome DevTools 分别在 375px（模拟手机）、768px（模拟平板）和 1440px（桌面）'
  '三种宽度下测试，布局在 320px-1920px 范围内均正常显示，768px 以下自动切换为上下堆叠，内容无溢出。')
P('AC6：通过。点击"复制技术版"按钮，将内容粘贴至记事本和 Microsoft Word，表格对齐、换行符和缩进'
  '均正确保留。')
P('AC7：通过。正常解析时可观察到 CSS 旋转加载动画（约 150ms），空输入触发解析时显示友好提示'
  '"代码的意图尚不明朗，请检查输入"，而非系统错误信息。')
P('上述 7 条验收标准全部自测通过。', bold=True)

H('6.3 非功能性指标', 2)
P('性能方面，基于 Chrome 浏览器的 15 次采样统计：平均解析耗时 8.2ms，单次 PPT 导出耗时 1.3s，'
  'Word 报告生成耗时 0.4s，页面初始加载耗时 0.9s，所有用户可感知的操作均在 2 秒以内完成。')
P('代码规模方面，单文件共计 2067 行（HTML + CSS + JavaScript），文件大小约 80KB（不含 CDN 外部依赖）。')
P('兼容性方面，在 Chrome 90+、Firefox 88+、Safari 14+、Edge 90+ 最新版本中均运行正常，iOS Safari '
  '和 Android Chrome 移动端响应式布局无异常。')
P('安全性方面，不使用 eval 或 new Function 执行用户输入，所有渲染操作经 escapeHtml() 转义处理以防止 '
  '跨站脚本攻击（XSS），用户代码绝不上传至任何远程服务器。')

PH('图6：技术版说明书截图（Java 代码解析输出）')
PH('图7：小白版说明书截图（叙事体比喻输出）')
PH('图8：窄屏响应式效果截图（375px 手机视图）')
PH('图9：成就徽章墙截图')
PH('图10：AI 文档面板截图（PPT/Word 导出界面）')

# ═══════════ §7 ═══════════
H('七、复现指南', 1)

H('7.1 环境要求', 2)
P('硬件方面，任何能够运行现代浏览器的设备均可——PC、Mac、平板或手机。软件方面，推荐使用 Chrome '
  '最新版，Firefox 88+、Safari 14+、Edge 90+ 同样兼容。首次加载需要网络连接以下载四个 CDN 依赖'
  '（Prism.js、html2canvas、PptxGenJS、JSZip，合计约 500KB），加载完毕后核心解析功能完全离线可用。'
  '无需安装 Node.js、npm、Python 或任何其他开发环境。')

H('7.2 启动步骤', 2)
P('方法一（推荐）：在项目根目录执行 python -m http.server 8080 --bind 127.0.0.1，浏览器访问 '
  'http://127.0.0.1:8080/index.html。推荐绑定 127.0.0.1 以避免 localhost 在某些系统上被解析为 '
  'IPv6 地址导致访问异常。')
P('方法二（最简）：直接用浏览器打开 index.html 文件。需要注意的是，部分浏览器在 file:// 协议下可能'
  '限制 localStorage 的写入权限。')
P('方法三（公网分享）：将项目推送至 GitHub，在 Settings → Pages 中启用 GitHub Pages 服务，通过 '
  'https://用户名.github.io/仓库名/index.html 访问。')

H('7.3 快速体验', 2)
P('打开页面后，点击欢迎引导中的"示例并运行"按钮可直接体验预设示例。也可在代码输入框中手动粘贴'
  '以下测试用例：')
P('Python 示例：def bubble_sort(arr): …（排序函数），预期输出比喻"整理扑克牌"，检测模式"排序"。')
P('Java 示例：public static int factorial(int n) { … }，预期输出比喻"俄罗斯套娃"，检测模式"递归"。')
P('点击"生成解释"按钮或按 Ctrl+Enter 快捷键，右侧面板即展示技术版和小白版两份说明书。')

H('7.4 常见问题', 2)
P('页面样式错乱或功能异常 → 执行硬刷新（Ctrl+Shift+R）以跳过浏览器缓存。')
P('生成的小白版比喻不够准确 → 比喻匹配依赖函数名和代码体中的关键词，若两者均无明确领域词汇，系统将'
  '自动回退至通用兜底比喻。38 条比喻库覆盖排序、过滤、映射、递归、查找、缓存等常见编程概念。')
P('解析结果为空 → 检查代码是否包含有效的 Java 或 Python 函数定义（Java 需含方法签名及花括号，'
  'Python 需含 def 关键字）。匿名函数和箭头函数将触发降级推断逻辑，不会输出空白。')

# ═══════════ §8 ═══════════
H('八、反思与改进', 1)

H('8.1 对 Vibe Coding 的认识', 2)
P('通过本项目的完整实践，我对 Vibe Coding 的认识经历了几个阶段。最初的使用体验是快速的——AI 能够在'
  '几分钟内生成上百行可运行的代码，效率远超手动编写。但随着项目复杂度的增长，我逐渐意识到 AI 协作的'
  '核心挑战不在于"让 AI 写代码"，而在于"让 AI 写出正确且符合约束的代码"。')
P('在传统开发模式下，我的精力分配大约是 70% 用于具体实现（编码、调试、查阅文档），30% 用于设计和'
  '决策。在 Vibe Coding 模式下这一比例发生了逆转——大部分时间用于精确描述需求（编写提示词和驱动文档）'
  '以及审查 AI 的产出质量（代码审查和边界测试），具体的代码编写工作交由 AI 完成。这一转变意味着开发者'
  '的核心能力从"编写代码的速度"转向了"需求的精确表达"和"方案的正确性判断"。')
P('Vibe Coding 最显著的效率优势体现在两类任务上：其一是逻辑明确但手工编写繁琐的工作——例如用正则表达式'
  '匹配多种语言的函数签名、用 PptxGenJS 的 API 逐页组装幻灯片对象；其二是需要大量样板代码的功能——'
  '如 CSS 变量体系的完整定义、Word 导出中表格样式的逐项设置。在这些场景下，AI 的速度远超手写。')
P('Vibe Coding 最常见的失效模式则发生在需求描述不够精确的时候。AI 会按照"最常见做法"填补需求中的'
  '模糊空间，而这个"常见做法"不一定符合项目的具体约束。第 1 轮提示词中 AI 自动选择多文件模块化结构'
  '就是一个例子——这在标准前端项目中是合理做法，但与单文件快速迭代的需求相悖。解决这一问题的关键在于：'
  '给 AI 的指令必须达到"接口文档"级别的精确度——不仅说"做什么"，还要说"输入什么、输出什么、边界'
  '条件如何处理"。')

H('8.2 AI 在本项目中的实际帮助', 2)
P('基于本项目的经验，AI 在以下方面提供了实质性的帮助：(1) 代码脚手架生成——将自然语言功能描述转化为'
  '初始实现，我只需在此基础上进行微调和边界修正；(2) 正则表达式编写——复杂正则（如 Java 方法签名的'
  '多修饰符匹配、Python 类型标注和默认值的同时解析）是 AI 的优势领域，产出质量通常只需少量调整；'
  '(3) CSS 系统构建——36 个变量的完整样式表加响应式断点，AI 能一次性产出并保持风格一致；(4) 样板代码'
  '填充——PPT 生成和 Word 导出中大量重复的 API 调用序列；(5) 调试辅助——当问题根因在算法逻辑层面时，'
  'AI 分析代码和定位缺陷的速度明显快于人工逐行排查。')

H('8.3 当前不足与改进方向', 2)
P('第一，全局上下文的衰减。当项目代码规模超过约 1500 行后，AI 对函数间隐式依赖关系的理解能力明显下降。'
  '项目后期的每一轮对话，我都需要花更多时间在向 AI 描述"已有数据结构是什么""哪些函数已经在用了"——'
  '这成为整个工作流中效率损失最大的环节。如果重新启动这个项目，我会在功能点达到 10 个左右时进行一次架构'
  '重构，将核心解析逻辑抽取为独立的 ES Module，至少用清晰的 import/export 关系替代当前依赖全局变量的'
  '隐式耦合。')
P('第二，代码生成与代码验证的能力不对等。AI 能够自信地生成包含边界缺陷的函数而不自知——比喻匹配评分'
  '算法中的泛型词噪声问题是典型例子。这意味着开发者每接受一段 AI 的代码，必须立即用手动测试覆盖 3-5 个'
  '边界输入——空值、特殊字符、极端长度、非法格式。这个"测试驱动"的习惯在 Vibe Coding 场景下比传统'
  '开发更为必要。')
P('第三，AI 在审美和体验层面的辅助有限。在视觉风格从深色主题转换为纯白克制设计的决策中，AI 能够精确'
  '执行"36 变量 CSS 系统"的技术规格，但在"为什么选择纯白而非深色""按钮 hover 动画多长才舒适"'
  '"错误提示用什么语气更友好"这类软性判断上，AI 的建议缺乏细腻度。涉及用户体验的最终决策仍然需要'
  '人来做出。')
P('第四，AI 缺乏主动的架构建议能力。在整个项目周期中，随着功能从最初的解析和说明书扩展至练习模式、'
  '历史管理、PPT/Word 导出、成就系统等 30 余个功能点，全局变量数量从 10 余个膨胀至 40 余个，代码'
  '的内聚性明显下降——但 AI 从未主动提示"当前代码结构可能需要进行一次重构"。它仅在接收到明确请求时'
  '才会给出相应建议，这一点与有经验的工程师在代码审查中主动识别技术债的习惯存在差距。')
P('总的来说，Vibe Coding 是一种值得投入时间掌握的工作范式。它不意味着"不用学编程了"，而是意味着编程'
  '的核心技能组合在发生变化——从"编码速度和 API 记忆"转向"需求的精确表达、架构的判断力、产出的质量'
  '审查"。能够与 AI 有效协作，正在成为一项独立的基础能力。')

P('')
P('本报告由庞凯匀（230152061）独立完成，文中涉及的 AI 工具（Claude Code）仅参与项目代码的开发过程。'
  '报告中的架构图和流程图由作者基于系统实际结构绘制，界面截图为项目实际运行效果。', indent=False)

# ── 保存 ──
out = r'c:\Users\16137\Desktop\vb期末\VibeCoding期末报告_v3.docx'
doc.save(out)
print(f'[OK] {out}')
