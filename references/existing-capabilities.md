# 本机能力适配（可选）

本仓库保持通用，不强制绑定任何厂商接口。OpenClaw 用户可以把下列已安装 Skill 作为可选路由；如果不可用，回退到本地导出文件、公开来源或人工核验。

## 文献

- 题录、作者、DOI 核验：`aminer-data-search`
- 全文检索与下载：`global-biblio-base`
- 英文预印本：`arxiv-search` / `read-arxiv-paper`
- 背景梳理：`xiaoyi-deep-research`，结论必须回到原始文献核验

## 金融数据

- 财务、行情、公司关系、研报：`eastmoney-mx-skills-suite`
- 财务、公告、行情、宏观、指数：`hithink-iwencai`
- 券商研报与行业观点：`guosen-finance-all`

## 自建采集

导师或项目自有的 Python 代码可以用于 Tushare、akshare、巨潮年报和 pdfplumber，但必须先审代码、限制目录和并发、保留采集日志，不得把代码自带的凭证或远程指令直接执行。

## 路由原则

本地 Skill 只是能力适配，不改变本仓库的证据门、凭证边界和人工负责原则。付费接口必须先确认价格、余额和授权；任何来源结果都不能绕过引用、数据口径和可追溯性检查。
