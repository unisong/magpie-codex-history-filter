# 社区版维护

本仓库是 Magpie 社区包 `@magpie-community/middleware-codex-history` 的镜像，只包含旧会话历史过滤：清理旧推理与协议密文、可移植条目 ID，以及把历史原生搜索记录转成文字。工作台、UI、模型检测和其他协议转码兼容只在[主仓库](https://github.com/unisong/codex-filter-manager)维护，不进入社区包。

## 与市场版本的对应

| 标签 | 市场版本 | 说明 |
| --- | --- | --- |
| `v0.1.0` | 0.1.0 | 安装文件与市场包一致，仅一行代码注释改为中性措辞 |
| `v0.1.1` | 0.1.1（当前） | 同上；`main` 在此基础上只增加离线测试与本说明 |

上述注释差异不影响行为。社区包的 PROVENANCE 固定主仓库 `v1.0.5` 时的提交，主仓库为隐私重建历史后，该提交不再位于任何分支或标签上，README 中指向该标签的链接因此失效；PROVENANCE 记录的两个源文件 SHA-256 不变。下一个社区版本应固定到本仓库可以检出的提交。

## 同步流程

1. 过滤修复先在主仓库完成并测试，只同步属于历史过滤的改动，并附回归用例。
2. 本仓库运行 `node --test test/*.test.mjs web-search.test.mjs` 与 `npm pack --ignore-scripts --dry-run`；社区工作副本运行 `bun test packages/codex-history` 和 `bun scripts/check.mjs codex-history`。
3. 社区包 README 只写社区安装命令，本仓库链接仅放在来源与致谢；PROVENANCE 固定可检出的提交。
4. 合并并分发后，以社区 `dist` 分支 `index.json` 核对版本与完整性，再在本仓库打同版本标签。提交 PR 不等于上架。

## 公开内容

README、代码注释、测试、提交说明、标签和 Release 正文不写真实供应商或中转站的名称、ID 与域名；测试使用虚构数据。第三方仓库地址只在致谢与来源记录中保留。使用主仓库本机 `.runtime/private-terms.txt` 检查待发布内容，词表本身不提交。
