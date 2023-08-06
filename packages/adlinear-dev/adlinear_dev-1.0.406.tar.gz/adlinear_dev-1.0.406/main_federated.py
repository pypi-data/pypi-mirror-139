import pandas as pd

from adlinear import fed_nmtf as fd
from adlinear import utilities as utl
import root_path
from transparentpath import Path
import os
import dotenv
from adlinear import nmfmodel as nmf

dotenv.load_dotenv()

if __name__ == "__main__":

    # Data localization
    rootpath = root_path.get_root_path()

    rd_path = Path(rootpath / os.getenv("rd_subpath"), fs="local")
    federated_path: object = Path(rd_path / os.getenv("federated_subpath"), fs="local")

    data_path: object = Path(federated_path / os.getenv("data_subpath"), fs="local")

    temp_data_path = Path(data_path / "temp_data/", fs="local")
    pictures_path = Path(data_path / "Pics", fs="local")
    out_data_path = Path(federated_path / "results/", fs="local")

    res_path = Path(federated_path / os.getenv("results_subpath"), fs="local")

    if os.getenv("fed_do_epithor", "False").lower() == "true":

        epithor_filename: str = os.getenv("fed_epithor_filename")
        df_epithor: pd.DataFrame = Path(data_path / epithor_filename, fs="local").read()
        df_epithor.drop(columns=df_epithor.columns[0:4], inplace=True)
        df_epithor.drop(labels=['Code', 'Suivi', 'Annee'], axis='columns', inplace=True)
        df_dense, _ = utl.drop_sparse_columns(df_epithor, minimum_fill_rate=0.8)
        df_epi_normalized, df_epi_means, df_epistdevs = utl.normalize_by_columns(df_dense, make_positive=True)
        df_n_lines = len(df_dense.index)
        epithor_nb_feat = len(df_dense.columns)
        epithor_ncomp = 10

        # initialisation
        global_model = nmf.NmfModel(df_epi_normalized, epithor_ncomp)
        global_h: pd.DataFrame = global_model.get_h()
        print(f"Erreur globale de la factorisation a {epithor_ncomp} composants: {global_model.get_precision()}")
        # centralizer
        centralizer: fd.NMFCentralizer = fd.NMFCentralizer(nfeat=epithor_nb_feat)
        centralizer.set_ncomp(ncomp=epithor_ncomp)
        # clients
        nb_clients: int = int(os.getenv("fed_nb_clients", 5))
        df_slice: int = int(df_n_lines / nb_clients)
        # création des clients
        clients = [fd.NMFClient(name="") for _ in range(nb_clients)]
        clt_names = []
        # attribution des données aux clients
        for icl, client in enumerate(clients):
            client.set_data(df_epi_normalized.iloc[int(icl * df_slice): int((icl+1) * df_slice), :])
        # config
        fed_config: fd.FederatedNMFConfig = fd.FederatedNMFConfig(nmfcentral=centralizer,
                                                                  clients=clients)
        fed_config.set_client_names([])

        fed_config.set_ncomp(epithor_ncomp)
        fed_config.set_features(df_epi_normalized.columns)
        # for _ in range(10):
        #     fed_config.request_full_round()

        fed_config.reset_counters()
        fed_config.get_central().set_h_guess(global_h)
        for _ in range(5):
            fed_config.request_full_round()
        fed_config.get_perf_log().loc["Error before"].plot()
        pass