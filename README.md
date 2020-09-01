# C42020-计算机设计大赛_信息挖掘

利用官网接口，以及公开数据，采集作品信息

[TOC]

## Quick Start

进入`main.py`,按照说明书合理调用`API` ，运行程序即可调度爬虫采集数据。

- **环境预备**

  - 部分API使用python3+selenium的采集方案，请确保电脑安装了`Chrome`以及对应版本的`Chromedriver.exe`，有经验的朋友可以直接修改源码~

- **安装第三方依赖**

  - 在工程文件中打开`Terminal` ；

    - `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

    

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
    # app.run_crawl_to_capture_workData(work_id='75945',power=30)
    app.run_crawl_to_capture_workData(['75945', '70773'], 2)
```

![image-20200901181716579](https://i.loli.net/2020/09/01/xG3LQqjwVubkCcK.png)

### 拷贝作品信息

- `app.run_crawl_to_capture_workData(work_id: str or list,power: int=4)`
  - work_id = 作品编号，支持**单个字符串**输入以及**List**多个字符串输入
    - **参数传递方案同上**
  - power = 协程功率，`power∈[1,∞)`，脚本内置弹性协程队列，此处可`随意`设置
- 运行后会在`/dataBase/BACKUP/`目录下生成以作品编号命名的`.mhtml`文件，该格式网页文件封装了源所有的文本插图和渲染效果，在断网情况下也不会丢失数据细节，部分作品插图较多，体积占用较大。（注：safari可能会打不开这种格式文件）

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    app.run_crawl_to_backup_workData('70773',power=1)
```

![QQ截图20200901181750](https://i.loli.net/2020/09/01/3nIbWH5cEiuDVs9.png)

## API

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
    # 话说这个id作品好赞...开眼了..来自华科大佬的神仙作品 tql！！
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
            return [i[1] for i in data]
```

- 食用方法

```python
from config import load_data_from_id_set

if __name__ == '__main__':
    id_flow: list = load_data_from_id_set(mode='spider_key')
    print(id_flow)
    print('id池大小：{}'.format(id_flow.__len__()))
```



## 注意事项

- 工程文件中的`/dataBase`目录下存放了脚本核心BASE文件，请勿随意挪动或删除文件，否则会出大问题！
- `config.py`中可以自己调整的参数并不多，请勿随意改动其中数值，否则也会出大问题~



## 文档树

```
中国大学生计算机设计大赛_抓取
 ├── dataBase
 │   ├── BACKUP
 │   ├── CNJSJ_BASE.csv
 │   ├── error_log.txt
 │   ├── id_pool.xlsx
 │   ├── id_set_01.csv
 │   ├── PSAR
 │   └── TPTDP
 ├── MiddleWare
 │   ├── app.py
 │   ├── cmp_data.py
 │   ├── raw_data_load.py
 │   └── __pycache__
 ├── SpiderNest
 │   ├── cnjsj_spider.py
 │   ├── ppy_flow_spider.py
 │   ├── snsProj_spider.py
 │   └── __pycache__
 ├── config.py
 ├── LICENSE
 ├── main.py
 ├── README.md
 └── requirements.txt
```
