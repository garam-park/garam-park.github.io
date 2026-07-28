# jekyll readme

## Docker로 Jekyll 사이트 생성

```sh
docker run --rm -v "$PWD":/srv/jekyll -it jekyll/jekyll jekyll new .
```

- --rm: 종료 시 컨테이너 삭제
- -v "$PWD":/srv/jekyll: 현재 디렉토리를 컨테이너에 마운트
- jekyll new .: 현재 디렉토리에 새 프로젝트 생성

## Docker로 Jekyll 서버 실행

명시적으로하는 것이 좋음

```sh
# 암묵적으로 하기
# 
docker run --rm -v "$PWD":/srv/jekyll -p 4000:4000 -it jekyll/jekyll jekyll serve --watch --force_polling

# 명시적으로 하기
# docker pull jekyll/jekyll:4.2.2
docker run --rm -v "$PWD":/srv/jekyll -p 4000:4000 -it jekyll/jekyll:4.2.2 jekyll serve --watch --force_polling
```

- --watch: 변경사항 감지
- --force_polling: Docker 환경에서는 파일 변경 감지가 잘 안되기 때문에 추가
- 브라우저에서 <http://localhost:4000> 열기

## Docker 로 _site 만드는 방법

```sh
docker run --rm -v "$PWD":/srv/jekyll -it jekyll/jekyll:4.2.2 jekyll build
```

## 배포용 이미지 빌드 (멀티스테이지)

`Dockerfile`이 Jekyll 빌드(ruby) → nginx 서빙까지 한 번에 처리하므로
`_site`를 미리 만들 필요 없이 단독으로 이미지를 만들 수 있다.

```sh
# 이미지 빌드
docker build -t blog .

# 컨테이너 실행 후 http://localhost:8080 확인
docker run --rm -p 8080:80 blog
```

### docker compose 로 실행

운영과 동일하게 멀티스테이지 이미지를 빌드해 nginx로 서빙한다.

```sh
docker compose up --build
# http://localhost:9090
```

### 로컬 개발 (라이브 리로드)

소스를 마운트해 `jekyll serve`로 띄운다. 글·레이아웃을 고치면 즉시 반영되며
이미지를 다시 빌드할 필요가 없다.

```sh
docker compose -f docker-compose.dev.yml up --build
# http://localhost:4000
```

### 레지스트리(ghcr.io) 배포

`main` 브랜치에 push 하면 GitHub Actions(`.github/workflows/docker-publish.yml`)가
이미지를 빌드해 `ghcr.io/garam-park/blog:latest` 로 자동 푸시한다.
