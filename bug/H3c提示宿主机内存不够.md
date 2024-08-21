# H3C 宿主机内存不够无法启动设备解决方法 

本人在使用H3C模拟器的时候有时经常发现无法启动设备，在网上也没找到合适的解决方法，

但其实原理很简单，电脑的内存不够，打开任务资源管理器

![img](W:\note\bug\H3c提示宿主机内存不够\14444a097456f19ab53221431b367219.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

![img](W:\note\bug\H3c提示宿主机内存不够\d3f238a61647a992e3eccede8093193f.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑 就是这个原因，电脑内存配置不行。

解决方法：关掉几个后台就行了，我当时开了两个浏览器，一个vscode和qq微信，还有wps,关掉几个就可以了