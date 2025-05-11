import pandas as pd
 
def transform_data(data, exchange_rate):
    """Mengubah data menjadi DataFrame."""
    df = pd.DataFrame(data)
    
    """Menghapus data invalid """
    if ((df["Title"] == "Unknown Product") | (df["Rating"] == "Invalid Rating") | (df['Price'] == "Price Unavailable")).any():
        df.drop(df[(df["Title"] == "Unknown Product") | (df["Rating"] == "Invalid Rating") | (df['Price'] == "Price Unavailable")].index, inplace=True)
    
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    # Transformasi Tipe Data
    df['Title'] = df['Title']
    # df['Price_in_dollars'] = df['Price'].str.replace(r"\[\.*?\]", "", regex=True).astype(float)
    # df['Price_in_dollars'] = df['Price'].astype("string").str.replace(r"[$", "").str.replace(r"]","").astype(float)
    df['Price'] = df['Price'].str.replace(r"$", "", regex=False).astype(float)
    df['Price_in_dollars'] = df['Price']
    df['Rating'] = df['Rating'].replace("Rating: ⭐", "", regex=True).str.strip()
    df['Rating'] = df['Rating'].replace("/ 5", "", regex=True).str.strip().astype(float)
    df['Number_Color'] = df['Number_Color'].replace("Colors", "", regex=True).str.strip().astype(int)
    df['Size'] = df['Size'].replace("Size:", "", regex=True).str.strip()
    df['Gender'] = df['Gender'].replace("Gender:", "", regex=True).str.strip()
    
    # Transformasi Exchange Rate
    df['Price_in_rupiah'] = (df['Price_in_dollars'] * exchange_rate).astype(int)
    
    # Menghapus duplikat
    df = df.drop_duplicates()
    
    # Menggulang reset index biar rapih
    df = df.reset_index(drop=True)
    
    return df