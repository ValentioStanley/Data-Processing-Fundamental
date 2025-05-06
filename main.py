from utils.extract import scrape_product
from utils.load import store_to_postgre
from utils.transform import transform_data

def main():
    """Fungsi utama untuk keseluruhan proses scraping, transformasi data, dan penyimpanan."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/'
    
    # Menjalankan scraping untuk mengambil data produk
    all_products_data = scrape_product(BASE_URL)
    
    # Jika data berhasil diambil, lakukan transformasi dan simpan ke PostgreSQL
    if all_products_data:
        # Mentransformasikan data (misalnya konversi mata uang, rating, dll)
        DataFrame = transform_data(all_products_data, 16000)  # Anggap 20000 adalah nilai tukar yang diperlukan
        print(DataFrame)
        print(DataFrame.dtypes)
        # try:
        #     # Mengubah data menjadi DataFrame
        #     DataFrame = transform_to_DataFrame(all_products_data)
            
        #     # Mentransformasikan data (misalnya konversi mata uang, rating, dll)
        #     DataFrame = transform_data(DataFrame, 16000)  # Anggap 20000 adalah nilai tukar yang diperlukan
        #     print(DataFrame)
            
        #     # Menyimpan data ke PostgreSQL
        #     db_url = 'postgresql+psycopg2://developer:developer@localhost:5432/fashionst'
        #     store_to_postgre(DataFrame, db_url)  # Memanggil fungsi untuk menyimpan ke database
        #     DataFrame.to_csv('products.csv', index=False)
        # except Exception as e:
        #     print(f"Terjadi kesalahan dalam proses: {e}")
    else:
        print("Tidak ada data yang ditemukan.")
 
if __name__ == '__main__':
    main()