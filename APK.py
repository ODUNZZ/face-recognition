from tkinter import *
import cv2
import os
import numpy as np
import mysql.connector
import RPi.GPIO as GPIO
import time
import datetime


def selesai_daftar ():
    ucapan.set("15 Data Wajah Diambil")
def perintah_hadap():
    ucapan.set("Hadapkan Wajah Anda Pada Webcamera")
def selesai_training():
    ucapan.set("Data Wajah Berhasil Di Training")
def selesai_rekognisi():
    ucapan.set("Silahkan Memasuki Perumahan")
def isi_tamu():
    ucapan.set("Silahkah Mengisi Data Tamu")
def tunggu_motret():
    ucapan.set("Harap Menunggu Untuk Pengambilan Gambar")
def simpan_tamu():
    ucapan.set("Gambar Wajah Tersimpan")


def masukin_database_tamu():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="191200",
        database="data_warga"
    )
    insertdt = mydb.cursor()
    insert_warga = "insert into register_warga(id,nama,nik,alamat) " \
                   "value('"+e_id.get()+"','"+e_nama.get()+"','"+e_nik.get()+"','"+e_alamat.get()+"')"
    insertdt.execute(insert_warga)
    mydb.commit()
    mydb.close()

def masukin_database_tamu():
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

def rekamDataWajah():
    refWajah = './Data Wajah/'
    cam = cv2.VideoCapture(0)
    cam.set(3, 774)  # ubah lebar camera
    cam.set(4, 613)  # ubah tinggi kamera
    pendeteksiWajah = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    perintah_hadap()
    id_wajah = e_id.get()
    ambilData = 1
    total_wajah = 15
    while True:
        retV, frame = cam.read()
        frame = cv2.flip(frame, 1)
        abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        wajah = pendeteksiWajah.detectMultiScale(abuAbu, 1.3, 3)  # frame, faktor skala, minNeighbors
        for (x, y, w, h) in wajah:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 5)
            namaFile = 'Wajah.' + str(id_wajah) + '.' + str(ambilData) + '.jpg'
            wajahAbu = abuAbu[y:y + h, x:x + w]
            wajahWarna = frame[y:y + h, x:x + w]
            if cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.imwrite(refWajah + namaFile, wajahWarna)
                ambilData += 1
                if ambilData > total_wajah:
                    # print(f'{total_wajah} Gambar Wajah Diambil')
                    selesai_daftar()
        cv2.imshow('Kameraku', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    masukin_database()
    cam.release()
    cv2.destroyAllWindows()

def latihWajah():
    folder_name = 'Data Wajah'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path_images = os.listdir(folder_name)

    image_arrays = []
    image_ids = []
    ambilData = 1
    for path_image in path_images:
        split_pth = path_image.split('.')
        image_id = int(split_pth[1])

        img_pth = os.path.join(folder_name, path_image)  # face data / <path_image>
        image = cv2.imread(img_pth)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image_array = np.array(image)
        image_arrays.append(image_array)
        image_ids.append(image_id)

        recognizer.train(image_arrays, np.array(image_ids))
        recognizer.save('latihwajah/train.xml')
        print('Berhasil Membuat Data Train!')
        ambilData += 1

    print(f"{ambilData} Berhasil Dilatihkan!")
    selesai_training()

def rekognisiWajah():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="191200",
        database="data_warga"
    )
    tmbl = mydb.cursor()
    tbl_warga = "SELECT nama FROM `register_warga` "
    tmbl.execute(tbl_warga)
    dt = tmbl.fetchall()
    names = ['Tidak Diketahui']
    i = 0
    for x in range(len(dt)):
        x = dt[i][0]
        names.append(x)
        i += 1
        if i == len(dt):
#             print(names)
            break
    cam = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    pendeteksiWajah = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam.set(3, 774)  # ubah lebar camera
    cam.set(4, 613)  # ubah tinggi kamera
    # membaca data training
    recognizer.read('latihwajah/train.xml')
    font = cv2.FONT_ITALIC
    ids = 1
    print("ini names ",names)
    minWidth = 0.1 * cam.get(3)
    minHeight = 0.1 * cam.get(4)
    while True:
        retV, frame = cam.read()
        frame = cv2.flip(frame, 1)  # di flip secara vertikal
        abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        wajah = pendeteksiWajah.detectMultiScale(abuAbu, 1.2, 5, minSize=(round(minWidth), round(minHeight)))  # frame, faktor skala, minNeighbors
        for (x, y, w, h) in wajah:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            wajahAbu = abuAbu[y:y + h, x:x + w]
            wajahWarna = frame[y:y + h, x:x + w]
            ids, confidence = recognizer.predict(wajahAbu)  # confidence = 0 artinya cocok sempur
            if confidence < 50:
                nameID = names[ids]
                confidenceTxT = "{0}%".format(round(100 - confidence))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, str(nameID), (x + 5, y - 5), font, 1, (0, 255, 0))
                cv2.putText(frame, str(confidenceTxT), (x + 5, y + h - 5), font, 1, (0, 255, 255))
                selesai_rekognisi()
                buka_pintu()
            else:
                nameID = names[0]
                confidenceTxT = "{0}%".format(round(100 - confidence))
                cv2.putText(frame, str(nameID), (x + 5, y - 5), font, 1, (0, 0, 255))
                cv2.putText(frame, str(confidenceTxT), (x + 5, y + h - 5), font, 1, (0, 255, 255))
                isi_tamu()
        cv2.imshow('Recognisi Wajah', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

def dataTamu():
    nama_tamu = e_nama.get()
    nik_tamu = e_nik.get()
    alamat_tamu = e_alamat.get()
    ambil_waktu = datetime.datetime.today()
    # Simpan Data Tamu
    file_tamu = open('./Data Tamu/Data_Tamu.txt', 'a')
    file_tamu.write(str(ambil_waktu)+ "/" + nama_tamu + "/" + nik_tamu + "/" + alamat_tamu + "\n")
    file_tamu.close()
    tunggu_motret()
    ref_tamu = './Data Tamu/'
    cam = cv2.VideoCapture(0)
    cam.set(3, 774)  # ubah lebar camera
    cam.set(4, 613)  # ubah tinggi kamera
    pendeteksiWajah = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    ambilData = 1
    total_wajah = 15
    while True:
        retV, frame = cam.read()
        frame = cv2.flip(frame, 1)
        abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        wajah = pendeteksiWajah.detectMultiScale(abuAbu, 1.3, 3)  # frame, faktor skala, minNeighbors
        for (x, y, w, h) in wajah:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 5)
            nama_foto = 'Wajah.' + str(nama_tamu) + '.jpg'
            wajahAbu = abuAbu[y:y + h, x:x + w]
            wajahWarna = frame[y:y + h, x:x + w]

            if cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.imwrite(ref_tamu + nama_foto, wajahWarna)
                ambilData += 1
                if ambilData > total_wajah:
#                   print(f'Gambar Wajah Disimpan')
                    simpan_tamu()
        cv2.imshow('Kameraku', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            buka_pintu()
            break
    masukin_database_tamu()
    cam.release()
    cv2.destroyAllWindows()

def latihWajah_tamu():
    folder_name = 'Data Tamu'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path_images = os.listdir(folder_name)

    image_arrays = []
    image_ids = []
    ambilData = 1
    for path_image in path_images:
        split_pth = path_image.split('.')
        image_id = int(split_pth[1])

        img_pth = os.path.join(folder_name, path_image)  # face data / <path_image>
        image = cv2.imread(img_pth)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image_array = np.array(image)
        image_arrays.append(image_array)
        image_ids.append(image_id)

        recognizer.train(image_arrays, np.array(image_ids))
        recognizer.save('Data Tamu/train.xml')
        print('Berhasil Membuat Data Train!')
        ambilData += 1

    print(f"{ambilData} Berhasil Dilatihkan!")
    selesai_training()

def rekognisiWajah_tamu():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="191200",
        database="data_tamu"
    )
    tmbl = mydb.cursor()
    tbl_tamu = "SELECT nama FROM `register_tamu` "
    tmbl.execute(tbl_tamu)
    dt = tmbl.fetchall()
    names = ['Tidak Diketahui']
    i = 0
    for x in range(len(dt)):
        x = dt[i][0]
        names.append(x)
        i += 1
        if i == len(dt):
#             print(names)
            break
    cam = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    pendeteksiWajah = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam.set(3, 774)  # ubah lebar camera
    cam.set(4, 613)  # ubah tinggi kamera
    # membaca data training
    recognizer.read('Data Tamu/train.xml')
    font = cv2.FONT_ITALIC
    ids = 1
    print("ini names ",names)
    minWidth = 0.1 * cam.get(3)
    minHeight = 0.1 * cam.get(4)
    while True:
        retV, frame = cam.read()
        frame = cv2.flip(frame, 1)  # di flip secara vertikal
        abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        wajah = pendeteksiWajah.detectMultiScale(abuAbu, 1.2, 5, minSize=(round(minWidth), round(minHeight)))  # frame, faktor skala, minNeighbors
        for (x, y, w, h) in wajah:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            wajahAbu = abuAbu[y:y + h, x:x + w]
            wajahWarna = frame[y:y + h, x:x + w]
            ids, confidence = recognizer.predict(wajahAbu)  # confidence = 0 artinya cocok sempur
            if confidence < 50:
                nameID = names[ids]
                confidenceTxT = "{0}%".format(round(100 - confidence))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, str(nameID), (x + 5, y - 5), font, 1, (0, 255, 0))
                cv2.putText(frame, str(confidenceTxT), (x + 5, y + h - 5), font, 1, (0, 255, 255))
                selesai_rekognisi()
                buka_pintu()
            else:
                nameID = names[0]
                confidenceTxT = "{0}%".format(round(100 - confidence))
                cv2.putText(frame, str(nameID), (x + 5, y - 5), font, 1, (0, 0, 255))
                cv2.putText(frame, str(confidenceTxT), (x + 5, y + h - 5), font, 1, (0, 255, 255))
                isi_tamu()
        cv2.imshow('Recognisi Wajah', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

def hapus_entry():
    e_nama.delete(0, END)
    e_nik.delete(0, END)
    e_alamat.delete(0, END)
    e_id.delete(0, END)
    ucapan.set("Selamat Datang Di Komplek Bumipakusarakan")

def buka_pintu():
    servoPIN = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)
    p.start(0)
    for i in range(0,1):
        p.ChangeDutyCycle(12)
        time.sleep(0.2)

    p.stop()
    GPIO.cleanup()

def tutup_pintu():
    servoPIN = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)
    p.start(0)
    for i in range(0,1):
        p.ChangeDutyCycle(7.5)
        time.sleep(0.2)

    p.stop()
    GPIO.cleanup()
    ucapan.set("Selamat Datang Di Komplek Bumipakusarakan")



#GUI
apk = Tk()

apk.title("Sistem Keamanan Komplek Bumipakusarakan")
apk.geometry("1536x864")

#set judul
var = StringVar()
judul = Label(apk, textvariable= var, bg= "#7BE872", font=("Raleway",28) )
var.set("Sistem Keamanan Komplek Bumipakusarakan")
judul.grid(column=1, row=0,columnspan=2, sticky="wens", rowspan= 1, )

#garis merah bawah judul
garis = Label(apk, text="_" *375, fg="#FA0909", )
garis.grid(column=1, row= 1, columnspan=2, sticky="wnen")

#----------------------------------------------------------
#kolom dan baris
apk.columnconfigure(0, weight=1) #dipake label kotak input
apk.columnconfigure(1, weight=1) #dipake kotak input
apk.columnconfigure(2, weight=1) #dipake tombol


apk.rowconfigure(0,weight=1) #judul
apk.rowconfigure(1,weight=1) #garis merah
apk.rowconfigure(2,weight=1) #identifikasi , pendaftaran, latih data, data tamu
apk.rowconfigure(3,weight=1)
apk.rowconfigure(4,weight=1)
apk.rowconfigure(5,weight=1)
apk.rowconfigure(6,weight=1)
apk.rowconfigure(7,weight=1)

#-----------------------------------------------------------------------
#tombol identifikasi
idnt = Button(apk, text="Identifikasi", command= rekognisiWajah, padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
idnt.grid(column=2, row= 2, columnspan=1, sticky="ne", ipadx= 32)

#tombol Pendaftaran
daftar = Button(apk, text="Pendaftaran", command= rekamDataWajah, padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
daftar.grid(column=2, row= 2,columnspan=1, sticky="nw", ipadx= 20)

#tombol Latih Data
lth_data = Button(apk, text="Latih Data", command= latihWajah, padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
lth_data.grid(column=2, row= 2,columnspan=1, sticky="sw", ipadx= 30)

#tombol Data Tamu
tamu = Button(apk, text="Data Tamu", command= dataTamu, padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
tamu.grid(column=2, row= 2,columnspan=1, sticky="se", ipadx= 33)

#tombol tutup pintu
tutup = Button(apk, text="Tutup", command= tutup_pintu,padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
tutup.grid(column=2, row= 3,columnspan=1, sticky="w", ipadx= 50)

#tombol buka pintu
buka = Button(apk, text="Buka", command= buka_pintu,padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
buka.grid(column = 2, row = 3, columnspan = 1, sticky= "e", ipadx = 60)

#tombol clear entry box
hapus = Button(apk, text="Hapus", command= hapus_entry, padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
hapus.grid(column=2, row= 5,columnspan=1, sticky="n", ipadx= 40)

#tombol latih data tamu
lth_tamu = Button(apk, text="Latih Data Tamu", command= latihWajah_tamu, padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
lth_tamu.grid(column=2, row= 4,columnspan=1, sticky="wn", ipadx= 0)

#tombol rekognisi tamu
idnt_tamu = Button(apk, text="Identifikasi Tamu", command= rekognisiWajah_tamu, padx=35, pady=10, background="#18CFF8", font=("Maven Pro", 15))
idnt_tamu.grid(column=2, row= 4,columnspan=1, sticky="en", ipadx= 0)
#----------------------------------------------
#label untuk kotak input
#nama
l_nama = Label(apk, text="Nama :",font=("Raleway",18) )
l_nama.grid(column=1, row=2, sticky= "nw")

#nik
l_nik = Label(apk, text="NIK :",font=("Raleway",18))
l_nik.grid(column=1, row= 3,sticky= "nw")

#alamat
l_alamat = Label(apk, text="Alamat :",font=("Raleway",18))
l_alamat.grid(column=1, row= 4,sticky= "nw")

#id daftar
l_id= Label(apk, text="Id (Daftar) : ", font=("Raleway",18))
l_id.grid(column=1, row= 5,sticky= "nw")


#---------------------------------
#kotak input user
# nama
e_nama = Entry(width=50,font=("Raleway",18))
e_nama.grid(column=1, row=2, sticky="n")

#nik
e_nik = Entry(width=50,font=("Raleway",18))
e_nik.grid(column=1, row= 3, sticky="n")

#alamat
e_alamat = Entry(width=50,font=("Raleway",18))
e_alamat.grid(column=1, row= 4, sticky="n")

#id buat daftar
e_id = Entry(width=50,font=("Raleway",18))
e_id.grid(column=1, row= 5, sticky="n")

#---------------------
#global ucapan
ucapan = StringVar()
kata = Label(apk, textvariable= ucapan,font=("Raleway",18) )
ucapan.set("Selamat Datang Di Komplek Bumipakusarakan")
kata.grid(column=1, row=6,columnspan= 1,rowspan=1, sticky="n")
apk.mainloop()