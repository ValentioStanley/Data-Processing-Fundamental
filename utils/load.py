from sqlalchemy import create_engine
 
def store_to_postgre(data, db_url, tablename, schema):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL."""
    try:
        # Membuat engine database
        engine = create_engine(db_url)
        with engine.connect() as con:
            data.to_sql(tablename, schema=schema, con=con, if_exists='append', index=False)
            print("Database Message: Berhasil menambahkan data ke database!")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")