#!/usr/bin/env python3

import sys

def main(argv):
    # TODO(LuHa): load options

    # TODO(LuHa): print emnu

    # TODO(LuHa): handle user input

    # TODO(LuHa): save options

    print('[Option] Excute option editor')
    print('[Option] Terminate option editor')

# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[OptionEditor] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
