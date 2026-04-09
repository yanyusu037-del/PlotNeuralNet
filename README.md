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

    ```powershell
"c:\Users\1suyanyu\Documents\GitHub\PlotNeuralNet\pyexamples"; ..\.venv\Scripts\python.exe unet_styled.py
    ```

    ```powershell
cd "c:\Users\1suyanyu\Documents\GitHub\PlotNeuralNet\SUIBE\unet"; & "C:\Users\1suyanyu\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode unet_styled.tex; & "C:\Users\1suyanyu\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode unet_styled.tex
    ```

### ViT 与 MSA 架构图绘制问题（2024年）

#### ViT 多页 PDF 问题

**问题描述**：使用 `\shortstack{..\\..}` 编写复杂标题时，编译出现 2 页 PDF（实际只有 1 页内容），错误信息为 "Extra }, or forgotten \endgroup"。

**根本原因**：
- `\shortstack{Patch Embed\\196x768}` 中嵌套的反斜杠转义和括号计数不匹配
- LaTeX 在处理多层嵌套的特殊字符时括号计数出错
- 虽然 PDF 仍可生成，但页数计算错误导致 pdflatex 认为有额外页面

**解决方案**：
1. 将复杂标题替换为简单文本：
   ```python
   # 改前（导致2页）：
   caption=r'{\shortstack{Patch Embed\\196x768}}'
   
   # 改后（1页）：
   caption='Patch Embed'
   ```

2. 使用 LaTeX 数学模式表达乘号：
   ```python
   caption=r'Transformer $(12 \times L)$'  # 而不是 L \times 或 \\times
   ```

3. 验证编译：
   - 检查输出是否为 "1 page" 而不是 "2 pages"
   - 使用参考实现（如 UNet）作为对比基准

#### 并列模块重叠问题

**问题描述**：当在同一图中绘制多个并行的编码器/解码器分支时，模块容易重叠或布局混乱。

**解决方案**：
1. **分层布局**：将并行分支分配到不同行：
   - ROW 1：上层（主编码路径）
   - ROW 2：下层（提示编码路径）
   - ROW 3：底层（解码合并层）

2. **行间距控制**：使用 y 坐标偏移调整行间距：
   ```python
   # 第二行，距上层 7.5 单位
   to_ConvConvRelu(name='prompt_points', ..., offset='(2.2,-7.5,0)', to='(preproc-south)')
   
   # 第三行，距上层 3.8 单位
   to_ConvConvRelu(name='decoder', ..., offset='(2.5,-3.8,0)', to='(img_emb-south)')
   ```

3. **清晰的数据流线**：用显式的 `\draw` 命令连接分支：
   ```python
   r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (img_emb-south) -- (decoder-north);"""
   r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (prompt_emb-east) -- ($(decoder-west)+(0,-0.3)$);"""
   ```

#### 嵌套 TikZ 命令问题

**问题描述**：使用 `to_connection()` 和 `to_skip()` 辅助函数时，生成的代码包含嵌套 `\tikz` 命令（如 `\copymidarrow`），导致"TeX capacity exceeded"或括号不匹配错误。

**解决方案**：
1. 避免使用生成嵌套 TikZ 的辅助函数
2. 直接编写 `\draw` 命令：
   ```python
   # 避免使用：
   # to_connection("node1", "node2")
   # to_skip(of='node1', to='node2', pos=1.25)
   
   # 改用直接绘制：
   r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (node1-east) -- (node2-west);"""
   ```

3. 确保 `\edgecolor` 在所有 TikZ 样式定义**之前**定义：
   ```python
   r"""\usetikzlibrary{calc}
\def\edgecolor{black}
""",  # 放在 to_begin() 前面
   to_begin(),
   ```

#### 推荐最佳实践

1. **参考现有实现**：使用已验证的 UNet、UNet_styled 作为模板
2. **逐步构建**：先构建单行（如仅编码器），再添加分支
3. **频繁编译测试**：每添加主要部分后立即编译，早期发现问题
4. **避免过度嵌套**：使用 `-Stealth` 箭头风格和 `copyconnection` 样式，但不要嵌套 `\tikz` 命令
5. **保持简洁**：复杂标题使用纯文本，数学符号用 LaTeX 数学模式
6. **验证单页输出**：确保最终 PDF 为 1 页（编译输出应为 "1 page"）

### MSA Adapter vs LoRA 架构对比（2024年）

#### Adapter 方法（MSA Adapter - `msa_styled.py`）

**设计理念**：
- 在预训练模型的前馈层后插入小型瓶颈模块（Adapter）
- 冻结所有 SAM 原始权重（ImageEncoderViT、PromptEncoder、MaskDecoder）为灰色
- 仅 Adapter 层可训练

**参数量**：
- 冻结权重：~71M（SAM-B）
- 可训练参数：~0.3M（Adapter）
- 总参数：~71.3M

**图示特点**：
- 灰色块：所有冻结的预训练组件
- 黑色箭头：数据流
- 输出图尺寸：1 页 PDF (598.6pt, 40,937 字节)

#### LoRA 方法（MSA LoRA - `msa_lora_styled.py`）

**设计理念**：
- 在多头注意力的 Q、K、V 投影层中注入低秩分解矩阵
- LoRA 模块 = 两个秩 $r$ 的矩阵分解：$W_{new} = W_{old} + AB^T$
- 冻结所有原始权重，仅训练低秩矩阵 A 和 B

**参数量**：
- 冻结权重：~71M（SAM-B）
- LoRA 参数：~0.5M（rank=8 in ViT, rank=4 in decoder）
- 总参数：~71.5M
- 相比 Adapter 多约 67% 参数，但分布更均匀

**图示特点**：
- 灰色块：所有冻结的原始权重
- 红色小方块：LoRA 注入点（通过虚线箭头连接）
- 红色虚线：表示 LoRA 参数的旁路连接
- 输出图尺寸：1 页 PDF (635.6pt, 66,306 字节)

#### 方法对比表

| 特性 | Adapter | LoRA |
|------|---------|------|
| **参数位置** | 前馈层后 | Attention Q,K,V |
| **训练成本** | 中等（顺序添加） | 较低（矩阵分解） |
| **推理延迟** | +5-10% | 接近零（可融合） |
| **参数量** | 0.3M | 0.5M |
| **可微调层数** | 少（仅 Adapter） | 多（所有 Attention） |
| **与原权重兼容** | 完全兼容 | 需要融合权重 |
| **适用场景** | 一般微调 | 多任务学习/知识蒸馏 |

#### 生成命令

**Adapter 版本**（灰色冻结块标记）：
```powershell
cd d:\PlotNeuralNet\pyexamples
..\.venv\Scripts\python.exe msa_styled.py
# 输出：SUIBE/MSA/msa_styled.tex → msa_styled.pdf
```

**LoRA 版本**（灰色冻结块 + 红色 LoRA 注入点）：
```powershell
cd d:\PlotNeuralNet\pyexamples
..\.venv\Scripts\python.exe msa_lora_styled.py
# 输出：SUIBE/MSA_LoRA/msa_lora_styled.tex → msa_lora_styled.pdf
```

**编译**（两个版本都采用相同流程）：
```powershell
cd 'D:\PlotNeuralNet\SUIBE\MSA'       # 或 MSA_LoRA
& 'D:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe' -interaction=nonstopmode msa_[styled|lora_styled].tex
```

#### 设计要点

1. **冻结块可视化**：两个版本都使用 `\draw [ultra thick, dashed, draw=gray, opacity=0.8]` 用**灰色虚线边框**标识冻结块
   - 优点：不遮挡块本身的颜色，清晰展示参数冻结状态
   - 代码示例：
   ```python
   to_ConvConvRelu(name='vit_blocks', ...)
   r"""\draw [ultra thick, dashed, draw=gray, opacity=0.8] (vit_blocks-south) rectangle (vit_blocks-north);"""
   ```

2. **LoRA 注入指示**：使用小型红色实心块表示 LoRA 参数，实心红色箭头连接
   - 位置调整避免与主块重叠
   - 代码示例：
   ```python
   to_Pool(name='lora_qkv', offset='(3.8,2.2,0)', to='(vit_blocks-west)', ...)
   r"""\fill[LoRAColor] (lora_qkv-south) rectangle (lora_qkv-north);"""
   r"""\draw [ultra thick,-Stealth,draw=red,opacity=0.9] (lora_qkv-southwest) -- (vit_blocks-north);"""
   ```

3. **图层间隔**：
   - Adapter 版本：598.6pt（1 页）
   - LoRA 版本：679.5pt（1 页，因 LoRA 注入点额外占用空间）

4. **图例标注**：底部添加清晰的图例，标注参数分布