import sys
import os
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

# MSA (Medical SAM) with LoRA - Low-Rank Adaptation
# LoRA在Q、K、V投影层的低秩分解注入
custom_style = r"""
% --- MSA LoRA style: Frozen Weights vs LoRA Parameters ---
\tikzset{every edge quotes/.append style={font=\large,inner sep=1pt,pos=0.35}}
\tikzset{depthlabel/.append style={font=\large,yshift=6pt}}
\tikzset{captionlabel/.append style={font=\large,yshift=-8pt}}
"""

arch = [
    to_head('../..'),
    to_cor(),

    # Custom colors for MSA LoRA
    r"""
\def\FrozenColor{gray!25}          % 冻结权重：浅灰色
\def\LoRAColor{rgb:red,4;white,1}  % LoRA参数：鲜红色（可训练，仅关键位置）
""",

    # ensure edgecolor is defined before to_begin()
    r"""\usetikzlibrary{calc}
\def\edgecolor{black}
""",
    to_begin(),
    custom_style,

    # ===== ROW 1: Image Encoding Path with LoRA in Transformer =====
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

    # ViT Blocks (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='vit_blocks', s_filer=768, n_filer=(256,256), offset='(2.5,0,0)', to='(patch_embed-east)',
                    width=(3.5,3.5), height=34, depth=34, caption='ViT Encoder (12L)'),
    r"""\fill [gray!25, opacity=0.35] (vit_blocks-south) rectangle (vit_blocks-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (patch_embed-east) -- (vit_blocks-west);""",

    # LoRA injection in Q,K,V (positioned well above ViT block, left-aligned for loop layout)
    to_Pool(name='lora_qkv', offset='(0,3.5,0)', to='(vit_blocks-north)', width=0.9, height=8, depth=8, caption='LoRA QKV'),
    r"""\fill[LoRAColor] (lora_qkv-south) rectangle (lora_qkv-north);""",
    r"""\draw [ultra thick,-Stealth,draw=red,opacity=0.9] (lora_qkv-south) -- (vit_blocks-north);""",

    # Image Embeddings output (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='img_emb', s_filer=256, n_filer=(256,256), offset='(2.5,0,0)', to='(vit_blocks-east)',
                    width=(1.8,1.8), height=34, depth=34, caption='Image Emb'),
    r"""\fill [gray!25, opacity=0.35] (img_emb-south) rectangle (img_emb-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (vit_blocks-east) -- (img_emb-west);""",

    # ===== ROW 2: Decoder Path with LoRA (Prompt path hidden for clarity) =====
    # MaskDecoder (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='decoder', s_filer=256, n_filer=(256,256), offset='(2.5,-3.8,0)', to='(img_emb-south)',
                    width=(4.5,4.5), height=32, depth=32, caption='MaskDecoder'),
    r"""\fill [gray!25, opacity=0.35] (decoder-south) rectangle (decoder-north);""",

    # Connection from Image Emb to Decoder (from center, not south)
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] ($(img_emb-south)!0.5!(img_emb-north)$) -- ($(decoder-north)!0.5!(decoder-south)$);""",

    # LoRA injection in Decoder output projection (positioned well above Decoder, centered for clarity)
    to_Pool(name='lora_decoder', offset='(0,3.5,0)', to='(decoder-north)', width=0.8, height=7, depth=7, caption='LoRA Dec'),
    r"""\fill[LoRAColor] (lora_decoder-south) rectangle (lora_decoder-north);""",
    r"""\draw [ultra thick,-Stealth,draw=red,opacity=0.9] (lora_decoder-south) -- (decoder-north);""",

    # IoU Head (FROZEN - semi-transparent gray overlay)
    to_ConvConvRelu(name='iou_head', s_filer=256, n_filer=(256,256), offset='(2.5,0,0)', to='(decoder-east)',
                    width=(1.8,1.8), height=32, depth=32, caption='IoU Head'),
    r"""\fill [gray!25, opacity=0.35] (iou_head-south) rectangle (iou_head-north);""",
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (decoder-east) -- (iou_head-west);""",

    # Output: Segmentation Masks
    to_ConvSoftMax(name='masks_out', s_filer=256, offset='(2.0,0,0)', to='(iou_head-east)', width=2.0, height=32, depth=32, caption='Output Masks'),
    r"""\draw [ultra thick,-Stealth,draw=black,opacity=0.7] (iou_head-east) -- (masks_out-west);""",

    to_end()
]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(script_dir, '..', 'SUIBE', 'MSA_LoRA')
    os.makedirs(outdir, exist_ok=True)
    pathname = os.path.join(outdir, 'msa_lora_styled.tex')
    to_generate(arch, pathname)


if __name__ == '__main__':
    main()
