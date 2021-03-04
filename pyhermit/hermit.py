# -*- coding:utf-8 -*-

"""
hermit.py 封装原生API
"""
import time
import json
import random
import requests


class Hermit(object):
    def __init__(self, hermit_link: str):
        self.link = "http://" + hermit_link

    def request(self, route: str):
        return requests.get(self.link + route, timeout=3)

    def data_screen(self):
        """获取屏幕长宽"""
        result = self.request('/data/screen').json()['data']
        return result['height'], result['width']

    def nodes_text(self):
        return self.request('/data/nodes').text

    def data_nodes(self):
        return json.dumps(self.request('/data/nodes').json(), sort_keys=True, indent=2, ensure_ascii=False)

    def in_page(self, text: str):
        if text in self.get_nodes_text():
            return True
        return False

    def _action(self, action_name) -> bool:
        result = self.request('/action/{0}'.format(action_name))
        if result.json()['code']:
            return False
        else:
            return True

    def action_back(self) -> bool:
        """基于无障碍的返回"""
        return self._action('back')

    def action_home(self) -> bool:
        """基于无障碍的按下Home键"""
        return self._action('home')

    def action_recents(self) -> bool:
        """基于无障碍的显示最近任务"""
        return self._action('recents')

    def action_noticefications(self) -> bool:
        """基于无障碍的打开通知栏"""
        return self._action('noticefications')

    def action_quick_settings(self) -> bool:
        """基于无障碍的拉开下拉栏"""
        return self._action('quick_settings')

    def action_power(self) -> bool:
        """基于无障碍的长按电源键"""
        return self._action('power')

    def action_split_screen(self) -> bool:
        """基于无障碍的分屏"""
        return self._action('split_screen')

    def action_lock_screen(self) -> bool:
        """基于无障碍的锁屏，限制Android 9.0"""
        return self._action('lock_screen')

    def action_screen_shot(self) -> bool:
        """基于无障碍的截屏，限制Android 9.0"""
        return self._action('screen_shot')

    def _click(self, by: str, obj: str, index: int = -1, count: bool = False, sleep: float = 0):
        time.sleep(sleep)
        router = '/click/{0}/{1}'.format(by, obj)
        if index != -1:
            router += '/{0}'.format(index)
        elif count:
            router += '/_count'
        result = self.request(router).json()
        if result.get('code') == 0:
            return result.get('data')
        return False

    def click_id(self, id_name: str, index: int = -1, count: bool = False, sleep: float = 0):
        """基于无障碍的根据资源ID点击"""
        time.sleep(sleep)
        return self._click('id', id_name, index, count)

    def click_text(self, text: str, index: int = -1, count: bool = False, sleep: float = 0):
        """基于无障碍的根据资源文本点击"""
        time.sleep(sleep)
        return self._click('text', text, index, count)

    def click_desc(self, desc: str, sleep: float = 0):
        """基于无障碍的根据资源描述点击"""
        time.sleep(sleep)
        return self._click('desc', desc)

    def click(self, x: int, y: int, sleep: float = 0):
        """无障碍点击坐标"""
        time.sleep(sleep)
        result = self.request('/click?x={0}&y={1}'.format(x, y)).json()
        if result['code']:
            return result['msg']
        return True

    def swipe(self, x1: int, y1: int, x2: int, y2: int, sleep: float = 0):
        """无障碍的方式 从（x1, y1）滑动到（x2, y2）"""
        time.sleep(sleep)
        result = self.request('/swipe?x1={0}&y1={1}&x2={2}&y2={3}'.format(x1, y1, x2, y2)).json()
        if result['code']:
            return False
        return True

    def input(self, by: str, obj: str, text: str, sleep: float = 0):
        rs = self.request('/input?by={0}&obj={1}&text={2}'.format(by, obj, text))
        return True

    def clipboard_pull(self):
        """成功返回字符串，失败返回 False"""
        result = self.request('/data/cliBoard').json()
        if result['code']:
            return False
        return result['data']

    def clipboard_push(self, content: str):
        """设置剪贴板内容"""
        data = {'content': content}
        r = requests.put(self.link + '/data/cliBoard', data=data)
        return True

    def is_root(self):
        """检查root权限"""
        r = requests.get(self.link + '/check/root', timeout=20).json()
        if r['msg']:
            return True
        return False

    def shell_key_event(self, key: int, sleep: float = 0):
        time.sleep(sleep)
        result = self.request('/shell/keyevent?keycode=' + str(key)).json()
        if result['code']:
            return False
        return True

    def shell_tap(self, x: int, y: int, sleep: float = 0):
        """通过shell的方式，点击（x, y）"""
        time.sleep(sleep)
        result = self.request('/shell/tap?x={0}&y={1}'.format(x, y)).json()
        if result['code']:
            return False
        return True

    def shell_swipe(self, x1: int, y1: int, x2: int, y2: int, sleep: float = 0):
        """通过shell的方式 从（x1, y1）滑动到（x2, y2）"""
        time.sleep(sleep)
        result = self.request('/shell/swipe?x1={0}&y1={1}&x2={2}&y2={3}'.format(x1, y1, x2, y2)).json()
        if result['code']:
            return False
        return True

    def input(self, by: str, obj: str, text: str, sleep: float = 0):
        rs = self.request('/input?by={0}&obj={1}&text={2}'.format(by, obj, text))
        return True

    def _is_clickable(self, attr: str, name: str) -> bool:
        """检查该页面是否有该元素"""
        if attr not in ['text', 'id', 'desc']:
            return False
        if attr == 'id':
            attr = 'resource-id'
        elif attr == 'desc':
            attr = 'content-desc'
        nodes = json.loads(self.data_nodes())['data']
        for i in nodes:
            if i.get(attr) and i[attr] == name:
                return True
        return False

    def click_channel(self, pipeline: list):
        for i in pipeline:
            key, value = list(i.keys())[0], list(i.values())[0]
            if not self._is_clickable(key, value):
                count = 5
                while count:
                    if self._is_clickable(key, value):
                        break
                    else:
                        time.sleep(1)
                        count -= 1
            self._click(key, value, 0.3)
        return True

    def _swipe(self, action: str, scope: int, use_shell: bool = False, sleep: float = 0.3):
        """基于shell的 滑动"""
        height, width = self.data_screen()

        swipe_type = self.swipe
        if use_shell:
            swipe_type = self.shell_swipe
        if scope in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            scope = scope * 0.1 / 4
        else:
            scope = 0.2

        seed1 = random.randint(0, 50)
        seed2 = random.randint(0, 50)
        seed = seed2 - seed1
        y1, y2 = int(height / 2) - int(height * scope) + seed, int(height / 2) + int(height * scope) - seed
        x1 = x2 = int(width / 2) + int(seed * 5)
        n1 = n2 = int(height / 2) + int(seed * 9)
        m1, m2 = int(width / 2) - int(width * scope) + seed, int(width / 2) + int(width * scope) - seed

        if action == 'up':
            swipe_type(x1, y2, x2, y1)
        elif action == 'down':
            swipe_type(x1, y1, x2, y2)
        elif action == 'left':
            swipe_type(m2, n1, m1, n2)
        else:
            swipe_type(m1, n1, m2, n2)
        time.sleep(sleep)

    def swipe_down(self, scope: int = 2, sleep: float = 0):
        self._swipe('down', scope, False, sleep)

    def swipe_up(self, scope: int = 2, sleep: float = 0):
        self._swipe('up', scope, False, sleep)

    def swipe_left(self, scope: int = 2, sleep: float = 0):
        self._swipe('left', scope, False, sleep)

    def swipe_right(self, scope: int = 2, sleep: float = 0):
        self._swipe('right', scope, False, sleep)

    def shell_swipe_down(self, scope: int = 2, sleep: float = 0):
        self._swipe('down', scope, True, sleep)

    def shell_swipe_up(self, scope: int = 2, sleep: float = 0):
        self._swipe('up', scope, True, sleep)

    def shell_swipe_left(self, scope: int = 2, sleep: float = 0):
        self._swipe('left', scope, True, sleep)

    def shell_swipe_right(self, scope: int = 2, sleep: float = 0):
        self._swipe('right', scope, True, sleep)

    def data_device(self):
        return self.request('/data/device').json()
