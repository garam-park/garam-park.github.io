# bundler 설치

```sh
sudo gem install bundler
```

# 지킬 사용법

```bash
bundle install
bundle exec jekyll serve
```

**빌드하기**

```
bundle exec jekyll build # _site 에 생김
```

## 우분투 설치

```
echo '# Install Ruby Gems to ~/gems' >> ~/.zshrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.zshrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 실행 환경 기록

1. ruby 3.1
2. Bundler version 2.2.24
