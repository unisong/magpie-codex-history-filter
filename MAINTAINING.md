# 社区版维护

本仓库是 Magpie 社区包 `@magpie-community/middleware-codex-history` 的镜像，只包含旧会话历史过滤：清理旧推理与协议密文、可移植条目 ID，以及把历史原生搜索记录转成文字。工作台、UI、模型检测和其他协议转码兼容只在[主仓库](https://github.com/unisong/codex-filter-manager)维护，不进入社区包。

## 与市场版本的对应

| 标签 | 市场版本 | 说明 |
| --- | --- | --- |
| `v0.1.2` | 0.1.2 | 路由组与 fallback 按每次实际尝试的供应商规则过滤；5 个安装文件与市场包逐字节一致 |
| `v0.1.1` | 0.1.1 | 安装文件与市场包一致，仅一行代码注释改为中性措辞 |
| `v0.1.0` | 0.1.0 | 同上 |

上述注释差异不影响行为。市场 0.1.0、0.1.1 的 PROVENANCE 固定主仓库 `v1.0.5` 时的提交，主仓库为隐私重建历史后，该提交不再位于任何分支或标签上。从 0.1.2 起，PROVENANCE 固定本仓库中可以检出的提交，并记录安装文件的 SHA-256。

0.1.2 让路由组与 fallback 的每次供应商尝试按该供应商规则过滤（`onProvider`）。[社区 PR #525](https://github.com/magpie-community/plugins/pull/525) 已于 2026-10-30 18:46（北京时间）合并，社区 `dist/index.json` 记录该版本于当天 18:51 分发。市场包的 SHA-512 与索引一致，`package.json`、`README.md`、`LICENSE`、`PROVENANCE.json` 和 `codex-history.middleware.js` 均与本仓库逐字节一致。

源码 `main`、Git 标签和 GitHub Release 是三个独立的发布状态，推送代码或合并社区 PR 都不会自动创建本仓库的 Release。0.1.2 曾在源码和市场已更新后仍缺标签与 Release，现已补齐。仓库独有的维护说明和离线测试不进入市场安装包；市场版本尚未递增时，不为了更新发布状态而修改安装文件或来源校验值。

## 同步流程

1. 过滤修复先在主仓库完成并测试，只同步属于历史过滤的改动，并附回归用例。
2. 本仓库运行 `node --test test/*.test.mjs web-search.test.mjs group-routing.test.mjs` 与 `npm pack --ignore-scripts --dry-run`；社区工作副本运行 `bun test packages/codex-history` 和 `bun scripts/check.mjs codex-history`。
3. 社区包 README 只写社区安装命令，本仓库链接仅放在来源与致谢；PROVENANCE 固定可检出的提交。
4. 合并并分发后，以社区 `dist` 分支 `index.json` 核对版本，校验实际下载包的完整性，并逐字节比较安装文件和来源校验值。提交 PR 不等于上架。
5. 完成分发核验后，更新本页版本表，推送维护提交和同版本标签，创建正式 GitHub Release 并设为 Latest。Release 链接到社区 PR，说明版本变更、安装方法与验证结果；不另行分发未经核对的安装包。
6. 最后复核远端 `main`、版本标签、Latest Release 和市场 `latest` 均指向预期版本。确认这四项之后才算发布完成；尚在等待社区审核时，应明确记录待办，不将 PR 提交成功表述为发布完成。

## 公开内容

README、代码注释、测试、提交说明、标签和 Release 正文不写真实供应商或中转站的名称、ID 与域名；测试使用虚构数据。第三方仓库地址只在致谢与来源记录中保留。使用主仓库本机 `.runtime/private-terms.txt` 检查待发布内容，词表本身不提交。
