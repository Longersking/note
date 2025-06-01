 [[sql注入基础篇]]
- ## Java常用数据库连接方式
	 1. JDBC
	 2. MyBatis
	 3. MyBatis-plus
	 4. Hibernate
- ## JDBC下的[[sql]]注入点审计思路
	1. 寻找动态拼接点
	 - 直接使用 + 进行拼接的sql语句（常用）
	 - append函数（常用）
	 - concat函数
	 - join函数
	2. 寻找使用Statment 类进行构建sql语句的代码
	3. 寻找 order by使用处
	 在sql语言中order by用于对查询结果集进行排序， order by语句后面需要是字段名或者字段位置。在使用PreparedStatement 预编译时，会将传递任意参数使用单引号包裹形成字符串因此使用预编译会导致设置的字段名被人认为是字符串而不是字段名，因此使用order by时将无法使用预编译
- ##  MyBatis的sql注入审计思路
	1. 寻找拼接符 $
	2. 寻找 order by
		在sql语言中order by用于对查询结果集进行排序， order by语句后面需要是字段名或者字段位置。在使用PreparedStatement 预编译时，会将传递任意参数使用单引号包裹形成字符串因此使用预编译会导致设置的字段名被人认为是字符串而不是字段名，因此使用order by时将无法使用预编译
	3. 寻找 in 注入
		IN语句 ：常用于where表达式中，其作用是查询某个范围内的数据。比如： select * from where field in (value1,value2,value3,…); 如上所示，in在查询某个范围数据是会用到多个参数，在Mybtis中如果直接使用占位符 #{} 进行查询会 将这些参数看做一个整体，查询会报错。因此很多开发人员可能会使用拼接符 ${} 对参数进行查询，从而造成了SQL注入漏洞。
	4. 寻找 like 注入
	  使用like语句进行查询时如果使用占位符 #{} 查询时程序会报错
- ### 实战审计华夏erp框架的sql注入点
	配置：
		1. jdk1.8
		2. mysql数据库
		3. 建立数据库表jsh_erp
		![[Pasted image 20250108153747.png]]
		4. 然后在表中执行源码中自带的sql文件
		![[Pasted image 20250108153825.png]]
		5. 同时使用maven下载项目组件
		![[Pasted image 20250108154006.png]]
		点击运行即可
		![[Pasted image 20250108154130.png]]
	审计：
		1. 查看配置文件；
		查找pom.xml文件发现是由mybatis框架连接数据库
		![[Pasted image 20250108154541.png]]
		2. 全局搜索敏感字符或者函数;
		由于是mybatis框架所以全局搜索 like,order by,in这些关键字，因为通常这些关键字在sql语句中无法使用预编译
		![[Pasted image 20250108154741.png]]
		点击跟进
		可以发现下面这段sql语句没有使用任何预防措施
		![[Pasted image 20250108154934.png]]
		全局搜索方法 `selectByConditionSupplier` 的调用
		![[Pasted image 20250108155224.png]]
		点击跟进
		![[Pasted image 20250108155245.png]]
		发现被方法select 调用，同时参数也一致，因此接着寻找select的方法调用，这时要使用快捷键ctrl + 鼠标左键点击方法select 跟进，否则可能会跟错方法
		跟进到了这
		![[Pasted image 20250108155505.png]]
		可以发现方法被 `getSupplierList`调用，并且参数不一致，但是可以先观察。
		经过观察发现所 `getSupplierList`方法中的参数是一个map集合，并且在方法返回调用的`select`方法中参数都是通过map集合提取出来的，因此在此方法中依旧可以确定参数可控。
		再跟进`getSupplierList`方法
		![[Pasted image 20250108155905.png]]
		再跟进`select`
		![[Pasted image 20250108155952.png]]
		参数依旧可以可控，再次跟进 `select`方法
		![[Pasted image 20250108160049.png]]
		这次终于看见接口了
		不难推测接口是get请求方式，而我们一路跟进过来的方法参数需要找的`parameterMap`
		可以发现`parameterMap`参数是将HTTP请求数据包中的search参数存放，因此sql注入点即在search参数中
		现在的目标则是寻找前端对应的功能点，以及具体接口，这里的接口为`/{apiName}/list`
		表示接口apiName其实是一个变量，全局搜索对应的/list接口，在html或者js文件中寻找
		![[Pasted image 20250108161231.png]]
		这种就是前端常见的接口写法，去查看几个
		![[Pasted image 20250108161412.png]]
		发现data传送的数据与我们刚刚找的方法参数名称不一致（其实是一样的，但是我们主要目标是寻找到我们刚刚跟进的方法），去看别的
			![[Pasted image 20250108162252.png]]
			![[Pasted image 20250108162309.png]]
		发现这个文件和我们一开始找到的sql语句配置文件相似
		![[Pasted image 20250108162354.png]]
	
	 因此可以断定是此接口
	 同时在浏览器找到对应的功能点进行抓包
	 ![[Pasted image 20250108162506.png]]
	 ![[Pasted image 20250108162643.png]]
	 发送到重放模块中
	 解码
	 ![[Pasted image 20250108162737.png]]
	 尝试改写参数
	 “supplier”:"'and sleep(5)--"
	 这里是已经返回的数据包在解码查看的，原始数据包还是要url编码，否则会报错
	 ![[Pasted image 20250108162951.png]]
	 可以发现已经成功延时了