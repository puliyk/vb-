/* ===========================================================
   解析引擎 — Java 和 Python 代码解析
   纯正则匹配，不调用任何外部 AI 接口，不执行用户代码
   输出统一数据结构：ParsedFunction
   =========================================================== */

/* =========================== 工具函数 =========================== */

/**
 * 拆分参数字符串，处理泛型尖括号内的逗号
 * 例："int a, List<Integer> b" → ["int a", "List<Integer> b"]
 */
function splitParams(paramsStr) {
  const parts = [];
  let depth = 0;
  let current = '';
  for (let i = 0; i < paramsStr.length; i++) {
    const ch = paramsStr[i];
    if (ch === ',' && depth === 0) {
      parts.push(current);
      current = '';
    } else {
      if (ch === '<' || ch === '(' || ch === '[') depth++;
      if (ch === '>' || ch === ')' || ch === ']') depth--;
      current += ch;
    }
  }
  const trimmed = current.trim();
  if (trimmed) parts.push(trimmed);
  return parts;
}

/**
 * HTML 转义，防止 XSS
 */
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/**
 * 从代码 return 语句推断返回值类型
 */
function inferReturnType(code) {
  if (/return\s+["'`]/.test(code)) return 'String';
  if (/return\s+(true|false)/.test(code)) return 'boolean';
  if (/return\s+\d+(\.\d+)?/.test(code)) return 'int';
  if (/return\s+new\s+(\w+)/.test(code)) {
    const m = code.match(/return\s+new\s+(\w+)/);
    return m ? m[1] : 'Object';
  }
  if (/return\s+\w+\s*\(/.test(code)) {
    const m = code.match(/return\s+(\w+)\s*\(/);
    return m ? '调用 ' + m[1] + '() 的结果' : '推断返回值';
  }
  if (/return\s+\w+/.test(code)) {
    const m = code.match(/return\s+(\w+)/);
    return m ? '变量: ' + m[1] : '推断返回值';
  }
  if (!/return/.test(code)) return 'void';
  return '推断返回值';
}

/**
 * 为匿名/无法解析的函数推断名称
 */
function inferFunctionName(code, lang) {
  // 优先从注释中提取
  const commentMatch = code.match(/(?:\/\/|#)\s*(.+)/);
  if (commentMatch) {
    const comment = commentMatch[1].trim();
    return comment.substring(0, 40);
  }

  const codeLower = code.toLowerCase();

  if (/sort|sorted/.test(codeLower)) return '排序函数';
  if (/filter|筛选/.test(codeLower)) return '过滤函数';
  if (/search|find|查找/.test(codeLower)) return '查找函数';
  if (/validate|check|验证/.test(codeLower)) return '校验函数';
  if (/parse|解析/.test(codeLower)) return '解析函数';
  if (/calc|sum|avg|计算/.test(codeLower)) return '计算函数';
  if (/read|读取|load|加载/.test(codeLower)) return '读取函数';
  if (/write|save|保存|写入/.test(codeLower)) return '写入函数';
  if (/convert|transform|转换/.test(codeLower)) return '转换函数';
  if (/print|log|输出|显示/.test(codeLower)) return '输出函数';
  if (/=>/.test(code) || /lambda/.test(codeLower)) return '匿名函数(lambda)';

  return lang === 'java' ? '未命名方法' : '未命名函数';
}

/**
 * 从代码中推断参数（用于非标准函数）
 */
function inferParams(code) {
  const params = [];
  const varRegex = /\b([a-zA-Z_]\w*)\s*=/g;
  const seen = new Set();
  const reserved = [
    'if', 'else', 'for', 'while', 'return', 'var', 'let', 'const', 'new',
    'int', 'String', 'boolean', 'void', 'def', 'import', 'from', 'class',
    'public', 'private', 'protected', 'static', 'final', 'throws'
  ];
  let m;
  while ((m = varRegex.exec(code)) !== null) {
    const name = m[1];
    if (!seen.has(name) && !reserved.includes(name)) {
      seen.add(name);
      if (params.length < 5) {
        params.push({ name: name, type: '推断参数' });
      }
    }
  }
  return params;
}

/* =========================== Java 解析器 =========================== */

/**
 * 解析 Java 代码片段
 * 识别：方法签名、参数、返回值、import、try-catch
 */
function parseJava(code) {
  const result = {
    methodName: '',
    parameters: [],
    returnType: '',
    dependencies: [],
    hasTryCatch: false,
    rawCode: code.trim()
  };

  // 提取 import 语句
  const importRegex = /import\s+([\w.]+(?:\s*\.\s*\*)?)\s*;/g;
  let m;
  while ((m = importRegex.exec(code)) !== null) {
    result.dependencies.push(m[1]);
  }

  // 检测 try-catch 结构
  result.hasTryCatch = /try\s*\{/.test(code);

  /*
   * 匹配 Java 方法签名
   * 支持：public static int add(int a, int b)
   *       private void process(String data)
   *       protected List<String> getItems()
   *       public static void main(String[] args)
   */
  const methodRegex = /(?:(?:public|private|protected)\s+)?(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?([\w.]+(?:<[^>]*>)?(?:\[\])?)\s+(\w+)\s*\(([^)]*)\)/;
  const methodMatch = code.match(methodRegex);

  if (methodMatch) {
    result.returnType = methodMatch[1];
    result.methodName = methodMatch[2];
    const paramsStr = methodMatch[3].trim();

    if (paramsStr) {
      result.parameters = splitParams(paramsStr).map(function(part) {
        var parts = part.trim().split(/\s+/);
        var name = parts.pop() || '';
        var type = parts.join(' ') || 'Object';
        return { name: name, type: type };
      });
    }
  } else {
    // 非标准方法 → 降级为智能推断
    result.methodName = inferFunctionName(code, 'java');
    result.returnType = inferReturnType(code);
    result.parameters = inferParams(code);
  }

  return result;
}

/* =========================== Python 解析器 =========================== */

/**
 * 解析 Python 代码片段
 * 识别：def 定义、参数（含默认值/类型注解）、import、try-except
 */
function parsePython(code) {
  const result = {
    methodName: '',
    parameters: [],
    returnType: '',
    dependencies: [],
    hasTryCatch: false,
    rawCode: code.trim()
  };

  // 提取 import / from...import
  const importRegex = /^(?:import|from)\s+([\w.]+)/gm;
  var m;
  while ((m = importRegex.exec(code)) !== null) {
    result.dependencies.push(m[1]);
  }

  // 检测 try-except 结构
  result.hasTryCatch = /try\s*:/i.test(code);

  // 匹配 def 函数定义
  // 支持：def name(param), def name(param: type), def name(param=default), def name() -> ReturnType:
  const defRegex = /def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(\w+))?\s*:/;
  const defMatch = code.match(defRegex);

  if (defMatch) {
    result.methodName = defMatch[1];
    result.returnType = defMatch[3] || inferReturnType(code);
    const paramsStr = defMatch[2].trim();

    if (paramsStr && paramsStr !== 'self' && paramsStr !== 'cls') {
      result.parameters = splitParams(paramsStr)
        .filter(function(p) {
          var name = p.trim().split(/\s*[:=]/)[0].trim();
          return name !== 'self' && name !== 'cls';
        })
        .map(function(part) {
          var trimmed = part.trim();
          var name = trimmed;
          var type = 'Any';

          // 去掉默认值（= 后面的部分）
          var eqIdx = trimmed.indexOf('=');
          var beforeDefault = eqIdx >= 0 ? trimmed.substring(0, eqIdx).trim() : trimmed;

          // 提取类型注解（: 后面的部分）
          var colonIdx = beforeDefault.indexOf(':');
          if (colonIdx >= 0) {
            name = beforeDefault.substring(0, colonIdx).trim();
            type = beforeDefault.substring(colonIdx + 1).trim();
          } else {
            name = beforeDefault;
          }

          return { name: name, type: type };
        });
    }
  } else {
    // 非标准函数 → 降级为智能推断
    result.methodName = inferFunctionName(code, 'python');
    result.returnType = inferReturnType(code);
    result.parameters = inferParams(code);
  }

  return result;
}
