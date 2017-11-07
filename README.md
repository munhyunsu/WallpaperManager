# Wallpaper manager

## Propose
- Scrap image at Booru-site
- Scrap image at Wallpaper haven
- Manage downloaded image
  - Check downloaded image: Ban/Save image

## Usage

### main/manager\_cli.py
- python3 manager\_cli.py


## The feature that need contributon

### The TODO feature
- The wallpaper manager GUI version
- (Pending) Display the number of images in downloads directory
  - It has some performance issue, so it pend until someone request it.
- (Optimization) Set sleep interval beteen image request
  - It keep network bandwith for the server and prevent block of server.
- (Optimization) The common code like load tags, search downloaded images, and so on are functionalized.

### The contributed feature(or incoming)
- None

## Version history

### 171103: 1.1.2
- (Bugfix) Exception handling
  - function to Handle exception on RandomChanger
    - IndexError occured when no files in downloads directory
- (Feature request) Mute category
  - It just image mute, until mute clear
  - Mute function is used, when user want temporary do not show that
- (Optimization) Modify timeout try-except state range
  - After several times usage the timeout exception is called at response wait
  - The timeout occured at low-speed network environment
- (GUI) The colored text for better visibility
- Auto-delete feature added
  - When the wallpaper change to new one, the old one is deleted
- Merge check wallpaper and random wallpaper
  - After now, auto-change feature is available in check wallpaper
  - The random wallpaper is deleted

### 171031: 1.1.1d
- (Bugfix) SIGTERM messages are sended only to child process when running random changer
  - (Bug) SIGTERM message is also going to parent process not only child.
    - Expecially to terminate random changer, the user press SIGTERM

### 171029: 1.1.1c
- (Bugfix) add import socket.timeout
  - occure library missing error when the request is timeout
  - (Bug) Execute dummy\_downloader.py
    - This happends because of dummy
- (Bugfix) change start\_download function behavior
  - It changed to call subprocess by paramater from by global variable
  - From now, dummy error is not showing

### 171024: 1.1.1b
- The slideshow using only downloaded images
  - It can receive sleep time from user

### 171019: 1.1.1a
- Compatitable to python 3.5.x
  - split os.scandir flow by python minor version

### 171017: 1.1.1
- (TODO) added alpha.Wallhaven.cc as image source
- Request timeout exception control (Graceful termination)

### 171016: 1.1.0
- Launch Wallpaper manager cli!
- Change language Korean to English
  - README, Source code comment

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
