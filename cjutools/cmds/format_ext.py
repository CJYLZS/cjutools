
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
            return 'from clipboard', dump_json(json.loads(content))[1:]
        else:
            with open(file, 'r', encoding='utf-8') as f:
                return file, dump_json(json.load(f))[1:]

    def __format_py(self, file=None, content=None):
        mod = import_module('autopep8')
        if content:
            return 'from clipboard', mod.fix_code(content)
        with open(file, 'r', encoding='utf-8') as f:
            return file, mod.fix_code(f.read())

    def __format(self):
        def check_and_format(option, format_func):
            if self.get_opt(option) != False:
                files = [d for d in self.get_opt(option).split(',') if len(d) > 0]
                if len(files) == 0:
                    info('try to use clipboard')
                    self.__res_list.append(
                        format_func(content=get_clipboard()))
                for file in files:
                    if not pexist(file):
                        warn(f'{file} not exist')
                        continue
                    with open(file, 'r') as f:
                        self.__res_list.append(format_func(file))
        check_and_format('j', self.__format_json)
        check_and_format('p', self.__format_py)

    def main(self):
        info(self.exec_dir)
        self.__res_list = []
        self.__format()
        for file, res in self.__res_list:
            print(f'{file:-^80}')
            print(res)
            if self.get_opt('o'):
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(res)
        if len(self.__res_list) == 0:
            info('nothing to do')
        return 0
