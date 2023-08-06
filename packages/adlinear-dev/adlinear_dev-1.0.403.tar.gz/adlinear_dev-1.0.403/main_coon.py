# import itertools
# import os
import argparse
from transparentpath import Path
import numpy as np
import pandas as pd
from adlinear import nmfmodel as nmf
from randomgenerators import randomgenerators as rng
import dotenv

local_main_coon = True
if local_main_coon:
    Path.set_global_fs("local")
else:
    Path.set_global_fs("gcs", bucket="nmf_experiments_dev", token="cred_gcs.json")
dotenv.load_dotenv()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Creates the yaml file to launch several iterations of a program on GCP",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-o", "--output", type=str, default="wfold_scree_plots.csv", help="Output file path")
    parser.add_argument("-r", "--runs", type=int, default=1, help="Number of iterations per node")
    parser.add_argument("-w", "--writefreq", type=int, default=1, help="Write frequency")
    parser.add_argument("-e", "--epsilon", type=float, default=0.10, help="Epsilon")
    parser.add_argument("-m", "--ncmin", type=int, default=2, help="Minimum number of components")
    parser.add_argument("-M", "--ncmax", type=int, default=45, help="Maximum number of components")
    parser.add_argument("-W", "--w_ncr", type=int, default=0, help="Ratio of #W-clusters to #components")
    parser.add_argument("-H", "--h_ncr", type=int, default=1, help="Ratio of #H-clusters to #components")
    # parser.add_argument("-a", "--wclust_f", type=float, default=1.0, help="#W clusters to #H clusters maximum ratio")
    parser.add_argument("-i", "--icorrmin", type=float, default=0.5, help="Minimum intra-cluster correlation")
    parser.add_argument("-I", "--icorrmax", type=float, default=0.95, help="Maximum intra-cluster correlation")
    parser.add_argument("-x", "--xcorrmin", type=float, default=0.0, help="Minimum extra-cluster correlation")
    parser.add_argument("-X", "--xcorrmax", type=float, default=0.5, help="Maximum extra-cluster correlation")
    parser.add_argument("-p", "--do_entropy", type=bool, default=False, help="Optional entropy calculation")
    args = parser.parse_args()
    outputpath = Path(args.output)
    epsilon = args.epsilon
    ncmin = args.ncmin
    ncmax = args.ncmax
    nruns = args.runs
    # wclust_f = args.wclust_f
    w_ncr = args.w_ncr
    h_ncr = args.h_ncr
    do_ent = args.do_entropy
    icorrmin = args.icorrmin
    icorrmax = args.icorrmax
    xcorrmin = args.xcorrmin
    xcorrmax = args.xcorrmax
    writefreq = args.writefreq

    print(f"Will execute {nruns} run(s), will write output(s) in {outputpath} every {writefreq} iteration(s)")

    rand_norms = True
    df_mini_scree_plots = pd.DataFrame(index=[], columns=[])
    for itrial in range(nruns):
        n_comp = np.random.randint(low=ncmin, high=ncmax)
        # intra_corr = np.random.uniform(low=icorrmin, high=icorrmax)
        # xtra_corr = np.random.uniform(low=xcorrmin, high=xcorrmax)
        h_size = np.random.randint(low=max(n_comp, 10), high=1000)
        w_size = np.random.randint(low=max(n_comp, int(h_size / 5.0)), high=5 * h_size)
        h_nc = int(h_ncr * n_comp)
        w_nc = int(w_ncr * n_comp)

        eps = np.random.uniform(low=0.0, high=epsilon)
        # noinspection PyTupleAssignmentBalance
        generated_M, _, _, _ = rng.generate_nmf_reconstruction(n_comp=n_comp, n_feat=h_size, n_obs=w_size,
                                                               h_icorr_min=icorrmin, h_xcorr_max=xcorrmax,
                                                               w_icorr_min=xcorrmin, w_xcorr_max=icorrmax,
                                                               random_norms=rand_norms, epsilon=eps, n_clust_w=w_nc,
                                                               n_clust_h=h_nc)
        rnstr = "RandNorms" if rand_norms else "ConstNorms"

        df_scree_plot = nmf.generate_scree_plot(generated_M, ncmin=ncmin, ncmax=ncmax, known_ncomp=n_comp,
                                                do_entropies=do_ent, do_stabilities=False)
        df_mini_scree_plots = nmf.collect_windows_from_scree_plot(df_collected_windows=df_mini_scree_plots,
                                                                  df_scree_plot=df_scree_plot, known_ncomp=n_comp,
                                                                  ncomp_margin=5)

        if itrial % writefreq == 0 or itrial == nruns-1:
            print(f"Saving iteration {itrial} in {outputpath}")
            # assert not df_mini_scree_plots.empty
            outputpath.write(df_mini_scree_plots)
            assert outputpath.isfile()
            assert not outputpath.read().empty
