import sys
import os
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

# Custom style overrides (larger labels and repositioning)
custom_style = r"""
% --- custom style overrides for UNet ---
\def\ConvColor{rgb:blue,5;white,3}
\def\PoolColor{rgb:green,4;white,4}
\def\UnpoolColor{rgb:orange,4;white,4}
% ----------------------------------------
""" + "\u005C" + "tikzset{connection/.style={line width=1mm,draw=black,opacity=0.9}}\n" \
           + "\u005C" + "tikzset{every edge quotes/.append style={font=\\large,inner sep=1pt,pos=0.35}}\n" \
           + "\u005C" + "tikzset{depthlabel/.append style={font=\\large,yshift=6pt}}\n" \
           + "\u005C" + "tikzset{captionlabel/.append style={font=\\large,yshift=-8pt}}\n"

arch = [
    to_head('../..'),
    to_cor(),
    to_begin(),
    custom_style,

    # input removed (use neutral/placeholder input or none)

    #block-001
    to_ConvConvRelu( name='ccr_b1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40  ),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.6),
    
    *block_2ConvPool( name='b2', botton='pool_b1', top='pool_b2', s_filer=256, n_filer=128, offset="(1.2,0,0)", size=(32,32,3.5), opacity=0.6 ),
    *block_2ConvPool( name='b3', botton='pool_b2', top='pool_b3', s_filer=128, n_filer=256, offset="(1.2,0,0)", size=(25,25,4.5), opacity=0.6 ),
    *block_2ConvPool( name='b4', botton='pool_b3', top='pool_b4', s_filer=64,  n_filer=512, offset="(1.2,0,0)", size=(16,16,5.5), opacity=0.6 ),

    #Bottleneck
    to_ConvConvRelu( name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2.4,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"  ),
    to_connection( "pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer=64,  n_filer=512, offset="(2.6,0,0)", size=(16,16,5.0), opacity=0.6, compact_labels=True ),
    to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.6,0,0)", size=(25,25,4.5), opacity=0.6, compact_labels=True ),
    to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.6,0,0)", size=(32,32,3.5), opacity=0.6, compact_labels=True ),
    to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    *block_Unconv( name="b9", botton="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.6,0,0)", size=(40,40,2.5), opacity=0.6, compact_labels=True ),
    to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),
    
    to_ConvSoftMax( name="soft1", s_filer=2, offset="(1.8,0,0)", to="(end_b9-east)", width=1.5, height=40, depth=40, caption="Softmax" ),
    to_connection( "end_b9", "soft1"),
     
    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    outdir = os.path.join('..', 'SUIBE', 'unet')
    os.makedirs(outdir, exist_ok=True)
    pathname = os.path.join(outdir, namefile + '.tex')
    to_generate(arch, pathname )

if __name__ == '__main__':
    main()
