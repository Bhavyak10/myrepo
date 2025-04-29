# app.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import ProgrammingError

# -------- 1. DATABASE CONNECTION --------
# (escape the @ in your password as %40)
DATABASE_URL = "postgresql://postgres:Bhav%40postgres10@localhost:5432/dmql_project"
engine = create_engine(DATABASE_URL)

# -------- 2. PAGE LAYOUT & TABLE LISTING --------
st.set_page_config(page_title="SQL Explorer", layout="wide")
st.title("Crime Database SQL Explorer")

# fetch all table names from the database and show in sidebar
inspector = inspect(engine)
tables = inspector.get_table_names()
st.sidebar.header("Tables in schema")
table_choice = st.sidebar.selectbox("Pick a table to browse", tables)

# give a quick “starter” query
default_query = f"SELECT *\nFROM {table_choice}\nLIMIT 100;"

# -------- 3. QUERY INPUT & EXECUTION --------
st.markdown("### Enter your SQL query:")
sql = st.text_area("SQL", value=default_query, height=150)

if st.button("Run query"):
    try:
        # run the query and cache it for speed
        @st.cache_data(show_spinner=False)
        def run_sql(q):
            return pd.read_sql(q, engine)
        df = run_sql(sql)
        st.success(f"Returned {len(df)} rows.")
        st.dataframe(df, use_container_width=True)

    except ProgrammingError as e:
        st.error(f"SQL Error: {e.orig.pgerror}")
    except Exception as e:
        st.error(f"Error: {e}")

# -------- 4. OPTIONAL: Show query plan --------
if st.checkbox("Show EXPLAIN query plan"):
    try:
        plan = pd.read_sql(f"EXPLAIN {sql}", engine)
        st.subheader("Query Plan:")
        st.text(plan.to_string(index=False, header=False))
    except Exception:
        st.warning("Could not generate EXPLAIN plan for that query.")

