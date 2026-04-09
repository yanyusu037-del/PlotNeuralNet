import sys
import os
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

# ViT styled diagram (clean, UNet-like structure)
custom_style = r"""
% --- ViT style ---
\def\InputColor{rgb:purple,5;white,2}
\def\PatchColor{rgb:cyan,5;white,2}
\def\TransColor{rgb:green,5;white,2}
\def\HeadColor{rgb:red,5;white,2}
% ----------------------------------------
\tikzset{every edge quotes/.append style={font=\large,inner sep=1pt,pos=0.35}}
\tikzset{depthlabel/.append style={font=\large,yshift=6pt}}
\tikzset{captionlabel/.append style={font=\large,yshift=-8pt}}
\tikzset{captionlabel/.append style={xshift=-30pt,yshift=20pt}}
"""

arch = [
    to_head('../..'),
    to_cor(),

    # ensure edgecolor is defined before styles are created in to_begin()
    r"""\usetikzlibrary{calc}
\def\edgecolor{black}
""",
    to_begin(),
    custom_style,

    # Input image
    to_ConvConvRelu(name='img_input', s_filer=224, n_filer=(3,3), offset='(0,0,0)', to='(0,0,0)',
                    width=(1.5,1.5), height=38, depth=38, caption='Image 224x224'),

    # Patch embedding
    to_ConvConvRelu(name='patch_linear', s_filer=768, n_filer=(768,768), offset='(3.0,0,0)', to='(img_input-east)',
                    width=(4,4), height=34, depth=34, caption='Patch Embed'),
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (img_input-east) -- (patch_linear-west);""",

    # CLS token + position
    to_ConvConvRelu(name='cls_pos', s_filer=197, n_filer=(768,768), offset='(2.5,0,0)', to='(patch_linear-east)',
                    width=(3.2,3.2), height=32, depth=32, caption='CLS + Pos'),
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (patch_linear-east) -- (cls_pos-west);""",

    # Transformer encoder block (visual placeholder)
    to_ConvConvRelu(name='transformer', s_filer=768, n_filer=(768,768), offset='(3.0,0,0)', to='(cls_pos-east)',
                    width=(4.5,4.5), height=42, depth=42, caption=r'Transformer $(12 \times L)$'),
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (cls_pos-east) -- (transformer-west);""",

    # Norm
    to_Pool(name='norm', offset='(2.2,0,0)', to='(transformer-east)', width=1.6, height=36, depth=36, caption='Norm'),
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (transformer-east) -- (norm-west);""",

    # Skip connection - UNet style with copymidarrow
    r"""\path (cls_pos-southeast) -- (cls_pos-northeast) coordinate[pos=1.25] (cls_pos-top) ;
\path (norm-south)  -- (norm-north)  coordinate[pos=1.25] (norm-top) ;
\draw [copyconnection]  (cls_pos-northeast)  
-- node {\copymidarrow}(cls_pos-top)
-- node {\copymidarrow}(norm-top)
-- node {\copymidarrow} (norm-north);
""",

    # Head
    to_ConvSoftMax(name='head', s_filer=1000, offset='(2.0,0,0)', to='(norm-east)', width=1.8, height=38, depth=38, caption='MLP Head 1000'),
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (norm-east) -- (head-west);""",

    # Skip connection 2 - Transformer to Head
    r"""\path (transformer-southeast) -- (transformer-northeast) coordinate[pos=1.25] (transformer-top) ;
\path (head-south)  -- (head-north)  coordinate[pos=1.25] (head-top) ;
\draw [copyconnection]  (transformer-northeast)  
-- node {\copymidarrow}(transformer-top)
-- node {\copymidarrow}(head-top)
-- node {\copymidarrow} (head-north);
""",

    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    outdir = os.path.join('..', 'SUIBE', 'ViT')
    os.makedirs(outdir, exist_ok=True)
    pathname = os.path.join(outdir, namefile + '.tex')
    to_generate(arch, pathname)


if __name__ == '__main__':
    main()
