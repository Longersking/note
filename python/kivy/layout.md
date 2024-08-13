# Layout

## FloatLayout布局

### 特点：允许将子部件通过位置和尺寸放置在窗口的任意位置。在不同分辨率移动设备中，当窗口尺寸改变时，放置在窗口的子部件也会相应地调整大小和位置。不会因窗口大小的改变使布局变地一团糟。

### 在kv中使用此布局

### kv文件

```python
<Button>:
    font_size:40
    size_hint:0.3,0.3

<FloatLayoutWidget>:
    canvas:
        Color:
            rgba:[1,1,1,1]
        Rectangle:
            size:self.size
            pos:self.pos

    Button:
        text:"按钮0"
        background_color:0.1,0.5,0.6,1
        pos_hint:{'x':0,'top':1}
    Button:
        text:"按钮1"
        background_color:0.1,0.5,0.6,1
        pos_hint:{'center_x':0.5,'center_y':0.5}
    Button:
        text:"按钮2"
        background_color:0.1,0.5,0.6,1
        pos_hint:{'right':1,'y':0}
    Button:
        text:"按钮3"
        background_color:0.1,0.5,0.6,1
        pos_hint:{'right':1,'top':1}
    Button:
        text:"按钮4"
        background_color:0.1,0.5,0.6,1
        pos_hint:{'x':0,'y':0}
```

### py文件

```python
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class FloatLayoutWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatLayoutWidget, self).__init__(**kwargs)


class FloatLayoutApp(App):
    def build(self):
        return FloatLayoutWidget()


if __name__ == '__main__':
    FloatLayoutApp().run()
```

![image-20240713001138590](http://111.229.225.13:81/i/2024/07/13/6smty-2.png)

### BoxLayout

### 特点：是一种可以将子部件水平或者垂直排列的布局。类似Android中的线性布局，子部件将会以10像素的间距平分父窗口的大小

### 在kivy中使用此布局

py

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class BoxLayoutWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayoutWidget, self).__init__(**kwargs)


class MainApp(App):
    def build(self):
        return BoxLayoutWidget()

if __name__ == '__main__':
    MainApp().run()
```

kv

```python
<BoxLayoutWidget>:
    Button:
        text:"按钮0"
        background_color:0,1,1,1
        font_size:40
    Button:
        text:"按钮1"
        background_color:0,1,1,1
        font_size:20
    Button:
        text:"按钮2"
        background_color:0,1,1,1
        font_size:35
    Button:
        text:"按钮3"
        background_color:0,1,1,1
        font_size:30
    Button:
        text:"按钮4"
        background_color:0,1,1,1
        font_size:25
```

![image-20240713003754002](http://111.229.225.13:81/i/2024/07/13/mcziv-2.png)

###  BoxLayout布局默认水平方向(horizontal)，可以指定orientation属性来设置方向，改为垂直方向

```python
layout = BoxLayout(orientation='vertical')
```

 在.kv文件中，把上面的'='替换为':'即可。如：box.kv内输入以下内容：

```python
<BoxLayoutWidget>:
	
	orientation:'vertical'
	canvas:
		Color:
			rgba:[1,1,1,1]
		Rectangle:
			size:self.size
			pos:self.pos
	
	Button:
		
		text:'Hello'
	Button:
		text:'BoxLayout'
 
	BoxLayout:
		
		orientation:'horizontal'
		
		Button:
			text:'first'
			size_hint_y:.2
		Button:
			text:'second'
			size_hint_y:.3
```

![image-20240713014117656](http://111.229.225.13:81/i/2024/07/13/2c290q-2.png)

#### 改变BoxLayout布局的间距

kv文件，python文件不变

```python
<BoxLayoutWidget>:
	orientation:'vertical'
	padding:[10,40,40,30]
 
	canvas:
		Color:
			rgba:[1,1,1,1]
		Rectangle:
			size:self.size
			pos:self.pos
	Button:
		text:'Hello'
		background_color:.6,.2,.2,.1
	Button:
		text:'BoxLayout'
		background_color:.2,.6,.3,1
	BoxLayout:
		orientation:'horizontal'
		spacing:20
		Button:
			text:'first'
			background_color:.2,.2,.7,1
		Button:
			text:'second'
			size_hint_y:.3
			background_color:.4,.2,.2,1
```

![image-20240713015945830](http://111.229.225.13:81/i/2024/07/13/2mymft-2.png)

在这段代码中，`padding` 和 `spacing` 都是用于控制布局中元素之间的间距的属性，不过它们的作用范围有所不同。 `padding` 是用于设置 BoxLayoutWidget 内部的内边距。它定义了 BoxLayoutWidget 内部的内容（如其中的按钮）与 BoxLayoutWidget 边缘之间的空白区域大小。在上述代码中，`padding:[10, 40, 40, 30]` 表示分别设置了左、上、右、下四个方向的内边距大小，即左边距为 10 个单位，上边距为 40 个单位，右边距为 40 个单位，下边距为 30 个单位。通过设置 `padding`，可以使内部的元素与 BoxLayoutWidget 的边缘保持一定的距离，避免内容过于靠近边缘，从而使布局更加美观和易读。 `spacing` 则是用于设置 BoxLayout 内部子部件（如按钮）之间的间距。在上述代码中，`spacing:20` 表示 BoxLayout 中的按钮之间的水平间距为 20 个单位。这意味着当 BoxLayout 按照水平方向排列子部件时，每个子部件之间都会有 20 个单位的间隔，使它们不会相互紧贴，增加了布局的清晰度和可读性。如果是垂直方向的 BoxLayout，则 `spacing` 会控制垂直方向上子部件之间的间距。 总结来说，`padding` 主要用于控制 BoxLayoutWidget 内部内容与自身边缘的距离，而 `spacing` 用于控制 BoxLayout 内部子部件之间的间隔。合理地设置 `padding` 和 `spacing` 可以帮助实现更好的布局效果。
