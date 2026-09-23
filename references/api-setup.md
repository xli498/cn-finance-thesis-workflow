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

- 最小验证：

```bash
curl --fail --show-error --location "https://api.crossref.org/works/10.1038/nature12373?mailto=$CROSSREF_MAILTO" | head -c 300
```

### 2. OpenAlex（推荐，免费，无需注册）

- 用途：2.5 亿+ 学术作品检索、被引、作者与机构。
- 入口：https://docs.openalex.org
- 申请：无需 Key。建议设置 `mailto`。
- 配置：

```bash
export OPENALEX_MAILTO=""      # 留空则匿名访问；填入你的邮箱可进入 polite pool
```

- 最小验证：

```bash
curl --fail --show-error --location "https://api.openalex.org/works?search=corporate+risk&per-page=1&mailto=$OPENALEX_MAILTO" | head -c 300
```

### 3. AMiner（中文友好，需注册 Key）

- 用途：论文题录、学者、机构、期刊、专利检索。
- 入口：https://www.aminer.cn → 开放平台 / API 服务
- 申请：注册账号 → 在开放平台创建应用 → 获取 API Key。
- 注意：**部分接口为付费接口**，调用前先确认单价与余额，并设置消费上限。
- 配置：

```bash
export AMINER_API_KEY=""       # 填入你自己的 AMiner Key
```

### 4. arXiv（免费，无需 Key）

- 用途：英文预印本检索与元数据。
- 入口：https://info.arxiv.org/help/api/index.html
- 申请：无需 Key。请遵守限速（建议 ≥3 秒/请求）。
- 最小验证：

```bash
curl --fail --show-error --location "https://export.arxiv.org/api/query?search_query=all:earnings+management&max_results=1" | head -c 300
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
python -c "import akshare as ak; print(ak.stock_zh_a_spot_em().head())"
```

验证依赖网络、Python 包版本和上游数据源可用性；失败时改用本地导出数据，不要用随机或合成数据替代。

### 2. Tushare（免费额度 + 积分制）

- 用途：行情、财务、公司资料、指数。
- 入口：https://tushare.pro → 注册 → 个人主页复制 Token
- 申请：注册后即可获得 Token；部分接口需要积分。
- 配置：

```bash
export TUSHARE_TOKEN=""        # 填入你自己的 Tushare Token
```

- 最小验证：

```bash
python -c "import os,tushare as ts; token=os.environ.get('TUSHARE_TOKEN',''); assert token, 'TUSHARE_TOKEN 为空：先申请并配置 Token'; ts.set_token(token); print(ts.pro_api().trade_cal(exchange='SSE', start_date='20240101', end_date='20240105').head())"
```

空 Token 运行失败是预期行为；没有 Token 时可跳过 Tushare，改用 akshare 或本地导出文件。

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
- [ ] 付费接口已确认单价与余额，并设置消费上限
- [ ] 抓取类来源已限速，且遵守平台条款
- [ ] 数据来源、版本与取数时间已记入 `data/raw/` 说明

---

## 五、常见问题

**Q：没有任何 Key 能用吗？**
能。Crossref、OpenAlex、arXiv、akshare 都不需要 Key，足够完成文献核验和基础数据获取。

**Q：我只想手动下载数据，可以吗？**
可以，而且推荐。把导出的 Excel / CSV / DTA 放入 `data/raw/`，直接进入清洗阶段。

**Q：接口失败怎么办？**
按降级链切换来源（见 SKILL.md 第 2 节），不要伪造数据或跳过口径记录。
