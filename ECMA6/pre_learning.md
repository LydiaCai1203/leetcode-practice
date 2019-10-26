# JavaScript(学习ECMA6之前的预热)

[TOC]
## 1.导论
    轻量级的脚本语言，不具备开发操作系统的能力，只能用来编写控制其它大型应用程序（浏览器）的脚本。JavaScript只能用来做数学和逻辑运算，本身不提供任何和I/O相关的API，都要靠宿主环境来提供，也就是说只能去调用宿主环境提供的底层的API。

### 1.1 JavaScript的宿主环境
    浏览器 还有 node项目。

### 1.2 JavaScript是什么类型的语言
    面向对象 + 函数式编程 语言。

### 1.3 JavaScript的核心语法
+ 1. 基本的语法构造
    + 操作符、控制结构、语句
+ 2. 标准库
    + Array、Date、Math
+ 3. 宿主环境提供的API（浏览器为例）
    + 浏览器控制类：操作浏览器
    + DOM类：操作网页的各种元素
    + Web类：实现互联网的各种功能
+ 4. 宿主环境提供的API（node环境为例）
    提供服务端环境的API，也就是提供操作系统的API
    + 文件操作API
    + 网络通信API
    + 等等

## 2. 为什么要学习JavaScript
    简单好学有前途，that's all。

### 2.1 广泛的使用领域--浏览器平台化
    由于浏览器的能力越来越强，不仅仅是浏览网页，还能操作本地文件，操作图片，调用摄像头等等功能。所以JavaScript可以完成更多的功能。

### 2.2 Node
    Node项目使得JavaScript可以用于开发大型的服务器的项目。

### 2.3 数据库操作
    NoSQL的概念是在JSON的概念上出现的，大部分的NoSQL数据库是可以由JavaScript来进行操作的。

### 2.4 移动平台开发
    Facebook 公司的 React Native 项目则是将 JavaScript 写的组件，编译成原生组件，从而使它们具备优秀的性能。

### 2.5 内嵌脚本语言
    越来越多的应用程序，将 JavaScript 作为内嵌的脚本语言，比如 Adobe 公司的著名 PDF 阅读器 Acrobat、Linux 桌面环境 GNOME 3。

### 2.6 跨平台的桌面应用程序
    Chromium OS、Windows 8 等操作系统直接支持 JavaScript 编写应用程序。
    好像很厉害的样子。

## 3. others
+ 1. opt + 花键 + I 直接打开chrome的控制台
+ 2. shift + enter 仅换行 不执行

## 4. 基本语法
+ **语句**
    + ; 表示语句结束
    + 三个空语句 == `;;;`
    + 多行语句可以写在同一行
+ **变量**
    + 变量是对值的具名引用
    + 如果只是声明一个对象`var a;`但是没有赋值，对象a的值就是`undefined`,`undefined`是一个实际存在的对象
    + `var a = 1; <=> a = 1;`
    + `var a, b;`
    + `var a=1; a='hello'` 动态类型语言
    + `var`重复声明对象无效
    + *变量提升*
        JavaScript引擎的工作方式就是先解析代码，然后获取所有声明的变量，再一行一行运行。
```javascript
var a;
console.log(a)     // undefined
a = 1;

console.log(a);    //1 不会报错 但是 是错误的做法
var a = 1;
```
+ **标识符**
    + 标识符的意思就是用来识别各种值的合法名称。
    + 命名规则:
        + 第一个字符：任意的Unicode字符 or `$` or `_`
        + 其它字符：任意Unicode字符 or `$` or numbers or `_`
        + of course 中文也是合法的字符
+ **注释**
    + 单行注释: `//`
    + 多行注释: `/* */`
    + 单行注释 支持HTML的注释：`<!--` `-->`
```javascript
x = 1; <!-- x = 2;
--> x = 3;
// 只有 x = 1; 才会被执行到，-->只有在行首，才有注释的作用，否则会被当成是正常的运算

function countdown(n) {
  while (n --> 0) console.log(n);
}
// 上述写法等价于  真牛皮 还是python好
function countdown(n) {
  while (n-- > 0) console.log(n);
}
```
+ **区块**
    + `{}` 可以将多条语句组合在一起，变成block，对于`var`命令来说，区块不具备变量域。
```javascript
{
    var a = 1;
}
a // 1
```
+ **条件语句**
    + `if`结构
    + `switch`结构
```javascript
if (m === 3) {                // 可以多行
  m += 1;
}

if (expression) statement;    // 可以一行

if (expression)
    statement;

// =(赋值表达式) ==(相等运算符) ===(严格相等运算符 优先采用)
if (x = 2) { // 不报错
if (2 = x) { // 报错

if (m === 3) {
  // 满足条件时，执行的语句
} else {
  // 不满足条件时，执行的语句
}

if (m === 0) {
  // ...
} else if (m === 1) {
  // ...
} else if (m === 2) {
  // ...
} else {
  // ...
}
```
```javascript
var x = 1;

switch (x) {
  case 1:                     // 内部使用的是 ===，在比较的时候不会发生类型转换
    console.log('x 等于1');
  case 2:
    console.log('x 等于2');
  default:
    console.log('x 等于其他值');
}
// x等于1
// x等于2
// x等于其他值
```

+ **三元运算符**
    + `var even = (n % 2 === 0) ? true : false;`
    + 上面这条语句甚至可以写成三行，厉害了。不知道Python可不可以。  
+ **循环语句**
    + `while`循环
    + `for`循环
    + `do while`循环
```javascript
while (true) {
  console.log('Hello, world');
}

for (var i = 0; i < 3; i++) {
  console.log(i);
}

for ( ; ; ) {        // 相当于是while(true) 这不合理啊这
  console.log(i);
}

var x = 3;
var i = 0;

do {
  console.log(i);
  i++;
} while(i < x);      // 至少循环一次 注意while后面的分号
```
+ **break 和 continue 语句**
    + 没啥特别的，一般含义，但是可以带参数，真牛逼。
+ **标签label**
```javascript
top:
  for (var i = 0; i < 3; i++){
    for (var j = 0; j < 3; j++){
      if (i === 1 && j === 1) break top;
      console.log('i=' + i + ', j=' + j);
    }
  }
// i=0, j=0
// i=0, j=1
// i=0, j=2
// i=1, j=0

foo: {
  console.log(1);
  break foo;
  console.log('本行不会输出');
}
console.log(2);
// 1
// 2

top:
  for (var i = 0; i < 3; i++){
    for (var j = 0; j < 3; j++){
      if (i === 1 && j === 1) continue top;
      console.log('i=' + i + ', j=' + j);
    }
  }
// i=0, j=0
// i=0, j=1
// i=0, j=2
// i=1, j=0
// i=2, j=0
// i=2, j=1
// i=2, j=2

// 这是屎一样的语法.......
```
## 5. 数据类型
+ **number**: 整数 or 小数
+ **string**
+ **boolean**: true or false
+ **undefined**: 未定义 or 不存在
+ **null**: 空值
+ **object**: 各种值的集合
    + 狭义的对象object
    + array
    + function

### 5.1 查看数据类型的运算符
+ **typeof**
+ **instanceof**
+ **Object.prototype.toString**
```javascript
//--------typeof-----------
typeof 123; // "number"
typeof '123'; // "string"
typeof false; // "boolean"
typeof undefined; // "undefined"

// 正确的写法
if (typeof v === "undefined") {
  // ...
}

typeof window; // "object"
typeof {}; // "object"
typeof []; // "object"
typeof null; // "object"

//-------instanceof---------
var o = {};
var a = [];

o instanceof Array; // false
a instanceof Array; // true
```

### 5.2 null、undefined
+ 1. `null` 和 `undefined` 都可以表示'没有'。语法效果几乎没有区别。
+ 2. `undefined == null` // true
+ 3. `undefined == false` // false 也就是说不相等 不会做什么所谓的类型转换
+ 4. `if (undefined)` // if里面判断undefined为false
+ 5. 这么奇葩的设计竟然也是历史原因，因为一开始模仿的Java, Java里面有null，所以javascript里面一开始也是使用的null
+ 6. `null + 1` // null会被转换为0，所以结果为1
+ 7. `undefined + 1` // 结果就是NaN，因为是无定义对象
+ 8. 着重看一下`undefined`的用法, 好奇怪啊！！！！！！
```javascript
// 变量声明了，但没有赋值
var i;
i // undefined

// 调用函数时，应该提供的参数没有提供，该参数等于 undefined
function f(x) {
  return x;
}
f() // undefined

// 对象没有赋值的属性
var  o = new Object();
o.p // undefined

// 函数没有返回值时，默认返回 undefined
function f() {}
f() // undefined
```
### 5.3 布尔值
+ **下列操作会返回布尔值**
    + 前置逻辑运算符： `! (Not)`
    + 相等运算符：`===`，`!==`，`==`，`!=`
    + 比较运算符：`>`，`>=`，`<`，`<=`
+ **转换规则是除了下面六个值被转为`false`，其他值都视为`true`**
    + `undefined`
    + `null`
    + `false`
    + `0`
    + `NaN`
    + " " or ' '
+ 真鸡儿有毒，`if([])` or `if({})`会被当作是true来对待。这怎么记得住啊。

### 5.4 数值
+ **整数和浮点数**
    
        在javascript中所有的数值都是以64位浮点数形式存储的。所以1 === 1.0的结果为true`。

    + 某些运算只有整数才能完成，此时javascript会将64位浮点数转换为32位整数
    + `1.0 + 2.0 === 3.0` 由于小数是不精确的，所以结果位false
    + `3.0/1.0` 结果不是精确的 要小心
    + `(0.3 - 0.2) === (0.2 - 0.1)` of course 是false

+ **数值精度**

        javascript 是64位浮点数。绝对值小于2的53次方的整数，都可以精确表示。由于2的53次方是一个16位的十进制数值，所以简单的法则就是，JavaScript 对15位的十进制数都可以 精确处理。
    
    + 第一位：表示正负
    + 第二位到第十二位：指数部分
    + 第十三位到第64位：小数的部分，也就是有效数字

+ **数值范围**

        64位浮点数的指数部分的值最大为2047，分出一半表示负数，则 JavaScript 能够表示的数值范围为21024到2-1023（开区间），超出这个范围的数无法表示。
    
    + `Math.pow(2, 1024)`   // Infinity
    + `Math.pow(2, -1075)`  // 0
    + 如果一个数字很小很小的时候，javascript也会将其表示为0
    + `Number.MAX_VALUE` // 1.7976931348623157e+308
      `Number.MIN_VALUE` // 5e-324

+ **数值的表示法**
    + 123e3 // 123000
      123e-3 // 0.123
      -3.1E+12
      .1e-23
+ **数值的进制**
    + 0xff // 255 十六进制
    + 0o377 // 255 八进制
    + 0b11 // 3 二进制
    + 通常来说，有前导0的数值会被视为八进制，但是如果前导0后面有数字8和9，则该数值被视为十进制。但是ES5的严格模式和ES6都已经废除了这种语法
+ **特殊的数值**
    + 两个0: +0 和 -0，不过这两个0都是等价的。但是 `(1 / +0) === (1 / -0) // false`。我真的不理解为啥这么多人用js，这么难用。
    + `(1 / +0)` 是 `+Infinity` 和 `(1 / -0)` 是 `-Infinity`
    + **NaN**
        
            NaN是javascript的特殊值，表示not number，主要出现在将字符串解析成数字出错的场合
        + `5 - 'x'`  // NaN
        + `Math.acos(2)`  // NaN
        + `0 / 0`  // NaN
        + 需要注意的是，`NaN`不是独立的数据类型，而是一个特殊数值，它的数据类型依然属于`Number`，使用`typeof`运算符可以看得很清楚
        + `NaN`不等于任何值，包括它本身
        + `[NaN].indexOf(NaN)`   // -1 indexof内部使用的是===
        + `Boolean(NaN)`   // false
        + `NaN`与任何数（包括它自己）的运算，得到的都是`NaN`。
    + **infinity**
        
            Infinity表示无穷，用来表示两种场景，一种是无穷大，一种是无穷小。如鬼非0的数值除以0，得到的也是Infinity。数字的正向溢出和负向溢出竟然都不会报错，有必要搞得这么复杂吗？？？？？？？？？？？？
        + `Math.pow(2, 1024)`
        + `0 / 0`   // NaN
        + `1 / 0 `  // Infinity
        + `1 / -0` // -Infinity
        + `Infinity > 1000`   // true
        + `-Infinity < 1000`   // true
        + `Infinity`与`NaN`比较，总是返回`false`
        + Infinity的四则运算，符合无穷的数学计算规则。`5 / Infinity`   // 0
        + `0 * Infinity`   // NaN
        + `0 / Infinity`   // 0
        + `infinity / 0`    // Infinity
        + 还有很多的规则 实在是让人摸不着头脑，暂时不写了，真的好坑。
+ **与数值相关的全局方法**
    + parseInt()
    + parseFloat()
    + isNaN() isNaN只对数值有效，如果传入其他值，会被先转成数值
    + isFinite() 方法返回一个布尔值，表示某个值是否为正常的数值
### 5.5 字符串
+ 双引号里面使用双引号也要使用\转义
+ HTML里面属性值使用双引号，所以js里面规定字符串要使用单引号
+ 一对双引号只能写单行字符串，如果写多行，要用\反斜杠
+ 多行字符串也可以用+来串联
```javascript
(function () { /*
line 1
line 2
line 3
*/}).toString().split('\n').slice(1, -1).join('\n')
// "line 1
// line 2
// line 3"
```
### 5.6 字符串与数组
+ 字符串可以被视为字符数组
+ 如果方括号中的数字超过字符串的长度，或者方括号中根本不是数字，则返回undefined
+ 无法改变字符串之中的单个字符
+ `var s = 'hello'; s.length`   // 5 该属性length也是无法改变的 竟然不会报错
### 5.7 字符集
    总结一下，对于码点在U+10000到U+10FFFF之间的字符，JavaScript 总是认为它们是两个字符（length属性为2）。所以处理的时候，必须把这一点考虑在内，也就是说，JavaScript 返回的字符串长度可能是不正确的。
### 5.8 Base64 转码
    所谓 Base64 就是一种编码方法，可以将任意值转成 0～9、A～Z、a-z、+和/这64个字符组成的可打印字符。使用它的主要目的，不是为了加密，而是为了不出现特殊字符，简化程序的处理。
+ `btoa()`：任意值转为 Base64 编码
+ `atob()`：Base64 编码转为原来的值
+ 注意，这两个方法不适合非 ASCII 码的字符，会报错。
+ 要将非 ASCII 码字符转为 Base64 编码，必须中间插入一个转码环节，再使用这两个方法
```javascript
function b64Encode(str) {
  return btoa(encodeURIComponent(str));
}

function b64Decode(str) {
  return decodeURIComponent(atob(str));
}

b64Encode('你好') // "JUU0JUJEJUEwJUU1JUE1JUJE"
b64Decode('JUU0JUJEJUEwJUU1JUE1JUJE') // "你好"
```
## 6. 对象
```javascript
var obj = {
  foo: 'Hello',
  bar: 'World'
};
```
+ 1. 如果键名是数值，会被自动转为字符串。
+ 2. 如果键名不符合标识名的条件（比如第一个字符为数字，或者含有空格或运算符），且也不是数字，则必须加上引号，否则会报错。
+ 3. 如果一个属性的值为函数，通常把这个属性称为“方法”，它可以像函数那样调用。
```javascript
var obj = {
  p: function (x) {
    return 2 * x;
  }
};

obj.p(1) // 2
```
+ 4. 如果属性的值还是一个对象，就形成了链式引用。
```javascript
var o1 = {};
var o2 = { bar: 'hello' };

o1.foo = o2;
o1.foo.bar // "hello"
```
+ 5. 对象的属性之间用逗号分隔，最后一个属性后面可以加逗号（trailing comma），也可以不加。
+ 6. 属性可以动态创建，不必在对象声明时就指定。

### 6.1 对象的引用
    如果不同的变量名指向同一个对象，那么它们都是这个对象的引用，也就是说指向同一个内存地址。修改其中一个变量，会影响到其他所有变量。这种引用只局限于对象，如果两个变量指向同一个原始类型的值。那么，变量这时都是值的拷贝。

### 6.2 表达式还是语句
    对象采用大括号表示，这导致了一个问题：如果行首是一个大括号，它到底是表达式还是语句？
+ `{ foo: 123 }`

        JavaScript 引擎读到上面这行代码，会发现可能有两种含义。第一种可能是，这是一个表达式，表示一个包含foo属性的对象；第二种可能是，这是一个语句，表示一个代码区块，里面有一个标签foo，指向表达式123。
+ 当javascript引擎无法确定是表达式还是语句的时候，一律解释成语句。
+ `{ console.log(123) }` // 123
+ 如果要解释为对象，最好在大括号前加上圆括号。因为圆括号的里面，只能是表达式，所以确保大括号只能解释为对象。
+ `({ foo: 123 })`  // 正确
+ `eval('{foo: 123}')` // 123  eval()函数是对字符串求值
+ `eval('({foo: 123})')` // {foo: 123}

### 6.3 属性的操作
    读取对象的属性，有两种方法，一种是使用点运算符，还有一种是使用方括号运算符。属性名会被转换成字符串，但是如果是数字作为键名，就不能使用点运算符了。
```javascript
var obj = {
  7: 'Hello World'
};

obj['7'] // "Hello World"
obj[3+4] // "Hello World"
```
+ 1. 属性支持后绑定
+ 2. Object.keys(obj) 可以打印出一个对象所有的属性
+ 3. delete obj.p 可以删除对象的属性。真的有毒，删除一个对象不存在的属性，不会报错，还会返回true。只有在删除不能删除的对象的属性的时候，才会返回false。
```javascript
var obj = Object.defineProperty({}, 'p', {
  value: 123,
  configurable: false
});

obj.p // 123
delete obj.p // false
```
+ 4. delete命令不能删除继承的属性，只能删除对象本身的属性。
+ 5. delete命令返回true的情况下，还是有可能访问到被删除的属性。比如delete obj.toString
+ 6. 检查属性是否存在:`var obj = { p: 1 };'p' in obj;`   // true
+ 7. 判断属性是否属于对象本身：`obj.hasOwnProperty('toString')`
+ 8. 属性的遍历: `for (var i in obj) {}`  // 但是会遍历对象可遍历的属性，跳过不可遍历的属性。不仅会遍历自身的属性，还是遍历继承来的属性。但是toString不会被遍历到，因为继承来的是不可遍历的属性，如果继承来的是可遍历的，就会被打印出来了。

### 6.4 with语句(并不建议使用)
    目的就是为了操作同一个对象的多个属性时，提供一些书写方便。
```javascript
var obj = {
  p1: 1,
  p2: 2,
};
with (obj) {
  p1 = 4;
  p2 = 5;
}
// 等同于
obj.p1 = 4;
obj.p2 = 5;
```
```javascript
// 例二
with (document.links[0]){
  console.log(href);
  console.log(title);
  console.log(style);
}
// 等同于
console.log(document.links[0].href);
console.log(document.links[0].title);
console.log(document.links[0].style);
```
+ 1. 注意，如果with区块内部有变量的赋值操作，必须是当前对象已经存在的属性，否则会创造一个当前作用域的全局变量。
```javascript
var obj = {};
with (obj) {
  p1 = 4;
  p2 = 5;
}

obj.p1 // undefined
p1 // 4
```

## 7. 函数

### 7.1 函数的声明
+ 1. function
```javascript
function print(s) {
  console.log(s);
}
```
+ 2. 函数表达式: 其实就是将匿名函数赋值给一个变量
```javascript
var print = function(s) {
  console.log(s);
};

// 如果在表达式里面带上了函数名，这个函数名只在函数体内部有效，在外部无效
var print = function x(s) {
  console.log(s);
};   // 注意这个分号，因为这个是函数表达式，这是个表达式

x    // ReferenceError: x is not defined  
```
+ 3. Function构造函数
    你可以传递任意数量的参数给Function构造函数，只有最后一个参数会被当做函数体，如果只有一个参数，该参数就是函数体。Function构造函数可以不使用new命令，返回结果完全一样。这种方式声明函数还很不直观，所以几乎没有人用。
```javascript
var add = new Function(
  'x',
  'y',
  'return x + y'
);

// 等同于
function add(x, y) {
  return x + y;
}

//--------------------------------
var foo = new Function(
  'return "hello world";'
);

// 等同于
function foo() {
  return 'hello world';
}
```

### 7.2 函数的重复声明
    重复声明由于变量提升，后面的f会覆盖前面的f，而且还不会报错。牛皮。
```javascript
function f() {
  console.log(1);
}
f() // 2

function f() {
  console.log(2);
}
f() // 2
```

### 7.3 圆括号运算符，return语句和递归
    return语句不是必需的，如果没有的话，该函数就不返回任何值，或者说返回undefine。函数可以调用自身，这就是递归（recursion）。

### 7.4 第一等公民
    由于函数与其他数据类型地位平等，所以在 JavaScript 语言中又称函数为第一等公民。
```javascript
function add(x, y) {
  return x + y;
}

// 将函数赋值给一个变量
var operator = add;

// 将函数作为参数和返回值
function a(op){
  return op;
}
a(add)(1, 1)
```

### 7.5 函数名的提升
    JavaScript 引擎将函数名视同变量名，所以采用function命令声明函数时，整个函数会像变量声明一样，被提升到代码头部。
```javascript
// 不会报错
f();
function f() {}

// 会报错
f();
var f = function (){};

// 不会报错
var f = function () {
  console.log('1');
}
function f() {
  console.log('2');
}
f()    // 1
```
**采用函数表达式的话，就不存在函数名提升的问题了。所以一般都是用函数表达式。**

### 7.6 函数的属性和方法
+ 1. **name 属性**
    
            返回函数的变量名；如果通过函数表达式，且是匿名函数，返回的就是变量名。如果是函数表达式，但是不是用匿名函数的话，返回的就不是变量名。
+ 2. **length 属性**：

            返回的是传入函数预期的参数个数。也就是形参个数。
+ 3. **toString 属性**：

            返回的是函数的源码，以字符串的形式返回。甚至可以利用这点，打印多行字符串。

### 7.7 函数的作用域
    需要注意的是，对于var命令而言，局部变量只能在函数内部声明，如果是在语句块中使用var进行声明的话，一律都是按照全局变量处理。
+ 1. 全局作用域（整个程序中都存在，任何地方都可以使用）
+ 2. 函数作用域（只在函数内部存在）
+ 3. 块级作用域(ES6新增)

### 7.8 函数内部的变量提升
    但凡是在函数内部使用var声明的变量，都会被提升到函数的头部。
```javascript
function foo(x) {
  if (x > 100) {
    var tmp = x - 100;
  }
}

// 等同于
function foo(x) {
  var tmp;
  if (x > 100) {
    tmp = x - 100;
  };
}
```

### 7.9 函数本身的作用域
    函数本身也是一个值，也有自己的作用域。它的作用域和变量一样，都是在其声明时候所在的作用域，和其运行时候的作用域无关。
```javascript
var a = 1;
var x = function () {
  console.log(a);
};

function f() {
  var a = 2;
  x();
}

f() // 1
```
```javascript
function foo() {
  var x = 1;
  function bar() {
    console.log(x);
  }
  return bar;
}

var x = 2;
var f = foo();
f() // 1
```

### 7.10 参数
+ 1. **参数的省略**
```javascript
function f(a, b) {
  return a;
}
f(); f(1); f(1, 2);   // 都是可以的，牛皮，省略的参数值就是undefined
f(undefined, 1)       // 如果想省略之前的参数，只能这样调用
```
+ 2. **传递参数，老生常谈，就是值传递 和 引用传递 的区别。**
```javascript
var obj = [1, 2, 3];

function f(o) {
  o = [2, 3, 4];
}
f(obj);

obj // [1, 2, 3]
```
+ 3. **同名参数**
```javascript
function f(a, a) {
  console.log(a);
}
f(1, 2) // 2

//-------------------------
function f(a, a) {
  console.log(a);
}
f(1) // undefined

//-------------------------
function f(a, a) {
  console.log(arguments[0]);
}
f(1) // 1 注意只有这样才可以取到第一个参数
```
+ 4. **arguments对象**

            arguments对象包含了函数运行时的所有参数，arguments[0]就是第一个参数，arguments[1]就是第二个参数，以此类推。这个对象只有在函数体内部，才可以使用。正常模式下，arguments对象可以在运行时修改。
```javascript
var f = function(a, b) {
  'use strict';            // 开启严格模式 注意这里！！！严格模式！！！
  arguments[0] = 3;
  arguments[1] = 2;
  return a + b;
}
f(1, 1) // 2 不可以修改
```
```javascript
function f() {
  return arguments.length;     // 可以在运行时获取实际参数的个数
}

f(1, 2, 3) // 3
f(1) // 1
f() // 0
```
+ 5. **再谈arguments和数组的关系**

            需要注意的是，虽然arguments很像数组，但它是一个对象。数组专有的方法（比如slice和forEach），不能在arguments对象上直接使用。如果要让arguments对象使用数组方法，真正的解决方法是将arguments转为真正的数组。下面是两种常用的转换方法：slice方法和逐一填入新数组。
```javascript
var args = Array.prototype.slice.call(arguments);

// 或者
var args = [];
for (var i = 0; i < arguments.length; i++) {
  args.push(arguments[i]);
}
```
+ 6. **arguments 的 callee 属性**

            arguments对象带有一个callee属性，返回它所对应的原函数。

### 7.11 闭包
    由于函数只有函数作用域和全局作用域，在函数内部是可以访问到全局作用域的变量的。但是在函数外部是无法访问到函数内部的变量的。如何在一个函数中访问另一个函数中的变量，只能通过在一个函数里面定义另一个函数。
```javascript
function f1() {
  var n = 999;
  function f2() {
　　console.log(n); // 999
  }
}
```
    但是上述的代码有一个缺点，f2虽然可以访问到f1中的变量，但是f1无法访问f2中的变量。这就是 JavaScript 语言特有的"链式作用域"结构（chain scope），子对象会一级一级地向上寻找所有父对象的变量。所以，父对象的所有变量，对子对象都是可见的，反之则不成立。
```javascript
function f1() {
  var n = 999;
  function f2() {
    console.log(n);
  }
  return f2;
}

var result = f1();
result(); // 999
```
    既然f2可以读取f1的变量，那么把f2返回，不就以为可以在f1外部调用f1中的变量了吗？由此就是必包的作用。在这里闭包就是f2，闭包的最大特点就是可以记住"诞生"的环境，在本质上，闭包就是将函数内部，和函数外部，连接在一起的一个桥梁。
+ **闭包最大的用处**
    + 1. 可以读取函数内部的变量
    + 2. 可以让这些变量始终保持在内存中，闭包可以使得它诞生的环境一直存在
```javascript
function createIncrementor(start) {
  return function () {
    return start++;
  };
}

var inc = createIncrementor(5);

inc() // 5
inc() // 6
inc() // 7
// 这么说的话好像还是挺神奇的.......
```
+ + 还有就是封装对象的私有属性和方法
```javascript
function Person(name) {
  var _age;
  function setAge(n) {
    _age = n;
  }
  function getAge() {
    return _age;
  }

  return {
    name: name,
    getAge: getAge,
    setAge: setAge
  };
}

var p1 = Person('张三');
p1.setAge(25);
p1.getAge() // 25
```

### 7.12 立即调用的函数表达式
    JavaScript 引擎看到行首是function关键字之后，认为这一段都是函数的定义，不应该以圆括号结尾，所以就报错了。解决方法就是不要让function出现在行首，让引擎将其理解成一个表达式。最简单的处理，就是将其放在一个圆括号里面。
```javascript
// 立即调用的函数表达式
(function(){ /* code */ }());
// 或者
(function(){ /* code */ })();
```
```javascript
var i = function(){ return 10; }();
true && function(){ /* code */ }();
0, function(){ /* code */ }();
```
```javascript
!function () { /* code */ }();
~function () { /* code */ }();
-function () { /* code */ }();
+function () { /* code */ }();
```

### 7.13 eval 命令
+ 基本用法
    
            接受一个字符串作为参数，并将这个字符串当作语句执行。eval('var a = 1;');a // 1
+ 如果参数字符串无法当作语句运行，那么就会报错。
+ 如果eval的参数不是字符串，那么会原样返回。`eval(123) // 123`
+ eval没有自己的作用域，都在当前作用域内执行，因此可能会修改当前作用域的变量的值，造成安全问题。但是如果使用严格模式，就不会影响到当前作用域的其它变量了。
```javascript
(function f() {
  'use strict';
  eval('var foo = 123');
  console.log(foo);  // ReferenceError: foo is not defined
})()

//---------------------
(function f() {
  'use strict';
  var foo = 1;
  eval('foo = 2');
  console.log(foo);  // 2 但是依旧可以对当前作用域中存在的变量做读写
})()
```
+ eval的本质是在当前作用域之中，注入代码。由于安全风险和不利于 JavaScript 引擎优化执行速度，所以一般不推荐使用。


### 7.14 eval 的别名调用
```javascript
// 这是eval的别名调用
var m = eval;
m('var x = 1');
x // 1
```
+ 1. JavaScript 的标准规定，凡是使用别名执行eval，eval内部一律是全局作用域。
```javascript
// 下面的这些调用都是全局调用
eval.call(null, '...')
window.eval('...')
(1, eval)('...')
(eval, eval)('...')
```

## 8. 数组
### 8.1 