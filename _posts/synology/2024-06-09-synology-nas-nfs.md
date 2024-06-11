---
layout: post_with_ad
title: Synology NAS 설정 기록
date: 2024-06-09 14:30:00 +0900
permalink: /synology/synology-nas-nfs
categories: synology
tags: synology nas, synology nas nfs, synology nas nfs 사용법, synology nas nfs 사용법
---

클라우드 서비스를 사용하는 이유는 여러가지가 있지만 가장 큰 이유는 안정성이다. 그런데 고객이 가장 바쁜 시간대에 문제가 발생하면서 적어도 오늘 할 작업에 대해서 readonly만 가능하라도 제공해야 하는 것을 뼈저리게 느껴서 nas 를 구매해서 데이터를 백업 하기로 마음 먹었다.

db 백업 스크립트를 작성하고 sql 파일로 만들어 보관 하려고 하니, 현재 홈네트워크에서 사용하는 가상화 서버에 NFS 마운트해서 해당 데이터를 보관하는 방법이다.
(우선 가상화서버에 NFS 마운트 하는 것은 성공했지만, 가상화 서버가 다운 됐을 경우 SQL 파일을 직접확인이 불가해서 rsync 를 사용해야...)

---
## 1. NFS 설정 켜기

우선 Synology에서 NFS 설정을 켜주어야 한다.

(현재 사용하는 DSM 7.2 버전이다.)

DMS 에 접속하여   `제어판` > `파일 서비스` > `NFS` 으로 이동한다.
![](/images/2024/06/09-1.png){:style="width:100%"}

위의 그림과 같이 NFS 서비스 활성화를 선택하고 적용을 클릭하여 설정을 저장한다.

이제는 NFS 를 사용할 수 있는 설정이 끝난 것이다.

---
## 2. 공유 폴더 설정

공유 폴더에 NFS 권한 할당해야 mount 해서 사용 가능하다.

제어판 > 공유 폴더 로 이동


NFS 클라이언트로 액세스할 공유 폴더를 선택하고 편집 을 클릭한다.

![](/images/2024/06/09-2.png){:style="width:100%"}

NFS 권한 으로 이동하고 생성을 클릭한다.

![](/images/2024/06/09-3.png){:style="width:100%"}

위와 같은 화면이 나온다.

`호스트 이름또는 IP` 부분에는 접속하려는 서버 IP 입력한다.

(subnet mask 나 cidr를 적당히 입력하는 것 같다.)

그리고 저장을 누른다. 그리고 마운트 경로는 아래의 그림같이 아랫쪽에서 확인이 가능하다.

![](/images/2024/06/09-4.png){:style="width:100%"}


