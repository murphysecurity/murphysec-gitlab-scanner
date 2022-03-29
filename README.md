# murphysec-gitlab-scanner

## 使用方式
### 全量扫描
python3 scan_all.py -A "your gitlab address" -T "your gitlab token" -t "your murphy token"
### 增量扫描
1、配置gitlab webhook，配置方式请自行百度<br>
2、python3 webapi.py

## TODO
* [x] 增加增量代码检测（gitlab webhook功能）
* [ ] 增加检测结果消息提醒
* [ ] 增加检测队列，加快检测速度