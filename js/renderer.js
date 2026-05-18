/* ===========================================================
   渲染引擎 — 技术版说明书 + 小白版说明书
   依赖：parser.js（escapeHtml）、metaphors.js（比喻库）
   =========================================================== */

/* =========================== 比喻匹配 =========================== */

/**
 * 根据函数名和代码内容匹配生活比喻
 * 遍历比喻库，找到第一个匹配的关键词即返回
 */
function matchMetaphor(codeLower, funcName) {
  var searchText = funcName.toLowerCase() + ' ' + codeLower;
  for (var i = 0; i < METAPHOR_LIBRARY.length; i++) {
    var entry = METAPHOR_LIBRARY[i];
    for (var j = 0; j < entry.keywords.length; j++) {
      if (searchText.indexOf(entry.keywords[j].toLowerCase()) !== -1) {
        return entry.metaphor;
      }
    }
  }
  return DEFAULT_METAPHOR;
}

/* =========================== 场景推断 =========================== */

/**
 * 推断代码的使用场景列表
 */
function inferScenarios(codeLower, funcName) {
  var scenarios = [];
  var name = funcName.toLowerCase();

  if (/sort|排序|order/i.test(name)) scenarios.push('需要对一组数据进行排序时');
  if (/search|find|查找|搜索|query/i.test(name)) scenarios.push('需要在大量数据中查找特定内容时');
  if (/filter|过滤|筛选/i.test(name)) scenarios.push('需要从一堆数据中筛选符合条件的条目时');
  if (/validate|check|验证|校验|valid/i.test(name)) scenarios.push('需要检查用户输入或数据是否符合规则时');
  if (/parse|解析/i.test(name)) scenarios.push('需要把文本格式的数据转换成结构化信息时');
  if (/read|get|fetch|读取|获取|load/i.test(name)) scenarios.push('需要从外部获取数据或读取文件时');
  if (/write|save|set|写入|保存|store/i.test(name)) scenarios.push('需要把数据保存或写入到某个位置时');
  if (/calc|compute|计算|sum|avg|mean|add|subtract|multiply|divide/i.test(name)) scenarios.push('需要进行数学计算或统计时');
  if (/convert|transform|转换|format/i.test(name)) scenarios.push('需要把数据从一种格式转换成另一种格式时');
  if (/encrypt|decrypt|hash|加密|解密/i.test(name)) scenarios.push('需要保护或还原敏感数据时');
  if (/init|setup|初始化|create|build/i.test(name)) scenarios.push('需要准备环境或创建新对象时');
  if (/print|log|输出|display|show|render/i.test(name)) scenarios.push('需要把信息展示给用户或记录到日志时');

  // 函数名匹配不到，从代码内容推断
  if (scenarios.length === 0) {
    if (/sort|sorted/.test(codeLower)) scenarios.push('需要对数据进行排序整理时');
    if (/filter|where/.test(codeLower)) scenarios.push('需要对数据进行条件筛选时');
    if (/map\s*\(|\.map\(/.test(codeLower)) scenarios.push('需要对集合中每个元素进行转换时');
    if (/for\s*\(|while\s*\(/.test(codeLower)) scenarios.push('需要遍历或重复处理数据时');
    if (/try\s*\{|try\s*:/.test(codeLower)) scenarios.push('需要处理可能出现错误的情况时');
    if (/import|require|from.*import/.test(codeLower)) scenarios.push('需要利用外部库或模块的功能时');
  }

  if (scenarios.length === 0) {
    scenarios.push('需要在程序中完成一个特定任务时');
  }
  return scenarios;
}

/* =========================== 输入输出推断 =========================== */

/**
 * 根据参数列表和返回值类型推断输入输出描述
 */
function inferIO(funcName, params, returnType) {
  var inputDesc = '';
  var outputDesc = '';

  if (params.length === 0) {
    inputDesc = '该功能不需要额外的输入参数，它可能从内部状态或全局变量中获取数据';
  } else {
    var paramDescs = params.map(function(p) {
      var pName = p.name.toLowerCase();
      if (/num|count|size|len|index|amount|total|sum/.test(pName)) return p.name + ': 一个数值';
      if (/str|text|name|label|msg|message|title/.test(pName)) return p.name + ': 一段文本';
      if (/arr|list|array|data|items|collection|elements/.test(pName)) return p.name + ': 一组数据';
      if (/flag|bool|is|enabled/.test(pName)) return p.name + ': 是/否';
      if (/obj|object|config|options|settings/.test(pName)) return p.name + ': 一个配置对象';
      if (/file|path|url|dir/.test(pName)) return p.name + ': 一个文件路径或地址';
      if (/key|id/.test(pName)) return p.name + ': 一个标识符';
      return p.name + ': 一个输入';
    });
    inputDesc = paramDescs.join('；');
  }

  var rt = returnType.toLowerCase();
  if (rt === 'void' || rt === 'none' || !rt) {
    outputDesc = '这个功能不返回具体值，它直接产生效果（比如修改数据、打印输出、保存文件等）';
  } else if (/int|float|double|num|number|long|short/.test(rt)) {
    outputDesc = '返回一个数字，代表计算结果';
  } else if (/string|str/.test(rt)) {
    outputDesc = '返回一段文本';
  } else if (/bool|boolean/.test(rt)) {
    outputDesc = '返回是/否（true/false），代表判断结果';
  } else if (/list|array|\[\]|集合/.test(rt)) {
    outputDesc = '返回一组数据，是一个列表或数组';
  } else if (/map|dict|dictionary/.test(rt)) {
    outputDesc = '返回一个键值对集合，像电话簿一样可以用键查值';
  } else {
    outputDesc = '返回处理后的结果';
  }

  return { inputDesc: inputDesc, outputDesc: outputDesc };
}

/* =========================== 技术版说明书 =========================== */

/**
 * 渲染技术版说明书 HTML
 */
function renderTechSpec(parsed, lang) {
  var langLabel = lang === 'java' ? 'Java' : 'Python';
  var langBadge = lang === 'java' ? 'badge-java' : 'badge-python';

  // 构建函数签名
  var paramsDisplay = parsed.parameters.map(function(p) {
    return p.type + ' ' + p.name;
  }).join(', ');
  var signature = '';
  if (lang === 'java') {
    signature = parsed.returnType + ' ' + parsed.methodName + '(' + paramsDisplay + ')';
  } else {
    signature = 'def ' + parsed.methodName + '(' + paramsDisplay + ')';
    if (parsed.returnType && parsed.returnType !== 'None' && parsed.returnType !== 'void') {
      signature += ' -> ' + parsed.returnType;
    }
  }

  // 参数表格行
  var paramRows = '';
  if (parsed.parameters.length > 0) {
    paramRows = parsed.parameters.map(function(p, i) {
      return '<tr>' +
        '<td>' + (i + 1) + '</td>' +
        '<td><code>' + escapeHtml(p.name) + '</code></td>' +
        '<td><span class="badge ' + langBadge + '">' + escapeHtml(p.type) + '</span></td>' +
      '</tr>';
    }).join('');
  } else {
    paramRows = '<tr><td colspan="3" style="color:var(--text2);text-align:center">无参数</td></tr>';
  }

  // 依赖列表
  var depHtml = '';
  if (parsed.dependencies.length > 0) {
    depHtml = '<ul class="dep-list">' +
      parsed.dependencies.map(function(d) {
        return '<li>' + escapeHtml(d) + '</li>';
      }).join('') +
    '</ul>';
  } else {
    depHtml = '<p style="color:var(--text2)">无外部依赖</p>';
  }

  // 异常处理
  var tryBadge = parsed.hasTryCatch
    ? '<span class="badge badge-try">包含异常处理（try-catch/except）</span>'
    : '<span class="badge badge-no-try">未检测到异常处理</span>';

  return '' +
    '<div class="spec-section">' +
      '<div class="spec-label">函数签名</div>' +
      '<div class="spec-signature">' + escapeHtml(signature) + '</div>' +
      '<div style="margin-top:6px"><span class="badge ' + langBadge + '">' + langLabel + '</span></div>' +
    '</div>' +
    '<div class="spec-section">' +
      '<div class="spec-label">参数列表</div>' +
      '<table class="spec-table">' +
        '<thead><tr><th>#</th><th>参数名</th><th>类型</th></tr></thead>' +
        '<tbody>' + paramRows + '</tbody>' +
      '</table>' +
    '</div>' +
    '<div class="spec-section">' +
      '<div class="spec-label">返回值</div>' +
      '<p><span class="badge ' + langBadge + '">' + escapeHtml(parsed.returnType || 'void') + '</span></p>' +
    '</div>' +
    '<div class="spec-section">' +
      '<div class="spec-label">依赖</div>' +
      depHtml +
    '</div>' +
    '<div class="spec-section">' +
      '<div class="spec-label">异常处理</div>' +
      tryBadge +
    '</div>';
}

/* =========================== 小白版说明书 =========================== */

/**
 * 渲染小白版说明书 HTML
 */
function renderBeginnerSpec(parsed, lang, metaphor, scenarios, io) {
  var langLabel = lang === 'java' ? 'Java' : 'Python';
  var lineCount = parsed.rawCode.split('\n').length;

  var html = '' +
    '<div class="spec-section">' +
      '<div class="spec-label">这个功能是什么</div>' +
      '<div class="metaphor-card">' +
        '<div class="icon">--</div>' +
        '<p><strong>' + escapeHtml(parsed.methodName) + '</strong> — ' + escapeHtml(metaphor) + '</p>' +
      '</div>' +
      '<p style="margin-top:8px;color:var(--text2);font-size:0.9rem">' +
        '代码语言：' + langLabel + ' &middot; ' + lineCount + ' 行代码' +
      '</p>' +
    '</div>' +
    '<div class="spec-section">' +
      '<div class="spec-label">什么时候会用到它</div>' +
      '<ul class="scenario-list">' +
        scenarios.map(function(s) { return '<li>' + escapeHtml(s) + '</li>'; }).join('') +
      '</ul>' +
    '</div>' +
    '<div class="spec-section">' +
      '<div class="spec-label">输入 / 输出</div>' +
      '<div class="io-grid">' +
        '<div class="io-box">' +
          '<div class="io-box-title">输入</div>' +
          '<p style="font-size:0.9rem;color:var(--text2)">' + escapeHtml(io.inputDesc) + '</p>' +
        '</div>' +
        '<div class="io-box">' +
          '<div class="io-box-title">输出</div>' +
          '<p style="font-size:0.9rem;color:var(--text2)">' + escapeHtml(io.outputDesc) + '</p>' +
        '</div>' +
      '</div>' +
    '</div>';

  // 依赖（可选）
  if (parsed.dependencies.length > 0) {
    html += '' +
      '<div class="spec-section">' +
        '<div class="spec-label">它借用了哪些工具</div>' +
        '<ul class="dep-list">' +
          parsed.dependencies.map(function(d) { return '<li>' + escapeHtml(d) + '</li>'; }).join('') +
        '</ul>' +
        '<p style="margin-top:4px;font-size:0.8rem;color:var(--text2)">就像做菜需要借用锅和刀，这些是代码借用的外部工具</p>' +
      '</div>';
  }

  // 异常保护（可选）
  if (parsed.hasTryCatch) {
    html += '' +
      '<div class="spec-section">' +
        '<div class="spec-label">它有安全保护</div>' +
        '<p style="color:var(--success)">这段代码包含了错误处理（像安全气囊），出问题时不会直接崩溃</p>' +
      '</div>';
  }

  return html;
}
