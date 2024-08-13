## 大小和位置

## 大小

- size_hint属性只能传入0-1之间的值，代表宽（高）与当前窗口的宽（高）的比例
- 例如size_hint:0.2,0.15 可以省略写为size_hint:.2,.15

在kv文件中写法

```python
size_hint:.2,.15
```

## 位置

- pos_hint属性通过比例值（0-1）进行设置。比例计算方式为将窗口看作是一个以左下角为起点（0，0）的坐标系。横轴为x轴，纵轴为y轴。例如窗口大小为w,高度为h,那么窗口内任意一点的值为[y/w,x/h]

- 对于一个控件：

  1. x轴上面需要确定三个点：左边界的x点，中间点的center_x，右边界right;

  2. y轴上面需要确定三个点：上边界top、正中间center_y，下边界y点

     ![](http://111.229.225.13:81/i/2024/07/12/sfrd85-2.png)

​		3.传入方式字典传值：pos_hint:{'x':0.2,'y':.6}  pos_hint:{'x':0.2,'y':.6}

​		py文件

```python
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class PosSet(FloatLayout):
    def __init__(self, **kwargs):
        super(PosSet, self).__init__(**kwargs)


class MainApp(App):
    def build(self):
        return PosSet()


if __name__ == '__main__':
    MainApp().run()

```



​	

​		kv文件

```python
<PosSet>:
    Button:
        text:"位置"
        #设置按钮大小
        size_hint:.2,.15
        #按钮位置
        pos_hint:{'x':0.2,'y':.6}
    Button:
        text:"位置"
        size_hint:.2,.15
       pos_hint:{'x':0.2,'y':.6}
```

![image-20240712172243521](http://111.229.225.13:81/i/2024/07/12/si2lr9-2.png)