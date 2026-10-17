# v0.1.1 · 与 Magpie 社区纯过滤版同步

本仓库的公开源码与 Magpie 社区 [PR #204](https://github.com/magpie-community/plugins/pull/204) 合并的 v0.1.1 保持一致。社区 `dist` 已发布此版本，GitHub 的 `.tgz` 附件使用同一份社区安装包。

- 开启供应商历史过滤后，将旧 `web_search_call` 转为带标记的助手文字，保留已记录的动作、查询、状态和来源，避免重放依赖原 reasoning 或资源 ID 的搜索条目。
- 保留后续结论与引用、普通工具参数和结果、`call_id` 配对；不重新搜索，也不补造未记录的结果。
- 保持供应商 Options、默认关闭、未配置供应商直通和加密压缩等不安全上下文的明确拒绝行为。
- 公开插件恢复为纯中间件：不含 UI、模型检测、保护、独立服务、启动脚本或额外模型请求。工作台继续单独本地维护。

## 安装

推荐从 Magpie 的 **Plugins → Discover → Gateway middleware** 安装或更新 **Codex History Filter**，也可使用：

```sh
magpie plugin add @magpie-community/middleware-codex-history
```

GitHub 安装使用固定标签：

```sh
magpie plugin add github:unisong/magpie-codex-history-filter#v0.1.1
```

或下载本页 ZIP，完整解压后添加该本地目录。配置方法见 [README](../README.md)。只启用一份历史过滤插件。

## 版本与旧工作台

社区纯过滤版的序列是 **v0.1.0 → v0.1.1**。旧 v0.2.0 / v0.2.1 是合并工作台的历史版本，不能按数字大小把它们当作社区版更新。旧标签和附件保留，当前社区版不加载工作台配置，也不提供检测或暂停。

本次公开仓库同步不会替换本机已安装的工作台。希望保留本地工作台的用户无需迁移；如改用纯过滤版，先停用旧工作台插件，备份并复制需要的过滤 Options，避免重复过滤。

## 验证与边界

离线测试覆盖 23 个网关用例、单入口与输入不变检查、6 个搜索历史回归。源码与安装包分别对照社区合并版本，安装包按社区 SHA-512 验证。测试不调用真实供应商。

该修复适用于携带明文历史的普通对话与文字总结，不解密加密压缩历史，不保证修复所有跨资源引用或 Azure 错误。Magpie 加载失败、异常或超时仍可能放行原请求。
