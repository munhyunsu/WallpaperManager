#!/usr/bin/env python3

import sys

def main(argv):
    print('[Option] Excute option editor')
    print('[Option] Terminate option editor')

# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[OptionEditor] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
