import argparse

def uniq(ls):
    # preserve order
    new = []
    for l in ls:
        if not l in new:
            new.append(l)
    return new

def check_locations(ranking, locs):
    # Sample
    # [10-Jan-23 10:07:38-init_log-INFO]: Output Folder: /workdir/4h//output/output_1673330852
    # [10-Jan-23 10:07:45-count_all-INFO]: #reports: 3818 (#malicious: 1270; #benign: 2548)
    # [10-Jan-23 10:07:47-show-INFO]: [INSN-0] 0x000000000040930f -> tiff2pdf.c:2913 (l2norm: 1.414214; normalized(N): 1.000000; normalized(S): 1.000000)
    # [10-Jan-23 10:07:47-show-INFO]: [INSN-1] 0x00000000004630fa -> tif_read.c:767 (l2norm: 1.414214; normalized(N): 1.000000; normalized(S): 1.000000)

    # ref
    # https://github.com/VulnLoc/VulnLoc/blob/e1f607abea71db0eb57b41684f3dfae0ecee4321/code/patchloc.py#L180
    # https://github.com/VulnLoc/VulnLoc/blob/e1f607abea71db0eb57b41684f3dfae0ecee4321/code/patchloc.py#L227

    # TODO: better matching
    loc_ranking = [r.split()[5] for r in ranking]
    loc_ranking_uniq = uniq(loc_ranking)

    r = None
    ru = None
    for loc in locs:
        loc = loc.replace("\n","")
        if not loc in loc_ranking:
            continue

        i = loc_ranking.index(loc)
        if r is None or i < r:
            r = i

        j = loc_ranking_uniq.index(loc)
        if ru is None or j < ru:
            ru = j

    if r is None:
        return None, None

    return (r+1, ru+1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('results')
    parser.add_argument('rc_dir')
    args = parser.parse_args()

    with open(args.results) as fres,\
        open(args.rc_dir + "/locations") as fpredef:

        ranking = [l for l in fres.readlines() if "show-INFO" in l]

        res_loc_dup, res_loc_uniq = check_locations(ranking, fpredef.readlines())

        loc_dup = " {}".format(res_loc_dup if res_loc_dup is not None else "")
        loc_uniq = " {}".format(res_loc_uniq if res_loc_uniq is not None else "")

        print("loc_uniq:{}".format(loc_uniq))
        print("loc_dup:{}".format(loc_dup))
