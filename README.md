# Wallpaper manager

## Propose
- Scrap image at Booru-site
- Scrap image at Wallpaper haven
- Scrap image at pixiv
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
- (Optimization) The common code like load tags, search downloaded images, and so on are functionalized.
- (Optimization) Move current working directory from execution location to source code location.
- (Feature) Add a pixiv to the image source.
  - (Not yet) The user can select artist, daily/monthly/yealy rank. tag as image search keyword.
- (GUI) Cut-off log for getting information easily.
  - The cut-off option need.
- (Feature) Option function in manager.
- (Feature) Tag set.
  - We need old tag function for compatibility.
- (Refactoring) The print log function needed.
  - print message with log level.
- (Refactoring) MVC model
  - Model: Database
  - View: What
  - Control: CLI
- (Refactoring) Change logging method
  - logging module globalization
  - global module needs
- GUI using TK
  - Viewer needed
- Parameter passing


### The contributed feature(or incoming)
- None

## Version history

### Scheduled: 1.1.4
- (Optimization) Remove unsed code (commented already) in wallchanger.py
- (GUI) Print message about request url for give user opportunity more information.
- (Feature) Add command `exit' to terminate program.

### 171214: 1.1.3
- (Refactoring) The list of image source disttach from each sources.
  - It can more efficient management using global\_variable
- (Optimization) Set sleep interval beteen image request
  - It keep network bandwith for the server and prevent block of server.
- (Optimization) Remove unsed code (commented already) in manager\_cli.py
- (Optimization) The code about the load ban database is utilized in utils.py.
- (Optimization) The load database function is unified at utils.py
- (Optimization) The change wallpaper function is moved to utils.py
- (Feature) The feature that delete file size 0
  - This feature implemented in manager\_cli.py
- (Feature) Add a pixiv to the image source.
  - The user can select daily rank.

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
