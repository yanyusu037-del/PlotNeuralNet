# PlotNeuralNet
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2526396.svg)](https://doi.org/10.5281/zenodo.2526396)

Latex code for drawing neural networks for reports and presentation. Have a look into examples to see how they are made. Additionally, lets consolidate any improvements that you make and fix any bugs to help more people with this code.

## Examples

Following are some network representations:

<p align="center"><img  src="https://user-images.githubusercontent.com/17570785/50308846-c2231880-049c-11e9-8763-3daa1024de78.png" width="85%" height="85%"></p>
<h6 align="center">FCN-8 (<a href="https://www.overleaf.com/read/kkqntfxnvbsk">view on Overleaf</a>)</h6>


<p align="center"><img  src="https://user-images.githubusercontent.com/17570785/50308873-e2eb6e00-049c-11e9-9587-9da6bdec011b.png" width="85%" height="85%"></p>
<h6 align="center">FCN-32 (<a href="https://www.overleaf.com/read/wsxpmkqvjnbs">view on Overleaf</a>)</h6>


<p align="center"><img  src="https://user-images.githubusercontent.com/17570785/50308911-03b3c380-049d-11e9-92d9-ce15669017ad.png" width="85%" height="85%"></p>
<h6 align="center">Holistically-Nested Edge Detection (<a href="https://www.overleaf.com/read/jxhnkcnwhfxp">view on Overleaf</a>)</h6>

## Getting Started
1. Install the following packages on Ubuntu.
    * Ubuntu 16.04
        ```
        sudo apt-get install texlive-latex-extra
        ```

    * Ubuntu 18.04.2
Base on this [website](https://gist.github.com/rain1024/98dd5e2c6c8c28f9ea9d), please install the following packages.
        ```
        sudo apt-get install texlive-latex-base
        sudo apt-get install texlive-fonts-recommended
        sudo apt-get install texlive-fonts-extra
        sudo apt-get install texlive-latex-extra
        ```

    * Windows
    1. Download and install [MikTeX](https://miktex.org/download).
    2. Download and install bash runner on Windows, recommends [Git bash](https://git-scm.com/download/win) or Cygwin(https://www.cygwin.com/)

2. Execute the example as followed.
    ```
    cd pyexamples/
    bash ../tikzmake.sh test_simple
    ```

## TODO

- [X] Python interface
- [ ] Add easy legend functionality
- [ ] Add more layer shapes like TruncatedPyramid, 2DSheet etc
- [ ] Add examples for RNN and likes.

## Latex usage

See [`examples`](examples) directory for usage.

## Python usage

First, create a new directory and a new Python file:

    $ mkdir my_project
    $ cd my_project
    vim my_arch.py

Add the following code to your new file:

```python
import sys
sys.path.append('../')
from pycore.tikzeng import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_Conv("conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2 ),
    to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)"),
    to_Conv("conv2", 128, 64, offset="(1,0,0)", to="(pool1-east)", height=32, depth=32, width=2 ),
    to_connection( "pool1", "conv2"),
    to_Pool("pool2", offset="(0,0,0)", to="(conv2-east)", height=28, depth=28, width=1),
    to_SoftMax("soft1", 10 ,"(3,0,0)", "(pool1-east)", caption="SOFT"  ),
    to_connection("pool2", "soft1"),
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
```

Now, run the program as follows:

    bash ../tikzmake.sh my_arch

## 工作流（基于当前实现，Windows）

下面是基于当前代码的推荐步骤，便于你生成并编译模型结构图：

- 创建并使用虚拟环境（项目根）

- 在 `pyexamples` 目录生成模型 `.tex`（示例以 UNet 为例）
    ```powershell
    cd pyexamples
    ..\.venv\Scripts\python.exe unet_styled.py
    # 生成路径示例： SUIBE/unet/unet_styled.tex（脚本会自动创建子目录）
    ```

- 每个模型独立子目录
    - 约定输出放在 `SUIBE/<model>/`（比如 `SUIBE/unet/`），便于管理多个模型的输出与结果。

- 编译 `.tex` 为 PDF（两次以确保引用/目录正确）
    ```powershell
    cd SUIBE\unet
    # 若 pdflatex 在 PATH 中：
    pdflatex -interaction=nonstopmode unet_styled.tex
    pdflatex -interaction=nonstopmode unet_styled.tex
    start unet_styled.pdf
    ```
    - 若 pdflatex 未加入 PATH，可用 MiKTeX 完整路径调用（按实际安装路径调整）：
    ```powershell
    & "C:\Users\<you>\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode unet_styled.tex
    ```

- MiKTeX 选择（无需管理员）
    - 可选择 “Only for: Current User” 安装，或下载 MiKTeX Portable 到可写目录并直接使用可执行文件。

- 关于 bash 脚本
    - 若想直接运行仓库内的 `.sh`，可用 `Git Bash`（推荐）或 `Cygwin`；也可在 PowerShell 中运行等效命令。

- 提交建议
    - 推荐把生成脚本（`pyexamples/*.py`）与修改提交到仓库；是否把自动生成的 `.tex`/`.pdf` 提交由团队策略决定（示例输出可不提交，或放 release）。

- word应用
1. 嵌入原始 PDF 文件（简单，显示为对象/图标）
Word 中：插入 → 对象 → 由文件创建（Insert → Object → Create from File）→ 选中你的 PDF → 确认。
优点：保留完整 PDF，可双击打开完整文件；缺点：Word 中可能只显示第一页或显示为图标，不会把每页展成 Word 页。
2。 把 PDF 每页转换为高分辨率位图再插入（兼容性好，页面布局可控）

## Troubleshooting / 常见问题与解决方案

- 问题：运行 `pdflatex` 报错 “pdflatex not found”。
    解决：需要安装 LaTeX（Windows 推荐 MiKTeX）。可选择用户安装（无需管理员）或使用 MiKTeX Portable（免安装）。安装后重启终端并验证：
    ```powershell
    pdflatex --version
    ```

- 问题：运行 `pyexamples/*.py` 报错 `ModuleNotFoundError: No module named 'pycore'`。
    解决：从 `pyexamples` 目录运行脚本（脚本使用 `sys.path.append('../')` 依赖相对路径），例如：
    ```powershell
    cd pyexamples
    ..\.venv\Scripts\python.exe unet_styled.py
    ```

- 问题：编译 `.tex` 时提示 `! LaTeX Error: File `import.sty' not found.`（或其它缺包）。
    解决：在 MiKTeX Console 中启用 “Install missing packages on-the-fly”，或手动安装缺失包（图形界面或命令行）：
    ```powershell
    mpm --install=import
    initexmf --update-fndb
    pdflatex -interaction=nonstopmode unet_styled.tex
    ```

- 问题：希望把生成的 `.tex` 放到指定目录。
    说明：我们已把 styled UNet 的输出放到 `SUIBE/unet_styled.tex`；如需更改，编辑 `pyexamples/unet_styled.py` 中的输出路径并重新运行。

- 常用编译命令（在 `SUIBE` 目录下运行）：
    ```powershell
    pdflatex -interaction=nonstopmode unet_styled.tex
    pdflatex -interaction=nonstopmode unet_styled.tex
    # 或使用 latexmk
    latexmk -pdf -interaction=nonstopmode unet_styled.tex
    ```



