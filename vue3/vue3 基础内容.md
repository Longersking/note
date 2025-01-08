- 声明式渲染
	 从编辑器中的单个Vue文件，它将从属于同一个组件的 HTML、CSS 和 JavaScript 封装在使用 `.vue` 后缀的文件中。
	 vue的核心是声明式渲染： 通过扩展于标准 HTML 的模板语法，我们可以根据 JavaScript 的状态来描述 HTML 应该是什么样子的。当状态改变时，HTML 会自动更新。
	 能在改变时触发更新的状态被称作是**响应式**的。我们可以使用 Vue 的 `reactive()` API 来声明响应式状态。由 `reactive()` 创建的对象都是 JavaScript [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)，其行为与普通对象一样：
```js
import { reactive } from 'vue'

const counter = reactive({
  count: 0
})

console.log(counter.count) // 0
counter.count++
```
`reactive()` 只适用于对象 (包括数组和内置类型，如 `Map` 和 `Set`)。而另一个 API `ref()` 则可以接受任何值类型。`ref` 会返回一个包裹对象，并在 `.value` 属性下暴露内部值。
```js
import { ref } from 'vue'

const message = ref('Hello World!')

console.log(message.value) // "Hello World!"
message.value = 'Changed'

```
在组件的 `<script setup>` 块中声明的响应式状态，可以直接在模板中使用。下面展示了我们如何使用双花括号语法，根据 `counter` 对象和 `message` ref 的值渲染动态文本：
```html
<h1>{{ message }}</h1>
<p>Count is: {{ counter.count }}</p>
```
在双花括号中的内容并不只限于标识符或路径——我们可以使用任何有效的 JavaScript 表达式。
```html
<h1>{{ message.split('').reverse().join('') }}</h1>
```
![[Pasted image 20250106010459.png]]
