#!/usr/bin/env python3

import check_ini

import os.path
import sys # exit, argv
import logging # 로깅
import configparser # configParser
import sqlite3 # SQL
import subprocess # change background
import time # sleep
import random # choice
import argparse # argparse

INIFILE = 'random_changer.ini'

class RandomChanger(object):
    """배경화면 복사 기본 클래스
    """
    def __init__(self, config_file):
        """설정 파일 입력 받기
        """
        # 입력 파일 확인
        if type(config_file) == dict:
            self.config = config_file
        else:
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
        # 설정 파일 확인
        if not check_ini.check_ini(self.config):
            sys.exit(0)
        # 로깅 시스템 셋업
        if not self._set_logging():
            sys.exit(0)
        # 내부 변수 초기화
        self._rating = 'sqe'
        self._sleep_time = 60

    def _set_logging(self):
        """로그 시스템 셋업
        """
        config = self.config
        filename = config['log']['file']
        level = config['log']['level']
        level = getattr(logging, level)
        try:
            logging.basicConfig(filename = filename,
                                level = level,
                                format = ('%(asctime)s '
                                        + '%(levelname)s: '
                                        + '%(message)s'),
                                datefmt = '%Y.%m.%d %H:%M:%S')
            return True
        except Exception as err:
            logging.critical('__set_logging 예외 발생: {0}'.format(
                    err))
            return False
     
    def _get_image_path(self):
        wallpaper_map = \
                self.config['wallpaper']['map'].splitlines()

        while True:
            choice_map = random.choice(wallpaper_map)
            (database, image) = choice_map.split(' ')
            connector = sqlite3.connect(database)
            cursor = connector.cursor()
            cursor.execute('SELECT md5, file_ext FROM image '
                         + self._get_where()
                         + 'ORDER BY RANDOM() '
                         + 'LIMIT 1')
            cursor_result = cursor.fetchone()
            (md5, file_ext) = cursor_result
            file_name = md5 + '.' + file_ext
            image_path = image + '/' + file_name
            image_path = os.path.abspath(image_path)
            image_path = 'file://' + image_path
            yield image_path

    def set_rating(self, rating):
        """WHERE문 제작용 변수 저장
        """
        self._rating = rating

    def _get_where(self):
        """WHERE문 제작
        """
        rating = self._rating
        # WHERE문 처리
        result = ''
        for rating_index in ['s', 'q', 'e']:
            if rating_index in rating:
                if not 'WHERE' in result:
                    result = result + 'WHERE '
                if 'rating' in result:
                    result = result + 'or '
                result = result + 'rating="' + rating_index + '" '
                #result = result + 'AND tag_string LIKE "%love_live!%" '
                #result = result + 'AND tag_string LIKE "%matsuura_kanan%" '
                #result = result + 'AND tag_string LIKE "%toujou_nozomi%" '
                #result = result + 'AND tag_string LIKE "%pokemon%" '
                #result = result + 'AND (tag_string LIKE "%pokemon%" OR tag_string LIKE "%love_live!%") '
                #result = result + 'AND tag_string LIKE "%pantyhose%" '
                #result = result + 'AND tag_string LIKE "%ass%" '
        # WHERE문 반환
        return result

    def set_sleep(self, sleep_time):
        """Sleep용 변수 저장
        """
        self._sleep_time = int(sleep_time)

    def start_change(self):
        """배경화면 변경 시작
        """
        config = self.config
        sleep_time = self._sleep_time
        image_path_generator = self._get_image_path()
        try:
            logging.info('배경화면 변경 시작: 종료하려면 Ctrl + C')
            for image_path in image_path_generator:
                subprocess.run(['gsettings',
                                'set',
                                'org.cinnamon.desktop.background',
                                'picture-uri',
                                image_path])
                subprocess.run(['gsettings',
                                'set',
                                'org.cinnamon.desktop.background',
                                'picture-opacity',
                                '100'])
                subprocess.run(['gsettings',
                                'set',
                                'org.cinnamon.desktop.background',
                                'picture-options',
                                'scaled'])
                logging.info('배경화면 변경: {0}'.format(image_path))
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            subprocess.run(['gsettings',
                            'set',
                            'org.cinnamon.desktop.background',
                            'picture-uri',
                            'file:///usr/share/backgrounds/linuxmint/edesigner_linuxmint.png'])
            subprocess.run(['gsettings',
                            'set',
                            'org.cinnamon.desktop.background',
                            'picture-opacity',
                            '100'])
            subprocess.run(['gsettings',
                            'set',
                            'org.cinnamon.desktop.background',
                            'picture-options',
                            'scaled'])
            logging.info('배경화면 변경 종료')
            return 0
        except:
            subprocess.run(['gsettings',
                            'set',
                            'org.cinnamon.desktop.background',
                            'picture-uri',
                            'file:///usr/share/backgrounds/linuxmint/sele_linuxmint.png'])
            subprocess.run(['gsettings',
                            'set',
                            'org.cinnamon.desktop.background',
                            'picture-opacity',
                            '100'])
            subprocess.run(['gsettings',
                            'set',
                            'org.cinnamon.desktop.background',
                            'picture-options',
                            'scaled'])
            logging.info('배경화면 변경 강제 종료')
            return 0


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rating', nargs='?', help='s/q/e 조합',
            default='sqe', type=str)
    parser.add_argument('-s', '--sleep', nargs='?', help='전환 시간',
            default='60', type=str)
    args = vars(parser.parse_args(argv[1:]))

    wallpaper_random_changer = RandomChanger(INIFILE)
    wallpaper_random_changer.set_rating(args['rating'])
    wallpaper_random_changer.set_sleep(args['sleep'])
    wallpaper_random_changer.start_change()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
