# ORCA 文档工程（ORCA docs）

基于官方 [ORCA 6.1 Tutorials / Manual](https://www.faccts.de/docs/orca/) 抓取、翻译并整理的中英双语文档站（MkDocs Material），页面内嵌 **fast-mol** 3D 结构查看器（`3D | input`）。

## 结构

| 路径 | 说明 |
|---|---|
| `md/en` `md/zh` | 教程 Markdown（英 / 中） |
| `md/manual/en` `md/manual/zh` | 手册章节 Markdown（来自官方 `_sources` + 翻译） |
| `md/images` | 教程共享图片 |
| `docs-site/` | MkDocs 站点源码（`mkdocs.yml`、hooks、主题） |
| `docs-site/docs/{en,zh}` | 站点内容（含 fast-mol 面板改造） |
| `crawl/` | 原始 HTML 镜像（**不入库**，可重爬） |

## 本地预览

```bash
cd docs-site
pip install mkdocs-material mkdocs-static-i18n
mkdocs build
python3 -m http.server 8000 --directory site
# http://127.0.0.1:8000/zh/
```

开发服务：

```bash
mkdocs serve
```

## 自动构建

Push 到 `main` 触发 GitHub Actions，构建 MkDocs 并发布到 `gh-pages` / 自定义 Pages。
