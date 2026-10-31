# 车辆年检助手（Vehicle Inspection Assistant）

> 一款面向车队 / 个人的 Windows 机动车年检计算与台账工具。单文件绿色 exe，苹果风界面，支持免检新政自动判定、逾期提醒、Excel 批量导入与导出。

[![平台](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)](#)
[![语言](https://img.shields.io/badge/aardio-%2B%20WebView2-orange)](#)
[![许可](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![最新版本](https://img.shields.io/github/v/release/haoyougen01/vehicle-inspection-helper?label=release&color=blue)](https://github.com/haoyougen01/vehicle-inspection-helper/releases/latest)

> **直接下载**：[Releases → VehicleInspectionHelper-v1.0.0-win64.zip](https://github.com/haoyougen01/vehicle-inspection-helper/releases/latest)（解压双击即用，免安装）

---

## 功能特性

**① 临时车辆查询**（不入库，只留痕）

- 输入车牌号 / 车架号(VIN) / 编号 / 产权登记日期 / 车辆类型 / 当前公里数，立即算出下一次年检截止日与剩余天数；
- 自动判定"免检领标"或"上线检测"，并给出办理窗口期（期满前 3 个月）；
- 20 年检验节点全景视图，逐节点标注「已过期 / 窗口期内·可办理 / 未到办理窗口」；
- 处置管理提示（使用满 10 年或行驶满 30 万公里）；
- 查询历史自动留痕（去重、最多 200 条），可回看、可清空，**不会污染车辆台账**。

**② 存量车跟踪管理**（台账）

- 新增 / 编辑 / 删除车辆，按紧急程度自动排序；
- 六格总览：总数、已逾期、2 个月内、3 个月内、正常、可处置；
- Excel / CSV 批量导入（表头关键字智能识别列，日期格式宽容）；
- 一键导出跟踪库或总览到 Excel（Excel 或 WPS 均可，带样式）；
- 启动时自动弹出年检提醒（含开机自启开关，注册表 Run 项，不写快捷方式）；
- 最小化到系统托盘：点最小化或关闭按钮不退出，托盘图标双击恢复，右键菜单可"显示主界面 / 开关开机自启 / 退出程序"。

## 快速开始

1. **开箱即用**：从 [Releases](https://github.com/haoyougen01/vehicle-inspection-helper/releases/latest) 下载 `VehicleInspectionHelper-v1.0.0-win64.zip`，解压到任意文件夹（建议单独建一个，如 `D:\车辆年检助手`）；或按下方「构建」自行编译；
2. 双击 `车辆年检助手.exe` 运行。首次启动会在 exe 同目录自动生成：
   - `车辆跟踪库.csv` —— 车辆台账
   - `查询历史.csv` —— 临时查询留痕
   - `ui/index.html` —— 界面文件（自动重建，勿手改）
3. 想批量导入车辆：管理页 →「导入 Excel 入库」，选择 xlsx/csv；格式参考 `示例数据/示例数据.csv`。

> 数据全部保存在本地 csv 中，绿色免安装、可随目录整体拷贝。删掉 exe 目录的 csv 即等于清空数据。

## 目录结构

```
车辆年检助手-开源版/
├── 工程/                  aardio 工程（源码）
│   ├── main.aardio        业务逻辑 + 数据层 + 通信层
│   ├── default.aproj      工程配置（F7 发布到 dist/）
│   ├── ui/index.html      全部界面（HTML/CSS/JS）
│   └── dist/              发布产物与示例数据（虚构）
├── 文档/
│   ├── 开发文档.md         架构、数据格式、业务规则、踩坑清单
│   └── 发布到GitHub.md     本仓库推送到 GitHub 的完整操作指南
├── 示例数据/示例数据.csv    导入格式示例（虚构 10 台车）
├── 工具/自动化测试/         发布与 UI 自动化脚本（可选）
├── .gitattributes         统一行尾（CSV/aardio 保持 CRLF）
├── LICENSE
└── README.md
```

## 年检规则（内置）

| 车辆类型 | 检验节点 |
|---|---|
| 非营运小微型载客汽车 / 摩托车（免检新政） | 第 2/4/8 年免检领标，第 6/10 年上线检测，第 11 年起每年上线 |
| 面包车及其他车型 | 第 2/4/6 年上线检测，第 7 年起每年上线 |

- 办理窗口：检验截止日前 3 个月内；
- 可处置条件：使用满 10 年或累计行驶 30 万公里；
- 计算基准日 = 产权登记日（月/日对齐，闰年 2/29 自动回退）。

## 构建（开发者）

需要 [aardio](https://www.aardio.com/)（Windows）与 WebView2 Runtime（Win10/11 一般自带）。

```text
1. aardio 打开 工程/default.aproj
2. 按 F7 发布 → 产物在 工程/dist/车辆年检助手.exe
```

界面文件通过 `var UI_HTML = $"~/ui/index.html";` 在编译期内嵌，因此**改完 index.html 必须重新发布**；程序启动时还会把界面写到 `dist/ui/index.html` 供 WebView2 加载。

更详细的架构、通信协议、数据格式与 20 条踩坑经验见 [文档/开发文档.md](文档/开发文档.md)。
把本仓库推到 GitHub（含认证方式、国内网络、常见报错）见 [文档/发布到GitHub.md](文档/发布到GitHub.md)。

## 数据与隐私

- 仓库内所有车辆数据均为**虚构**：车牌形如 `京A00001`、`沪A00010`，VIN 统一以 `LTEST` 开头，编号 `T2024001` 起，姓名/联系方式一概没有。
- 程序不联网上传任何数据（仅可选地取一次网络时间校准本机时钟），台账只写本地 csv。

## 常见问题

| 现象 | 处理 |
|---|---|
| 启动提示"后台接口未就绪" | 缺少 WebView2 Runtime，或界面文件被占用，重启程序 |
| 导入 Excel 没反应 | 本机需装 Excel 或 WPS；失败详情看 exe 同目录 `导入调试日志.txt` |
| 时间不准 | 程序优先取网络北京时间，断网时回退本机时钟 |
| 想重置演示数据 | 用 `示例数据/示例数据.csv` 重新导入，或直接替换 `工程/dist/车辆跟踪库.csv` |

## 许可与免责

- 代码以 **MIT License** 发布，可自由使用、修改、商用，保留版权声明即可。
- 年检规则依据公开的免检新政整理，**仅供辅助参考，不构成法律或行政依据**；实际以交管部门、检验机构的要求为准。
