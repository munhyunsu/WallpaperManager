#!/usr/bin/env python3

import utils

# image source
IMAGESOURCES = ['danbooru',
                'yandere',
                'wallhaven',
                'pixiv']

# timeout
TIMEOUT = 30

# TODO(LuHa): This variable is shared across program.
#options = utils.get_database('options.secret', across = True)
# TODO(LuHa): set logger level
# CRITICAL 50
# ERROR 40
# WARNING 30
# INFO 20
# DEBUG 10
# NOTSET 0
#logging.basicConfig(format = 
#        '%(asctime)s:%(created)s:%(levelno)s:%(message)s',
#                    level = logging.NOTSET)
#logger = logging.getLogger('WM')
#logger.propagate = False
#file_handler = logging.FileHandler('wm.log')
#file_handler.setLevel(logging.ERROR)
#console_handler = logging.StreamHandler(sys.stdout)
#console_handler.setLevel(options['log'])
#logger.addHandler(file_handler)
#logger.addHandler(console_handler)
