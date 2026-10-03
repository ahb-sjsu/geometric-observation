import json, math, numpy as np
SYN = {'Gauss8', 'Gauss8-s12'}; DEG = {'GaussCoupled', 'GaussCoupled-s11'}
rows = [r for r in json.load(open('s2noise_measured_corrected.json')) if r['dataset'] not in DEG]
groups = (('control (Gauss8)', lambda r: r['dataset'] in SYN),
          ('real, column views', lambda r: r['dataset'] not in SYN and not (r['view'].startswith('mix') or r['view'] == 'orth')),
          ('real, rotated views', lambda r: r['dataset'] not in SYN and (r['view'].startswith('mix') or r['view'] == 'orth')))
for lab, sel in groups:
    rs = [r for r in rows if sel(r)]
    pred = np.array([r['pred_removed'] for r in rs]); mean = np.array([r['mean_rep'] for r in rs])
    sem = np.array([r['sd_rep'] for r in rs]) / math.sqrt(20)
    print(f"{lab:20s} n={len(rs):2d} median pred {np.median(pred):.4f} median mean {np.median(mean):+.4f} "
          f"median shortfall {np.median(pred - mean):+.4f}; |mean-pred| > 3 SE in {np.mean(np.abs(mean - pred) > 3 * sem):.0%}")
