import { connect } from "@dagger.io/dagger";

// Dagger 파이프라인 실행: client 객체를 통해 모든 작업을 수행합니다.
connect(async (client) => {
  // 1. nginx:1.25.5-alpine 이미지를 기반으로 컨테이너 생성
  const nginx = client.container().from("nginx:1.25.5-alpine");

  // 2. 로컬 _site 폴더를 nginx 컨테이너의 웹 루트(/usr/share/nginx/html)로 복사
  const siteDir = client.host().directory("_site");
  const web = nginx.withDirectory("/usr/share/nginx/html", siteDir);

  // 3. 완성된 이미지를 nginx-site.tar 파일로 내보내기
  // await web.export("./nginx-site.tar");

  // 4. 필요시 Docker 레지스트리로 이미지 푸시 (주석 해제 시 사용)
  await web.publish("ghcr.io/garam-park/blog:latest");
});
