
from cjutils.cmd import *
from cjutils.utils import *


class cmd(cmd_base):
    def __init__(self, options_argv=..., brief_intro="", enable_plugins=True) -> None:
        super().__init__([
            ('j', 'json', 'format json file, multiple file separate with ","', "", False),
            ('p', 'python', 'format python file, multiple file separate with ","', "", False),
            ('o', 'overwrite', 'overwrite file', False, False)
        ], brief_intro="format tool", enable_plugins=False)

    def __format_json(self, file=None, content=None):
        if content:
            return '', dump_json(json.loads(content))[1:]
        else:
            with open(file, 'r') as f:
                return file, dump_json(json.load(f))[1:]

    def __format_py(self, file=None, content=None):
        mod = import_module('autopep8')
        if content:
            return '', mod.fix_code(content)
        with open(file, 'r') as f:
            return file, mod.fix_code(f.read())

    def __format(self):
        if self.get_opt('j'):
            files = self.get_opt('j').split(',')
            if len(files) == 0:
                info('try to use clipboard')
                self.__res_list.append(
                    self.__format_json(content=get_clipboard()))
            for file in files:
                if not pexist(file):
                    warn(f'{file} not exist')
                    continue
                with open(file, 'r') as f:
                    self.__res_list.append(self.__format_json(file))

        elif self.get_opt('p'):
            files = self.get_opt('p').split(',')
            if len(files) == 0:
                info('try to use clipboard')
                self.__res_list.append(
                    self.__format_py(content=get_clipboard()))
            for file in files:
                if not pexist(file):
                    warn(f'{file} not exist')
                    continue
                with open(file, 'r') as f:
                    self.__res_list.append(self.__format_py(file))
        else:
            info('nothing to do')

    def main(self):
        self.__res_list = []
        self.__format()
        for file, res in self.__res_list:
            print(f'{file:-^80}')
            print(res)
            if self.get_opt('o'):
                with open(file, 'w') as f:
                    f.write(res)
        return 0
