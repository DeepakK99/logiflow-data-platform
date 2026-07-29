"""Quickly query the data using duckdb"""

import duckdb

con = duckdb.connect()

con.install_extension("delta")
con.load_extension("delta")

con.sql("""
SELECT *
FROM delta_scan('data/bronze/master/carriers')
""").show()