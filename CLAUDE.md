# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

纯前端"代码解释器"——用户粘贴 Java/Python 函数代码，自动生成技术版说明书和小白版叙事体说明书。所有解析在浏览器本地完成。

**学生**：庞凯匀 · 230152061 · 期末考核项目

## Run & develop

```bash
# 启动开发服务器（推荐绑定到 IPv4，避免 localhost 在某些系统解析为 IPv6 导致访问异常）
cd vb期末
# 推荐（绑定到 127.0.0.1）：
python -m http.server 8080 --bind 127.0.0.1
# 或（若想用默认绑定）：
# python -m http.server 8080
# 浏览器打开（优先使用 127.0.0.1 以避免 localhost 解析差异）
# http://127.0.0.1:8080/index.html
# 自测（运行内置 HashTest）：
# http://127.0.0.1:8080/index.html?runHashTest=1
# 硬刷新 Ctrl+Shift+R（跳过缓存）
```

无需 `npm install`、无需构建。CDN 引入 Prism.js + html2canvas，其余纯原生 JS。

## Architecture

**单文件项目**：`index.html`（709行）包含全部 HTML/CSS/JS。

### 函数分层

| 层 | 函数 | 职责 |
|------|------|------|
| 解析引擎 | `parseJava()` `parsePython()` | 正则提取方法签名、参数、import、try-catch |
| 语句解释 | `generateStatementExplanation()` → `explainPythonLine()` / `explainJavaLine()` | 逐行翻译 if/for/def/print/return |
| 比喻匹配 | `matchMetaphorEntry()` | 遍历 38 条概念域映射库，加权信号打分 |
| 洞察+模式 | `detectPatterns()` `calculateHealthScore()` | 检测递归/排序/缓存等 12 种模式；0-100 健康度评分 |
| 叙事生成 | `generateNarrativeBeginnerDoc()` | 散文体小白版，首句加粗比喻，零列表 |
| 渲染 | `renderTechDoc()` `renderBeginnerDoc()` | 生成 innerHTML 写入右侧面板 |
| 统计 | `recordParse()` `renderAllUI()` `checkBadges()` | 更新 6 个仪表板组件 + localStorage 持久化 |

### 数据流

```
用户粘贴代码 → 点"生成解释"
  → parseJava/parsePython(code) → ParsedFunction
  → matchMetaphorEntry(code, parsed) → {entry, matchQuality}
  → detectPatterns(parsed, code) → ['递归','排序',...]
  → renderTechDoc(parsed, lang) → 技术版 HTML
  → renderBeginnerDoc(parsed, lang, match) → 小白版 HTML
  → recordParse(lang, duration, code, tag, patterns)
     → 更新 parseStats / patternStats / metaphorHits / history / badges
     → localStorage.setItem
     → renderAllUI()
```

### localStorage 数据结构

```js
appStats = {
  total, javaCount, pythonCount, totalTime, avgTime,
  patternStats: { "递归": 5, "排序": 3 },   // 模式出现次数
  metaphorHits: { "sort": 12, "filter": 7 }, // 关键词命中次数
  history: [{code, language, funcName, timestamp}], // 最多8条
  badgeState: { first_blood: {unlocked, time}, java_master: {...} },
  nightOwl: false
}
```

### 比喻库结构（概念域映射）

```js
const METAPHOR_LIBRARY = [
  { keywords:['sort','排序'], concept:'排序', metaphor:'整理扑克牌',
    action:'把杂乱变为有序', inputDesc:'乱序数据', outputDesc:'有序结果' }
  // ...38条
];
```

### 页面布局（Crowz 仪表板）

```
左侧边栏(260px)            右侧主内容(6层)
├─ 头像 + 标题             ① 顶部栏：Dashboard + 语言下拉
├─ 仪表盘(点击→统计行)     ② 4 卡片统计行
├─ 说明书(点击→核心区)     ③ 代码输入(左) | 说明书(右双标签)
├─ 成就(点击→徽章墙)       ④ Top performers | Channels
└─ v3.0                   ⑤ 徽章墙 | 最近解析
                          ⑥ Full Stats / Log out
```

响应式：≤1000px 双栏变单栏+侧边栏隐藏，≤900px 卡片/洞察/底部各自 2→1 列。

## Key constraints

- **纯本地解析**：不调任何外部 AI API，全靠正则
- **不执行代码**：不 `eval` / `new Function` 用户输入
- **不存储用户数据**：localStorage 仅存统计数据（解析次数、模式排行等），不存用户代码到服务器
- **仅 Java/Python**：两种语言，切换用 `#langSelect`
- **单文件**：HTML+CSS+JS 全在 `index.html`，无框架

## Testing

手动测试：粘贴样例代码 → 点"生成解释" → 检查右侧说明书 + 顶部统计卡片变化。

边界用例：空输入、纯变量声明、箭头函数/匿名函数、复杂嵌套、语言切换。

Node.js 快速语法检查：`node -e "new Function(require('fs').readFileSync('index.html','utf8').match(/<script>([\s\S]*?)<\/script>/g).pop().replace(/<\/?script>/g,''))"`

## CDN dependencies

- Prism.js 1.29.0 (cdnjs): 语法高亮，Java + Python 语言包
- html2canvas 1.4.1 (cdnjs): 导出 PNG 分享卡片
