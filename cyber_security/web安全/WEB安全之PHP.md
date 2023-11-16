## php语言缺陷

[第20天：WEB攻防-PHP特性&缺陷对比函数&CTF考点&CMS审计实例_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1pQ4y1s7kH/?p=20&vd_source=41fa125dd9ad7e3ca523f6b7394846c8)



### 一、等于号缺陷

php中存在三种等于号

=，==，===

=:赋值

==：不会对比类型

===：类型也会比较

例如1 == 1.0

在php中被认为是对的

```php
<?php 
header("Content-Type:text/html;charset=utf-8");
$flag = "you are right!";
$a = '1';
if($a == $_GET['y']){
    echo $flag;
}else{
    echo "error";
}
?>
```

![image-20231115173900676](http://111.229.225.13:81/i/2023/11/15/srdevc-2.png)

可以发现$a = '1'是字符型，传入的是浮点型，但是依旧可以成功

![image-20231115174226188](http://111.229.225.13:81/i/2023/11/15/std0k4-2.png)

修改代码

```php
$a === $_GET['y']
```

![image-20231115174353915](http://111.229.225.13:81/i/2023/11/15/su2fdx-2.png)

发现不行了

总结 == 两边为字符串和数字时，字符串以数字开头时，以开头数字直到字母出现为止作为转换结果，开头不是数字的字符串或者为空则转换为0

布尔值true与任意字符串都相等，除了0

hash值与字符串相比较，例如开头为0e后面全为数字的话，进行比较时就会被当作科学计数法来计算

### 二、MD5 函数缺陷

```php
<?php 

header("Content-Type:text/html;charset=utf-8");
$flag = "you are right!";

if($_GET['username'] != $_GET['password']){
    if((md5($_GET['username'])) == md5($_GET["password"])){
        echo $flag;
    }
}else{
    echo "error";
}
?>
<!-- QNKCDZO

240610708 -->

<!-- 0e830400451993494058024219903391
0e462097431906509019562988736854 -->
```

在于利用 ==特性 因为QNKCDZO

240610708 对应的MD5值分别为0e830400451993494058024219903391
0e462097431906509019562988736854 

而== 比较时，hash值与字符串相比较，例如开头为0e后面全为数字的话，进行比较时就会被当作科学计数法来计算

所以等价于 0 == 0



```php
<?php 

header("Content-Type:text/html;charset=utf-8");
$flag = "you are right!";

if($_GET['username'] != $_GET['password']){
    if((md5($_GET['username'])) === md5($_GET["password"])){
        echo $flag;
    }
}else{
    echo "error";
}
?>
```

像刚才一样

![image-20231115210529925](http://111.229.225.13:81/i/2023/11/15/ytg690-2.png)

会发现无法绕过

所以采用数组传值的方式

![image-20231115210617252](http://111.229.225.13:81/i/2023/11/15/ytyye0-2.png)

如果改用 === 时，可以利用md5函数的特性

在php中md5函数无法处理数组类型，md5(数组)会返回null 所以等价于null === null 

成功绕过

### 三、intval函数缺陷

引用[PHP intval()函数详解，intval()函数漏洞原理及绕过思路_intval绕过-CSDN博客](https://blog.csdn.net/wangyuxiang946/article/details/131156104)



1.intval 函数可以获取变量的整数值。**常用于强制类型转换**

语法 int  intval($var,$base)

$var:需要转换成integer的**变量**

$base:转换所使用的**进制**

$base允许为空值

此时会根据$var的格式来调整转换的进制

- 如果$var以0开头，就使用8进制
- 如果$var以0x开头，就使用16进制
- 否则，就使用十进制

绕过思路：当某一个数字被过滤时，可以使用它的8进制或者16进制来绕过

2.intval转换数组类型时，不关心数组中的内容，只判断数组中有没有元素

空数组返回0

非空返回1

3.转换小数时，只返回个位数，不遵循四舍五入原则

绕过思路，当某一个数字被过滤时可以给他增加小数位来绕过

4.转换字符串

intval转换字符串类型时就会判断字符串是否以数字开头

如果以数字开头，就返回1个或者多个连续的数字

5.支持取反~符号

intval函数可以支持特殊符号

var_dump(intval(~10)) => int(-11)

**(这里确实对于 -11)**

var_dump(intval(~~10)) => int(10)

绕过思路：当某一个数字被过滤时，可以通过两次取反操作绕过

6.算数运算符

intval支持算数运算符

var_dump(intval(05+5)) => int(10)

绕过思路，算数运算符

7.浮点数精度丢失问题

var_dump(intval(0.58*100.0)) =>  int(57)

### 四、strpos函数

  寻找某个字符串在整个字符串出现的起始位置

可以通过特殊编码绕过

例如 %0a666