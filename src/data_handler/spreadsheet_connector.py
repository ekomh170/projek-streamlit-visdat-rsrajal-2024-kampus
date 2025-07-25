import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from urllib.parse import urlparse, parse_qs
import json
import io

# Fungsi untuk menghubungkan dan mengambil data dari Google Spreadsheet

def extract_sheet_id(sheet_url):
    """
    Ekstrak sheet ID dari URL Google Spreadsheet.
    """
    parsed = urlparse(sheet_url)
    path_parts = parsed.path.split('/')
    if 'd' in path_parts:
        idx = path_parts.index('d')
        return path_parts[idx+1]
    return None

def load_sheet_data(sheet_url, worksheet_name, creds_path='credentials.json'):
    """
    Mengambil data dari Google Spreadsheet dan mengembalikan DataFrame pandas.
    sheet_url: URL share Google Spreadsheet
    worksheet_name: Nama worksheet/tab yang ingin diambil
    creds_path: Path ke file credentials.json atau string JSON (dari st.secrets)
    """
    # Scope untuk Google Sheets dan Drive
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    # Jika creds_path adalah string JSON (bukan path file), load dari string
    if isinstance(creds_path, str) and creds_path.strip().startswith('{'):
        creds_dict = json.loads(creds_path)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet_id = extract_sheet_id(sheet_url)
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(worksheet_name)
    # Ambil semua data dari worksheet
    data = worksheet.get_all_values()
    # Ambil header dari baris ke-14 (indeks 13)
    header = data[13]
    rows = data[14:]  # Ambil semua data setelah header
    df = pd.DataFrame(rows, columns=header)
    # Anonimkan Nama Pasien
    def shorten_name(name):
        if not name:
            return ""
        return name.strip()[:4]
    if 'Nama Pasien' in df.columns:
        df['Nama Pasien'] = df['Nama Pasien'].apply(shorten_name)
        df.insert(df.columns.get_loc('Nama Pasien') + 1, 'Status Nama Pasien', '✅ Teranonimkan')
    if 'Petugas' in df.columns:
        df['Petugas'] = df['Petugas'].apply(shorten_name)
        df.insert(df.columns.get_loc('Petugas') + 1, 'Status Petugas', '✅ Teranonimkan')
    # Hapus kolom tanpa nama (header kosong)
    df = df.loc[:, ~df.columns.str.match('^Unnamed|^$')]
    # Hapus baris yang seluruhnya kosong
    df = df.dropna(how='all')
    return df

# Fungsi untuk cek koneksi Google Spreadsheet (gspread)
def cek_koneksi_gspread(creds_path='credentials.json'):
    """
    Mengecek koneksi ke Google Spreadsheet menggunakan gspread dan service account.
    Mengembalikan status koneksi (True/False) dan pesan.
    creds_path: Path ke file credentials.json atau string JSON (dari st.secrets)
    """
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    try:
        if isinstance(creds_path, str) and creds_path.strip().startswith('{'):
            creds_dict = json.loads(creds_path)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        # Test: ambil daftar spreadsheet (atau spreadsheet dummy)
        _ = client.openall()
        return True, "Koneksi ke Google Spreadsheet berhasil!"
    except Exception as e:
        return False, f"Gagal koneksi ke Google Spreadsheet: {e}"

# Contoh penggunaan fungsi koneksi Google Spreadsheet
if __name__ == "__main__":
    sheet_url = "https://docs.google.com/spreadsheets/d/1Uqg-6Zp64VCv9_1b4soV9KSkRL0WkMjbcxmXWnVxpYA/edit?usp=sharing"
    worksheet_name = "Januari"
    df = load_sheet_data(sheet_url, worksheet_name)
    print(df.head())
