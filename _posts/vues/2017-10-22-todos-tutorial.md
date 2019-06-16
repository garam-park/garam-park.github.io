---
layout: post_with_ad
title:  VueJs 빠른시작 - Todo 만들기
date:   2017-10-21 15:48:00 +0900
permalink : /vue-js-posts/todos-tutorial
categories: vuejs
tags : vuejs 튜토리얼, vue, vuejs, tutorial, restful, vuejs, 튜토리얼, 예제 연습, vuejs 입문, Vue js 입문
excerpt : VueJs는 놀라우리만큼 간단하면서 직관적이고 배우기 쉽고 필요한 모든 게 준비된 front-end framework 입니다. front-end 개발자가 아닌 제가 공부하면 엄청난 생상성의 향상이 있음을 깨닫고 적극적으로 사내 프로젝트에 적용했습니다.VueJs의 모든 기능을 공부하기 보다는 간단한 예제를 만들어 보세요.
---
<br>
<iframe width="560" height="315" src="https://www.youtube.com/embed/b_sZiPXezSo" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>{:style="width:100%"}
<br>
## **1 소개**

VueJs는 놀라우리만큼 간단하면서 직관적이고 배우기 쉽고 필요한 모든 게 준비된 front-end framework 입니다. front-end 개발자가 아닌 제가 공부하면 엄청난 생상성의 향상이 있음을 깨닫고 적극적으로 사내 프로젝트에 적용했습니다.
VueJs의 모든 기능을 공부하기 보다는 간단한 예제를 만들어 보세요.

예제 코드는 [여기](https://github.com/storygcode/todos-client)를 참고하세요.
데모 페이지는 [여기](http://storyg.co/todos-client)에서 확인하시기 바랍니다.

## **2 선행하기**

이 예제를 알기 위해서는 아래에 나열한 목록에 있는 지식을 알고 설치가 되어있다는 전제하에 설명합니다.

### **2.1 선행지식**

+ `html`,`css`,`javascript`
+ `REST API`
+ `npm`

### **2.2 필요한 설치**

+ `npm`

## **3 프로젝트 만들기**

처음으로는 vue-cli 를 설치합니다. vue-cli 는 VueJs를 일반적인 프로젝트 구조와 개발환경을 미리 정의하여 새로운 프로젝트를 더욱 쉽게 시작할 수 있도록 도와줍니다. 더 자세한 내용은 [링크](https://github.com/vuejs/vue-cli)를 참조하세요. 아래는 npm을 이용하여 vue-cli 를 설치하는 명령을 보여줍니다. `-g`(global) 옵션으로 실행하는 프로그램 형태로 설치해줍니다.

```shell
npm install vue-cli -g
```
vue-cli의 설치가 끝나면 vue-cli를 이용하여 프로젝트를 만듭니다.다음은 webpack 템플릿을 이용한 프로젝트 만들기 명령어 입니다.

```shell
vue init webpack todos-client
```
이 명령어를 실행하면 몇까지 옵션이 나옵니다. 옵션 중에서 vue-router를 사용할 것이냐는 옵션은 필수적으로 선택해야 이 튜토리얼에 같이 참여 할 수 있습니다. 

```shell
? Project name todos-client
? Project description A Vue.js project
? Author storyg <blog@storyg.co>
? Vue build standalone
? Install vue-router? Yes
? Use ESLint to lint your code? No
? Setup unit tests with Karma + Mocha? No
? Setup e2e tests with Nightwatch? No
```

여기서 다음은 NO 로 선택했습니다. 튜토리얼을 하는데 도움이 안되기 때문입니다.

+ Use ESLint to lint your code
+ Setup unit tests with Karma + Mocha
+ Setup e2e tests with Nightwatch

설치가 끝나면 다음과 같은 설명을 볼 수 있습니다.

```
 To get started:
   
     cd todo-client
     npm install
     npm run dev
```
위의 명령을 프로젝트 root에서 시작하면 로컬 서버로 프로젝트가 돌아가는 것을 확인 할 수 있습니다.

![예제페이지](/images/npm-run-dev.png){:style="width:100%"}


## **4 자습**

이제부터 프로젝트를 하나씩 살펴 보도록 하겠습니다. 프로젝트의 대부분은 개발 환경 설정입니다. 우리가 다뤄야 하는 부분은 src 폴더와 정말 필요하다면 index.html 페이지가 됩니다. 가능하다면 index.html 파일은 수정하지 않도록 합니다.

### **4.1 index.html 살펴보기**

처음으로 root에 있는 index.html. 파일을 살펴보면 다음과 같습니다.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>todos-client</title>
  </head>
  <body>
    <div id="app"></div>
    <!-- built files will be auto injected -->
  </body>
</html>
```

주석 처리 되어있는 부분을 보면 빌드된 파일들은 자동으로 삽입된다고 합니다. 프로젝트의 메타태그나 꼭 필요한 것이 있을 때에만 수정을 합니다.

### **4.2 src 폴더 살펴보기**

우리가 정말 보아야하는 부분은 src 부분입니다. 각각의 요소를 살펴보면 다음과 같습니다.

```
src
├── assets
│   └── logo.png
├── components
│   └── HelloWorld.vue
├── router
│   └── index.js
├── App.vue
└── main.js
```

+ **assets**
	
	 외부에서 가지고 온 이미지, 파일, css, js 파일 등을 넣어두는 폴더입니다.

+ **components**
	
	 VueJs 에서 사용하는 확장명 `vue` 파일 들을 생성하고 구현하는 곳입니다. 프로젝트 생성 후에는 'HelloWorld.vue' 파일이 있습니다.

+ **router/index.js**
	
	 Vue 에서는 서버사이드에서 제공하는 라우팅을 사용하지 않아도 라우팅을 할 수 있도록 도와주는 Vue Router 가 있습니다. 이것을 가지고 페이지를 서버에 요청하지 않아도 새롭운 페이지로 이동할 수 있습니다.

+ **App.vue**
	
	 프로젝트가 다루는 컴포넌트가 표시되는 Root 컴포넌트입니다.

+ **main.js**
	
	 프로젝트의 Base 파일입니다. 전역 설정을 하려면 main.js를 수정합니다.

### **4.3 프로젝트 실험**

이제 부터 우리는 템플릿에 기본적으로 추가되어있는 파일들을 수정하면서 어떻게 동작하는지 살펴보도록 하겠습니다.

#### **4.3.1 index.html 수정해보기**

가장 처음 살펴 볼 것은 index.html 파일입니다. 프로그램 수정이 필요할 때 가장 마지막까지 고치지 말아야 하는 파일이 index.html 파일입니다. 프로그램 할 때에 전역 변수, 함수 사용을 자제하라는 뜻과 일맥상통하다고 보시면 됩니다. index.html 파일을 수정하지 않고 해결 해보려고 노력해야 합니다. 이 튜토리얼에서는 `bootstrap`를 이용하여 스타일 작업을 할 예정이므로 index.html 파일에 bootstrap 파일들을 클래식한 방법으로 추가하도록 하겠습니다.

	! 실제로는 npm 에서 스타일 패키지를 다운로드 받아서 하는 방법이 있지만 사전지식이 필요로 하므로 index.html 파일에 스타일 관련 코드를 추가하였습니다.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>todo-client</title>
    <!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

  </head>
  <body>
    <div class="container">
      <div id="app"></div>
    </div>
    <!-- built files will be auto injected -->
  </body>

  <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <!-- Latest compiled and minified JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</html>
```

최신의 3버전의 부트스트랩은 클래식한 방법으로 추가하였습니다. 이렇게 해서 모든 Vue Component에서 bootstrap 의 스타일을 사용할 수 있습니다.

#### **4.3.2 App.vue 파일 수정해보기**

App.vue 소스는 다음과 같습니다. 

```html
<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
```

Vue 컴포넌트는 3 가지로 이뤄져 있습니다.

+ 템플릿
+ 스크립트
+ 스타일

좀더 자세한 내용에 대해서는 [VueJs 페이지](https://kr.vuejs.org/v2/guide/single-file-components.html)를 확인하시기 바랍니다.

App.vue 파일에 Button 을 추가해서 부트스트랩 스타일이 바르게 적용되는지 확인하겠습니다. 템플릿 파트에 Button 을 추가해 봅시다.

```html
...
<template>
  <div id="app">
    <button class="btn btn-primary">Button</button>
    ...
   </div>
</template>
...
```

npm run dev 가 계속 진행 중이라면 변경 사항에 대한 적용을 웹브라우저에서 확인 가능합니다. 추가적으로 로고 이미지도 변경할 수 있습니다. 여러분께서 가지고 있는 이미지로 변경해보세요.

#### **4.3.3 router/index.js 파일 수정해보기**

vue-router 는 기존에 서버에서만 사용하던 라우터를 프론트엔드에서도 사용할 수 있도록 도와줍니다.

```js
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: HelloWorld
    }
  ]
});

```

라우터의 인스턴스를 생성하여 던져 주는 일을 하는 것을 볼 수 있습니다. 우리는 '/example' 로 들어갔을 때 HelloWorld 페이지를 한번 더 보여주도록 변경해 보겠습니다.

```js
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: HelloWorld
    },
    {
      path: '/example',
      name: 'example',
      component: HelloWorld
    }
  ]
});
```

주소창에 'http://localhost:8080/example' 로 이동하면 '/'에서 본 화면을 그대로 확인 할 수 있습니다. 왜냐하면 같은 주소에서 같은 컴포넌트가 보이도록 라우트를 추가했기 때문이입니다.

#### **4.3.3 components/Example.vue 추가**

example 라우터에 새로운 것 컴포넌트가 나오도록 하려면 가장 처음으로 해야하는 것이 컴포넌트를 만드는 것입니다. components 폴더에 Example.vue 라는 파일을 만들어 다음과 같이 합니다.

```html
<template>
  <div class="panel panel-default">
    <div class="panel-heading">Panel heading without title</div>
    <div class="panel-body">
      Panel content
    </div>
  </div>
</template>

<script>
export default {
  name: 'Example',
  data () {
    return {
      msg: 'Basic panel example'
    }
  }
}
</script>

```

이제 라우터에서 컴포넌트를 추가합니다.

```js
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Example from '@/components/Example'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: HelloWorld
    },
    {
      path: '/example',
      name: 'Example',
      component: Example
    }
  ]
});
```

![예제페이지](/images/vuejs-3.png){:style="width:100%"}

## **5 구현 해보기**

REST API를 이용하여 튜토리얼 프로젝트를 진행해보겠습니다. API를 사용하여 구현하기 전에 임시 데이터를 가지고 앱의 틀을 만들어 보도록 하겠습니다.

### **5.1 데모**

데모 페이지는 [여기](http://storyg.co/todos-client)에서 확인하시기 바랍니다.

### **5.2 시작**

#### **5.2.1 TODO 페이지**

가장 먼저 해야할 일은 컴포넌트를 선언하는 것입니다. 'TodoPage.vue' 이라는 파일을 만들어 'TODO' 를 다루는 컴포넌트를 만들어 보겠습니다. 'src/components'에 TodoPage.vue 파일을 만들고 가장 기본인 되는 코드를 넣어보겠습니다. 템플릿과 스크립트가 있는 컴포넌트 파일입니다.

```html
<template>
  <div>
    {{msg}}
  </div>
</template>

<script>
  export default {
    data(){
      return {
        msg:'Example Vue'
      };
    },
    mounted() {
      console.log('Component mounted.')
    }
  }
</script>
```

다음으로 'src/router/index.js' 파일를 수정하여 '/todos' 주소에서 TodoPage.vue 를 보이도록 수정하겠습니다.

```js
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Example from '@/components/Example'
import TodoPage from '@/components/TodoPage'//추가

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: HelloWorld
    },
    {
      path: '/example',
      name: 'Example',
      component: Example
    },
    {//추가
      path: '/todos',
      name: 'TodoPage',
      component: TodoPage
    }
  ]
});

```

컴포넌트를 `import`하고 라우터에 해당 컴포너트를 사용하도록 수정했습니다. '/todos'에서 컴포넌트가 잘 나오는 지 확인해보세요.

TodoPage에 UI 코드를 수정해 봅니다.

```html
<template>
<div class="container">
  <h2>Todo List</h2>
  <div class="input-group" style="margin-bottom:10px;">
    <input type="text" class="form-control" placeholder="할일을 입력하세요">
    <span class="input-group-btn">
      <button class="btn btn-default" type="button">추가</button>
    </span>
  </div>
  <ul class="list-group">
    <li class="list-group-item">
      청소하기
      <div class="btn-group pull-right" style="font-size: 12px; line-height: 1;">
        <button type="button" class="btn-link dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          더보기<span class="caret"></span>
        </button>
        <ul class="dropdown-menu">
          <li><a href="#">삭제</a></li>
        </ul>
      </div>
    </li>
  </ul>
</div>
</template>
```

다음과 같이 스타일링이 된 페이지를 볼 수 있습니다. 모바일 페이지를 보기위해서는 index.html 파일에 메타 테그를 추가해야합니다.

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

App.vue 파일에 스타일도 필요 없기 때문에 지워줍니다.

```html
<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>
```

![예제페이지](/images/vuejs-4.png){:style="width:100%"}

임시 데이터를 넣어서 동작하도록 해봅시다. 우선 스크립트에 데이터를 넣습니다.

```js
export default {
  name: 'TodoPage',
  data () {
    return {
      todos: [
        {
          name:'청소'
        },
        {
          name:'블로그 쓰기'
        },
        {
          name:'밥먹기'
        },
        {
          name:'안녕'
        }
      ]
    }
  }
}
```

이 데이터를 템플릿에 적용합니다.

```html
<li class="list-group-item" v-for="(todo, index) in todos">
{%raw%}{{todo.name}}{%endraw%}
	<div class="btn-group pull-right" 
		style="font-size: 12px; line-height: 1;">
		<button type="button" 
		class="btn-link dropdown-toggle" 
		data-toggle="dropdown" 
		aria-haspopup="true" 
		aria-expanded="false">
			더보기<span class="caret"></span>
		</button>
		<ul class="dropdown-menu">
			<li><a href="#">삭제</a></li>
		</ul>
	</div>
</li>
```

TodoPage.vue의 전체 소스코드는 다음과 같습니다.

```html
<template>
<div class="container">
  <h2>Todo List</h2>
  <div class="input-group" style="margin-bottom:10px;">
    <input type="text" class="form-control" placeholder="할일을 입력하세요">
    <span class="input-group-btn">
      <button class="btn btn-default" type="button">추가</button>
    </span>
  </div>
  <ul class="list-group">
    <li class="list-group-item" v-for="(todo, index) in todos">
    {%raw%}{{todo.name}}{%endraw%}
      <div class="btn-group pull-right" 
        style="font-size: 12px; line-height: 1;">
        <button type="button" 
        class="btn-link dropdown-toggle" 
        data-toggle="dropdown" 
        aria-haspopup="true" 
        aria-expanded="false">
          더보기<span class="caret"></span>
        </button>
        <ul class="dropdown-menu">
          <li><a href="#">삭제</a></li>
        </ul>
      </div>
    </li>
  </ul>
</div>
</template>

<script>
export default {
  name: 'TodoPage',
  data () {
    return {
      todos: [
        {
          name:'청소'
        },
        {
          name:'블로그 쓰기'
        },
        {
          name:'밥먹기'
        },
        {
          name:'안녕'
        }
      ]
    }
  }
}
</script>
```

![예제페이지](/images/vuejs-5.png){:style="width:100%"}

삭제 기능을 만들어 봅시다.


```html
...
<li>
	<a href="#" @click="deleteTodo(index)">삭제</a>
</li>
...
<script>
export default {
	methods:{
		deleteTodo(i){
			this.todos.splice(i,1);
		}
	}
}
</script>
```

![예제페이지](/images/vue-2017-10-22 12_37_19-delete.gif){:style="width:100%"}

추가 기능을 만들어 봅시다.

```html
...
<div class="input-group" style="margin-bottom:10px;">
	<input type="text" class="form-control" 
		placeholder="할일을 입력하세요" 
		v-model="name" 
		v-on:keyup.enter="createTodo(name)">
	<span class="input-group-btn">
		<button class="btn btn-default" type="button" 
		@click="createTodo(name)">추가</button>
	</span>
</div>
...
<script>
export default {
	name: 'TodoPage',
	data () {
		return {
			name:null,
			todos: [{name:'청소'},{name:'블로그 쓰기'},{name:'밥먹기'},{name:'안녕'}]
		}
	},
	methods:{
		deleteTodo(i){
			this.todos.splice(0,1);
		},
		createTodo(name){
			if(name != null){
				this.todos.push({name:name});
				this.name = null
			}
		}
	}
}
</script>
```

![예제페이지](/images/vue-2017-10-22 12_37_47-create.gif){:style="width:100%"}

#### **5.2.2 API 확인**

Todos API는 여러가지 `TODO`를 다루는 API 입니다.

해당 ~~[API 문서](/apis/todos)~~를 확인해보세요.

#### **5.2.3 axios 설치 및 기능 구현**

일반적으로 REST API는 리소스와 연관 되어있습니다. 그리고 리소스에는 5가지 기본적인 기능을 제공합니다.

+ List
+ CREATE
+ READ
+ UPDATE
+ DELETE

각 기능은 API에 정의되어 있습니다. 이런 API를 사용하기 위해서는 axios 와 같은 비동기 HTTP 클라이언 라이브러리를 사용해야 합니다. 다음은 axios 를 설치하는 명령어입니다.

```shell
npm install axios --save-dev
```

설치가 완료되면 'src/main.js'에 다음과 같이 axios 사용할 수 있도록 설정합니다.

```javascript
...
import axios from 'axios'
Vue.prototype.$http = axios
...

```

이 설정이 끝나면 Vue 에서 axios를 전역적으로 사용 할 수 있습니다.

가장 먼저 Todo List를 가져와 보도록 하겠습니다. methods 에 'getTodos()' 함수를 다음과 같이 정의 합니다.

```javascript
getTodos(){
	this.$http.get('http://todos.garam.xyz/api/todos')
	.then((result) => {
			console.log(result)
	})
}
```

API 실행되려면 이벤트 발생시나 Vue의 라이프 사이클 중에 선택하여 들어가야합니다. [공식 페이지](https://kr.vuejs.org/v2/guide/instance.html)에서 확인 하시기 바랍니다. mounted 는 Vue Component가 페이지에 끼워지고(mounted) 나서 호출되는 함수 입니다.

다음은 'mounted' hook에서 'getTodos()' 함수를 호출하는 코드입니다.

```javascript
export default {
  name: 'TodoPage',
  data () {...},
  methods:{...},
  mounted(){
    this.getTodos();
  }
}
```

'getTodos()' 함수를 통해서 API 에서 주는 데이터를 확인 할 수 있습니다. 데이터를 todos에 삽입해 보도록 하겠습니다.

```javascript
...
data(){ 
	return {
	name:null,
	todos: [],
	}
}
...
getTodos(){
	var vm = this;
	this.$http.get('http://todos.garam.xyz/api/todos')
	.then((result) => {
			vm.todos = result.data.data;
	})
}
...

```

수정 후에는 데이터베이서에서 API를 호출해한 데이터가 설정 됩니다. 이제 API를 이용하여 Todo에 새로운 할일을 추가하는 코드를 넣어보도록 하겠습니다. 'createTodo()'를 살짝 수정해봅시다.

```javascript
createTodo(name){
	if(name != null){
		var vm = this;
		this.$http.defaults.headers.post['Content-Type'] = 'application/json';
		this.$http.post('http://todos.garam.xyz/api/todos',{
			name:name
		}).then((result) => {
				vm.todos.push(result.data);
		})
		this.name = null
	}
},
```

이제 삭제를 구현해보겠습니다. 버튼을 눌렀을 때, Todo 객체를 넘겨주도록 변경하고 'deleteTodo()'를 다음과 같이 수정합니다.

```html
<li>
  <a href="#" @click="deleteTodo(todo)">삭제</a>
</li>
```

```javascript
deleteTodo(todo){
	var vm = this
	this.todos.forEach(function(_todo,i, obj){
		if(_todo.id === todo.id){
			vm.$http.delete('http://todos.garam.xyz/api/todos/'+todo.id)
			.then((result) => {
					obj.splice(i, 1)
			})	
		}
	})
},
```
## **6 마침**

이렇게 REST API 를 이용한 간단한 예제를 만들어보았습니다.
