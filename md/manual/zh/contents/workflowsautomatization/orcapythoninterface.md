```{index} ORCA Python Interface, OPI
```

(sec:workflowsautomatization.opi)=
# ORCA Python 接口（ORCA Python Interface, OPI）

:::{admonition} 重要
:class: important
**有关 OPI 的全面信息，请参阅 [OPI 文档](https://www.faccts.de/docs/opi/docs) 和 [OPI GitHub 仓库](https://github.com/faccts/opi)。**
:::

ORCA Python 接口（ORCA Python Interface，OPI）是一个多功能工具，可通过 Python 无缝访问 ORCA 计算。OPI 库提供了许多函数和类，便于定义计算设置、执行不同类型的 ORCA 计算并处理所得到的输出数据。它是开源的，可在 [GitHub](https://github.com/faccts/opi) 上免费获取。详细的安装说明和用法示例请参阅官方 [OPI 文档](https://www.faccts.de/docs/opi/docs)。

:::{versionadded} 6.1.0
OPI 的首个版本随 ORCA 6.1 发布。请注意，OPI 的开源开发独立于 ORCA 软件本身进行管理。有关最新更新和变更，请查阅 [OPI GitHub 仓库](https://github.com/faccts/opi) 和 [OPI 文档](https://www.faccts.de/docs/opi/docs)。
:::

## 安装（Installation）

OPI 既可以直接从 PyPI 安装：

```orca
pip install orca-pi
```

也可以从 GitHub 安装：

```orca
git clone https://github.com/faccts/opi.git
cd opi
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install .
```

为了正确使用 OPI，我们建议将其安装在 venv 环境中。更多说明请参阅 [OPI 文档](https://www.faccts.de/docs/opi/docs)。

