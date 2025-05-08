from utils.extract import scrape_product
from utils.load import store_to_postgre
from utils.transform import transform_data
from utils.spreadsheet import insertToSpreadsheet

def main():
    """Fungsi utama untuk keseluruhan proses scraping, transformasi data, dan penyimpanan."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/'
    
    all_products_data = scrape_product(BASE_URL)
    
    if all_products_data:

        try:
            # Transformasi data (misalnya konversi mata uang, rating, dll)
            df = transform_data(all_products_data, 16000)  
            print(df)
            print(df.dtypes)
            
             # Convert kolom timestamp dari date ke string agar bisa menampung ke JSON untuk diinsert ke spreadsheet
            df['Timestamp'] = df['Timestamp'].astype('string')
            
            # Menyimpan data ke PostgreSQL
            db_url = 'xxx' # Disamarkan dulu karena sensitif untuk sharing
            tablename = 'products'
            schema = 'public'
            store_to_postgre(df, db_url, tablename, schema)
            
            df.to_csv('products.csv', index=False) # Export to CSV langsung ke dalam workplace ini
            insertToSpreadsheet([df.columns.values.tolist()] + df.values.tolist()) # Menyimpan data ke spreadsheet
            
        except Exception as e:
            print(f"Terjadi kesalahan dalam proses: {e}")
    else:
        print("Tidak ada data yang ditemukan.")
 
if __name__ == '__main__':
    main()