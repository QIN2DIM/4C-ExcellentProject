[语雀同步文档](https://www.yuque.com/docs/share/c056d958-0c22-482f-8a9f-7cd86d178ef2?#)|中文

> 国内部分地区局域网可能无法正常显示github插图，请跳转语雀同步文档

# C4-2020中国大学生计算机设计大赛_信息采集爬虫

CCCC-中国大学生计算机设计大赛 :scroll:**历史作品博物馆**:scroll:



## :crossed_swords: 写在最前

- :1st_place_medal:：咳咳- -本人大二狗，有幸作为项目负责人参与了2020中国大学生计算机设计大赛，并拿下了大数据赛道全国一等奖。
- :kissing_heart:：做这个小脚本的初衷也比较简单垂直~无意中看到了某个设计方向的作品，感触很深:100:（本科生能独立完成这样的作品，真是太震撼了！嗯我说的就是“红楼梦信息交互设计”的华科小姐姐团队，真正的面向薪资编程！）
- :badminton:：于是便有了一个**收藏并展示该类比赛优秀作品**的想法，于是本人点开官网后发现最新的作品展示还要追溯到2015年-……行吧那就撸起袖子自己写了一个自动化采集程序，该程序会自动化采集作品数据，并生成永久访问链接，**展示的信息会经过数据脱敏，仅放出项目idea以及作品申报信息，供大家考古学习**（除非作者自己写出来了。。）；那必然~如果发现自己的idea有人已经实现过了，成绩还不错，那就避免雷同咯~
- :rocket:：咳咳- -第一次写自述如此罗嗦，总而言之该脚本主要功能就是**采集作品信息**和**拷贝作品信息**。我会在均衡程序的鲁棒性后，引入**垂搜引擎**，帮助使用者秒搜`同质idea`以及`优秀参赛作品`
- :tea:：最终的作品展示方式，我会慎重考虑。如果官方工作人员觉得不太妥，可以私聊本人喝茶（嗯！道歉是认真的！)，如果觉得本项目有望吸引更多的年轻人参赛施展才智，提高竞赛的知名度与含金量~可以私聊本人喝咖啡（咳咳..）



## :carousel_horse: Quick Start

进入`main.py`,按照说明书合理调用`API` ，运行程序即可调度爬虫采集数据。

- **环境预备**

  - 部分API使用python3+selenium的采集方案，且该脚本仅支持Chrome驱动。本人已预装`./MiddleWare/chromedriver.exe`，请将宁的谷歌浏览器更新到最新版本。

- **安装第三方依赖**

  - 在工程文件中打开`Terminal` ；

    ```python
    # 更新pip
    python -m pip install --upgrade pip
    
    # 通过依赖文档，批量索引第三方库;部分包可能需要手动安装
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

### 采集作品信息

- `app.run_crawl_to_capture_workData(work_id: str or list,power: int)`
  - work_id = 作品编号，支持**单个字符串**输入以及**List**多个字符串输入
    - **采集模式**：
    - 【1】传入单个作品编号；
    - 【2】传入包含多个作品编号的列表；
    - 【3】传入空字符串或不传入`work_id`，则默认采集BASE中所有的ID对应的作品数据(目前有4076个数据在库)，此时请适当调高协程功率
  - power = 协程功率，`power∈[1,∞)`，脚本内置弹性协程队列，此处可`随意`设置
- 运行后会在`/dataBase/`目录下生成`合成.csv`文件
- 从`config`配置文件中打印变量`title`即可查询信息键

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    id_list = ['75945','68589']
    # app.run_crawl_to_capture_workData(work_id='72862',power=30)
    app.run_crawl_to_capture_workData(id_list, id_list.__len()__)
```

![image-20200901181716579](https://i.loli.net/2020/09/01/xG3LQqjwVubkCcK.png)

### 拷贝作品信息

- **演示视频**[《BackupSpider of CNJSJ》](https://www.yuque.com/docs/share/148083ac-c703-4f7c-978b-321b4ae8e6d9?#) 

- `app.run_crawl_to_capture_workData(work_id: str or list,power: int=4)`
  - work_id = 作品编号，支持**单个字符串**输入以及**List**多个字符串输入
    - **参数传递方案同上**
  - power = 协程功率，`power∈[1,∞)`，脚本内置弹性协程队列，此处可`随意`设置
- 运行后会在`/dataBase/BACKUP/`目录下生成以作品编号命名的`.mhtml`文件，该格式网页文件封装了源所有的文本插图和渲染效果，在断网情况下也不会丢失数据细节，部分作品插图较多，体积占用较大。（注：safari可能会打不开这种格式文件）

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    # 话说这个id作品好赞...开眼了..来自华科大佬的神仙作品 tql！！
    app.run_crawl_to_backup_workData('72862',power=1)
```

<img src="https://i.loli.net/2020/09/01/3nIbWH5cEiuDVs9.png" alt="QQ截图20200901181750" style="zoom:80%;" />

![20200629_155209](https://i.loli.net/2020/09/01/MmYqsBRbPEZglv2.gif)

## :smirk:API

在从`MiddleWare`中导入`app`，即可调用脚本功能，别忘了调用`config`配置文件设置全局变量~

```python
from MiddleWare import app
from config import *
```



### 作品查询~学校成果

- `app.get_school_psar(school_name: str,save: bool)`
  - school_name = 学校名称。这里不支持模糊匹配，请输入**全称**！
  - save = 保存输出。默认为False；建议为True，运行后会在`/dataBase/PSAR`目录下生成对应学校的分析结果，文件格式为`.json`，信息键仅包括`获奖信息`以及`作品链接`。文件会**自动打开**。

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    app.get_school_psar(school_name='华中科技大学',save=True)
```

- `/华中科技大学_分析报告.json`

```json
{
    "华中科技大学": {
        "成果概要": {
            "一等奖": 2,
            "二等奖": 8,
            "三等奖": 2
        },
        "作品细节": {
            "一等奖": [
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72849": "皖江之阴，青山之阳；青阳有腔，放遇一欢。"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72862": " 红楼梦·可视化赏析信息交互系统"
                }
            ],
            "二等奖": [
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72750": "Limfx科研博客"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72764": "梦·山海"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72795": "济世方舱"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72796": "山哈彩带"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72800": "敦煌·梵音"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72821": "放大镜下的昆虫世界"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72822": "九华折扇——数字化非遗文化信息可视化设计"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=74879": "别让它灭绝"
                }
            ],
            "三等奖": [
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72783": "皮影传承，戏中人生"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72799": "希冀"
                }
            ]
        }
    }
}
```



### 作品查询~奖级AND赛道

- `app.find_works_by_level(level: str,class_: str)`
  - level = 作品等级。这里需要**规范输入**，只能输入以下选项
    - `一等奖`、`二等奖`、`三等奖`
  - class_ = 作品赛道。这里支持模糊匹配。在`/dataBase/TPTDP/class_name.txt`中有C4-2020所有赛道的全称
- 食用说明：`level`和`class_`都不是必选参数，比如只想知道一等奖的所有作品，只需传入`level`即可，`class_`可不传或传入空字符串。
- ~~**（嗯！别骂了别骂了，Excel也能做到）**~~

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    # app.find_works_by_level(level='一等奖', class_='大数据')
    # app.find_works_by_level(level='', class_='人工智能')
    app.find_works_by_level(level='一等奖', class_='')
```

![image-20200901180705173](https://i.loli.net/2020/09/01/XJazcpSA9sbjO5y.png)

### 作品查询~比赛摘要

- `app.get_summary()`可打印决赛成绩概况~~（后来觉得这个功能太鸡肋了，就没再写这个API，可凑合着看看）~~

![image-20200901180943555](https://i.loli.net/2020/09/01/lwi1PuNOf9v4QE2.png)

### 作品查询~链接直达

- `app.find_works_by_id(key: str, goto: bool)`
  - key = 作品编号，仅支持单个字符串输入
  - goto = 是否打开网页。若为True，则使用默认浏览器打开作品首页
- ~~确实又是个很鸡肋的API~~
- 运行后会在`/dataBase/PSAR/ASH.json`中留下临时文件

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    app.find_works_by_id('72862')
```



### works_id数据加载

- 由于表数据结构比较乱，我已经写好了一个全局load id 的函数，使用方法也很粗暴，调用该函数并传入`spider_key`，即可获取含表头的在库id列表。获取列表后使用切片去除表头候即可获得干净的数据~
- 因为合成BASE文件有点大，故使用`csv.field_size_limit()`捕获数据流。

函数源码如下：

```python
# config.py
def load_data_from_id_set(mode) -> list:
    """
    data_set = title
    :param mode: 截取模式,
                spider_key : 联采
                str:works_id : 该作品编号对应的数据
                list:works_id :
    :return:返回表头+数据，使用切片[1:]截出数据集
    """

    # 当爬虫程序使用此函数时，并传入‘spider_key’口令，函数执行特殊命令，返回含表头的作品编号 List[str,str...]
    # 返回的列表里包含了所有在库的works_id,既当爬虫爬虫程序传入该口令时，将采取所有作品信息
    with open(id_fp, 'r', encoding='utf-8') as f:
        csv.field_size_limit(500 * 1024 * 1024)
        reader = csv.reader(f)
        data = [i for i in reader]
        if mode == 'spider_key':
            # 清洗数据
            return [i[1] for i in data if i[1] != 'N/A']
```

- 食用方法

```python
from MiddleWare import app

if __name__ == '__main__':
    # 返回无表头 id 列表
    id_flow: list = app.get_all_works_id()
    # 数据预览
    print('id池大小：{}'.format(id_flow.__len__()))
```

## :small_red_triangle: 注意事项

- 工程文件中的`/dataBase`目录下存放了脚本核心BASE文件，请勿随意挪动或删除文件，否则会出大问题！
- `config.py`中可以自己调整的参数并不多，请勿随意改动其中数值，否则也会出大问题~



## :loudspeaker: 更新日志

- **2020.09.06**
  1. 已将所有`2020-MTH作品申报信息`离线封装
  2. 将采集功能都封装进`app.py`里，所有功能都可通过该模块调用
  3. 添加语雀同步文档，解决部分地区图文显示异常的问题
  4. 项目除虫，增加了垃圾回收机制

## :chart_with_upwards_trend: TODO

- [ ] 搭建类BLOG前端，开放接口映射优秀作品文件
- [ ] 服务器部署
- [ ] 引入鲁棒均衡模组
- [ ] 添加垂搜引擎，提供API接口