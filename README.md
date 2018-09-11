# BookStubbornSeats
基于[UJN-Lib-Seat-API](https://github.com/iozephyr/UJN-Lib-Seat-API)的图书馆预约

### 说明
基于风哥的API,进行了功能的扩展, 速度的提升.为了尝试极限速度, 采用[Stackless Python](https://github.com/stackless-dev/stackless/wiki),但是理解不深,发现并不能或者说不适用当前场景,不过放在这慢慢研究.还希望有明白的大佬能给指点指点.


### 测试环境

- Python 2.7.15 Stackless 3.1b3 060516
- CentOS 7.4

### 功能

- 多线程并发
- 方便配置同一座位不同时段多账户,一键预约
- 内网设备自动签到,一键签到

### 使用说明
仅供研究讨论,不会放置详细的使用和部署说明.
1. 需要requests模块
2. 入口在myscript/myscript.py
3. 根据粗略计算,在我的渣机上https方式比http平均慢0.5s.默认方式为https,可在api.py中修改.
---

##### 9/11: 
- __[优化]__ 预约失败采用quickbook补救

---

##### 9/11: 
- __[问题]__ 服务器时间有误差,找出最恰当时机
- __[优化]__ json异常捕获后记录出错字符串,然后再次抛出

- - -

##### 9/10: 

- __[问题]__ 图书馆将默认密码由和学号相同改成身份证后7位去掉最后一位.
- __[问题]__ 周二问题
- __[问题]__ 规则修正: 5:00之前只能约第二天.
- __[优化]__ 日志格式化配合线程ID

- - -
**敬告: 请不要尝试打开牟利的潘多拉盒**

*适用于[济南大学图书馆座位预约](http://seat.ujn.edu.cn/login?targetUri=%2F), 也应该适合其他应用利昂图书馆管理的平台(leosys).*
