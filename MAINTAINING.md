# 社区版维护与同步

本仓库的 `main` 和最新正式 Release 对齐 Magpie 社区的纯历史过滤插件，当前为 **v0.1.1**。社区来源是 [packages/codex-history](https://github.com/magpie-community/plugins/tree/main/packages/codex-history)，本次修复已在 [PR #204](https://github.com/magpie-community/plugins/pull/204) 合并。

## 哪些内容需要一致

- 版本号、`package.json`、请求入口、过滤规则和默认值、源码适配器、回归用例、测试、README、许可及来源记录保持一致。
- GitHub Release 的 `.tgz` 使用社区 `dist` 的原始安装包，按索引中的 SHA-512 校验；ZIP 只把该包解压成便于添加的本地目录。
- 本仓库可以增加维护说明和离线 CI。它们不进入插件安装包，不增加 UI、后台、模型检测或自动保护。
- 社区包名保持 `@magpie-community/middleware-codex-history`。本仓库不自行发布社区 npm 作用域。

## 本地验证

```sh
node --test test/cases.test.mjs web-search.test.mjs
npm pack --ignore-scripts --dry-run
```

在社区仓库还需运行 `bun test packages/codex-history`。测试只使用虚构请求，不调用真实供应商。安装包仅包含 `package.json`、`codex-history.middleware.js`、`README.md`、`LICENSE` 和 `PROVENANCE.json`。

## 后续更新

1. 为社区纯过滤插件提交小范围修复，更新版本、测试和必要说明。
2. 合并后从社区源码同步本仓库；核对 `dist/index.json` 的实际版本和完整性值。GitHub 发版不等于社区市场已更新。
3. 对照社区安装包检查五个文件及版本，运行离线验证，再发布同版本 GitHub Release。更新功能边界时同步迁移说明。
4. 是否增加小型原生过滤设置页，后续根据用户反馈决定；目前通过 Magpie 的 Options 配置。

## 历史工作台与迁移

本仓库只保留社区纯过滤版的 Release：v0.1.0、v0.1.1。此前 v0.2.0 / v0.2.1 的合并工作台 Release 已移除；旧提交与 Git 标签仅作为源码历史，不用于分发或社区更新。以后工作台不在本仓库发版。

完整模型工作台的源码与后续开发统一在 [Codex Filter Manager](https://github.com/unisong/codex-filter-manager/tree/main/magpie-workbench) 维护。公共 `main` 的同步不更新本机已安装插件、不改写 Magpie Options、Codex `base_url` 或检测数据。原固定本地工作台目录仍可使用；不要在启用它的同时，再启用另一份历史过滤插件。

用户若决定从合并工作台迁移到纯过滤版，先私下备份需要的 Options 与工作台数据，在 Magpie 中停用旧插件，再安装社区版并复制所需过滤规则。纯过滤版只使用 `providers` 和 `aliases`，没有模型检测与暂停保护，也不提供工作台入口。
