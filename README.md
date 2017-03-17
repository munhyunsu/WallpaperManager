# 배경화면 관리자

## 목표
- Booru 계열 서비스 배경화면 수집기
- Wallpaper 계열 서비스 배경화면 수집기
- 수집한 배경화면 관리
- 수집한 배경화면 샘플링을 이용해 슬라이드쇼 지원

## 사용법

### BooruCrawler
- Booru 계열 배경화면 수집기 기본 클래스

### DanbooruCrawler
- Danbooru 배경화면 수집기

### YandereCrawler
- Yandere 배경화면 수집기

### BaseSelector
- 배경화면 선택기 기본 클래스

### WallpaperSelector
- 배경화면 선택기
  - 인자로 s / q / e 의 조합을 받음

### WallpaperChanger
- 배경화면 변경기
  - 인자로 s / q / e 의 조합을 받음
  - 170317 현재 Linux Mint Cinnamon 에서만 동작

## 추가 예정 혹은 기여 대기 기능

### 추가 예정
- https://alpha.wallhaven.cc/ 수집 및 관리

### 기여 대기 기능
- None

## 버전 히스토리

### 170317: 1.0.1a
- 배경화면 변경기 인자 옵션 추가
- 배경화면 선택기 인자 옵션 추가

### 170317: 1.0.1
- 배경화면 변경기 추가

### 170316: 1.0.0a
- 배경화면 선택기 인자를 받도록 수정

### 170316: 1.0.0
- Hobby 프로젝트에서 분리!
  - https://github.com/munhyunsu/Hobby.git
