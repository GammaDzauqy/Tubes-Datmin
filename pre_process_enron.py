import pandas as pd
import os
import re

# Nama file CSV yang Anda download dari Kaggle
input_csv = 'emails.csv' 
output_folder = 'data'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def parse_email(raw_message):
    """Memisahkan Subject dan Body dari format email mentah Enron."""
    # Mencari baris Subject
    subject_match = re.search(r"Subject: (.*)", raw_message)
    subject = subject_match.group(1).strip() if subject_match else "No Subject"
    
    # Menghapus header (Body biasanya muncul setelah baris 'X-FileName')
    parts = re.split(r"X-FileName: .*\n", raw_message)
    body = parts[1].strip() if len(parts) > 1 else raw_message
    return subject, body

print("Sedang memproses dokumen... Harap tunggu.")

try:
    # Membaca hanya sedikit baris agar cepat karena file asli sangat besar
    reader = pd.read_csv(input_csv, chunksize=100)
    df_chunk = next(reader)
    
    count = 0
    for index, row in df_chunk.iterrows():
        subject, body = parse_email(row['message'])
        
        # Validasi: Pastikan isi email cukup panjang untuk diringkas (CPMK 6)
        if len(body.split()) < 30: 
            continue
            
        filename = f"{output_folder}/arsip_{count+1}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            # Format: Baris pertama perihal, baris berikutnya isi
            f.write(f"PERIHAL: {subject}\n\n{body}")
        
        count += 1
        if count == 30: # Batas minimal sesuai ketentuan tugas
            break

    print(f"Selesai! {count} file .txt telah dibuat di folder '{output_folder}'.")

except FileNotFoundError:
    print(f"Error: File '{input_csv}' tidak ditemukan. Pastikan file CSV ada di folder yang sama.")