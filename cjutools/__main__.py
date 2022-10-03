import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from cjutils.cmd import cmd_base
from cjutils.utils import *


class cmd(cmd_base):
    def __init__(self) -> None:
        super().__init__([
        ], brief_intro="tools base", enable_plugins=True, plugin_dir=os.path.realpath(pjoin(dirname(__file__), 'cmds/')), enable_empty_options=False)

    def main(self):

        return 0


if __name__ == "__main__":
    sys.exit(cmd().main())
