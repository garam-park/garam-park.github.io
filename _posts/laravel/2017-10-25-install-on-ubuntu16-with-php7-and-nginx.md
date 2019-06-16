---
layout: post_with_ad
title: "[Laravel] 라라벨 설치하기 PHP7.0 + Nginx"
permalink: /laravels/install-on-ubuntu16-with-php7-and-nginx
date: 2017-10-25 07:49:24 +0900
categories: design pattern
tags : laravel, laravel install, nginx, install laravel, laravel install with nginx, laravel inatll with php7, php7, 라라벨설치, 라라벨 설치
excerpt : PHP7에서 놀라운 성능계선이 있었기 때문에 PHP5 버전을 사용하기 보다는 PHP7버전을 사용하는 것이 좋고 보안적으로도 좋아졌다고 합니다. 이 글에서는 라라벨을 PHP7과 nginx로 서버설정하는 방법에 대해서 설명합니다.
---

## **시작하기**

PHP7에서 놀라운 성능계선이 있었기 때문에 PHP5 버전을 사용하기 보다는 PHP7버전을 사용하는 것이 좋고 보안적으로도 좋아졌다고 합니다. 이 글에서는 라라벨을 PHP7과 nginx로 서버설정하는 방법에 대해서 설명합니다.

## **Composer 설치**

최신 `composer`를 설치하기 위해서는 다음 코드를 입력합니다. `composer` 공식 홈페이지에가면 각 운영체제별로 설치하는 방법이 나와있습니다. [링크](https://getcomposer.org/download/)를 참조하세요. 아래의 코드 중에서 해시키의 경우 최신 업데이트가 되면 변경됩니다. 변경된 해키기 확인은 [여기](https://composer.github.io/pubkeys.html)를 확인하세요.

```shell
sudo apt update
sudo apt install php7.0 wget
wget https://getcomposer.org/installer
mv installer composer-setup.php
php -r "if (hash_file('SHA384', 'composer-setup.php') === '544e09ee996cdf60ece3804abc52599c22b1f40f4323403c44d44fdfdd586475ca9813a858088ffbc1f233e9b180f061') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
```

컴포저를 `bin`폴더로 옴겨 줍니다.

```shell
sudo mv composer.phar /usr/local/bin/composer
```

### **중요 패키지 설치**

라라벨에서는 필수적인 몇몇 프로그램이 있습니다. 다음과 같이 설치해주세요.

```shell
sudo apt install vim nginx git #vim 대신 nano 가능
sudo apt install php7.0-fpm php7.0-mysql php7.0-zip php7.0-gd
sudo apt install mcrypt php7.0-mcrypt
sudo apt install php7.0-mbstring php7.0-xml
```

### **설정 변경**

`/etc/php/7.0/fpm/php.ini`를 설정 파일에서 `cgi.fix_pathinfo`를 0으로 설정해줍니다.

```
cgi.fix_pathinfo=0
```

해당 값이 1인 경우에는 비정상적인 접근이 가능합니다. 자세한 내용은 해당 설정 주석 내용을 확인하세요.

### **nginx site 정보 수정**

`/etc/nginx/site-available`에 있는 `default` 파일을 다음 코드와 변경해 줍니다.

```nginx
server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;

        root /var/www/laravel/public;
        index index.php index.html index.htm;

        # Make site accessible from http://localhost/
        server_name <Your Domain name / Public IP Address>;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ /index.php?$query_string;
                # Uncomment to enable naxsi on this location
                # include /etc/nginx/naxsi.rules
        }
        location ~ \.php$ {
                try_files $uri =404;
                fastcgi_split_path_info ^(.+\.php)(/.+)$;
                fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
                fastcgi_index index.php;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;
        }
}
```

코드중에서 `root` 부분은 laravel 프로젝트 루트에 있는 `public` 폴더로 설정합니다. `server_name`의 경우 진입하는 주소를 넣어줍니다. ~~'\_' 으로 하면 모든 경로가 포함됩니다.~~

### **라라벨 프로젝트 다운로드**

다음은 라라벨 패키지를 프로젝트 형태로 받아줍니다.

```shell
cd ~
sudo composer create-project laravel/laravel
#sudo composer create-project laravel/laravel tutorial
```

위의 `sudo composer create-project laravel/laravel` 명령어 뒤에 문자열을 추가하면 원하는 폴더명으로 프로젝트 폴더를 만들 수 있습니다. 주석 처리된 부분은 tutorial이라는 이름으로 프로젝트를 만들어 주는 명령어입니다.

### **라라벨 프로젝트 의존성 설치**

다음과 같이 의존 패키지들을 설치합니다.

```shell
cd laravel
composer install
```

위의 설정 파일은`root`에 `/var/www/laravel/public`으로 설정되어있기 때문에 해당 설정데로 하기 위해서는 다음과 같이 이동합니다.

```shell
cd /var/www
sudo ln -s ~/laravel # 잘안될 경우 설치 경로를 직접 입력해주세요.
```

### **라라벨 프로젝트 그룹 및 접근제한 설정**

```shell
sudo chown -R :www-data .
sudo chmod -R 775 ./storage
```

### **서버 재시작**

```shell
sudo service php7.0-fpm start
sudo service nginx start
```

이후에 접속 테스트 후 laravel 페이지가 응답하는지 확인하시기 바랍니다.


