---
layout: post_with_ad
title: 재귀호출
permalink: /dna/recursion
date: 2017-10-29 19:46:07 +0900
categories: dna, data structure and algorithm
tags : 알고리즘, 자료구조, 재귀함수,재귀호출, algorithm, data structure, recursion, recursive function
excerpt : 재귀함수는 무엇일까요? 대단한 것이 없습니다. 자기자신을 호출하는 함수를 말합니다. 하지만 재귀함수가 개발에서 어떤 의미를 가지는 지 알기위해서는 좀더 자세히 살펴보아야 합니다. 이 글은 재귀함수를 좀 더 잘 사용하기 위해서 알아야 하는 것들을 서술 했습니다.
---

## 재귀(Recursion)란?

	자기 자신을 다시 호출하는 함수(function)

재귀함수는 무엇일까요? 대단한 것이 없습니다. 자기자신을 호출하는 함수를 말합니다. 하지만 재귀함수가 개발에서 어떤 의미를 가지는 지 알기위해서는 좀더 자세히 살펴보아야 합니다. 이 글은 재귀함수를 좀 더 잘 사용하기 위해서 알아야 하는 것들을 서술 했습니다.

**PHP 예제**
```php?start_inline=true
function recursiveFunc(){
	//...
	recursiveFunc();
	//...
}
```

### for/while 문 대신하여 재귀함수 사용하기

'for'문이나 'while'문을 사용하지 않고 재귀함수를 사용하여 구현할 수 있습니다. for와 while, 재귀함수는 서로 바꿔 가면서 구현이 가능합니다. 간단한 예제로 정수`int`형 2개를 인자로 받아 두 값 사이에 있는 정수를 모두 더 하는 함수를 구해봅시다.

	간단한 예제를 위해서 from이 to보다 작음을 보장하는 코드는 넣지 않았습니다.

#### **두 정수사이의 모든 값 더하기**

**for문을 사용한 경우**

```php?start_inline=true
function sumInt($from,$to)
{
	$sum = 0;

	for ($i = $from; $i <= $to; $i++) { 
		$sum += $i;
	}

	return $sum;
}

print(sumInt(1,2));
```

**while문 사용한 경우**

```php?start_inline=true
function sumInt($from,$to)
{
	$sum = 0;

	while ($i++ < $to) {
		$sum += $i;
	}

	return $sum;
}
```

**재귀함수 사용한 경우**

```php?start_inline=true
function sumInt($from,$to)
{	
	if($from < $to){
		//n에서 m 사이 수를 더하는 것은 n + ((n+1)+m)이랑 같다.
		return $from + sumInt($from+1,$to);
	}else{//n에서 n사이수를 모두 더하면 n
		return $to;
	}
}
```

### 사용시 주의점

재귀함수는 무한 루프에 빠지기 쉽습니다.(while문과 성질이 비슷) 재귀함수를 호출할 경우에는 두 가지 조건을 생각해야합니다. 

+ 기반 조건(Base case)
+ 종료 조건(Terminate case)

`기반조건`은 어떤 함수를 구현할 때 작은 문제로 쪼개질 수 있을 때 사용되는 조건이고 이외의 조건이 바론 `종료조건`입니다. 반대의 경우도 마찬가지입니다. `종료조건 `이외의 조건을 기반조건이라고 할 수 있습니다. 두 조건은 서로 `여집합` 관계여야 합니다.

위에서 살펴본 `두 정수사이의 모든 값 더하기`예제에서 재귀함수는 `기반조건`를 전제로 만들어진 함수이고 `종료조건`을 전제로 만든 함수는 다음과 같습니다.

```php?start_inline=true
/**
 * 종료조건을 전제로 만든 함수
 */
function sumInt($from,$to)
{	
	if($from == $to){//종료조건
		//n에서 n사이수를 모두 더하면 n
		return $to;//또는 $to
	}else{
		//n에서 m 사이 수를 더하는 것은 n + ((n+1)+m)이랑 같다.
		return $from + sumInt($from+1,$to);
	}
}
```

### 그렇다면 왜 재귀함수를 사용해야하나?

사실 재귀함수를 꼭 사용할 필요는 없습니다. 재귀함수 대신 while 혹은 for 문을 사용하여도 됩니다. 대신 선택의 문제입니다. 하지만 while/for/재귀함수를 선택하는 기준은 분명합니다. **가독성**입니다. while문으로 구현했을 때 가독성이 좋을 때는 while문으로, for 문이 가독성 높을 때는 for문으로, 재귀함수가 가독성이 높을 경우에는 재귀함수를 사용하면 됩니다.

### 재귀함수 예제

아래의 예제들은 재귀함수 이야기가 나올 때 자주 등장하는 예제들입니다. 보통 재귀함수로 구현했을 때 가독성이 높아지는 예제들입니다.

#### 팩토리얼

```php?start_inline=true
function factorial($n = 1)
{
	if(n <= 1)
		return 1;
	else 
		return n * factorial(n-1);
}
```

#### 하노이탑
```php?start_inline=true
function move($from, $to){
	print("$from 에서 $to 로 이동");
}

function hanoi($n, $from, $by, $to){
	if ($n == 1)
			move($from, $to);
	else{
			hanoi($n - 1, $from, $to, $by);
			move($from, $to);
			hanoi($n - 1, $by, $from, $to);
	}
}
```

#### 유클리드 호제법(최대공약수 구하기)

```php?start_inline=true
function gcd($a, $b) {
	return ($a % $b == 0 ? $b : gcd($b,$a%$b));
}
```

#### 피보나치 수열

```php?start_inline=true
function fib($n)
{
	if($n == 0 )
		return 0;
	else if($n == 1)
		return 1;
	else 
		return fib($n-1) + fib($n-2);
}
```