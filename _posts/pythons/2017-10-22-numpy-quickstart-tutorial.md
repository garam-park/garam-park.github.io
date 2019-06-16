---
layout: post
title:  "기초 - Numpy QuickStart 자습서"
permalink : /numpy-tutorials/basics
published : true
date:   2017-10-22 05:16:56 +0900
categories: numpy, python
tags : numpy, python, garam, blog
excerpt : NumPy의 주요한 객체는 동일한 요소를 갖는 다중 배열입니다. 대부분 같은 숫자로 되어있는 요소들의 테이블 입니다. 요소는 양의 정수의 튜플로 인덱스 되어있습니다. Numpy에서는 차원을 축(axes)이라고 불리우고. 축의 개수가 랭크(rank)입니다.
---

## **기초**

NumPy의 주요한 객체는 동일한 요소를 갖는 다중 배열입니다. 대부분 같은 숫자로 되어있는 요소들의 테이블 입니다. 요소는 양의 정수의 튜플로 인덱스 되어있습니다. Numpy에서는 차원을 `축(axes)`이라고 불리우고. 축의 개수가 `랭크(rank)`입니다.

예를 들어 3차원 공간의 점([1, 2, 1])의 좌표는 랭크 1의 배열입니다. 하나의 축만 가지고 있기 때문입니다.
그리고 그 점은 축은 3의 길이를 가지고 있습니다. 아래의 예제 코드에서 보면 2차원이기 때문에 랭크는 2를 가지고 있습니다. 첫번째 차원(축)은 길이가 2이고 다음 차원은 길이가 3입니다.

```python
[[ 1., 0., 0.],
 [ 0., 1., 2.]]
```
NumPy의 배열 클래스는 `ndarray` 라고 합니다. `numpy.array`는 표준 파이썬 라이브러리 클래스 `array.array`와 같지 않다는 것에 주의해야 합니다. 표준 라이브러리는 1차원 배열로 다뤄지고 기능이 더 적습니다.

아래에는 `ndarray` 객체에서 중요한 속성들입니다 :

**`ndarray.ndim`**

축(차원)의 개수. 파이썬에서는 차원의 개수를 랭크라고 말합니다.

**`ndarray.shape`**

배열의 차원들. 각 차원에서 배열의 사이즈를 표시하는 정수들의 튜플입니다.
n 행과 m 열을 갖는 매트릭스를 예를들면 `shape` 은 (n,m) 입니다.
shape 튜플의 길이는 랭크입니다. ndim은  number of dimensions입니다. 

**`ndarray.size`**

배열의 모든 요소들의 개수입니다. shape의 요소들의 모두 곱한 값과 같습니다.

**`ndarray.dtype`**

배열에서의 요소들의 타입을 설명합니다. 하나의 배열은 dtype의 표준 파이썬 타입들의 사용하여 생성하거나 특정할 수 있습니다. 추가적으로 설명하자면  NumPy는 자체적으로 가진 타입을 제공합니다. 예를 들면 `numpy.int32`, `numpy.int16`, and `numpy.float64` 입니다.

**`ndarray.itemsize`**

배열의 각 요소의 바이트에서의 사이즈. 예를 들면 float64 형식의 요소의 배열은 itemsize 8 (64/8)를 가지고 complex32 형식의 요소를 같는다면 itemsize 4 를 갖게 됩니다.`ndarray.itemsize`과 `ndarray.dtype.itemsize`는 같습니다.

**`ndarray.data`**

배열의 실제 요소를 가지고 있는 버퍼. 일반적으로 이 속성을 사용하지는 않습니다. 대신해 우리는 배열안에 있는 요소를 인덱싱 패실리티를 이용하여 접근합니다.

### **예제**

```python
>>> import numpy as np
>>> a = np.arange(15).reshape(3, 5)
>>> a
array([[ 0,  1,  2,  3,  4],
       [ 5,  6,  7,  8,  9],
       [10, 11, 12, 13, 14]])
>>> a.shape
(3, 5)
>>> a.ndim
2
>>> a.dtype.name
'int64'
>>> a.itemsize
8
>>> a.size
15
>>> type(a)
<type 'numpy.ndarray'>
>>> b = np.array([6, 7, 8])
>>> b
array([6, 7, 8])
>>> type(b)
<type 'numpy.ndarray'>
```

### **배열생성**

배열을 생성하는 여러 가지 방법이 있습니다. 

예를 들면, `array` 함수를 이용하여 파이썬의 리스트나 튜플을 이용하여 배열을 생성할 수 있습니다. 생성될 배열의 타입은 입력되어진 요소들로부터 배열의 타입이 추론되어집니다.

```python
>>> import numpy as np
>>> a = np.array([2,3,4])
>>> a
array([2, 3, 4])
>>> a.dtype
dtype('int64')
>>> b = np.array([1.2, 3.5, 5.1])
>>> b.dtype
dtype('float64')

```

숫자로 이뤄진 단일 리스트를 인자로 제공해야합니다. 함수의 인자로 여러 숫자를 넣고 `array`로 호출하여 빈번한 에러가 발생합니다. 아래의 예제를 확인해보세요.

```python
>>> a = np.array(1,2,3,4)    # 틀림
>>> a = np.array([1,2,3,4])  # 맞음
```

`array`함수는 시퀀스(연속된 수)를 가진 시퀀스 2차원 배열로, 시퀀스를 가진 시퀀스를 가진 시퀀스는 3차원 배열로 만듭니다. 이런 식으로 n 차원 배열을 만듭니다.

```python
>>> b = np.array([(1.5,2,3), (4,5,6)])
>>> b
array([[ 1.5,  2. ,  3. ],
       [ 4. ,  5. ,  6. ]])
```

배열을 생성할 때, 명시적으로 배열의 타입을 지정할 수 있습니다: 

```python
>>> c = np.array( [ [1,2], [3,4] ], dtype=complex )
>>> c
array([[ 1.+0.j,  2.+0.j],
       [ 3.+0.j,  4.+0.j]])
```

배열의 모양는 알지만 종종 배열의 요소 자체가 알려지지 않을 때가 있습니다.그러므로, 초기 값을 가진 배열을 생성하는 여러가지 함수를 제공합니다. 이것들은 배열을 늘림의 필요성과 비용이 많이 드는 작업을 최소화합니다. 

`zero` 함수는 영(0)으로 채워진 배열을 만듭니다. `ones` 함수는 일(1)로 채워진 배열을 만듭니다. `empty` 함수는 메모리 상태에 의존적이고 임의적이 내용의 배열을 만듭니다. 기본적으로 `float64`타입의 dtype 배열이 생성됩니다.

```python
>>> np.zeros( (3,4) )
array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
>>> np.ones( (2,3,4), dtype=np.int16 ) # dtype 을 명시적으로 표시할 수 있습니다.
array([[[ 1, 1, 1, 1],
        [ 1, 1, 1, 1],
        [ 1, 1, 1, 1]],
       [[ 1, 1, 1, 1],
        [ 1, 1, 1, 1],
        [ 1, 1, 1, 1]]], dtype=int16)
>>> np.empty( (2,3) ) # 초기화 안되어서 리턴되는 값은 다를 수 있습니다.
array([[  3.73603959e-262,   6.02658058e-154,   6.55490914e-260],
       [  5.30498948e-313,   3.14673309e-307,   1.00000000e+000]])
```

숫자의 시퀀스(연속한 수)를 생성하기 위해서 NumPy는 `range`와 비슷한 함수를 제공하는데  `list` 대신하여 `array`를 넘겨줍니다.

```python
>>> np.arange( 10, 30, 5 )
array([10, 15, 20, 25])
>>> np.arange( 0, 2, 0.3 ) # 실수도 사용 가능합니다.
array([ 0. ,  0.3,  0.6,  0.9,  1.2,  1.5,  1.8])
```

`arrayg`에 실수 부동소수점을 사용하게 되면 일반적으로 예측할 수 없는 요소들을 얻게 됩니다. (컴퓨터에서는) 유한한 부동소스점일 수 밖에 없기 때문입니다. 그러한 이유로 `linspace`를 사용하는 것이 일반적으로 낫습니다. 차이를 이용하여 배열을 생성하는 것 대신하여 우리가 원하는 개수를 인자로 받습니다.

```python
>>> from numpy import pi
>>> np.linspace( 0, 2, 9 )# 0 부터 2 사이에 있는 9 개 숫자 
array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ,  1.25,  1.5 ,  1.75,  2.  ])
>>> x = np.linspace( 0, 2*pi, 100 )        # 많은 포인트를 가진 함수를 평가할 때 유용합니다.
>>> f = np.sin(x)
```

**살펴보기**

	array, zeros, zeros_like, ones, ones_like, empty, empty_like, arange, linspace, numpy.random.rand, numpy.random.randn, fromfunction, fromfile

### **배열 출력**

When you print an array, NumPy displays it in a similar way to nested lists, but with the following layout:

NumPy에서 배열을 출력할 때 중첩된 리스트와 비슷하게 보여줍니다. 하지만 다음의 레이아웃.

+ 마지막 축은 왼쪽에서 오른쪽으로 출력
+ 두번째에서 마지막은 위에서 아래로 출력
+ 나머지는 위에서 아래로 출력

1차원은 배열처럼 출력되고 2차원은 매트릭스처럼 3차원은 매트릭스의 리스트처럼 출력됩니다.

```python
>>> a = np.arange(6)  # 1챠원 베열
>>> print(a)
[0 1 2 3 4 5]
>>>
>>> b = np.arange(12).reshape(4,3)  # 2챠원 베열
>>> print(b)
[[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]
>>>
>>> c = np.arange(24).reshape(2,3,4)  # 3챠원 베열
>>> print(c)
[[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]
 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
```

`reshape`은 [아래](/numpy-tutorials/basics/)에서 더 자세한 내용을 볼수 있습니다. `reshape`.

만약에 배열이 프린트하기에 너무 크다면, NumPy는 자동적으로 중간 부분을 생략하고 코너 부분의 것맡 출력합니다.

```python
>>> print(np.arange(10000))
[   0    1    2 ..., 9997 9998 9999]
>>>
>>> print(np.arange(10000).reshape(100,100))
[[   0    1    2 ...,   97   98   99]
 [ 100  101  102 ...,  197  198  199]
 [ 200  201  202 ...,  297  298  299]
 ...,
 [9700 9701 9702 ..., 9797 9798 9799]
 [9800 9801 9802 ..., 9897 9898 9899]
 [9900 9901 9902 ..., 9997 9998 9999]]
```

이러한 동작을 막고 강제로 NumPy에서 전체 배열을 출력하고 싶다면, `set_printoptions` 옵션을 변경할 수 있습니다.

```python
>>> np.set_printoptions(threshold='nan')
```

### **기본연산**

배열에 있는 수학 연산들 `요소적`으로 적용됩니다. 새로운 배열은 결과로 채워져 생성됩니다.

```python
>>> a = np.array( [20,30,40,50] )
>>> b = np.arange( 4 )
>>> b
array([0, 1, 2, 3])
>>> c = a-b
>>> c
array([20, 29, 38, 47])
>>> b**2
array([0, 1, 4, 9])
>>> 10*np.sin(a)
array([ 9.12945251, -9.88031624,  7.4511316 , -2.62374854])
>>> a<35
array([ True, True, False, False], dtype=bool)
```

다른 많은 매트릭스 언어와는 다르게 프러덕트(product) 연산자 `*`는 NumPy 배열에서는 요소적으로 동작합니다. 매트릭스의 프로덕트을 `dot` 함수나 메소드를 사용하여 수행할 수 있습니다 : 

```python
>>> A = np.array( [[1,1],
...             [0,1]] )
>>> B = np.array( [[2,0],
...             [3,4]] )
>>> A*B                         # 요소마다 곱(product)
array([[2, 0],
       [0, 4]])
>>> A.dot(B)                    # 매트릭스 곱(product)
array([[5, 4],
       [3, 4]])
>>> np.dot(A, B)                # 다른 방식의 매트릭스 곱(product)
array([[5, 4],
       [3, 4]])
```

`+=` and `*=`와 같은 몇몇 연산자는 새로 생성하는 것 보다는 이미 있는 배열에 수정하는 방식으로 동작합니다.

```python
>>> a = np.ones((2,3), dtype=int)
>>> b = np.random.random((2,3))
>>> a *= 3
>>> a
array([[3, 3, 3],
       [3, 3, 3]])
>>> b += a
>>> b
array([[ 3.417022  ,  3.72032449,  3.00011437],
       [ 3.30233257,  3.14675589,  3.09233859]])
>>> a += b                  # b는 자동적으로 integer 타입으로 변경되지 않는다.
Traceback (most recent call last):
  ...
TypeError: Cannot cast ufunc add output from dtype('float64') to dtype('int64') with casting rule 'same_kind'
```

When operating with arrays of different types, the type of the resulting array corresponds to the more general or precise one (a behavior known as upcasting).

다른 타입과 같인 연산 된다면 결과로 나오는 배열의 타입은 일반적이거나 정확한 타입의 것으로 변환됩니다.

```python
>>> a = np.ones(3, dtype=np.int32)
>>> b = np.linspace(0,pi,3)
>>> b.dtype.name
'float64'
>>> c = a+b
>>> c
array([ 1.        ,  2.57079633,  4.14159265])
>>> c.dtype.name
'float64'
>>> d = np.exp(c*1j)
>>> d
array([ 0.54030231+0.84147098j, -0.84147098+0.54030231j,
       -0.54030231-0.84147098j])
>>> d.dtype.name
'complex128'
```

모든 요소들의 합과 같은 많은 단항연산자들 `ndarray`의 메소드로 구현되어 있습니다.

```python 
>>> a = np.random.random((2,3))
>>> a
array([[ 0.18626021,  0.34556073,  0.39676747],
       [ 0.53881673,  0.41919451,  0.6852195 ]])
>>> a.sum()
2.5718191614547998
>>> a.min()
0.1862602113776709
>>> a.max()
0.6852195003967595
```

기본적으로, 이러한 연산들은 배열의 모양과는 관계없이 숫자들의 리스트 처럼 적용됩니다. 하지만 배열의 특정한 `축`을 연산의 인자로 할 수 있습니다.

```python
>>> b = np.arange(12).reshape(3,4)
>>> b
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>>
>>> b.sum(axis=0)                            # 각 컬럼에 총합
array([12, 15, 18, 21])
>>>
>>> b.min(axis=1)                            # 각 열의 최소 값
array([0, 4, 8])
>>>
>>> b.cumsum(axis=1)                         # 각 열의 누적 총합
array([[ 0,  1,  3,  6],
       [ 4,  9, 15, 22],
       [ 8, 17, 27, 38]])
```

### **보편적인 함수**

NumPy는 sin, cos, exp 와 같은 수학적 함수들을 제공합니다. Numpy에서 이러한 함수들을 `ufunc`(universal functions)로 불리웁니다. NumPy에서는 이러한 함수들은 배열에서 요소적으로 수행하여 또 다른 배열을 결과로 만듭니다.

```python
>>> B = np.arange(3)
>>> B
array([0, 1, 2])
>>> np.exp(B)
array([ 1.        ,  2.71828183,  7.3890561 ])
>>> np.sqrt(B)
array([ 0.        ,  1.        ,  1.41421356])
>>> C = np.array([2., -1., 4.])
>>> np.add(B, C)
array([ 2.,  0.,  6.])
```


**살펴보기**

  all, any, apply_along_axis, argmax, argmin, argsort, average, bincount, ceil, clip, conj, corrcoef, cov, cross, cumprod, cumsum, diff, dot, floor, inner, inv, lexsort, max, maximum, mean, median, min, minimum, nonzero, outer, prod, re, round, sort, std, sum, trace, transpose, var, vdot, vectorize, where

### **인덱싱 슬라이싱 이터레이팅**

**일차원** 배열은 리스트나 Python 시퀀스처럼 인덱싱, 슬라이싱, 이터레이팅 할 수 있습니다.

```python
>>> a = np.arange(10)**3
>>> a
array([  0,   1,   8,  27,  64, 125, 216, 343, 512, 729])
>>> a[2]
8
>>> a[2:5]
array([ 8, 27, 64])
>>> a[:6:2] = -1000    # equivalent to a[0:6:2] = -1000; from start to position 6, exclusive, set every 2nd element to -1000
>>> a
array([-1000,     1, -1000,    27, -1000,   125,   216,   343,   512,   729])
>>> a[ : :-1]                                 # reversed a
array([  729,   512,   343,   216,   125, -1000,    27, -1000,     1, -1000])
>>> for i in a:
...     print(i**(1/3.))
...
nan
1.0
nan
3.0
nan
5.0
6.0
7.0
8.0
9.0
```

**Multidimensional** arrays can have one index per axis. These indices are given in a tuple separated by commas:

**다 차원** 배열에서는 축(axis) 당 하나의 인덱스를 가질 수 있습니다. 이 인덱스들은 `,`(commas)로 분리된 튜플에서 제공됩니다.

```python
>>> def f(x,y):
...     return 10*x+y
...
>>> b = np.fromfunction(f,(5,4),dtype=int)
>>> b
array([[ 0,  1,  2,  3],
       [10, 11, 12, 13],
       [20, 21, 22, 23],
       [30, 31, 32, 33],
       [40, 41, 42, 43]])
>>> b[2,3]
23
>>> b[0:5, 1]                       # b의 모든 행에서 두번째 열값
array([ 1, 11, 21, 31, 41])
>>> b[ : ,1]                        # 앞선 예제와 같음
array([ 1, 11, 21, 31, 41])
>>> b[1:3, : ]                      # 두번째와 세번째 행에서의 각 열
array([[10, 11, 12, 13],
       [20, 21, 22, 23]])
```

<!-- 축에 있는 값보다 더 작은 값으로 인덱스를 사용하면 the missing indices are considered complete slices: -->

배열의 인데스로 음수를 사용할 수 있습니다.

```python
>>> b[-1]                                  # 마지막 행. b[-1,:]와 같음
array([40, 41, 42, 43])
```

The expression within brackets in b[i] is treated as an i followed by as many instances of : as needed to represent the remaining axes. NumPy also allows you to write this using dots as b[i,...].

b[i]에서 브라켓 사이에 있는 표현은 로써 다뤄진다.

The dots (...) represent as many colons as needed to produce a complete indexing tuple. For example, if x is a rank 5 array (i.e., it has 5 axes), then


+ x[1,2,...] is equivalent to x[1,2,:,:,:],
+ x[...,3] to x[:,:,:,:,3] and
+ x[4,...,5,:] to x[4,:,:,5,:].

```python
>>> c = np.array( [[[  0,  1,  2],               # a 3D array (two stacked 2D arrays)
...                 [ 10, 12, 13]],
...                [[100,101,102],
...                 [110,112,113]]])
>>> c.shape
(2, 2, 3)
>>> c[1,...]                                   # same as c[1,:,:] or c[1]
array([[100, 101, 102],
       [110, 112, 113]])
>>> c[...,2]                                   # same as c[:,:,2]
array([[  2,  13],
       [102, 113]])
```

**Iterating** over multidimensional arrays is done with respect to the first axis:

```python
>>> for row in b:
...     print(row)
...
[0 1 2 3]
[10 11 12 13]
[20 21 22 23]
[30 31 32 33]
[40 41 42 43]
```

However, if one wants to perform an operation on each element in the array, one can use the `flat` attribute which is an iterator over all the elements of the array:

```python
>>> for element in b.flat:
...     print(element)
...
0
1
2
3
10
11
12
13
20
21
22
23
30
31
32
33
40
41
42
43
```

```
See also
Indexing, Indexing (reference), newaxis, ndenumerate, indices
```

### **Shape Manipulation**

#### **Changing the shape of an array**

#### **Stacking together different arrays**

#### **Splitting one array into several smaller ones**

### **Copies and Views**

#### **No Copy at All**

#### **View or Shallow Copy**

#### **Deep Copy**

#### **Functions and Methods Overview**

### **Less Basic**

#### **Broadcasting rules**

### **Fancy indexing and index tricks**

#### **Indexing with Arrays of Indices**

#### **Indexing with Boolean Arrays**

#### **The ix_() function**

#### **Indexing with strings**

### **Linear Algebra**

#### **Simple Array Operations**

### **Tricks and Tips**

#### **“Automatic” Reshaping**

#### **Vector Stacking**

#### **Histograms**

### **Further reading**


