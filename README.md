
# 2022/1/26 更新 V3版本
DataV平台更新了V3版本的最新数据，获取方法与之前有一些区别。
目前更新了V3版本的数据的获取方法，并添加了超时重试的功能。
切换至V3分支以获取最新代码和数据

# GeoMapData_CN
## 最新中国省市区县geoJSON格式地图数据（包含子区域）<br/>
### 包括:<br/>
#### 全国地图: china.json<br/>
#### 全国各省地图：province<br/>
#### 全国各市地图：city<br/>
#### 全国各区县地图：county<br/>
#### 全国省市区县所对应行政区划代码以及中心点的坐标：location.json (方便用于echarts上显示某个点的位置)

可直接用于echarts地图的显示

数据来源： http://datav.aliyun.com/tools/atlas/

getMap.py为简易的爬虫脚本，需要无子域的地图或者自定义需求，自行修改
