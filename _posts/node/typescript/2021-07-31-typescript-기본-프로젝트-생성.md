---
layout: post_with_ad
title: typescript 기본 프로젝트 생성
date: 2021-07-31 18:50:06 +0900
permalink: /node/typescript-기본-프로젝트-생성
categories: node typescript
tags: node typescript
lang: ko
description: "TypeScript 기본 프로젝트를 세팅하는 방법. npm init부터 typescript 설치와 tsconfig 구성까지 최소 프로젝트 구조를 잡는 과정을 정리합니다."
---

### ts project 구조 잡기

```bash
npm init -y
npm i typescript -D
node_modules/typescript/bin/tsc --init
```

### Hello World console

```bash
mkdir src
touch src/index.ts
```

```tsx
// index.ts
console.log("hello world");
```

```tsx
// generate src/index.js
node_modules/typescript/bin/tsc src/index.ts
```

```tsx
// src/index.js
console.log("hello world");
node src/index.js
=> hello world
```

tsconfig.json 수정

```json
{
  "compilerOptions": {
    "target": "es2015",
    "module": "commonjs",
    // complie 된 파일이 있는 곳
    "outDir": "./out",
    "strict": true,
    // typescript 파일 있는 곳
    "rootDirs": ["src"],
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

```bash
rm src/index.js
# tsconfig.json 을 바탕으로 컴파일
node_modules/typescript/bin/tsc
# out/index.js 생성됨
node out/index.js
=> hello world
```

### ts-node

```bash
npm i ts-node -D
node_modules/ts-node/dist/bin.js src/index.ts
=> hello world
```

### ts jest

```bash
npm i jest @types/jest ts-jest
touch jest.config.js
```

```jsx
module.exports = {
  transform: { "^.+\\.ts?$": "ts-jest" },
  testEnvironment: "node",
  testRegex: "/tests/.*\\.(test|spec)?\\.(ts|tsx)$",
  moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"],
  cacheDirectory: ".jest/cache",
};
```

```jsx
// package.json
"scripts": {
    "test": "jest"
  },
```

```jsx
//sum.ts
export default (...a: number[]) => a.reduce((acc, val) => acc + val, 0);
```

```jsx
//tests/sum.test.ts
import sum from "../src/sum";

test("basic", () => {
  expect(sum()).toBe(0);
});

test("basic again", () => {
  expect(sum(1, 2)).toBe(3);
});
```

```jsx
npm t
//or
npm test
//or
npm run test
```

### eslint 적용

```bash
npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

### 한번에 적용하기

```sh
npm init -y
npm i typescript ts-node jest @types/jest ts-jest --save-dev
npm i tsconfig-paths tsconfig-paths-jest
mkdir src
mkdir tests
echo '{
  "compilerOptions": {
    "target": "ES2021",
    "module": "ESNext",
    // complie 된 파일이 있는 곳
    "outDir": "./out",
    "strict": true,
    // typescript 파일 있는 곳
    "declaration": true,
    "rootDirs": ["src"],
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["./src"]
}' > tsconfig.json
echo "module.exports = {
    transform: {'^.+\\.ts?$': 'ts-jest'},
    testEnvironment: 'node',
    testRegex: '/tests/.*\\.(test|spec)?\\.(ts|tsx)$',
    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
    cacheDirectory: '.jest/cache',
}" > jest.config.js
echo "node_modules
.jest
" > .gitignore
```
