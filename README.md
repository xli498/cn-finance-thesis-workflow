# CN Finance Thesis Workflow

> 中文金融 / 会计 / 管理类**实证论文**全流程工作流：从选题到答辩，做成可检查、可暂停、可回滚的阶段流程。

面向使用面板数据、A 股样本的研究者与学生，覆盖：

**选题与可行性 → 文献与假设 → 数据获取 → 数据清洗 → 实证与稳健性 → 写作 → 引用核验 → 排版 → 答辩**

## 特点

- **证据优先的不变量**：不编造文献、不编造结果、不编造要求，结论强度不超过证据。
- **七阶段状态机**：每阶段有明确产物与质量门，未过门不推进。
- **确定性文本检查**：六维度规则检查（可信度、术语、格式、语体、逻辑、结构），可复现、不依赖模型判断。
- **数据清洗 SOP**：面向 A 股面板数据的标准筛选顺序与高频陷阱。
- **可配置的接口层**：所有外部数据来源都是可选占位，默认不依赖任何厂商专属服务。
- **公开路径优先**：没有机构数据库授权时，也可以用公开文献接口、开源数据工具或本地手动导出的数据完成流程；授权数据库只是增强选项。
- **不承诺黑盒结果**：不承诺查重率、AI 检测分数、通过率或录用结果。

## 目录结构

```text
SKILL.md                          # 主流程与规则
references/
  api-setup.md                    # ★ 首次使用先读：各数据源申请与配置指引
  stage-gates.md                  # 阶段质量门 Checklist
  cleaning-checklist.md           # 数据清洗细则
  robustness-checklist.md         # 稳健性与内生性清单
  writing-rules.md                # 中文实证论文写作规则
  text-check-rules.md             # 文本确定性检查规则
```

## 新手快速上手

### 第一步：下载

在本仓库页面点击 **Code → Download ZIP** 并解压。也可以用 Git：

```bash
git clone https://github.com/xli498/cn-finance-thesis-workflow.git
```

解压后确认目录中有 `SKILL.md`、`README.md` 和 `references/` 文件夹。

### 第二步：让 Agent 加载

把整个 `cn-finance-thesis-workflow` 文件夹放进你使用的 Agent 所支持的技能目录。技能目录因平台和安装方式不同而异；请按该 Agent 的官方说明选择路径。**不要只复制 `SKILL.md`**，`references/` 里的阶段门、API 指引和检查清单也需要保留。

重启或刷新 Agent 的技能列表（如果平台要求），确认它能识别 `cn-finance-thesis-workflow`。然后发送：

```text
请使用 cn-finance-thesis-workflow。先判断我的论文处于哪个阶段，只做本阶段任务，并列出需要我提供的材料；不要编造文献、数据或结果。
```

### 第三步：先从零配置开始

**不需要先申请 API，也不需要把任何 Key 填进 Skill。** 可以先让 Agent 帮你整理研究问题、变量草案、数据需求清单和阶段计划；有人已有本地授权数据时，也可直接用 Excel / CSV / DTA 开始。

确实需要联网检索或取数时，再打开 [`references/api-setup.md`](references/api-setup.md)，按所选来源的官方说明自行配置。只选自己能合法使用的数据源；没有机构数据库授权时，跳过授权数据库，改用公开接口、开源数据工具或本地已有文件。Key 应保存在本机环境变量或平台的 Secret 管理器中，切勿写进仓库、论文文件或聊天记录。

### 第四步：按阶段推进

工作流有 S0–S6 七个阶段。先根据 `SKILL.md` 第 3 节判断当前阶段，再按该阶段 SOP 工作；结束时对照 `references/stage-gates.md` 检查，未通过就先补齐，不要跳阶段。

### 作为纯流程文档使用

不使用 Agent 也可以：按 `SKILL.md` 第 3 节判断阶段、按第 4 节执行，并参考 `references/` 下的清单逐项人工核验。
## 配置数据源

**首次使用请读 [`references/api-setup.md`](references/api-setup.md)**，里面有每个来源的申请入口、费用与额度说明、配置方式与最小验证命令。额度和接口政策可能变化，请以各平台官方页面为准。

零配置也能用：Crossref、OpenAlex、arXiv、akshare 都不需要 Key。已有本地导出数据的话，直接从清洗阶段开始即可。

## 环境变量（全部可选，默认空值）

本项目是**流程规范 / Agent 指令 Skill**，不是包含采集器、回归程序或文本检查脚本的完整软件包。安装后可以立即用于规划、审查和组织研究；真正取数、清洗、回归和排版仍需使用者选择工具并执行。

| 变量 | 用途 |
|---|---|
| `AMINER_API_KEY` | AMiner 题录与 DOI 核验 |
| `TUSHARE_TOKEN` | Tushare 行情与财务数据 |
| `OPENALEX_MAILTO` | OpenAlex polite pool 邮箱 |
| `CROSSREF_MAILTO` | Crossref polite pool 邮箱 |

> 不要把任何 Key、Token、Cookie 或账号密码提交到本仓库。

## 隐私与安全

- 本仓库不包含任何个人身份信息、账号凭证、本地路径或私有接口配置。
- 所有凭证均由使用者自行注入；`.gitignore` 已排除常见密钥文件。
- 使用商业数据库与公开披露平台时，请遵守各自的服务条款与限速要求。
- 本工作流用于**辅助研究过程**，署名、伦理审查与最终提交由作者本人负责。

## 许可

MIT License，见 [LICENSE](LICENSE)。
