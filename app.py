import io
import pandas as pd
import streamlit as st

from scripts.parsers.parse_23andme import load_23andme
from scripts.annotators.ensembl_variation import annotate_variants

st.set_page_config(page_title="GeneDecode – 23andMe Demo", layout="wide")
st.title("GeneDecode • 23andMe Demo")
st.caption("Upload a 23andMe raw text file → parse → quick Ensembl annotation preview")

uploaded = st.file_uploader("Upload 23andMe raw file (.txt)", type=["txt"])
limit = st.slider("Annotate first N variants (for speed)", min_value=100, max_value=5000, value=1000, step=100)

if uploaded is not None:
    # Read as bytes and load via parser
    bytes_data = uploaded.read()
    df = load_23andme(io.BytesIO(bytes_data))
    st.success(f"Loaded {len(df):,} variants from {uploaded.name}")
    st.write(df.head())

    if st.button("Annotate preview"):
        ann = annotate_variants(
            df=df,
            cache_file="cache/ensembl_variation_cache.json",
            limit=limit,
            requests_per_sec=10.0
        )
        st.info("Preview of annotated variants")
        st.dataframe(ann.head(50))
        # Simple summary
        n_clin = (ann["clinical_significance"].fillna("") != "").sum()
        st.metric("Variants with clinical significance (preview set)", f"{n_clin:,}")
        