# 维护与发布

本仓库从 v0.2.0 起发布合并工作台，保留原包名 `magpie-middleware-codex-history` 和 v0.1.0 标签。合并版已准备同步至 Magpie 社区市场；**推送本仓库或创建 GitHub Release 不会自动更新市场，需待社区审核合并与分发**。

| 分发入口 | 仓库 / 包名 | 谁能发布 |
| --- | --- | --- |
| GitHub 合并工作台与 Release | `unisong/magpie-codex-history-filter`，包名 `magpie-middleware-codex-history` | 本仓库维护者 |
| Magpie 社区市场（合并版待审核） | `magpie-community/plugins/packages/codex-history`，包名 `@magpie-community/middleware-codex-history` | 维护者提交 PR，社区审核合并后自动分发 |

## 每次更新

1. 在本仓库修复问题，更新 `package.json`、`server/engine.mjs` 与 `server/http.mjs` 的版本字段、界面版本文字与对应测试。编写 Release 说明；纯诊断工具不能进入请求关键路径，也不能新增隐私日志。
2. 运行 `npm run build`、`npm test`、`python test/web-check.py`。宿主改动需运行 `python test/magpie-smoke.py --binary /path/to/magpie.exe --bun /path/to/magpie-bun.exe`，使用临时便携宿主和模拟上游。不要在安装中的插件目录测试，不用真实供应商凭据。
3. 用 `python tools/screenshots.py` 更新演示截图。暂存公共文件后运行 `npm run release:check` 和 `python tools/package-release.py`，检查包内没有个人路径、凭据、检测数据或运行中的生成门禁。推送并等 CI 通过后发布 ZIP、TGZ 与校验值；发布过的标签和附件不可覆盖。README 安装命令需同步更新。
4. 社区市场单独维护：从最新社区 `main` 创建新分支，更新 `packages/codex-history/`，不要复用已合并的旧 PR。同步合并工作台时保留社区包名、发布入口及测试要求，明确新增后台、文件读写和可选检测的边界；不能仅复制 package.json。打包必须重新生成无私密门禁的入口，并用真实宿主和模拟上游验证社区包名安装。
5. 保留社区包名、`repository.directory`、标准 Bun 测试入口，更新其版本、`files` 和 README。同步原生页面时保留 `permissions: ["providers:list"]`；如功能分类有变化，再修改 registry 和总 README。
6. 提交 PR，附问题、改动、测试结果及对配置/隐私的影响。审核合并后，检查 `publish` 的 **test** 与 **dist** 步骤、dist 索引的版本与完整性值。不能只看 workflow 总体红绿：无关 npm 包的发布失败不一定阻断本插件 dist 分发。
7. 用隔离目录验证新版本可从市场包名安装，再告知用户升级。市场正式可用以前，不要把 GitHub 发版等同于市场上架。

社区补丁若先于本仓库合入，应将相同修复同步回本仓库，避免两份源码分叉。当前过滤逻辑源自 Codex Filter Manager，修改共用算法时也应评估同步至该项目的 `magpie-plugin/history-filter.mjs` 和本地插件。

## 用户怎样更新

- **市场安装**：通过 Magpie 插件页更新，或 `magpie plugin update`（该命令会更新全部插件）。不同 Magpie 版本的后台更新和缓存策略可能不同，核对 Installed 中的实际版本。
- **固定 GitHub 标签安装**：仍固定在该标签；用新标签地址更新或重新安装，旧标签不会自动跳到新标签。迁移前备份本插件的 Options，不要公开整个 plugins.json。
- **本地目录安装**：替换本地源码不会自动从市场下载新版本。按 README 迁移，停用旧副本后安装市场版，不要同时开启两份。

## npm 和权限

`@magpie-community/*` 属于社区组织。不要自行向其作用域发布或索要其 npm 凭据。当前社区 dist 分发支持尚未首次发布到 npm 的新包；未来是否首次 npm 发布由社区维护者处理。贡献者只需有自己 fork 的推送权限和提交 PR 的 GitHub 登录。

## v0.2.0 分发边界

合并版使用 Magpie 自带 Bun，无需另装 Node.js。原生页只管理历史过滤；完整工作台在本机浏览器打开。安装默认不启用过滤、监测或保护。历史算法保持根目录原始钩子与 `history/` 相同 SHA-256，模型库保留来源与 MIT 许可。不要从安装中的插件拷贝 `workbench.middleware.js` 回源码；后台可能已在该文件写入私密探针凭据和暂停规则，发版必须由 `npm run build` 重新生成公共入口。
