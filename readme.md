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
