/* ===========================================================
   主控制器 — 事件绑定、状态管理、复制/导出功能
   =========================================================== */

/* =========================== 状态 =========================== */

var lastParsed = null;     // 最近一次解析结果
var lastLang = 'java';     // 最近解析使用的语言
var lastMetaphor = '';     // 最近匹配的比喻文本
var lastScenarios = [];    // 最近推断的使用场景
var lastIO = null;         // 最近推断的输入输出 { inputDesc, outputDesc }

/* =========================== Toast 提示 =========================== */

function showToast(msg) {
  var toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(function() {
    toast.classList.remove('show');
  }, 2000);
}

/* =========================== 核心：解析并渲染 =========================== */

function doParse() {
  var codeInput = document.getElementById('codeInput');
  var errorToast = document.getElementById('errorToast');
  var loadingOverlay = document.getElementById('loadingOverlay');
  var lang = document.getElementById('langSelect').value;
  var code = codeInput.value;

  // 空输入校验
  if (!code.trim()) {
    errorToast.textContent = '请先粘贴一段 Java 或 Python 函数代码，再点击解析。';
    errorToast.classList.add('active');
    return;
  }
  errorToast.classList.remove('active');

  // 显示加载动画
  loadingOverlay.classList.add('active');

  // 使用 setTimeout 确保加载动画有机会渲染
  setTimeout(function() {
    try {
      // 根据语言选择解析器
      var parsed;
      if (lang === 'java') {
        parsed = parseJava(code);
      } else {
        parsed = parsePython(code);
      }

      lastParsed = parsed;
      lastLang = lang;

      // 匹配比喻、场景、输入输出
      var codeLower = code.toLowerCase();
      lastMetaphor = matchMetaphor(codeLower, parsed.methodName);
      lastScenarios = inferScenarios(codeLower, parsed.methodName);
      lastIO = inferIO(parsed.methodName, parsed.parameters, parsed.returnType);

      // 渲染技术版
      var techContent = document.getElementById('techContent');
      var techEmpty = document.getElementById('techEmpty');
      techContent.innerHTML = renderTechSpec(parsed, lang);
      techContent.style.display = 'block';
      techEmpty.style.display = 'none';

      // 渲染小白版
      var beginnerContent = document.getElementById('beginnerContent');
      var beginnerEmpty = document.getElementById('beginnerEmpty');
      beginnerContent.innerHTML = renderBeginnerSpec(parsed, lang, lastMetaphor, lastScenarios, lastIO);
      beginnerContent.style.display = 'block';
      beginnerEmpty.style.display = 'none';

      // 刷新 Prism 语法高亮
      if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
      }
    } catch (err) {
      errorToast.textContent = '解析失败，请检查代码是否为有效的 Java / Python 函数。错误详情：' + err.message;
      errorToast.classList.add('active');
      console.error('解析错误:', err);
    } finally {
      loadingOverlay.classList.remove('active');
    }
  }, 150);
}

/* =========================== 复制到剪贴板 =========================== */

function copySpec(type) {
  if (!lastParsed) {
    showToast('请先解析代码后再复制');
    return;
  }

  var text = '';
  var paramsDisplay = lastParsed.parameters.map(function(p) {
    return p.type + ' ' + p.name;
  }).join(', ');

  if (type === 'tech') {
    var signature = lastLang === 'java'
      ? lastParsed.returnType + ' ' + lastParsed.methodName + '(' + paramsDisplay + ')'
      : 'def ' + lastParsed.methodName + '(' + paramsDisplay + ')' +
        (lastParsed.returnType && lastParsed.returnType !== 'void' && lastParsed.returnType !== 'None'
          ? ' -> ' + lastParsed.returnType : '');

    var langLabel = lastLang === 'java' ? 'Java' : 'Python';

    text = '═══════════════════════════════════\n';
    text += '  技术版说明书 (' + langLabel + ')\n';
    text += '═══════════════════════════════════\n\n';
    text += '[函数签名]\n' + signature + '\n\n';
    text += '[参数列表]\n';
    if (lastParsed.parameters.length > 0) {
      lastParsed.parameters.forEach(function(p, i) {
        text += '  ' + (i + 1) + '. ' + p.name + ' : ' + p.type + '\n';
      });
    } else {
      text += '  (无参数)\n';
    }
    text += '\n[返回值]\n' + (lastParsed.returnType || 'void') + '\n\n';
    text += '[依赖]\n';
    if (lastParsed.dependencies.length > 0) {
      lastParsed.dependencies.forEach(function(d) { text += '  - ' + d + '\n'; });
    } else {
      text += '  (无外部依赖)\n';
    }
    text += '\n[异常处理]\n';
    text += lastParsed.hasTryCatch ? '包含 try-catch/except' : '未检测到异常处理';
  } else {
    var langLabel = lastLang === 'java' ? 'Java' : 'Python';

    text = '═══════════════════════════════════\n';
    text += '  小白版说明书 (' + langLabel + ')\n';
    text += '═══════════════════════════════════\n\n';
    text += '[这个功能是什么]\n' + lastParsed.methodName + ' — ' + lastMetaphor + '\n\n';
    text += '[使用场景]\n';
    lastScenarios.forEach(function(s) { text += '  - ' + s + '\n'; });
    text += '\n[输入]\n' + lastIO.inputDesc + '\n\n';
    text += '[输出]\n' + lastIO.outputDesc + '\n';
    if (lastParsed.dependencies.length > 0) {
      text += '\n[借用的工具]\n';
      lastParsed.dependencies.forEach(function(d) { text += '  - ' + d + '\n'; });
    }
    if (lastParsed.hasTryCatch) {
      text += '\n[安全保护] 包含错误处理\n';
    }
  }

  // 使用 Clipboard API，带降级方案
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function() {
      showToast('已复制到剪贴板！粘贴到记事本可看到完整格式');
    }).catch(function() {
      fallbackCopy(text);
    });
  } else {
    fallbackCopy(text);
  }
}

/** 降级复制方案（创建临时 textarea） */
function fallbackCopy(text) {
  var ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
  showToast('已复制到剪贴板！');
}

/* =========================== 导出分享卡片 =========================== */

function exportCard() {
  if (!lastParsed) {
    showToast('请先解析代码后再导出');
    return;
  }

  if (typeof html2canvas === 'undefined') {
    showToast('html2canvas 还未加载完成，请稍后再试');
    return;
  }

  var outputPanel = document.getElementById('outputPanel');

  html2canvas(outputPanel, { scale: 2, backgroundColor: '#1a1a2e' }).then(function(canvas) {
    var link = document.createElement('a');
    link.download = '代码说明书_' + lastParsed.methodName + '.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
    showToast('分享卡片已导出！');
  }).catch(function(err) {
    console.error('导出失败:', err);
    showToast('导出失败，请重试');
  });
}

/* =========================== 标签页切换 =========================== */

function switchTab(targetTab) {
  // 切换标签按钮激活态
  var buttons = document.querySelectorAll('.tab-btn');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove('active');
  }
  document.querySelector('.tab-btn[data-tab="' + targetTab + '"]').classList.add('active');

  // 切换内容区
  var contents = document.querySelectorAll('.tab-content');
  for (var j = 0; j < contents.length; j++) {
    contents[j].classList.remove('active');
  }
  document.getElementById(targetTab + 'Tab').classList.add('active');
}

/* =========================== 事件绑定 =========================== */

document.addEventListener('DOMContentLoaded', function() {

  // 解析按钮
  document.getElementById('parseBtn').addEventListener('click', doParse);

  // Ctrl+Enter 快捷解析
  document.getElementById('codeInput').addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      doParse();
    }
    // 输入时清除错误
    document.getElementById('errorToast').classList.remove('active');
  });

  // 复制按钮
  document.getElementById('copyTechBtn').addEventListener('click', function() {
    copySpec('tech');
  });
  document.getElementById('copyBeginnerBtn').addEventListener('click', function() {
    copySpec('beginner');
  });

  // 导出卡片按钮
  document.getElementById('exportBtn').addEventListener('click', exportCard);

  // 标签页切换
  var tabButtons = document.querySelectorAll('.tab-btn');
  for (var i = 0; i < tabButtons.length; i++) {
    tabButtons[i].addEventListener('click', function() {
      switchTab(this.dataset.tab);
    });
  }

  // 初始化 Prism 高亮
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }

  console.log('代码片段智能说明书生成器已就绪');
});
