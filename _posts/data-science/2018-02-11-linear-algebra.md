---
layout: post_with_ad
title:  "3장 선형대수"
permalink : /data-science/04-linear-algebra
date:   2018-02-11 14:33:51 +09:00
categories: python3
tags :  python
excerpt : hello data science
---

## 선형대수

## **4.1 벡터**

### **벡터의 합**

각 성분끼리 더 한다.

**python3**

```python
def vector_add(v, w):
    return [v_i + w_i for v_i, w_i in zip(v,w)]

v = [1,2]
w = [3,4]

ret = vector_add(v,w);
```

**numpy**

```python
v = np.array([1,2])
w = np.array([3,4])
z = v + w #array(4,6)
```

### **벡터의 차**

각 성분끼리 뺀다.

**python3**

```python
def vector_subtract(v, w):
    return [v_i - w_i for v_i, w_i in zip(v,w)]
```

**numpy**

```python
v = np.array([1,2])
w = np.array([3,4])
z = v - w #array([-2, -2])
```

### **벡터의 총합**

벡터의 각 요소를 모두 더한다.

**python3**

```python
#Reduce 를 이용
def vector_sum1(vectors):
    return reduce(vector_add, vectors)

#for 문을 이용
def vector_sum2(vectors):
	result = vectors[0]
	for vector in vectors[1:]:
		result = vector_add(result,vector)
	return result

#partial 를 이용
vector_sum3 = partial(reduce,vector_add)

```

**numpy**

```python
np.sum([1,2,3]) #6
#https://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html
```

### **스칼라 벡터 곱**

벡터의 각 요소에 스칼라를 곱한다.

**python3**

```python
def scalar_multiply(c, v):
    return [c * v_i for v_i in v]
```

**numpy**

```python
a = np.array([1,2,3,4])
b = 3 * a # b 는 array([ 6,  9, 12])
c = a * 3 # c 는 array([ 6,  9, 12])
```

### **벡터 성분의 평균**

벡터의 각 요소 값의 평균을 구한다.

**python3**

```python
def vector_mean(vectors):
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))
```

**numpy**

```python
a = np.array([[1, 2], [3, 4]])
b = np.mean(a) # b 는 2.5
```

### **벡터 내적(inner product)**

두 백터의 같은 성분 끼리 곱한 후 모두 더해준 값. 결과는 스칼라이다.한 벡터가 다른 벡터로 투영된 길이를 나타낸다고 볼 수 있다.

**python3**

```python
def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))
```

**numpy**

```python
a = np.array([1,2,3])
b = np.array([2,2,2]) 
c = np.inner(a, b) # 1 * 2 + 2 * 2 + 3 * 2
# c = 12 
```

### **각 성분의 제곱의 합**

각 성분을 곱한 후에 더 한 값, 벡터의 길이의 제곱

**python3**

```python
def sum_of_squares(v):
    return dot(v, v)
```

**numpy**

```python
a = np.array([1,2,3])
b = np.sum(a**2) # b = 1 + 4 + 9 = 14
```

### **벡터의 크기**

벡터의 크기, 스칼라 값.

**python3**

```python
def magnitude(v):
    return math.sqrt(sum_of_squares(v))
```

**numpy**

```python
a = np.array([2,2,2,2])
b = np.linalg.norm(a) #b 는 4 , 4 + 4 + 4 + 4 = 16 = 4의 제곱
```

### **두 벡터간의 거리의 제곱**

**python3**

```python
def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))
```

```python
a = np.array([4,3,2,1])
b = np.array([2,1,0,-1])
c = np.sum((a-b)**2) # 16
```

### **두 벡터간의 거리**

**numpy**

```python
a = np.array([4,3,2,1])
b = np.array([2,1,0,-1])
c = math.sqrt(np.sum((a-b)**2)) #4.0
```

### **두 벡터간의 거리 1**

```python
def distance1(v, w):
   return math.sqrt(squared_distance(v, w))
```

### **두 벡터간의 거리 2**

```python
def distance2(v, w):
   return magnitude(vector_subtract(v,w))
```

## **4.2 행렬**

### **형태**

**python3**

```python
def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols
```

**numpy**

```python
a = np.array([[1,2,3],[4,5,6]])
b = np.shape(a) # b는 (2,3), 2행 3열
```

### **행**

**python3**

```python
def get_row(A, i):
    return A[i]
```

**numpy**

```python
a = np.array([[1,2,3],[4,5,6]])
a[0]#array([1, 2, 3])
a[1]#array([4, 5, 6])
```

### **열**

**python3**

```python
def get_column(A, j):
    return [A_i[j] for A_i in A]
```

**numpy**

```python
a = np.array([[1,2,3],[4,5,6]])
a[:,0]#array([1, 4])
a[:,1]#array([2, 5])
a[:,2]#array([3, 6])
```


### **행렬 만들기**

**python3**

```python
def make_matrix(num_rows, num_cols, entry_fn):
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]
```

**numpy**

```python
a = np.array([[1,2,3],
             [4,5,6]])
```

### **단위 행렬**

**python3**

```python
def is_diagonal(i, j):
    return 1 if i == j else 0
```

**numpy**

```python
np.eye(2)
#array([[ 1.,  0.],
#       [ 0.,  1.]])
np.eye(3)
#array([[ 1.,  0.,  0.],
#       [ 0.,  1.,  0.],
#       [ 0.,  0.,  1.]])
np.eye(4)
#array([[ 1.,  0.,  0.,  0.],
#       [ 0.,  1.,  0.,  0.],
#       [ 0.,  0.,  1.,  0.],
#       [ 0.,  0.,  0.,  1.]])
```

## **더 알아보기**

### **zip** `zip(*iterables)` 함수

```python
list(zip([1, 2, 3], [4, 5, 6])) # [(1, 4), (2, 5), (3, 6)]
list(zip([1, 2, 3], [4, 5, 6], [7, 8, 9])) #[(1, 4, 7), (2, 5, 8), (3, 6, 9)]
list(zip("abc", "def")) #[('a', 'd'), ('b', 'e'), ('c', 'f')]
```
