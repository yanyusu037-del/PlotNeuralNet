import sys
import os
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

# MSA (Medical SAM Adapter) 架构图 - 多行并行设计
# 冻结块用灰色，Adapter可训练块用彩色
custom_style = r"""
% --- MSA Adapter style: Frozen vs Trainable ---
\def\FrozenColor{rgb:gray,3;white,7}          % 冻结块：浅灰色
\def\AdapterColor{rgb:green,5;white,2}        % Adapter：绿色（可训练）
\def\InputColor{rgb:purple,5;white,2}         % 输入：紫色
\def\PromptColor{rgb:orange,5;white,2}        % 提示：橙色
% ----------------------------------------
\tikzset{every edge quotes/.append style={font=\large,inner sep=1pt,pos=0.35}}
\tikzset{depthlabel/.append style={font=\large,yshift=6pt}}
\tikzset{captionlabel/.append style={font=\large,yshift=-8pt}}
% Hide dashed lines in box edges by making them invisible
\tikzset{every edge/.append style={draw=none}}
"""

arch = [
    to_head('../..'),
    to_cor(),

    # ensure edgecolor is defined before to_begin()
    r"""\usetikzlibrary{calc}
\def\edgecolor{black}
""",
    to_begin(),
    custom_style,

    # ===== ROW 1: Image Encoding Path (Frozen) =====
    # Input image (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='input', s_filer=1024, n_filer=(3,3), offset='(0,0,0)', to='(0,0,0)',
                    width=(1.8,1.8), height=36, depth=36, caption='Image'),
    r"""\fill [gray!25, opacity=0.35] (input-south) rectangle (input-north);""",

    # Preprocessing (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='preproc', s_filer=1024, n_filer=(3,3), offset='(2.2,0,0)', to='(input-east)',
                    width=(1.8,1.8), height=36, depth=36, caption='Preprocess'),
    r"""\fill [gray!25, opacity=0.35] (preproc-south) rectangle (preproc-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (input-east) -- (preproc-west);""",

    # Patch Embedding (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='patch_embed', s_filer=768, n_filer=(256,256), offset='(2.2,0,0)', to='(preproc-east)',
                    width=(2.2,2.2), height=32, depth=32, caption='Patch Embed'),
    r"""\fill [gray!25, opacity=0.35] (patch_embed-south) rectangle (patch_embed-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (preproc-east) -- (patch_embed-west);""",

    # ViT Blocks (Encoder) - FROZEN
    to_ConvConvRelu(name='vit_blocks', s_filer=768, n_filer=(256,256), offset='(2.5,0,0)', to='(patch_embed-east)',
                    width=(3.5,3.5), height=34, depth=34, caption='ViT Encoder (12L)'),
    r"""\fill [gray!25, opacity=0.35] (vit_blocks-south) rectangle (vit_blocks-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (patch_embed-east) -- (vit_blocks-west);""",

    # Image Embeddings output - FROZEN
    to_Pool(name='img_emb', offset='(2.5,0,0)', to='(vit_blocks-east)', width=1.8, height=34, depth=34, caption='Image Emb'),
    r"""\fill [gray!25, opacity=0.35] (img_emb-south) rectangle (img_emb-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (vit_blocks-east) -- (img_emb-west);""",

    # ===== ROW 2: Prompt Encoding Path (Frozen) =====
    # Prompt Encoder branch - use relative positioning
    to_ConvConvRelu(name='prompt_points', s_filer=256, n_filer=(256,256), offset='(2.2,-7.5,0)', to='(preproc-south)',
                    width=(2.0,2.0), height=24, depth=24, caption='Points'),
    r"""\fill [gray!25, opacity=0.35] (prompt_points-south) rectangle (prompt_points-north);""",

    to_ConvConvRelu(name='prompt_boxes', s_filer=256, n_filer=(256,256), offset='(2.2,0,0)', to='(prompt_points-east)',
                    width=(2.0,2.0), height=24, depth=24, caption='Boxes'),
    r"""\fill [gray!25, opacity=0.35] (prompt_boxes-south) rectangle (prompt_boxes-north);""",

    to_ConvConvRelu(name='prompt_masks', s_filer=256, n_filer=(256,256), offset='(2.2,0,0)', to='(prompt_boxes-east)',
                    width=(2.0,2.0), height=24, depth=24, caption='Masks'),
    r"""\fill [gray!25, opacity=0.35] (prompt_masks-south) rectangle (prompt_masks-north);""",

    # Prompt Encoder merge - FROZEN
    to_Pool(name='prompt_emb', offset='(1.8,0,0)', to='(prompt_masks-east)', width=1.8, height=24, depth=24, caption='Prompt Emb'),
    r"""\fill [gray!25, opacity=0.35] (prompt_emb-south) rectangle (prompt_emb-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (prompt_masks-east) -- (prompt_emb-west);""",

    # ===== ROW 3: Decoder Path (Frozen) =====
    # MaskDecoder (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='decoder', s_filer=256, n_filer=(256,256), offset='(2.5,-3.8,0)', to='(img_emb-south)',
                    width=(4.5,4.5), height=32, depth=32, caption='MaskDecoder'),
    r"""\fill [gray!25, opacity=0.35] (decoder-south) rectangle (decoder-north);""",

    # Connection from Image Emb to Decoder (from center, not south)
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] ($(img_emb-south)!0.5!(img_emb-north)$) -- ($(decoder-north)!0.5!(decoder-south)$);""",

    # Connection from Prompt Emb to Decoder
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (prompt_emb-east) -- ($(decoder-west)+(0,-0.3)$);""",

    # IoU Head (quality prediction) - FROZEN
    to_Pool(name='iou_head', offset='(2.5,0,0)', to='(decoder-east)', width=1.8, height=32, depth=32, caption='IoU Head'),
    r"""\fill [gray!25, opacity=0.35] (iou_head-south) rectangle (iou_head-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (decoder-east) -- (iou_head-west);""",

    # Output: Segmentation Masks (可训练 - 保持彩色)
    to_ConvSoftMax(name='masks_out', s_filer=256, offset='(2.0,0,0)', to='(iou_head-east)', width=2.0, height=32, depth=32, caption='Output Masks'),
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (iou_head-east) -- (masks_out-west);""",

    to_end()
]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(script_dir, '..', 'SUIBE', 'MSA')
    os.makedirs(outdir, exist_ok=True)
    pathname = os.path.join(outdir, 'msa_styled.tex')
    to_generate(arch, pathname)


if __name__ == '__main__':
    main()

