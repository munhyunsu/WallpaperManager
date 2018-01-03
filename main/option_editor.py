#!/usr/bin/env python3

import sys
import json

import utils

def main(argv):
    # TODO(LuHa): load options
    options = utils.get_database('options.secret', across = True)

    # TODO(LuHa): print menu
    while True:
        print('\n----+----+ Edit options ----+----+')
        print('Current options')
        print(json.dumps(options, indent = '  '))
        print('1. Toggle downloaded image log')
        print('b. Back')

        user_input = input('User input: ')
        user_input = user_input.lower()
        user_input = user_input.strip()
        # TODO(LuHa): handle user input
        if user_input == '1':
            options['log'] = not options.get('log', False)
        elif user_input == 'b':
            break

    # TODO(LuHa): save options
    utils.set_database('options.secret', options, across = True)


# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[OptionEditor] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
