import sys
import os
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

# 门控Adapter模块 - 单个模块结构图
# 展示Adapter的内部结构和门控机制

custom_style = r"""
% --- Gated Adapter Module Style ---
\def\FrozenColor{gray!25}              % 冻结权重：浅灰色
\def\AdapterColor{green!60}            % Adapter可训练：绿色
\def\GateColor{blue!60}                % 门控：蓝色
\def\ActivColor{orange!50}             % 激活函数：橙色
% ----------------------------------------
"""

arch = [
    to_head('../..'),
    to_cor(),

    # ensure edgecolor is defined before to_begin()
    r"""\usetikzlibrary{calc}
\def\edgecolor{black}
""",
    to_begin(),
    r"""\tikzset{every edge quotes/.append style={font=\large,inner sep=1pt,pos=0.35}}""",
    r"""\tikzset{depthlabel/.append style={font=\large,yshift=6pt}}""",
    r"""\tikzset{captionlabel/.append style={font=\large,yshift=-8pt}}""",
    r"""\tikzset{every edge/.append style={draw=black}}""",
    custom_style,

    # ===== Gated Adapter Module Structure =====
    # Input (FROZEN - from pre-trained model)
    to_Pool(name='input', offset='(0,0,0)', to='(0,0,0)', width=1.5, height=28, depth=28, caption='Input'),
    r"""\fill [gray!25, opacity=0.35] (input-south) rectangle (input-north);""",
    r"""\node [text=black, font=\Large, inner sep=0] at ($(input-south) + (-0.3, -0.5)$) {768};""",

    # Down-Project Layer (TRAINABLE - dimension reduction: 768→192)
    to_Pool(name='down_proj', offset='(3.2,0,0)', to='(input-east)', width=1.5, height=26, depth=26, caption='Down'),
    r"""\fill [\AdapterColor, opacity=0.6] (down_proj-south) rectangle (down_proj-north);""",
    r"""\node [text=black, font=\Large, inner sep=0] at ($(down_proj-south) + (-0.3, -0.5)$) {192};""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (input-east) -- (down_proj-west);""",

    # ReLU Activation
    to_Pool(name='relu', offset='(2.3,0,0)', to='(down_proj-east)', width=1.5, height=22, depth=22, caption='ReLU'),
    r"""\fill [\ActivColor, opacity=0.5] (relu-south) rectangle (relu-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (down_proj-east) -- (relu-west);""",

    # Up-Project Layer (TRAINABLE - dimension recovery: 192→768)
    to_Pool(name='up_proj', offset='(3.2,0,0)', to='(relu-east)', width=1.5, height=26, depth=26, caption='Up'),
    r"""\fill [\AdapterColor, opacity=0.6] (up_proj-south) rectangle (up_proj-north);""",
    r"""\node [text=black, font=\Large, inner sep=0] at ($(up_proj-south) + (-0.3, -0.5)$) {768};""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (relu-east) -- (up_proj-west);""",

    # Gate Module (TRAINABLE - dynamic 3-branch gate: Space / Depth / MLP)
    # place gate below down_proj using a known anchor (down_proj-south)
    to_Pool(name='gate', offset='(0.5,-1.8,0)', to='(down_proj-south)', width=1.2, height=8, depth=8, caption='Gate'),
    r"""\fill [\GateColor, opacity=0.75] (gate-south) rectangle (gate-north);""",
    # three gate outputs to Space / Depth / MLP (split arrows)
    # swap mlp and space labels to avoid crossing
    # adjust gate output directions and lower space arrow slightly to avoid overlap
    r"""\draw [ultra thick,-Stealth,draw=blue,opacity=0.9] (gate-east) -- ++(1.0,0) node [midway, above] {mlp} coordinate (gate-mlp);""",
    r"""\draw [ultra thick,-Stealth,draw=blue,opacity=0.9] (gate-south) -- ++(0,-1.0) node [midway, left] {depth} coordinate (gate-depth);""",
    r"""\draw [ultra thick,-Stealth,draw=blue,opacity=0.9] (gate-west) -- ++(-1.0,-0.15) node [midway, above] {space} coordinate (gate-space);""",

    # compact multiplier icons aligned between Up and Add
    # place multipliers so mlp is on the right and space on the left to match gate outputs
    # (removed explicit multiplier × nodes — use direct gated connections into add)
    # Connect gate outputs directly to the merge node (no × symbols)
    r"""\draw [thick,draw=blue,opacity=0.9] (gate-space) -- (add-west);""",
    r"""\draw [thick,draw=blue,opacity=0.9] (gate-mlp) -- (add-west);""",
    r"""\draw [thick,draw=blue,opacity=0.9] (gate-depth) -- (add-west);""",

    # Merge gated outputs and add residual (single, clear add node)
    to_Pool(name='add', offset='(2.2,0,0)', to='(up_proj-east)', width=2.2, height=28, depth=28, caption='+Res'),
    r"""\fill [\AdapterColor, opacity=0.3] (add-south) rectangle (add-north);""",
    # connect all three multipliers into the add node so no branch is left dangling
    # gate outputs already draw into add; also add the up_proj->add connection to keep flow
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (up_proj-east) -- (add-west);""",
    
    # Residual skip connection (arc path: up -> right -> down, like UNet skip)
    r"""\path (input-east) -- ++(0,2.5) coordinate (input-top) ;""",
    r"""\path (add-west) -- ++(0,2.5) coordinate (add-top) ;""",
    r"""\draw [ultra thick,-Stealth,draw=green,opacity=0.6] (input-east) -- (input-top) -- (add-top) -- (add-west);""",

    # Output
    to_Pool(name='output', offset='(3.2,0,0)', to='(add-east)', width=1.5, height=28, depth=28, caption='Output'),
    r"""\fill [gray!25, opacity=0.35] (output-south) rectangle (output-north);""",
    r"""\node [text=black, font=\Large, inner sep=0] at ($(output-south) + (-0.3, -0.5)$) {768};""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (add-east) -- (output-west);""",

    to_end()
]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(script_dir, '..', 'SUIBE', 'GatedAdapter')
    os.makedirs(outdir, exist_ok=True)
    pathname = os.path.join(outdir, 'gated_adapter_module.tex')
    to_generate(arch, pathname)


if __name__ == '__main__':
    main()
