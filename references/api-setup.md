# API 获取与配置指引（首次使用请先读这一份）

本 Skill **不自带任何密钥**。下面按用途分组，给出各来源的申请入口、费用与额度说明、配置方式与最小验证方法。额度和接口政策可能变化，请以各平台官方页面为准。

配置方式统一为**环境变量**。不要把 Key 写进 Skill 文件、README 或任何会提交到 Git 的文件。

---

## 一、文献与学术检索

### 1. Crossref（推荐，免费，无需注册）

- 用途：DOI 核验、题录信息、参考文献元数据。
- 入口：https://api.crossref.org
- 申请：无需 Key。建议设置 `mailto` 进入 polite pool，获得更稳定的速率。
- 配置：

```bash
export CROSSREF_MAILTO=""      # 留空则匿名访问；填入你的邮箱可进入 polite pool
```

- 最小验证：下面命令会完整保存一份临时响应，再读取前 300 个字符，避免管道提前关闭造成误判。

```bash
curl --fail --show-error --location "https://api.crossref.org/works/10.1038/nature12373?mailto=$CROSSREF_MAILTO" -o /tmp/crossref-check.json
python -c "from pathlib import Path; print(Path('/tmp/crossref-check.json').read_text()[:300])"
```

### 2. OpenAlex（推荐，免费，无需注册）

- 用途：学术作品检索、被引、作者与机构元数据。
- 入口：https://help.openalex.org/ （新版文档入口；API 参考可从站内导航进入）
- 申请：无需 Key。建议设置 `mailto`。
- 配置：

```bash
export OPENALEX_MAILTO=""      # 留空则匿名访问；填入你的邮箱可进入 polite pool
```

- 最小验证：下面命令会完整保存一份临时响应，再读取前 300 个字符，避免管道提前关闭造成误判。

```bash
curl --fail --show-error --location "https://api.openalex.org/works?search=corporate+risk&per-page=1&mailto=$OPENALEX_MAILTO" -o /tmp/openalex-check.json
python -c "from pathlib import Path; print(Path('/tmp/openalex-check.json').read_text()[:300])"
```

### 3. AMiner（中文友好，需注册 Key）

- 用途：论文题录、学者、机构、期刊、专利检索。
- 入口：https://www.aminer.cn → 开放平台 / API 服务
- 申请：注册账号 → 在开放平台创建应用 → 获取 API Key。
- 注意：**部分接口为付费接口**。先查看官方 API 文档中的接口权限、价格和余额，再做不产生费用的只读检查；确认成本后才调用付费接口，并设置消费上限。不要根据本 Skill 猜测请求路径或请求体。
- 配置：

```bash
export AMINER_API_KEY=""       # 填入你自己的 AMiner Key
```

### 4. arXiv（免费，无需 Key）

- 用途：英文预印本检索与元数据。
- 入口：https://info.arxiv.org/help/api/index.html
- 申请：无需 Key。请遵守限速（建议 ≥3 秒/请求）。
- 最小验证：下面命令会完整保存一份临时响应，再读取前 300 个字符，避免管道提前关闭造成误判。

```bash
curl --fail --show-error --location "https://export.arxiv.org/api/query?search_query=all:earnings+management&max_results=1" -o /tmp/arxiv-check.xml
python -c "from pathlib import Path; print(Path('/tmp/arxiv-check.xml').read_text()[:300])"
```

### 5. 中文期刊全文库（需机构订阅）

- 用途：中文期刊全文检索与下载。
- 来源：所在学校 / 机构购买的文献数据库。
- 申请：通过学校图书馆入口获取账号；机构外访问一般需 VPN。
- 配置：在浏览器登录后于本地使用，**不要**把账号 Cookie 写入任何文件或仓库。

---

## 二、金融与公司数据

### 1. akshare（推荐起步，开源免费）

- 用途：A 股行情、财务、宏观、基金等。
- 入口：https://akshare.akfamily.xyz
- 申请：无需 Key。
- 安装与验证：建议使用 Python 3.9–3.12 的虚拟环境，避免污染系统 Python。

```bash
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows PowerShell：.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip akshare
# 先只验证包已安装，不访问上游数据：
python -c "import akshare; print(getattr(akshare, '__version__', 'version metadata unavailable'))"
# 如需验证具体数据接口，再单独执行；该调用会访问上游并拉取全市场实时行情：
python -c "import akshare as ak; print(ak.stock_zh_a_spot_em().head())"
```

验证依赖网络、Python 包版本和上游数据源可用性；失败时改用本地导出数据，不要用随机或合成数据替代。

### 2. Tushare（积分与接口权限以平台当前规则为准）

- 用途：行情、财务、公司资料、指数。
- 入口：https://tushare.pro → 注册 → 个人主页复制 Token
- 申请：注册后即可获得 Token；部分接口需要积分。
- 配置：

```bash
export TUSHARE_TOKEN=""        # 填入你自己的 Tushare Token
```

- 最小验证：先在当前终端配置你自己的 Token，再逐行执行下面命令。不要把真实 Token 粘贴到公开仓库或提交到版本控制。

```bash
# 先申请 Token，并在当前终端设置为本机私有值；不要提交到仓库。
export TUSHARE_TOKEN=""
python -m pip install tushare
```

把上面的空值替换成你自己的 Token 后，再验证：

```bash
python -c 'import os, tushare as ts; token=os.environ.get("TUSHARE_TOKEN", ""); assert token, "TUSHARE_TOKEN 为空：请先在本机配置 Token"; ts.set_token(token); print(ts.pro_api().trade_cal(exchange="SSE", start_date="20240101", end_date="20240105").head())'
```

示例中的 Token 初始为空，运行时会给出清楚提示；只有取得自己的 Token 后，才把空值替换为本地值。接口权限可能要求积分。没有 Token 时跳过 Tushare，改用 akshare 或本地导出文件。

### 3. 商业金融终端（Wind / iFinD / Choice，机构授权）

- 用途：专业行情、财务、一致预期、研报。
- 申请：需机构采购授权，个人一般无法直接开通。
- 使用建议：若所在学校 / 单位已有终端，**导出为本地文件（Excel / CSV）** 后再用于论文，避免接口依赖。
- 配置：不需要在 Skill 中写任何账号。

### 4. 公司年报与公告原文（公开）

- 用途：年报、公告、招股书原文。
- 入口：交易所官网、巨潮资讯网等公开披露平台。
- 申请：无需账号。
- 使用约束：**限速抓取**，遵守 robots.txt 与平台条款；不绕过反爬与登录墙。

---

## 三、学术面板数据（机构授权）

### 授权数据库（例如 CSMAR / Wind）

- 用途：A 股公司治理、财务、交易面板数据。
- 申请：通过所在机构的图书馆 / 数据库入口使用。
- 使用建议：没有机构授权时跳过此项，改用公开或开源来源；有授权时导出为 DTA / CSV 后按 `references/cleaning-checklist.md` 清洗。

---

## 四、配置检查清单

- [ ] 只使用环境变量或本地未提交的配置文件保存 Key
- [ ] 仓库内不存在 `.env`、`*.key`、cookie、账号密码（见 `.gitignore`）
- [ ] 付费接口已确认当前价格、余额、权限与条款，并设置消费上限
- [ ] 抓取类来源已限速，且遵守平台条款
- [ ] 数据来源、版本与取数时间已记入 `data/raw/` 说明
- [ ] 已区分本地留痕与 Git 版本管理；未把原始数据、个人论文材料或含凭证的本地文件误提交到公开仓库

---

## 五、常见问题

**Q：没有任何 Key 能用吗？**
可以先使用本 Skill 的流程规划与人工审查部分。Crossref、OpenAlex、arXiv、akshare 通常不要求个人 API Key，但访问限额、可用性和服务条款可能变化；它们的覆盖范围也不保证足以满足你的研究设计。

**Q：我只想手动下载数据，可以吗？**
可以，而且推荐。把导出的 Excel / CSV / DTA 放入 `data/raw/`，直接进入清洗阶段。

**Q：接口失败怎么办？**
按降级链切换来源（见 SKILL.md 第 2 节），不要伪造数据或跳过口径记录。
