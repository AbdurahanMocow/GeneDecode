import pandas as pd

def load_23andme(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path, sep="\t", comment="#",
        names=["rsid", "chrom", "pos", "genotype"],
        dtype={"rsid": "string", "chrom": "string", "pos": "Int64", "genotype": "string"}
    )
    df = df.dropna(subset=["rsid", "genotype"]).reset_index(drop=True)
    return df

if __name__ == "__main__":
    inp = "data/sample_23andme.txt"
    out = "outputs/variants_basic.csv"
    df = load_23andme(inp)
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} variants → {out}")