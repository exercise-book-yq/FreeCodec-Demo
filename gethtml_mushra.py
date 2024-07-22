from email.mime import base
from jinja2 import FileSystemLoader, Environment

import os
import random

from glob import glob

def get_rows(gtype):
    ret=[]
    # tgts = glob(f'Target/*wav')
    # tgts.sort()
    # # print(tgts)
    # for i, tgt in enumerate(tgts):
        # basename = os.path.basename(tgt)[:-4]

    dacodec_1= 'data/ours'
    dacodec_2 ='data/ours-no_distill'
    dacodec_3 = 'data/ours-spk_vq'
    # supercodec_4 = "data/SuperCodec-6kbps"
    # supercodec_6 = "data/SuperCodec-6kbps"
    encodec_1 = "data/ticodec-500bps"
    encodec_2 = 'data/ticodec-1000bps'
    encodec_3 = 'data/dac-500bps'
    # encodec_4 = 'data/EnCodec-Ours-6kbps'
    encodec_5 = 'data/dac-1000bps'
    # ticodec_1 = 'data/encodec-1500bps'
    # ticodec_2 = 'data/encodec-3000bps'
    # ticodec_3 = 'data/supercodec-1000bps'

    # encodec_6 = 'data/Encodec-6kbps'
    lyra_1 = 'data/lyra-v1'
    lyra_2 = 'data/lyra-v2'
    
    opus_1 = 'data/opus-6k'
    opus_2 = 'data/opus-9k'
    speex ='data/speex'

    wavs = sorted(glob(f'data/target/{gtype}/*.wav'))
    # print(wavs)
    for wav in wavs:
        # print(wav)
        basename = os.path.basename(wav)[:-4]
        print(basename)
        
        # src = os.path.join("data", "wavs", f"{src_basename}.wav")
        tgt = os.path.join("data/target", gtype, f"{basename}.wav")
        
        row = (
                # src_basename,
                basename,
                tgt,
                os.path.join(dacodec_1, gtype, f"{basename}.wav"),
                os.path.join(dacodec_2, gtype, f'{basename}.wav'),
                os.path.join(dacodec_3, gtype, f'{basename}.wav'),
                os.path.join(encodec_1, gtype, f'{basename}.wav'),
                os.path.join(encodec_2, gtype, f'{basename}.wav'),
                os.path.join(encodec_3, gtype, f'{basename}.wav'),
                # os.path.join(encodec_4, gtype, f'{basename}.wav'),
                os.path.join(encodec_5, gtype, f'{basename}.wav'),
                # os.path.join(ticodec_1, gtype, f'{basename}.wav'),
                # os.path.join(ticodec_2, gtype, f'{basename}.wav'),
                # os.path.join(ticodec_3, gtype, f'{basename}.wav'),
                # os.path.join(encodec_6, gtype, f'{basename}.wav'),
                os.path.join(lyra_1, gtype, f'{basename}_decoded.wav'),
                os.path.join(lyra_2, gtype, f'{basename}_decoded.wav'),
                os.path.join(opus_1, gtype, f'{basename}.wav'),
                os.path.join(opus_2, gtype, f'{basename}.wav'),
                os.path.join(speex, gtype, f'{basename}.wav')
        )
        ret.append(row)
    # print(ret[0])
    return ret

def gen_rows_vc(gtype):
    ret = []

    ours = 'vc/ours'
    yourtts = 'vc/yourtts'
    wav2vec_vc = 'vc/wav2vec-vc'

    wavs = sorted(glob(f'vc/ours/{gtype}/*.wav'))

    for wav in wavs:
        basename = os.path.basename(wav)
        src_basename = basename.split('-')[0]
        tgt_basename = basename.split('-')[1][:-4]
        src = os.path.join("vc", f"source/{gtype}", f"{src_basename}.wav")
        tgt = os.path.join("vc", f"target/{gtype}", f"{tgt_basename}.wav")
        row = (
                src_basename,
                tgt_basename,
                src, 
                tgt,
                os.path.join(ours, gtype, f'{src_basename}-{tgt_basename}.wav'),
                os.path.join(yourtts, gtype, f'{src_basename}-{tgt_basename}.wav'),
                os.path.join(wav2vec_vc, gtype, f'{src_basename}-{tgt_basename}.wav')
        )
        ret.append(row)
    return ret



def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("base.html.jinja2")

    rows = get_rows("vctk")

    rows1 = get_rows("test-clean")
    rows2= gen_rows_vc("vctk")
    rows3 = gen_rows_vc("test-clean")
    # print(rows[0])

    html = template.render(
        s2s_rows=rows,
        u2s_rows=rows1,
        vc_s2s_rows=rows2,
        vc_u2s_rows=rows3
    )
    with open("mushra-1.html", "w", encoding="utf-8") as f:
        f.write(html)
    # print(html)

if __name__ == "__main__":
    main()