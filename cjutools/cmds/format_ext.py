
from cjutils.cmd import *
from cjutils.utils import *


class cmd(cmd_base):
    def __init__(self, options_argv=..., brief_intro="", enable_plugins=True) -> None:
        super().__init__([
            ('j', 'json', 'format json file, multiple file separate with ","', "", False),
            ('p', 'python', 'format python file, multiple file separate with ","', "", False),
            ('f', 'fiddler', 'format fiddler request to python code', "", False),
            ('i', 'in-place', 'make changes to files in place', False, False),
            ('o', 'output', 'output result to file', "", False)
        ], brief_intro="format tool", enable_plugins=False)

    def __from_fiddler_text_to_code(self, text: bytes):
        tmp = text.decode().split('\r\n\r\n')
        assert len(tmp) <= 2, f'format error:\n{text}'
        if len(tmp) == 1:
            header = tmp[0]
            body = None
        else:
            header, body = tmp
        header_lines = header.split('\r\n')
        mode, url, _ = header_lines[0].split()
        code = f'req_url = "{url}"\nreq_headers = {{\n'
        for line in header_lines[1:-1]:
            key, *val = line.split(':')
            key = key.replace('"', '\\"')
            val = ':'.join(val).replace('"', '\\"').strip()
            code += f'    "{key}": "{val}",\n'
        key, *val = header_lines[-1].split(':')
        key = key.replace('"', '\\"')
        val = ':'.join(val).replace('"', '\\"').strip()
        code += f'    "{key}": "{val}"\n'
        code += '}\n'
        if mode == 'POST':
            body = body.replace('"', '\\"')
            code += f'req_body = "{body}"\n'
            code += f'req = requests.post(url = req_url, headers = req_headers, data = req_body, verify = False)\n'
        elif mode == 'GET':
            code += f'req = requests.get(url = req_url, headers = req_headers, verify = False)\n'
        else:
            assert False, f'unknown mode: {mode}'
        return code

    def __format_fiddler(self, file=None, content=None):
        if content:
            if isinstance(content, str):
                content = content.encode()
            return self.__from_clipboard, self.__from_fiddler_text_to_code(content)
        with open(file, 'rb') as f:
            return file, self.__from_fiddler_text_to_code(f.read())

    def __format_json(self, file=None, content=None):
        if content:
            return self.__from_clipboard, dump_json(json.loads(content))[1:]
        with open(file, 'r', encoding='utf-8') as f:
            return file, dump_json(json.load(f))[1:]

    def __format_py(self, file=None, content=None):
        mod = import_module('autopep8')
        if content:
            return self.__from_clipboard, mod.fix_code(content)
        with open(file, 'r', encoding='utf-8') as f:
            return file, mod.fix_code(f.read())

    def __format(self):
        def check_and_format(option, format_func):
            if self.get_opt(option) != False:
                files = [d for d in self.get_opt(
                    option).split(',') if len(d) > 0]
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
        check_and_format('f', self.__format_fiddler)

    def main(self):
        self.__res_list = []
        self.__from_clipboard = 'from clipboard'
        self.__format()
        for file, res in self.__res_list:
            print(f'{file:-^80}')
            print(res)
            if self.get_opt('i') and file != self.__from_clipboard:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(res)
            if self.get_opt('o'):
                with open(self.get_opt('o'), 'a', encoding='utf-8') as f:
                    f.write(res)

        if len(self.__res_list) == 0:
            info('nothing to do')
        return 0
