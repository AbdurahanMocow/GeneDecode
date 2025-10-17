# scripts/run_23andme.py
"""
One-command runner for 23andMe files.
Usage:
  python scripts/run_23andme.py --file data/raw/<your_file>.txt --limit 1000
"""

import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd

from scripts.parsers.parse_23andme import load_23andme
from scripts.annotators.ensembl_variation import annotate_variants


def main():
    ap = argparse.ArgumentParser(description="Process a 23andMe raw data file.")
    ap.add_argument("--file", required=True, help="Path to 23andMe raw text file")
    ap.add_argument("--limit", type=int, default=-1,
                    help="Rows to annotate (-1 = all; use 1000 for quick test)")
    ap.add_argument("--rps", type=int, default=10, help="Requests/sec to Ensembl")
    ap.add_argument("--cache", default="cache/ensembl_variation_cache.json",
                    help="Path to JSON cache file")
    args = ap.parse_args()

    in_path = Path(args.file)
    assert in_path.exists(), f"Input not found: {in_path}"

    # Make output dirs
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    Path("cache").mkdir(exist_ok=True)

    # Timestamped basenames so you can keep multiple runs
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    basic_csv = processed_dir / f"23andme_variants_basic_{stamp}.csv"
    annotated_csv = processed_dir / f"23andme_variants_annotated_{stamp}.csv"

    print(f"Loading: {in_path}")
    df = load_23andme(str(in_path))
    print(f"Loaded {len(df):,} variants")

    # Save parsed/basic
    df.to_csv(basic_csv, index=False)
    print(f"Saved basic CSV → {basic_csv}")

    # Optionally limit rows for speed
    df_to_annotate = df if args.limit in (-1, None) else df.head(args.limit)

    print("Annotating with Ensembl…")
    annotated = annotate_variants(
        df_to_annotate,
        cache_file=args.cache,
        requests_per_sec=args.rps
    )

    # Merge back to full set if we limited (keep unannotated rows too)
    if len(df_to_annotate) < len(df):
        annotated = pd.concat([
            annotated,
            df.iloc[len(df_to_annotate):].assign(
                gene=pd.NA, consequence=pd.NA, info=pd.NA
            )
        ], ignore_index=True)

    annotated.to_csv(annotated_csv, index=False)
    print(f"Saved annotated CSV → {annotated_csv}")
    print("Done ✅")


if __name__ == "__main__":
    main()
    