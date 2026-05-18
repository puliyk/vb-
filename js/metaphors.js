/* ===========================================================
   生活比喻库 — 38 条映射
   结构：{ keywords: string[], metaphor: string }
   keywords 为触发词（中英文均可），全部小写匹配
   =========================================================== */

const METAPHOR_LIBRARY = [
  {
    keywords: ['sort', '排序', 'sorted', 'orderby'],
    metaphor: '就像把一叠乱序的扑克牌按数字从小到大整理好'
  },
  {
    keywords: ['filter', '过滤', 'where', '筛选'],
    metaphor: '像用筛子筛面粉，只留下符合要求的颗粒'
  },
  {
    keywords: ['map', '映射', 'transform', '转换', 'apply'],
    metaphor: '像是给每个苹果都贴上标签，变成一篮新的水果'
  },
  {
    keywords: ['reduce', '聚合', 'fold', 'accumulate', 'sum'],
    metaphor: '像是把一堆零钱全部换成一张大钞'
  },
  {
    keywords: ['递归', 'recursion', 'recursive'],
    metaphor: '像俄罗斯套娃，一层层打开直到最小的那个娃娃'
  },
  {
    keywords: ['read', '读取', 'readfile', 'open'],
    metaphor: '像是打开冰箱门，从里面拿出需要的食物'
  },
  {
    keywords: ['write', '写入', 'writefile', 'save', '保存'],
    metaphor: '像写日记，把今天的想法记录到本子上'
  },
  {
    keywords: ['search', '查找', 'find', '搜索', 'indexof', 'contains'],
    metaphor: '像是在图书馆里按编号找一本书'
  },
  {
    keywords: ['loop', '循环', 'for', 'while', 'foreach', '遍历', 'iterate'],
    metaphor: '像流水线上的工人，对每个产品重复同样的操作'
  },
  {
    keywords: ['if', 'else', '条件', '判断', 'switch', '分支'],
    metaphor: '像走到十字路口，根据路标选择往哪个方向走'
  },
  {
    keywords: ['function', '方法', '函数', 'def'],
    metaphor: '像一份菜谱，告诉你需要什么食材（输入），怎么做（处理），做出什么菜（输出）'
  },
  {
    keywords: ['class', '类', '对象', 'object', 'new'],
    metaphor: '像汽车的设计蓝图，同一张图纸可以造出很多辆颜色不同的车'
  },
  {
    keywords: ['array', 'list', '数组', '列表', '集合'],
    metaphor: '像购物清单，把要买的东西一行行列出来，可以随时增减'
  },
  {
    keywords: ['dictionary', 'dict', 'map', 'hashmap', '字典', '键值'],
    metaphor: '像电话簿，每个名字（键）对应一个号码（值），查名字就能找到号码'
  },
  {
    keywords: ['try', 'catch', 'except', '异常', '错误处理', 'exception'],
    metaphor: '像汽车的安全气囊，平时不影响驾驶，但出事故时能保护你不受伤'
  },
  {
    keywords: ['import', 'require', '引入', '依赖', 'from', 'include'],
    metaphor: '像是借用别人的工具，不需要自己从头造轮子'
  },
  {
    keywords: ['variable', '变量', '赋值', 'let', 'const'],
    metaphor: '像一张便签纸，上面写着一个值，随时可以修改或查看'
  },
  {
    keywords: ['string', '字符串', '文本', 'str'],
    metaphor: '像一串字母和符号串成的珠链，可以拼接、裁剪、替换'
  },
  {
    keywords: ['api', 'http', 'fetch', '请求', 'request', 'curl'],
    metaphor: '像在餐厅点餐，你告诉服务员想要什么（请求），厨房做好了端给你（响应）'
  },
  {
    keywords: ['cache', '缓存', 'memo', '记忆'],
    metaphor: '像备忘录，把算好的结果存起来，下次直接拿来用，不用重新算'
  },
  {
    keywords: ['database', '数据库', 'sql', 'db'],
    metaphor: '像一个巨大而整齐的文件柜，每个抽屉都有编号，方便存取资料'
  },
  {
    keywords: ['algorithm', '算法'],
    metaphor: '像搭乐高的说明书，每一步都写清楚怎么操作才能完成目标'
  },
  {
    keywords: ['callback', '回调', '回调函数'],
    metaphor: '像是给别人留你的电话号码，事情办完了他们会打给你通知结果'
  },
  {
    keywords: ['async', 'await', 'promise', '异步', 'then'],
    metaphor: '像在网上下外卖订单，下了单不用一直盯着厨房，饭好了你会收到通知'
  },
  {
    keywords: ['encrypt', '加密', 'decrypt', '解密', 'hash', '哈希'],
    metaphor: '像把秘密锁进保险箱，只有有密码的人才能打开看到内容'
  },
  {
    keywords: ['compress', '压缩', 'zip', 'gzip'],
    metaphor: '像用真空压缩袋收纳衣物，节省存储空间，要用的时候再解压展开'
  },
  {
    keywords: ['parse', '解析', 'parser', 'token'],
    metaphor: '像拆开一个包装精美的礼物，一层层剥开看到里面的东西'
  },
  {
    keywords: ['validate', '验证', '校验', 'check', 'assert'],
    metaphor: '像门口的保安，检查来访者的证件才放行，不让可疑的人进来'
  },
  {
    keywords: ['log', '日志', 'logger', 'print', '输出', 'console'],
    metaphor: '像航海日志，记录航行中发生的每件重要的事，方便以后回溯'
  },
  {
    keywords: ['queue', '队列', 'fifo'],
    metaphor: '像在电影院排队买票，先来先服务，后来排后面'
  },
  {
    keywords: ['stack', '栈', 'lifo', '堆栈'],
    metaphor: '像一叠盘子，最后叠上去的盘子最先拿下来用'
  },
  {
    keywords: ['tree', '树', '二叉树'],
    metaphor: '像家族的族谱树，从祖先开始，一层层分支出子女'
  },
  {
    keywords: ['graph', '图', 'network', '网络'],
    metaphor: '像地铁线路图，每个站是一个节点，线路是它们之间的连接'
  },
  {
    keywords: ['singleton', '单例', '唯一', 'single'],
    metaphor: '像地球只有一个，无论你在哪问「地球在哪」，答案都是同一个'
  },
  {
    keywords: ['factory', '工厂', 'create'],
    metaphor: '像汽车工厂的生产线，你告诉它要什么车型，它就给你造出对应的车'
  },
  {
    keywords: ['observer', '观察者', 'listener', 'event', '监听', '订阅'],
    metaphor: '像订阅了报纸，每天报社都会把最新的新闻送到你家门口'
  },
  {
    keywords: ['decorator', '装饰器', 'wrapper', '包装'],
    metaphor: '像给手机先贴膜再套上保护壳，功能没变但多了额外保护'
  },
  {
    keywords: ['iterator', '迭代器', '遍历器'],
    metaphor: '像是翻书页，每翻一页就看到新的内容，直到翻完整本书'
  }
];

const DEFAULT_METAPHOR = '这是一个代码功能块，输入一些东西，经过处理后输出结果，就像把食材放进料理机，按下按钮就能得到混合好的食物';
