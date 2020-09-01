# C42020-计算机设计大赛_信息挖掘

利用官网接口，以及公开数据，采集作品信息

## Quick Start

进入`main.py`,合理设置`power`控制协程功率 ，运行程序即可采集**”第一批“**决赛入围作品的数据

### 采集作品信息

- `app.run_crawl_to_capture_workData(work_id: str or list,power: int)`
  - work_id = 作品编号，支持**单个字符串**输入以及**List**多个字符串输入
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

### 拷贝作品信息

- `app.run_crawl_to_capture_workData(work_id: str or list,power: int=4)`
  - work_id = 作品编号，支持**单个字符串**输入以及**List**多个字符串输入
  - power = 协程功率，`power∈[1,∞)`，脚本内置弹性协程队列，此处可`随意`设置
- 运行后会在`/dataBase/BACKUP/`目录下生成以作品编号命名的`.mhtml`文件，该格式网页文件封装了源所有的文本插图和渲染效果，在断网情况下也不会丢失数据细节，部分作品插图较多，体积占用较大。（注：safari可能会打不开这种格式文件）

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    app.run_crawl_to_backup_workData('70773',power=1)

```



## API

在从`MiddleWare`中导入`app`，即可调用脚本功能，别忘了调用`config`配置文件设置全局变量~

```python
from MiddleWare import app
from config import *
```



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





