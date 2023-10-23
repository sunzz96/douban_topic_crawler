# 豆瓣小组话题爬虫

Feature：发HTTP GET请求实现（就是速度快的意思）

## Requirements

建议Python3.9

```
conda install requests lxml json pandas openpyxl
pip install beautifulsoup4
```

## Usage

1.去url里看topic序号，设置topic_idx为topic序号字符串（注意加引号）

2.设置cnt为话题的帖子数量（注意这里是整型，别加括号）

3.直接运行，等会儿会生成一个xlsx文件

## Feature

设置了随机延时为豆瓣服务器减少并发（其实是怕被豆瓣拉黑），所以有一定的时延，每次请求间隔1-9秒

有些话题是文章，要访问只能打开新的网页，这种也能爬到全文

## 后记

本来是给女票写的一次性代码，因为复用了几次，感觉还是挺好用，就拿出来给其他社科人用一用
