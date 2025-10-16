from pathlib import Path
import pandas as pd

def load_23andme(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")

    df = pd.read_csv(
        p,
        sep="\t",
        comment="#",
        names=["rsid", "chrom", "pos", "genotype"],
        dtype={"rsid": "string", "chrom": "string", "pos": "Int64", "genotype": "string"},
        engine="python",
    )

    df = df.dropna(subset=["rsid"]).reset_index(drop=True)
    return df
