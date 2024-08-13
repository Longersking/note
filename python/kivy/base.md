# 基础

### [Kivy中文编程指南：基础知识 - 《Kivy 1.9.2 中文开发文档帮助手册教程》 - 极客文档 (geekdaxue.co)](https://geekdaxue.co/read/Kivy-doc-zh/02-Kivy-Basics.md)

### 示例代码

## HELLOWORLD

```python
import kivy
kivy.require('1.0.6') # 注意要把这个版本号改变成你现有的Kivy版本号!

from kivy.app import App # 译者注：这里就是从kivy.app包里面导入App类
from kivy.uix.label import Label # 译者注：这里是从kivy.uix.label包中导入Label控件，这里都注意开头字母要大写

class MyApp(App):

    def build(self): # 译者注：这里是实现build()方法
        return Label(text='Hello world') # 译者注：在这个方法里面使用了Label控件

if __name__ == '__main__':
    MyApp().run() # 译者注：这里就是运行了。
```

![image-20240624213639900](http://111.229.225.13:81/i/2024/06/24/zc160o-2.png)

### 代码讲解

```python
from kivy.app import App
```

用于让自定义的app类去继承，导入的类位于kivy安装目录下的app.py文件下

```python
from kivy.uix.label import Label
```

kivy.uix 包 用于容纳用户界面元素标签，比如各种输出布局和控件

kivy生命周期

![image-20240624214159404](http://111.229.225.13:81/i/2024/06/24/zfasgq-2.png)

```python
MyApp().run()
```

相当于启动入口

```python
def build(self):
	return Label(text='Hello world')
```

build函数所处的是要进行初始化和返回根控件的位置。根控件返回的操作在下面这一行中实现



## 实现登录页面

```python
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(GridLayout):


    def __init__(self, **kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Username"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text="Password"))
        self.password = TextInput(multiline=False,password=True)
        self.add_widget(self.password)


class MyApp(App):


    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
```

代码解释

```python
from kivy.uix.gridlayout import GridLayout
```

导入Gridlayout布局，并将Gridlayout类作为基类作为根控件

```python
 class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen,self).__init__(**kwargs)
```

这里通过 _\_init\_\_ 方法传递（self,**kwargs）可传递多参数进行调用，这里一定要用super关键字来覆盖父类方法

结果图

![image-20240624220109862](http://111.229.225.13:81/i/2024/06/24/10ehil2-2.png)

