#!/usr/bin/env python3

import sys

def main(argv):
    # TODO(LuHa): load options

    # TODO(LuHa): print menu
    while True:
        print('1. Toggle downloaded image log')
        print('b. Back')

        user_input = input('User input: ')
        user_input = user_input.lower()
        user_input = user_input.strip()
        # TODO(LuHa): handle user input
        if user_input == '1':
            pass
        elif user_input == 'b':
            break

    # TODO(LuHa): save options

    print('[Option] Excute option editor')
    print('[Option] Terminate option editor')

# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[OptionEditor] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
