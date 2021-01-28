# hermit-py
对hermit 的API进行简单的封装，做成了这个Python Moudle，推荐通过wheel的方式安装。  
目前对点击、滑动、模拟输入、找组件、等支持较好，支持查看页面的实时布局信息，再通过布局信息进行点击滑动等操作。 
支持剪贴板相关的操作，支持设置剪贴的任意语言内容。解决了adb不能设置为中文的痛点。  

### 未来  
如果反响尚可，会持续优化，注入更多新的功能，比如可视化查看组件信息等。

### 请先看三个演示，再阅读下方的详细说明
### 演示1：群聊抢红包  
![](https://www.lookcos.cn/wp-content/uploads/2021/01/2021012805375112.gif)
```python
import time
from pyhermit import Hermit

hm = Hermit('127.0.0.1:9999')

# 每隔0.1秒监视一次
while not hm._is_clickable('text', '微信红包'):
    time.sleep(0.1)

hm.click_text('微信红包')
# 模拟器配置低，打开红包过程略慢，需要等待1秒钟，才能再开。
hm.click_desc('开', 1)
```

### 演示2：打开酷安并快速找到并进入iPhone SE区  
![](https://www.lookcos.cn/wp-content/uploads/2021/01/2021012805074049.gif)

```python
import time
from pyhermit import Hermit
# 实例化
hm = Hermit('127.0.0.1:9999')
# 按下home键
hm.action_home()
hm.click_channel([
    {'text': '酷安'}, {'text': '闲聊'},
    {'text': '数码'}, {'text': '平板'},
    {'text': '手机'}, {'text': '苹果'}
])
# 如果没找到，就一直下滑，直到找到为止。
while not hm._is_clickable('text', 'iPhone SE'):
    hm.swipe_up(4)
    time.sleep(0.2)
hm.click_text('iPhone SE')
```

###演示3： 打开微信，并搜索v2ex  
![](https://www.lookcos.cn/wp-content/uploads/2021/01/202101280528008.gif)
```python
import time
from pyhermit import Hermit

hm = Hermit('127.0.0.1:9999')

hm.click_text('微信', 1)
hm.shell_tap(670, 86)
time.sleep(1)
hm.input('id', 'com.tencent.mm:id/bhn', 'v2ex')
hm.click_id('com.tencent.mm:id/b3b', 1)
time.sleep(5) # 等待搜索结果
hm.swipe_up(5)
```  

### 实例化  
在此之前，请确保要操作设备已经安装了hermit APP。
```python
from pyhermit import Hermit
hm = Hermit('127.0.0.1:9999')
"""
127.0.0.1:9999 是hermit APP 运行的IP地址加端口。
如果是模拟器，需要先连接 adb，再设置端口转发即可，以mumu为例，如下：
"""
```
```bash
adb connect 127.0.0.1:7555
adb forward tcp:9999 tcp:9999
# 看到返回 9999， 就是成功了。
```
### 点击与滑动  
点击与滑动是最基本的操作了，支持无障碍和root两种方式。  
无障碍能够根据页面中 `text`、`resource-id`、`content-desc`进行查找组件并点击。  
root方式则可以点击屏幕中任意一个坐标位置，和无障碍能够较好的相互互补。  
- 无障碍的方式点击
```python

# 下面分别演示，通过text、resource-id、和content-desc点击
hm.click_text('酷安', 1)
hm.click_id('com.coolapk.market:id/title_view')
hm.click_desc('搜索')
"""
这三个函数，都有一个缺省参数，sleep，单位为秒，可以等待上一个操作执行。
例如，当你打开一个APP，他有首屏广告时，我们需要等待之后再执行点击。

一个一个click似乎不太过瘾，那么可以尝试用`channel`打一套组合拳。
"""
hm.click_channel([
    {'text': '酷安'}, {'id': 'com.coolapk.market:id/title_view'},
    {'desc': '搜索'},
])
# 它会遍历并执行数组中的操作，自带判断功能，默认5s等待时间（每秒判断一次是否可点击），超时自动下一个。
```
- root的点击与滑动  
```python

# 申请root权限  
hm.is_root()
# 点击坐标（100, 100）（2，同为缺省参数，等待上一个操作的时间）
hm.shell_tap(100, 100, 2)

# 从（x1, y1）滑动到（x2, y2）
hm.shell_swipe(100, 100, 100, 500)

# 衍生的上下左右滑动(加入了随机数值，防止被检测)  
hm.swipe_up()
hm.swipe_down()
hm.swipe_left()
hm.swipe_right()
# 他们都有一个缺省参数scope，默认为2，表示幅度，范围[1, 10]。 数值越大，范围越大
hm.swipe_up(5)  # 大约滑动半屏距离
hm.swipe_up(10) # 大约滑动满屏距离
```

### 全局操作  

```python
hm.action_back() # 返回  
hm.action_home() # 按home键 
hm.action_power() # 长按电源键  
hm.action_recents() # 显示最近任务  
hm.action_noticefications() # 拉下通知栏  
hm.action_lock_screen() # 锁屏  
hm.action_quick_settings() # 下拉打开快速设置  
hm.action_split_screen() # 分屏 限制 Android 9.0  
hm.action_screen_shot()  # 截屏 限制 Android 9.0  
```

### 剪贴板操作 
```python
hm.cliboard_push('法外狂徒')  # 设置剪贴板内容  
hm.cliboard_pull() # 读取剪切板内容
```  

### 有用的辅助操作
```python
from pyhermit import Hermit
hm = Hermit('127.0.0.1:9999')

# 打印当前界面的布局信息, 可以用来找resource-id、text等，进而进行点击与模拟输入  
print(hm.get_nodes())

# 以下方法均返回 布尔类型
hm.is_root() # 申请并判断是否有root权限  
hm.in_page('加载完毕')  # 判断`加载完毕` 是否再当前页面中 

# 判断当前视图中，是否有text=微信的可点击组件
hm._is_clickable('text', '微信')  

```
