# WEB安全之python

## python-pyc反编译

python类似java一样，存在编译过程，先将源码文件*.py编译成

*.pyc文件，然后通过python解释器执行

- 生成pyc文件

  创建一个py文件随便输入几句代码(1.py)

  ![image-20231122212024225](http://111.229.225.13:81/i/2023/11/22/z2dkoe-2.png)

  

  通过python交互终端

  ```python
  >>>import py_compile
  >>>py_compile.compile("1.py")
  ```

  ![image-20231122212201574](http://111.229.225.13:81/i/2023/11/22/z3e93u-2.png)

  ![image-20231122212244806](http://111.229.225.13:81/i/2023/11/22/z3n8mh-2.png)

  文件对应的目录会生成一个文件夹，里面就是pyc文件

  ![image-20231122212403745](http://111.229.225.13:81/i/2023/11/22/z4l791-2.png)

  或者使用python -m py_compile 1.py

  python -m compileall 存放py文件目录

- 反编译pyc，将pyc文件转换为py文件

  安装uncompyle库

  命令行

  ```
  uncompyle6  1.pyc > 2.py
  ```

  此方法尝试没有成功

  或者使用在线工具
  
  [python反编译 - 在线工具 (tool.lu)](https://tool.lu/pyc/)
  
  
  
  
  
  

## ssti漏洞

本质上属于一种注入类型漏洞

**出现原因**：没有对用户输入的参数做校验，代码不够严谨，存在可控参数被用户调用

**出现场景**：使用模板引擎开发的web应用，使得攻击者可以利用原生模板的语法进行攻击，php中tp，java中spring，python中Flask框架等均可能出现此漏洞，多见于插件，页面模板，包括404页面

**判断漏洞**：将payload载入可传参的地方，通过页面渲染的结果进行判断payload是否被编译

**搭建测试环境**：python3.11.5 + vscode + flask

```python
from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.route('/')
def index():
    char = request.args.get('key')
    html = '<h1>Welcome, %s !</h1>' % char
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)


```



![image-20231125143316289](http://111.229.225.13:81/i/2023/11/25/npbp7x-2.png)

**相关利用的魔术方法** 

通过

| \__class\__      | 查看当前对象的当前类                    |
| ---------------- | --------------------------------------- |
| \__base\__       | 查找当前类的父类                        |
| \__mro\__        | 查找当前类的所有继承类                  |
| \__subclasses\__ | 查找父类下的所以子类                    |
| \__init\__       | 查看类是否重载，出现wrapper表示没有重载 |
| \__globals\__    | 以字典的形式返回当前对象的全部全局变量  |
| \__builtins\__   | 提供对python的所以内置标识符的直接访问  |

可以构造一些危害较大的payload

![image-20231125145354010](http://111.229.225.13:81/i/2023/11/25/o1exp2-2.png)