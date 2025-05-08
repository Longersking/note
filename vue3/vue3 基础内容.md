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
# Attribute 绑定
在vue中双大括号只能用于文本插值。为了给attribute绑定一个动态值，需要使用 `v-bind`指令
```html
<div v-bind:id="dynamicId"></div>
```
**指令**是由 `v-` 开头的一种特殊 attribute。它们是 Vue 模板语法的一部分。和文本插值类似，指令的值是可以访问组件状态的 JavaScript 表达式。关于 `v-bind` 和指令语法的完整细节请详阅[指南 - 模板语法](https://cn.vuejs.org/guide/essentials/template-syntax.html)。
冒号后面的部分 (`:id`) 是指令的“参数”。此处，元素的 `id` attribute 将与组件状态里的 `dynamicId` 属性保持同步。

由于 `v-bind` 使用地非常频繁，它有一个专门的简写语法：
```html
<div :id="dynamicId"></div>
```
![[Pasted image 20250108171742.png]]
# 事件监听
我们可以使用 `v-on` 指令监听 DOM 事件：
```html
<button v-on:click="increment">{{ count }}</button>
```
因为其经常使用，`v-on` 也有一个简写语法：
```html
<button @click="increment">{{ count }}</button>
```
此处，`increment` 引用了一个在 `<script setup>` 中声明的函数：
```js
<script setup>
import { ref } from 'vue'

const count = ref(0)

function increment() {
  // 更新组件状态
  count.value++
}
</script>
```
在函数中，我们可以通过修改 ref 来更新组件状态。

事件处理函数也可以使用内置表达式，并且可以使用修饰符简化常见任务。这些细节包含在[指南 - 事件处理](https://cn.vuejs.org/guide/essentials/event-handling.html)。
![[Pasted image 20250108171854.png]]
![[Pasted image 20250108171950.png]]
# 表单绑定
我们可以同时使用 `v-bind` 和 `v-on` 来在表单的输入元素上创建双向绑定：
```html
<input :value="text" @input="onInput">****
```

```js
function onInput(e) {
  // v-on 处理函数会接收原生 DOM 事件
  // 作为其参数。
  text.value = e.target.value
}
```
试着在文本框里输入——你会看到 `<p>` 里的文本也随着你的输入更新了。

为了简化双向绑定，Vue 提供了一个 `v-model` 指令，它实际上是上述操作的语法糖：
```html
<input v-model="text">
```
`v-model` 会将被绑定的值与 `<input>` 的值自动同步，这样我们就不必再使用事件处理函数了。

`v-model` 不仅支持文本输入框，也支持诸如多选框、单选框、下拉框之类的输入类型。我们在[指南 - 表单绑定](https://cn.vuejs.org/guide/essentials/forms.html)中讨论了更多的细节。
重构前
![[Pasted image 20250108172115.png]]
重构后
![[Pasted image 20250108172135.png]]
# 条件渲染
我们可以使用 `v-if` 指令来有条件地渲染元素：
```html
<h1 v-if="awesome">Vue is awesome!</h1>
```
这个 `<h1>` 标签只会在 `awesome` 的值为[真值 (Truthy)](https://developer.mozilla.org/zh-CN/docs/Glossary/Truthy) 时渲染。若 `awesome` 更改为[假值 (Falsy)](https://developer.mozilla.org/zh-CN/docs/Glossary/Falsy)，它将被从 DOM 中移除。

我们也可以使用 `v-else` 和 `v-else-if` 来表示其他的条件分支：
```html
<h1 v-if="awesome">Vue is awesome!</h1>
<h1 v-else>Oh no 😢</h1>
```
现在，示例程序同时展示了两个 `<h1>` 标签，并且按钮不执行任何操作。尝试给它们添加 `v-if` 和 `v-else` 指令，并实现 `toggle()` 方法，让我们可以使用按钮在它们之间切换。

更多细节请查阅 `v-if`：[指南 - 条件渲染](https://cn.vuejs.org/guide/essentials/conditional.html)
修改前
![[Pasted image 20250108172304.png]]
修改后
![[Pasted image 20250108172315.png]]
# 列表渲染

我们可以使用 `v-for` 指令来渲染一个基于源数组的列表：
```html
<ul>
  <li v-for="todo in todos" :key="todo.id">
    {{ todo.text }}
  </li>
</ul>
```
这里的 `todo` 是一个局部变量，表示当前正在迭代的数组元素。它只能在 `v-for` 所绑定的元素上或是其内部访问，就像函数的作用域一样。

注意，我们还给每个 todo 对象设置了唯一的 `id`，并且将它作为[特殊的 `key` attribute](https://cn.vuejs.org/api/built-in-special-attributes.html#key) 绑定到每个 `<li>`。`key` 使得 Vue 能够精确的移动每个 `<li>`，以匹配对应的对象在数组中的位置。

更新列表有两种方式：

1. 在源数组上调用[变更方法](https://stackoverflow.com/questions/9009879/which-javascript-array-functions-are-mutating)：
```js
	todos.value.push(newTodo)
```
2. 使用新的数组替代原数组：
    
    ```js
    todos.value = todos.value.filter(/* ... */)
    ```
    

这里有一个简单的 todo 列表——试着实现一下 `addTodo()` 和 `removeTodo()` 这两个方法的逻辑，使列表能够正常工作！

关于 `v-for` 的更多细节：[指南 - 列表渲染](https://cn.vuejs.org/guide/essentials/list.html)
![[Pasted image 20250108172435.png]]
# 计算属性

让我们在上一步的 todo 列表基础上继续。现在，我们已经给每一个 todo 添加了切换功能。这是通过给每一个 todo 对象添加 `done` 属性来实现的，并且使用了 `v-model` 将其绑定到复选框上：


```html
<li v-for="todo in todos">
  <input type="checkbox" v-model="todo.done">
  ...
</li>
```

下一个可以添加的改进是隐藏已经完成的 todo。我们已经有了一个能够切换 `hideCompleted` 状态的按钮。但是应该如何基于状态渲染不同的列表项呢？

介绍一个新 API：[`computed()`](https://cn.vuejs.org/guide/essentials/computed.html)。它可以让我们创建一个计算属性 ref，这个 ref 会动态地根据其他响应式数据源来计算其 `.value`：


```js
import { ref, computed } from 'vue'

const hideCompleted = ref(false)
const todos = ref([
  /* ... */
])

const filteredTodos = computed(() => {
  // 根据 `todos.value` & `hideCompleted.value`
  // 返回过滤后的 todo 项目
})
```



```html
- <li v-for="todo in todos">
+ <li v-for="todo in filteredTodos">
```

计算属性会自动跟踪其计算中所使用的到的其他响应式状态，并将它们收集为自己的依赖。计算结果会被缓存，并只有在其依赖发生改变时才会被自动更新。
![[Pasted image 20250108172701.png]]
# 生命周期和模板引用
目前为止，Vue 为我们处理了所有的 DOM 更新，这要归功于响应性和声明式渲染。然而，有时我们也会不可避免地需要手动操作 DOM。

这时我们需要使用**模板引用**——也就是指向模板中一个 DOM 元素的 ref。我们需要通过[这个特殊的 `ref` attribute](https://cn.vuejs.org/api/built-in-special-attributes.html#ref) 来实现模板引用：


```html
<p ref="pElementRef">hello</p>
```

要访问该引用，我们需要声明一个同名的 ref：



```js
const pElementRef = ref(null)
```

注意这个 ref 使用 `null` 值来初始化。这是因为当 `<script setup>` 执行时，DOM 元素还不存在。模板引用 ref 只能在组件**挂载**后访问。

要在挂载之后执行代码，我们可以使用 `onMounted()` 函数：



```js
import { onMounted } from 'vue'

onMounted(() => {
  // 此时组件已经挂载。
})
```

这被称为**生命周期钩子**——它允许我们注册一个在组件的特定生命周期调用的回调函数。还有一些其他的钩子如 `onUpdated` 和 `onUnmounted`。更多细节请查阅[生命周期图示](https://cn.vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram)。

![[Pasted image 20250108172753.png]]
# 侦听器

有时我们需要响应性地执行一些“副作用”——例如，当一个数字改变时将其输出到控制台。我们可以通过侦听器来实现它：

js

```
import { ref, watch } from 'vue'

const count = ref(0)

watch(count, (newCount) => {
  // 没错，console.log() 是一个副作用
  console.log(`new count is: ${newCount}`)
})
```

`watch()` 可以直接侦听一个 ref，并且只要 `count` 的值改变就会触发回调。`watch()` 也可以侦听其他类型的数据源——更多详情请参阅[指南 - 侦听器](https://cn.vuejs.org/guide/essentials/watchers.html)。

一个比在控制台输出更加实际的例子是当 ID 改变时抓取新的数据。在右边的例子中就是这样一个组件。该组件被挂载时，会从模拟 API 中抓取 todo 数据，同时还有一个按钮可以改变要抓取的 todo 的 ID
![[Pasted image 20250108172838.png]]
# 组件

目前为止，我们只使用了单个组件。真正的 Vue 应用往往是由嵌套组件创建的。

父组件可以在模板中渲染另一个组件作为子组件。要使用子组件，我们需要先导入它：

```js
import ChildComp from './ChildComp.vue'
```

然后我们就可以在模板中使用组件，就像这样：


```html
<ChildComp />
```

尝试导入子组件并在模板中渲染它。
![[Pasted image 20250108173416.png]]
![[Pasted image 20250108173428.png]]
# Props

子组件可以通过 **props** 从父组件接受动态数据。首先，需要声明它所接受的 props：


```vue
<!-- ChildComp.vue -->
<script setup>
const props = defineProps({
  msg: String
})
</script>
```

注意 `defineProps()` 是一个编译时宏，并不需要导入。一旦声明，`msg` prop 就可以在子组件的模板中使用。它也可以通过 `defineProps()` 所返回的对象在 JavaScript 中访问。

父组件可以像声明 HTML attributes 一样传递 props。若要传递动态值，也可以使用 `v-bind` 语法：

```html
<ChildComp :msg="greeting" />
```

![[Pasted image 20250108173714.png]]
![[Pasted image 20250108173722.png]]
# 插槽

除了通过 props 传递数据外，父组件还可以通过**插槽** (slots) 将模板片段传递给子组件：

```vue
<ChildComp>
  This is some slot content!
</ChildComp>
```

在子组件中，可以使用 `<slot>` 元素作为插槽出口 (slot outlet) 渲染父组件中的插槽内容 (slot content)：


```vue
<!-- 在子组件的模板中 -->
<slot/>
```

`<slot>` 插口中的内容将被当作“默认”内容：它会在父组件没有传递任何插槽内容时显示：


```vue
<slot>Fallback content</slot>
```
![[Pasted image 20250108174152.png]]
![[Pasted image 20250108174207.png]]
