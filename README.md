# PyHermit

>此Python模块基于Hermit API的封装而成，并对原有的功能进行了强化，从而能够轻松的控制设备而无需关心API。依赖于requests。

#### 下载地址
Github release： [https://github.com/LookCos/hermit-py/releases](https://github.com/LookCos/hermit-py/releases)

####  简要说明  
由于是基于API的封装，而对API的调用仅在一瞬间，安卓系统未必立即执行完毕。  
所以在一些常规的操作函数都末尾增加了一个缺省函数 `sleep`，表示延迟这些秒数之后再执行。

####  实例化  
在此之前，请确保要操作设备已经安装了Hermit APP。具体请参考文档中安装部分。
```python
from pyhermit import Hermit
hm = Hermit('127.0.0.1:9999')
```
> 127.0.0.1:9999 是Hermit API的地址，具体参考 安装与使用。

####  基于无障碍的点击与滑动
```python3
# 延迟3s，点击坐标(100, 100)
hm.click(100, 100, 3)

# 从坐标(100, 200)滑动至(100, 1000)
hm.swipe(100, 200, 100, 1000)

# 点击属性`text=关注`的控件（默认第一个）
hm.click_text("关注")

# 点击第三个，属性`text=关注`的控件
hm.click_text("关注", index=2)

# 统计属性`text=关注`的控件的数量
count = hm.click_text("关注", count=True)
print(count)

# 点击 属性`resource-id=com.tencent.mm:id/bhn`的控件（默认第一个）
hm.click_id("com.tencent.mm:id/bhn")

# 点击第3个 属性`resource-id=com.tencent.mm:id/bhn`的控件
hm.click_id("com.tencent.mm:id/bhn", index=2)

# 统计 属性`resource-id=com.tencent.mm:id/bhn`的控件的数量
count = hm.click_id("com.tencent.mm:id/bhn", count=True)
print(count)

# 点击 属性`content-desc=搜索`的控件
hm.click_desc("搜索")

"""上下左右滑动，加入随机因子，每次轨迹不同。
    param:: scope, 表示滑动屏幕幅度，范围[1-10],
    param:: sleep, 缺省参数，但是是执行滑动后再延迟。
"""
hm.swipe_up(5) # 向上滑大约屏幕的一半
hm.swipe_down(3, 5) # 下滑屏幕的3/10后延迟5秒
hm.swipe_left(1) # 左滑一点点
hm.swipe_right(10) # 右滑满屏 （如果有手势，大概率会触发返回）

"""模拟输入功能
    param:: by, 通过何种方式选择输入框控件，可选 id, text, desc
    param:: obj, 上述方式的对应值
    param:: text, 要输入的内容
    下面方法表示，在resourc-id=com.tencent.mm:id/bhn 的输入框中，输入`Hermit`
"""
hm.input('id', 'com.tencent.mm:id/bhn', 'Hermit')


"""一个一个click似乎不太过瘾，那么可以尝试用`channel`打一套组合拳。"""
hm.click_channel([
    {'text': '酷安'}, {'id': 'com.coolapk.market:id/title_view'},
    {'desc': '搜索'},
])
# 它会遍历并执行数组中的操作，自带判断功能，默认5s等待时间（每秒判断一次是否可点击），超时自动下一个。
```

####  基于无障碍的全局操作  

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

####  基于Root的一些操作  
```python3
# 延迟3s，点击坐标(100, 100)
hm.shell_tap(100, 100, 3)

# 从坐标(100, 200)滑动至(100, 1000)
hm.shell_swipe(100, 200, 100, 1000)

# 和无障碍一样，也支持了上下左右滑动，参数相同
hm.shell_swipe_up()
hm.shell_swipe_down()
hm.shell_swipe_left()
hm.shell_swipe_right()

# 发送keyevent事件
hm.shell_key_event(3) # 按下home键
# 更多的请参考这里 https://developer.android.com/reference/android/view/KeyEvent.html
```

####  剪贴板操作 
```python
hm.clipboard_push('法外狂徒')  # 设置剪贴板内容  
hm.clipboard_pull() # 读取剪切板内容
```  

####  获取信息类
```python
# 打印当前界面的布局信息, 可以用来找resource-id、text等，
# 进而进行点击与模拟输入，但是更建议使用可视化的分析工具，详情见工具。
print(hm.data_nodes())

# 获得屏幕的长宽信息 
print(hm.data_screen())

# 获得设备的 型号、制造商、CPU、内存、存储等信息
print(hm.data_device())

# 以下方法均返回 布尔类型
hm.is_root() # 申请并判断是否有root权限  
hm.in_page('加载完毕')  # 判断`加载完毕` 是否再当前页面中 

# 判断当前视图中，是否有text=微信的可点击组件
hm._is_clickable('text', '微信')
```



####  下面是一些演示，更多的方法请参考API以调用
####  演示1：群聊抢红包  
![](https://www.lookcos.cn/usr/uploads/2021/01/2021012805375112.gif)
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

####  演示2：打开酷安并快速找到并进入iPhone SE区  
![](https://www.lookcos.cn/usr/uploads/2021/01/2021012805074049.gif)

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

#### 演示3： 打开微信，并搜索v2ex  
![](https://www.lookcos.cn/usr/uploads/2021/01/202101280528008.gif)
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
