---
layout: post_with_ad
title: 템플릿 메소드 패턴
permalink: /design-patterns/template-method
date: 2017-11-01 00:43:50 +0900
categories: design pattern
tags : design-pattern, 디자인패턴, 디자인 패턴, design, pattern,design pattern,template method , template method pattern,gof pattern, gof 패턴
excerpt : 많은 경우에 일정한 절차를 가진 프로그램을 하는 경우가 많이 있습니다. 안드로이드 개발에서는 액티비티(Activity) 생명주기(Life Cycle)가 있고 VueJs 개발에서는 인스턴스 생명주기, iOS에서 View 생명주기 등이 템플릿 메소드입니다. 
---

### **탬플릿 메소드 패턴 요약 설명**

+ **타입** : `행위`
+ **설명** : 어떤 절차적인 단계가 있는 경우 미리 절차에 대한 것만 선언해 두고 이후 구현은 하위 클래스에게 위힘하는 패턴

#### **UML**

![](/images/dp/uml-template.png){:style="width:100%;padding-left:20%;padding-right:20%"}

#### **우리가 마주치는 템플릿 메소드**

많은 경우에 일정한 절차를 가진 프로그램을 하는 경우가 많이 있습니다. 안드로이드 개발에서는 액티비티(Activity) 생명주기(Life Cycle)가 있고 iOS에서 View 생명주기 등이 템플릿 메소드입니다. 

#### **예제**

콘솔창에 상하로 구분선를 넣고 그 사이에 원하는 문자열을 출력하는 프로그램을 만든다고 가정해 봅시다. 그렇다면 우리에게 필요한 것을 '출력을 원하는 문자열' 윗쪽에 '출력할 구분선' 출력하고 '출력을 원하는 문자열' 아랫쪽에도 '출력할 구분선' 출력합니다.

+ 위쪽 구분선
+ 출력하고 싶은 문자열
+ 아래쪽 구분선

윗쪽 구분선을 출력하는 함수를 `printUpSeparator()` 라고 하고 아래쪽 구분선을 출력하는 함수를 `printBottomSeparator()` 라 하고 원하는 문자열을 출력하는 함수를 `printContent()` 라고 했을 때 호출되는 순서는 

`printUpSeparator()`->`printContent()`-> `printBottomSeparator()` 

일 것입니다. 이 순서는 꼭 지켜져야 합니다. 이 순서를 지켜주는 함수를 `printContentWithBox()` 라고 하면 이 함수는 다음과 같은 모양일 것입니다.

```java
//java

public void printContentWithBox(String str){
	printUpSeparator(str);
	printContent(str);
	printBottomSeparator(str);
}

```

추가적으로 구분선의 모양은 바꿀 수 있게 하고 싶습니다. 그래서 함수 `printUpSeparator()` , `printBottomSeparator()` ,`printContent()` 는 구현이 필요한 가상 메소드로 선언만 됩니다.`printContentWithBox()` 함수는 이 세 함수를 호출하는 함수이기 때문에 구현이 완성된 함수입니다. 이 두가지 종류의 요구사항을 모두 담을 수 있는 형태의 객체는 추상 클래스입니다.

```java
//java
abstract class BoxPrinter {

	void printUpSeparator(String str);
	void printContent(String str);
	void printBottomSeparator(String str);

	public void printContentWithBox(String str){
		printUpSeparator(str);
		printContent(str);
		printBottomSeparator(str);
	}
}
```


다음에 나오는 각 언어로 구현한 템플릿 메소드 패턴입니다.

**Java 예제**

```java
abstract class BoxPrinter {
	
	protected void printUpSeparator(String str);
	protected void printContent(String str);
	protected void printBottomSeparator(String str);

	public void printContentWithBox(String str){
		printUpSeparator(str);
		printContent(str);
		printBottomSeparator(str);
	}
}

class SimpleBoxPrinter extends BoxPrinter{
	
	protected  void printUpSeparator(String str){
		System.out.println("--------------");
	}
	
	protected  void printContent(String str){
		System.out.println($str);
	}
	
	protected  void printBottomSeparator(String str){
		System.out.println("--------------");
	}
}
```


**PHP 예제**

```php
#준비중
```

**C++ 예제**

```cpp
//준비중
```

**Python 예제**

```python
#준비중
```

**C# 예제**

```csharp
//준비중
```
