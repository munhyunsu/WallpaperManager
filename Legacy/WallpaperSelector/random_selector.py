#!/usr/bin/env python3

from BaseSelector import base_selector
import check_ini

import os # makedirs
import sys # exit, argv
import logging # 로깅
import configparser # configParser
import sqlite3 # SQL
import shutil # copyfile
import argparse # argparse

INIFILE = 'random_selector.ini'

class RandomSelector(base_selector.BaseSelector):
    """배경화면 복사 기본 클래스
    """
    def __init__(self, config_file):
        """설정 파일 입력 받기
        """
        # 부모 클래스 초기화
        base_selector.BaseSelector.__init__(self, config_file)
        # 입력 파일 확인
        if type(config_file) == dict:
            self.config = config_file
        else:
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
        # 설정 파일 확인
        if not check_ini.check_ini(self.config):
            sys.exit(0)
        # 내부 변수 초기화
        self._rating = 'sqe'

    def _prepare_copy(self):
        """복사 준비
        1. 목표 위치 생성 및 비우기
        """
        config = self.config
        dst_path = config['wallpaper']['path']
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        files_in_dst_path = os.scandir(dst_path)
        for entry in files_in_dst_path:
            if not entry.name.startswith('.') \
                    and entry.is_file():
                os.remove(entry.path)
     
    def _get_path(self):
        wallpaper_path = self.config['wallpaper']['path']
        wallpaper_number = str(self.config['wallpaper']['number'])
        wallpaper_map = \
                self.config['wallpaper']['map'].splitlines()

        for map_line in wallpaper_map:
            (database, image) = map_line.split(' ')
            connector = sqlite3.connect(database)
            cursor = connector.cursor()
            cursor.execute('SELECT md5, file_ext FROM image '
                         + self._get_where()
                         + 'ORDER BY RANDOM() '
                         + 'LIMIT ' + wallpaper_number)
            cursor_result = cursor.fetchall()
            for (md5, file_ext) in cursor_result:
                file_name = md5 + '.' + file_ext
                src_path = image + '/' + file_name
                dst_path = wallpaper_path + '/' + file_name
                yield (src_path, dst_path)

    def set_rating(self, rating):
        """등급 설정
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
        # WHERE문 반환
        return result


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rating', nargs='?', help='s/q/e 조합',
            default='seq', type=str)
    args = vars(parser.parse_args(argv[1:]))

    wallpaper_random_selector = RandomSelector(INIFILE)
    wallpaper_random_selector.set_rating(args['rating'])
    wallpaper_random_selector.start_copy()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
