from pathlib import Path
import yaml
from parsers.parse_23andme import load_23andme
from annotators.ensembl_variation import annotate_rsids

def ensure_dirs(*paths: str) -> None:
    for p in paths:
        Path(p).parent.mkdir(parents=True, exist_ok=True)

def run_from_config(cfg_path: str) -> None:
    cfg = yaml.safe_load(Path(cfg_path).read_text(encoding="utf-8"))

    inp_file = cfg["input"]["file"]
    parsed_csv = cfg["output"]["parsed_csv"]
    annotated_csv = cfg["output"]["annotated_csv"]
    ann_cfg = cfg["annotator"]

    print(f"→ Loading: {inp_file}")
    df = load_23andme(inp_file)
    print(f"   Loaded {len(df):,} variants")

    ensure_dirs(parsed_csv)
    df.to_csv(parsed_csv, index=False)
    print(f"✓ Saved parsed CSV → {parsed_csv}")

    print("→ Annotating variants (Ensembl API)...")
    df_ann = annotate_rsids(
        df,
        cache_file=ann_cfg["cache_file"],
        limit=ann_cfg["limit"],
        requests_per_sec=ann_cfg["requests_per_sec"]
    )
    ensure_dirs(annotated_csv)
    df_ann.to_csv(annotated_csv, index=False)
    print(f"✓ Annotated CSV saved → {annotated_csv}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", "-c", required=True)
    args = ap.parse_args()
    run_from_config(args.config)
    