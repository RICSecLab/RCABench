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
    # 0x000055555555eb84 -- rdx min_reg_val_less 0x5555555f1740 -- 0.9949575371549894 -- add rdx, rax (path rank: 0.8621912170574705) //t2p_readwrite_pdf_image_tile at tiff2pdf.c:2911

    # ref
    # https://github.com/RUB-SysSec/aurora/blob/master/root_cause_analysis/root_cause_analysis/src/addr2line.rs
    # Aurora shows only basenames.
    # Aurora calls addr2line with "-e {} -a 0x{:x} -f -C -s -i -p".

    loc_ranking = [r.split("//")[-1].split()[2] for r in ranking\
            if (not "inlined by" in r) and ("at" in r.split("//")[-1])]
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

        ranking = [l for l in fres.readlines() if " -- " in l]

        res_loc_dup, res_loc_uniq = check_locations(ranking, fpredef.readlines())

        loc_dup = " {}".format(res_loc_dup if res_loc_dup is not None else "")
        loc_uniq = " {}".format(res_loc_uniq if res_loc_uniq is not None else "")

        print("loc_uniq:{}".format(loc_uniq))
        print("loc_dup:{}".format(loc_dup))
