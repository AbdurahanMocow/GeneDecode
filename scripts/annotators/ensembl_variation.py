from __future__ import annotations
from pathlib import Path
import json, time
from typing import Dict, List
import requests
import pandas as pd
from tqdm import tqdm

ENSEMBL_VAR_URL = "https://rest.ensembl.org/variation/homo_sapiens/{rsid}?content-type=application/json"

def _load_cache(cache_file: Path) -> Dict[str, dict]:
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save_cache(cache: Dict[str, dict], cache_file: Path) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(cache), encoding="utf-8")

def annotate_rsids(
    df: pd.DataFrame,
    cache_file: str,
    limit: int = -1,
    requests_per_sec: float = 10.0,
) -> pd.DataFrame:
    cache_path = Path(cache_file)
    cache = _load_cache(cache_path)

    rsids: List[str] = df["rsid"].astype(str).tolist()
    if limit and limit > 0:
        rsids = rsids[:limit]

    out_rows = []
    delay = 1.0 / max(requests_per_sec, 0.1)

    for rs in tqdm(rsids, desc="Annotating (Ensembl)", unit="rsid"):
        data = cache.get(rs)
        if data is None:
            try:
                resp = requests.get(ENSEMBL_VAR_URL.format(rsid=rs), timeout=10)
                data = resp.json() if resp.status_code == 200 else {"_error": f"http {resp.status_code}"}
            except Exception as e:
                data = {"_error": f"{type(e).__name__}"}
            cache[rs] = data
            time.sleep(delay)

        genes, clin = [], []
        try:
            for s in data.get("synonyms", []):
                genes.append(s)
            for c in data.get("clinical_significance", []):
                clin.append(c)
        except Exception:
            pass

        out_rows.append({
            "rsid": rs,
            "genes": ",".join(sorted(set(genes))),
            "clinical_significance": ",".join(sorted(set(clin)))
        })

    _save_cache(cache, cache_path)
    ann = pd.DataFrame(out_rows)
    merged = df.merge(ann, on="rsid", how="left")
    return merged
# ---- compatibility alias for pipeline ----
def annotate_variants(
    df: pd.DataFrame,
    cache_file: str = "cache/ensembl_variation_cache.json",
    limit: int = -1,
    requests_per_sec: float = 10.0,
) -> pd.DataFrame:
    """
    Wrapper to make annotate_rsids() compatible with run_23andme.py
    """
    return annotate_rsids(
        df=df,
        cache_file=cache_file,
        limit=limit,
        requests_per_sec=requests_per_sec,
    )