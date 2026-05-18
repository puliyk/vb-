代码片段智能说明书生成器 – 技术设计
技术栈
前端：HTML5 + CSS3 + 原生 JavaScript (ES6)

样式：CSS Grid + Flexbox（无 UI 框架）

语法高亮：Prism.js（CDN 引入）

截图导出：html2canvas（CDN 引入）

部署：GitHub Pages / Vercel / 本地运行

项目结构
text
code2doc-generator/
├── index.html              # 主页面（包含内联样式和脚本）
├── styles.css              # 可选：独立样式文件（也可内联）
├── scripts.js              # 可选：独立脚本文件（也可内联）
├── README.md               # 项目说明
└── assets/                 # 可选：图片等资源
实际开发建议：为方便 VibeCoding 快速迭代，初期可将 CSS 和 JS 内联在 index.html 中，后期再拆分。

数据模型
ParsedFunction（解析结果）
javascript
{
  methodName: string,        // 函数名
  parameters: [              // 参数列表
    {
      name: string,          // 参数名
      type: string           // 参数类型（Java）或 "Any"（Python）
    }
  ],
  returnType: string,        // 返回值类型（Java）或推断值（Python）
  dependencies: string[],    // 依赖列表（import / require / from...import）
  hasTryCatch: boolean,      // 是否包含异常处理
  rawCode: string            // 原始代码片段（用于比喻匹配）
}
MetaphorEntry（比喻映射）
javascript
{
  keywords: string[],        // 触发关键词（如 "sort", "filter"）
  metaphor: string           // 生活比喻文本
}
比喻库（硬编码，至少 20 条，最终 38 条）
javascript
const metaphorLibrary = [
  { keywords: ["sort"], metaphor: "就像把一叠乱序的扑克牌按照数字从小到大整理好" },
  { keywords: ["filter"], metaphor: "像用筛子筛面粉，只留下符合要求的颗粒" },
  { keywords: ["map"], metaphor: "像是给每个苹果都贴上标签，变成一个新的水果篮" },
  { keywords: ["reduce"], metaphor: "像是把一堆零钱全部换成一张大钞" },
  { keywords: ["递归", "recursion"], metaphor: "像俄罗斯套娃，一层层打开直到最小的那个娃娃" },
  { keywords: ["读取文件", "readFile"], metaphor: "像是打开冰箱门，从里面拿出食物" },
  // ... 其余条目
];
关键技术点
1. 双栏响应式布局
使用 CSS Grid 实现左右两栏：grid-template-columns: 1fr 1fr

媒体查询 @media (max-width: 768px) 改为 1fr 单列，自动堆叠

右侧说明书区使用 Flexbox 内部布局，包含两个标签页（技术版/小白版）

2. 正则解析引擎（无 AI 接口）
Java 解析：

识别方法声明：/(public|private|protected|static)?\s*(\w+)\s+(\w+)\s*\(([^)]*)\)\s*\{/

提取 import：/import\s+([\w\.]+);/g

检测 try-catch：/try\s*\{/

Python 解析：

识别函数定义：/def\s+(\w+)\s*\(([^)]*)\)/

提取 import：/^(?:import|from)\s+([\w\.]+)/gm

检测 try-except：/try\s*:/i

返回值推断：Python 中扫描 return 关键字

3. 生活比喻匹配策略
将函数名 + 原始代码转为小写

遍历比喻库，匹配 keywords 中的任意关键词

匹配到则返回对应比喻，否则返回兜底文本（“这是一个代码功能块，输入一些东西，经过处理后输出结果”）

4. 加载动画与异步体验
点击解析按钮时，显示隐藏的 loading 元素（CSS 旋转动画）

使用 setTimeout 或 Promise 模拟异步（实际解析很快，但为了体验留 100ms 间隙）

解析完成后更新 DOM，隐藏 loading

5. 复制技术版内容
使用 navigator.clipboard.writeText() 方法

提取技术版说明书区域的纯文本（innerText 或手动拼接）

复制成功后弹出提示（alert 或 toast）

6. 导出分享卡片（第12周）
引入 html2canvas CDN

获取目标说明书区域的 DOM 元素

调用 html2canvas(element, { scale: 2 }) 生成 canvas

将 canvas 转为 PNG 并触发下载（创建 <a> 标签，设置 download 属性）

7. 边界错误处理
空代码：检测 textarea.value.trim() === ""，弹出提示并阻止解析

解析失败：try-catch 包裹解析逻辑，显示友好错误消息（如“解析失败，请检查代码是否为有效的 Java/Python 函数”）

匿名函数/箭头函数：无显式 function/def 关键字时，尝试从代码文本中提取意图（如包含 => 则猜测为箭头函数，显示通用描述）

8. 代码高亮集成
页面加载时调用 Prism.highlightAll()

解析完成后（DOM 更新后）再次调用 Prism.highlightAll() 刷新

语言切换时，更新代码块上的 language-* 类名（如 language-java / language-python）

技术约束说明
不使用任何后端：所有解析、渲染均在用户浏览器完成

不调用外部 AI：基于正则和规则匹配，保证隐私和离线可用

无数据存储：不保存用户代码，关闭页面即清除

轻量化：除 Prism.js 和 html2canvas 外无第三方库，总大小 < 200KB