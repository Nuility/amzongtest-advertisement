问题分析
经过检查，我发现以下问题：

核心问题：依赖服务未启动
MySQL数据库未运行

配置：mysql+pymysql://user:pass@localhost:3306/amazon_ads
状态：未运行或连接失败
影响：所有数据库操作会失败，导致API返回500错误
Redis缓存服务未运行

配置：redis://localhost:6379/0
状态：未运行（端口6379无法连接）
影响：缓存功能不可用（代码已做容错处理，不会崩溃）
配置问题
前端API路径不匹配
前端配置：http://localhost:8000/api
后端实际：http://localhost:8000/metrics（无/api前缀）
影响：前端调用API会404
数据库表不存在
即使MySQL启动，也需要：
创建数据库 amazon_ads
运行数据库迁移创建表结构（Campaign、Keyword等）
需要做的修改
第一步：启动依赖服务
启动MySQL数据库服务
启动Redis缓存服务
创建数据库 amazon_ads
第二步：修复配置
修改数据库连接字符串（用户名、密码、地址）
修改前端API_BASE_URL，去掉/api前缀
或者在后端添加/api前缀
第三步：初始化数据库
运行数据库迁移脚本创建表结构
插入测试数据（可选）
第四步：验证
测试后端API能否正常访问数据库
测试前端能否正常显示数据