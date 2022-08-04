# Face Recognition

## Description
Program ini dirancang untuk dijalankan pada perangkat Raspberry Pi karena membutuhkan pin GPIO untuk mengatur motor servo. Jika program dijalankan pada perangkat laptop atau PC maka ada beberapa perubahan pada program untuk menjalankan motor servo. Sebelum memulai program, ada beberapa hal yang perlu disiapkan yaitu: 
1. Library yang digunakan
2. Folder penyimpanan 
3. Database menggunakan MySQL 
4. Mengatur penggunaan perangkat keras (kamera)

## 1. Library yang digunakan
Untuk menjalankan program ini diperlukan beberapa library yang digunakan seperti OpenCV, Numpy, dan mysql.connector. Penginstallan library dilakukan pada CMD (Command Prompt) atau terminal di komputermu.
- Cara install OpenCV pada perangkat windows anda.  
```bash
python3 -m pip install opencv-contrib-python
```
- Cara install Numpy
```bash
python -m pip install numpy
```
- Cara install library database
```bash
pip install mysql-connector-python
```

## 2. Folder Penyimpanan
Kalian harus membuat 3 folder dengan nama 'Data Wajah', 'latih wajah' dan 'Data Wajah Tamu'. (nama folder harus sama percis)
Untuk folder 'Data Wajah Tamu' disimpan didalam folder 'Data Tamu'. 

## 3. Database Menggunakan MySQL
Database yang digunakan pada sistem ini menggunakan MySQL. Sebelum menyambungkan sistem dengan database, kita perlu membuat kerangka dari database nya itu sendiri. 
Saya membuat dua database yaitu database warga dan juga database tamu, dimana database warga untuk menyimpan data warga yang didaftarkan kedalam sistem dan database tamu berguna untuk menyimpan data tamu yang berkunjung. 
Untuk database warga saya beri nama 'data_warga' yang berisi tabel bernama 'register_warga', sedangkan untuk database tamu saya beri nama 'data_tamu' yang berisi tabel bernama 'register_tamu'.  
Anda dapat mengatur beberapa hal seperti host,user dan database yang akan digunakan pada perintah dibawah ini. 
```bash
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="191200",
        database="data_tamu"
    )
    insertdt = mydb.cursor()
    insert_tamu = "insert into register_tamu(id,nama,nik,alamat) " \
                   "value('"+e_id.get()+"','"+e_nama.get()+"','"+e_nik.get()+"','"+e_alamat.get()+"')"
    insertdt.execute(insert_tamu)
    mydb.commit()
    mydb.close()
```
## 4. Mengatur Penggunaan Perangkat Keras (Kamera) 
Setelah sistem sudah siap, langkah terahir mengatur penggunaan perangkat keras seperti kamera dan motor servo.
- Pengaturan penggunaan kamera. 
```bash
cam = cv2.VideoCapture(0)
```
Index dari kamera akan berbeda tergantung kamera yang terhubung pada perangkat yang anda gunakan. 


