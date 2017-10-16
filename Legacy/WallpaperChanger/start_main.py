#!/usr/bin/env python3

import sys
import tkinter

class WallpaperManager(tkinter.Frame):
    """배경화면 관리기 프론트엔드
    """
    def __init__(self, master = None):
        """초기화 함수
        """
        # 초기 내부 변수 설정
        self.master = master
        self.is_sliding = False
        # 시작 함수 호출
        super().__init__(master)
        self.pack()
        self.create_root()

    def create_root(self):
        """메인 윈도우 생성
        """
        # 내부 변수 불러오기
        master = self.master
        # 윈도우 타이틀 설정
        master.title('배경화면 관리기 by LuHa')
        # 등급 설정 라벨
        rating_labelframe = tkinter.LabelFrame(master = master)
        rating_labelframe['text'] = '등급'
        rating_labelframe.pack(side = 'top')
        # 등급 설정 체크 박스
        rating_safe_check = tkinter.Checkbutton(rating_labelframe)
        rating_safe_check['text'] = 'Safe'
        rating_safe_check.pack(side = 'left')
        rating_questionable_check = tkinter.Checkbutton(rating_labelframe)
        rating_questionable_check['text'] = 'Questionable'
        rating_questionable_check.pack(side = 'left')
        rating_explicit_check = tkinter.Checkbutton(rating_labelframe)
        rating_explicit_check['text'] = 'Explicit'
        rating_explicit_check.pack(side = 'left')
        # 배경화면 변경 버튼
        change_button = tkinter.Button(master = master)
        change_button['text'] = '배경화면 슬라이드쇼 시작'
        change_button['command'] = self.toggle_slideshow
        change_button.pack(side = 'top')
        self.change_button = change_button
        # 종료 버튼
        close_button = tkinter.Button(master = master)
        close_button['text'] = '종료'
        close_button['fg'] = 'red'
        close_button['command'] = self.destroy_root
        close_button.pack(side = 'bottom')
        self.close_button = close_button

    def toggle_slideshow(self):
        """슬라이드쇼 시작/종료
        """
        # 내부 변수 불러오기
        is_sliding = self.is_sliding
        change_button = self.change_button
        # 배경화면 멈춰있을 때
        if is_sliding == False:
            print('배경화면 슬라이드쇼 시작')
            change_button['text'] = '배경화면 슬라이드쇼 중지'
            change_button['fg'] = 'blue'
            is_sliding = True
        elif is_sliding == True:
            print('배경화면 슬라이드쇼 중지')
            change_button['text'] = '배경화면 슬라이드쇼 시작'
            change_button['fg'] = 'black'
            is_sliding = False
        # 활용한 내부 변수 저장
        self.is_sliding = is_sliding

    def destroy_root(self):
        """메인 윈도우 제거: 프로그램 종료
        """
        # 내부 변수 불러오기
        master = self.master
        # 종료
        master.destroy()


def main(argv):
    """그래픽유저인터페이스 실행
    마스터 프레임을 생성해서 GUI 메인 호출
    """
    print('배경화면 관리기 시작')
    master = tkinter.Tk()
    starter = WallpaperManager(master = master)
    starter.mainloop()
    print('배경화면 관리기 종료')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
