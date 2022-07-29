# Face Recognition

## Description
Program ini dirancang untuk dijalankan pada perangkat Raspberry Pi karena membutuhkan pin GPIO untuk mengatur motor servo. Jika program dijalankan pada perangkat laptop atau PC maka ada beberapa perubahan pada program untuk menjalankan motor servo. Sebelum memulai program, ada beberapa hal yang perlu disiapkan yaitu: 
1. Library yang digunakan
2. Folder penyimpanan 
3. Database menggunakan MySQL 
4. Mengatur penggunaan perangkat keras (kamera dan motor servo)

## 1. Library yang digunakan
Untuk menjalankan program ini diperlukan beberapa library yang digunakan seperti OpenCV, Numpy, dan mysql.connector. Penginstallan library dilakukan pada CMD (Command Prompt) atau terminal di komputermu.
- Cara install OpenCV pada perangkat windows anda.  
```bash
python3 -m pip install opencv-contrib-python
```
- Cara install Numpy

## 2. Folder Penyimpanan
Kalian harus membuat 3 folder dengan nama 'Data Wajah', 'latih wajah' dan 'Data Wajah Tamu'. (nama folder harus sama percis)
Untuk folder 'Data Wajah Tamu' disimpan didalam folder 'Data Tamu'. 

## 2. Database Menggunakan MySQL


