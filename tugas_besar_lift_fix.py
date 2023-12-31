# PROGRAM: LIFT


# KAMUS:
# TOTAL_LANTAI : integer - Total lantai gedung
# BERAT_PENGGUNA_MAKSIMUM : integer - Batas maksimum berat di dalam lift
# POSISI_AWAL_LIFT : integer - Posisi awal lift
# alur_lift : array of integer - Alur pergerakan lift
# alur_lift_atas : array of integer - Alur pergerakan lift ketika naik
# alur_lift_bawah : array of integer - Alur pergerakan lift ketika turun
# arah : boolean - Pergerakan ke atas bernilai True, ke bawah bernilai False
# pengguna : matrix of integer - Menyimpan data posisi dan permintaan masing-masing pengguna


# ALGORITMA:
# FUNCTIONS:
def tambahkan(arr, a):
  '''
  Menambahkan elemen a ke indeks terakhir array arr dan menambah 1 satuan panjang array arr
  '''
  array = [i for i in range(len(arr)+1)]
  for i in range(len(arr)):
    array[i] = arr[i]
  array[-1] = a
  return array


def hapuskan(array, a):
  '''
  Menghapus elemen a pada array dan mengurangi 1 satuan panjang array
  '''
  for i in range(len(array)):
    if array[i] == a:
      array[i] = None

  count = 0
  arr = [None] * (len(array) - 1)
  for i in range(len(array)):
    if array[i] != None:
      arr[count] = array[i]
      count += 1
      
  return arr
  

def hapus_none(array):
  '''
  Menghapus semua elemen none pada array
  '''
  arr = []
  for i in range(len(array)):
    if array[i] != None:
      arr = tambahkan(arr, array[i])

  return arr


def tak_berulang(array):
  '''
  Membuat tidak ada elemen di dalam array yang berulang berturut-turut
  '''
  array_tak_berulang = []

  for i in range(len(array)-1):
    if array[i] != array[i+1]:
      array_tak_berulang = tambahkan(array_tak_berulang, array[i])

  array_tak_berulang = tambahkan(array_tak_berulang, array[len(array)-1])
  return array_tak_berulang


def sort_descending(array):
  '''
  function buat sorting array (dari tinggi ke rendah)
  '''
  for i in range(len(array)):
      for j in range(i, len(array)):
          if array[i] < array[j]:
              penampung = array[i]
              array[i] = array[j]
              array[j] = penampung
  return array


def sort_ascending(array):
  '''
  function buat sorting array (dari rendah ke tinggi)
  '''
  for i in range(len(array)):
      for j in range(i, len(array)):
          if array[i] > array[j]:
              penampung = array[j]
              array[j] = array[i]
              array[i] = penampung
  return array


def pengguna_keluar(pengguna):
  '''
  Menghapus tujuan pengguna pada array pengguna ketika mencapai lantai yang dituju
  '''
  for i in range(len(pengguna)):
    if i in pengguna[i]:
      pengguna[i] = hapuskan(pengguna[i], i)
  return pengguna


def pengguna_kosong(pengguna):
  '''
  Menentukan apakah tiap-tiap isi array pengguna tidak memiliki nilai
  '''
  for i in range(len(pengguna)):
    if pengguna[i]:
      return False
  return True


def masukkan_input_user(pengguna):
  '''
  User input meliputi: total pengguna tiap lantai dengan permintaan dan tujuan tiap-tiap pengguna
  '''
  print()
  print()
  print("-------------------------------------------------------------")
  # Input lantai-lantai yang memiliki permintaan
  jumlah_permintaan = int(input("Masukkan total posisi lantai berbeda yang memiliki permintaan: "))
  lantai_permintaan = [0 for i in range(jumlah_permintaan)]
  for i in range(jumlah_permintaan):
    lantai_permintaan[i] = int(input(f"{i+1}. Masukkan posisi lantai yang memiliki permintaan: "))
  lantai_permintaan = sort_ascending(lantai_permintaan)
  print()

  
  # Input permintaan tiap lantai yang memiliki permintaan
  for i in lantai_permintaan:
    total_pengguna_lantai = int(input(f"Masukkan total pengguna di lantai ke-{i}: "))


    # Input tujuan tiap-tiap pengguna
    for j in range(total_pengguna_lantai):
      tujuan = int(input(f"Masukkan tujuan pengguna ke-{j+1}: "))
      pengguna[i] = tambahkan(pengguna[i], tujuan)
    print()


  # Menghilangkan input elemen tujuan berulang dan ketika input tujuan == lantai saat ini
  pengguna = pengguna_keluar(pengguna)
  for i in range(len(pengguna)):
    if len(pengguna[i]) > 1:
      pengguna[i] = tak_berulang(pengguna[i])
  
  return pengguna


def menentukan_arah(pengguna, alur_lift): 
  '''
  menentukan arah dan posisi permintaan awal
  '''
  # Cek tiap-tiap lantai yang memiliki permintaan
  posisi_lift_terakhir = alur_lift[-1]
  ada_permintaan = []
  for i in range(len(pengguna)):
    if pengguna[i]:
      ada_permintaan = tambahkan(ada_permintaan, i)


  # Cek jarak permintaan terdekat dengan posisi lift terakhir
  terdekat = int(((ada_permintaan[0] - posisi_lift_terakhir)**2)**(1/2))
  lantai_terdekat = ada_permintaan[0]
  for i in range(len(ada_permintaan)):
    jarak = int(((ada_permintaan[i] - posisi_lift_terakhir)**2)**(1/2))
    if jarak < terdekat:
      terdekat = jarak
      lantai_terdekat = ada_permintaan[i]


  # Cek arah pergerakan lift sesuai permintaan awal
  if pengguna[lantai_terdekat][0] > lantai_terdekat:
    arah = True
  if pengguna[lantai_terdekat][0] < lantai_terdekat:
    arah = False
  
  return arah, lantai_terdekat
def lift_naik(pengguna, alur_lift, alur_lift_atas):
  '''
  Track pergerakan ketika lift naik, menghapus tujuan yang terpenuhi pada array pengguna, dan track total berat dalam lift
  '''
  arah, posisi_permintaan = menentukan_arah(pengguna, alur_lift)
  tujuan_teratas = pengguna[posisi_permintaan][0]
  tujuan_atas = [tujuan_teratas]
  berat_pengguna = 0


  while arah:
    # Scan tiap-tiap lantai ketika lift ke atas
    for i in range(posisi_permintaan, tujuan_teratas + 1):
      # Cek apakah lantai saat ini termasuk list tujuan lift saat ke atas
      if posisi_permintaan in tujuan_atas:
        alur_lift_atas = tambahkan(alur_lift_atas, posisi_permintaan)
        # Berat dikurang berat pengguna keluar
        berat_pengguna -= int(input(f"(Berat = {berat_pengguna}) - Masukkan total berat pengguna yang keluar di lantai ke-{posisi_permintaan} (Kg): "))


      # Scan tiap-tiap tujuan pengguna pada lantai saat ini
      for j in range(len(pengguna[posisi_permintaan])):
        # Menentukan tujuan teratas
        if pengguna[posisi_permintaan][j] > tujuan_teratas:
          tujuan_teratas = pengguna[posisi_permintaan][j]


        # Menambahkan list tujuan lift saat ke atas
        if pengguna[posisi_permintaan][j] > posisi_permintaan:
          # Tambahkan berat pengguna masuk
          container = berat_pengguna
          berat_pengguna += int(input(f"(Berat = {berat_pengguna}) - Masukkan total berat pengguna ke-{j+1} yang masuk di lantai ke-{posisi_permintaan} (Kg): "))
          while berat_pengguna > BERAT_PENGGUNA_MAKSIMUM:
            print(f"(Berat = {berat_pengguna}) - Berat total pengguna melebihi kapasitas, kurangi total berat pengguna!")
            berat_pengguna = container
            berat_pengguna += int(input(f"(Berat = {berat_pengguna}) - Masukkan total berat pengguna ke-{j+1} yang masuk di lantai ke-{posisi_permintaan} (Kg): "))

          tujuan_atas = tambahkan(tujuan_atas, pengguna[posisi_permintaan][j])
          alur_lift_atas = tambahkan(alur_lift_atas, posisi_permintaan)
          # Hapus tujuan terpenuhi pada array pengguna
          pengguna[posisi_permintaan][j] = None
      

      # Hapus tujuan terpenuhi pada array pengguna
      pengguna[posisi_permintaan] = hapus_none(pengguna[posisi_permintaan])

      
      # Cek kondisi ketika lift mencapai tujuan teratas, kemudian berhenti
      if posisi_permintaan == tujuan_teratas:
          alur_lift_atas = tambahkan(alur_lift_atas, posisi_permintaan)
          arah = False


      # +1 posisi lantai saat ini
      if posisi_permintaan < TOTAL_LANTAI:
        posisi_permintaan += 1
    

  # Sorting array
  alur_lift_atas = sort_ascending(alur_lift_atas)

  # masukkan alur_lift_atas ke alur_lift
  for i in range(len(alur_lift_atas)):
    alur_lift = tambahkan(alur_lift, alur_lift_atas[i])

  # Agar tidak ada elemen berulang
  alur_lift = tak_berulang(alur_lift)

  return alur_lift, pengguna


def lift_turun(pengguna, alur_lift, alur_lift_bawah):
  '''
  Track pergerakan ketika lift turun, menghapus tujuan yang terpenuhi pada array pengguna, dan track total berat dalam lift
  '''
  arah, posisi_permintaan = menentukan_arah(pengguna, alur_lift)
  tujuan_terbawah = pengguna[posisi_permintaan][0]
  tujuan_bawah = [tujuan_terbawah]
  berat_pengguna = 0


  while not arah:
    # Scan tiap-tiap lantai ketika lift ke bawah
    for i in range(posisi_permintaan, tujuan_terbawah - 1, -1):
      # Cek apakah lantai saat ini termasuk list tujuan lift saat ke bawah
      if posisi_permintaan in tujuan_bawah:
        alur_lift_bawah = tambahkan(alur_lift_bawah, posisi_permintaan)
        # Berat dikurang berat pengguna keluar
        berat_pengguna -= int(input(f"(Berat = {berat_pengguna}) - Masukkan total berat pengguna yang keluar di lantai ke-{posisi_permintaan} (Kg): "))


      # Scan tiap-tiap tujuan pengguna pada lantai saat ini
      for j in range(len(pengguna[posisi_permintaan])):
        # Menentukan tujuan terbawah
        if pengguna[posisi_permintaan][j] < tujuan_terbawah:
          tujuan_terbawah = pengguna[posisi_permintaan][j]


        # Menambahkan list tujuan lift saat ke bawah
        if pengguna[posisi_permintaan][j] < posisi_permintaan:
          # Tambahkan berat pengguna masuk
          container = berat_pengguna
          berat_pengguna += int(input(f"(Berat = {berat_pengguna}) - Masukkan total berat pengguna ke-{j+1} yang masuk di lantai ke-{posisi_permintaan} (Kg): "))
          while berat_pengguna > BERAT_PENGGUNA_MAKSIMUM:
            print(f"(Berat = {berat_pengguna}) - Berat total pengguna melebihi kapasitas, kurangi total berat pengguna!")
            berat_pengguna = container
            berat_pengguna += int(input(f"(Berat = {berat_pengguna}) - Masukkan total berat pengguna ke-{j+1} yang masuk di lantai ke-{posisi_permintaan} (Kg): "))

          tujuan_bawah = tambahkan(tujuan_bawah, pengguna[posisi_permintaan][j])
          alur_lift_bawah = tambahkan(alur_lift_bawah, posisi_permintaan)
          # Hapus tujuan terpenuhi pada array pengguna
          pengguna[posisi_permintaan][j] = None

      # Hapus tujuan terpenuhi pada array pengguna
      pengguna[posisi_permintaan] = hapus_none(pengguna[posisi_permintaan])
      
  
      # Cek kondisi ketika lift mencapai tujuan terbawah, kemudian berhenti
      if posisi_permintaan == tujuan_terbawah:
          alur_lift_bawah = tambahkan(alur_lift_bawah, posisi_permintaan)
          arah = True


      # -1 posisi lantai saat ini
      if posisi_permintaan > 0:
        posisi_permintaan -= 1

    
  # Sorting array
  alur_lift_bawah = sort_descending(alur_lift_bawah)


  # masukkan alur_lift_bawah ke alur_lift
  for i in range(len(alur_lift_bawah)):
    alur_lift = tambahkan(alur_lift, alur_lift_bawah[i])


  # Agar tidak ada elemen berulang
  alur_lift = tak_berulang(alur_lift)

  return alur_lift, pengguna


# -------------------------------------------------------------------------------------------------------------------------------------------


# INPUT:
TOTAL_LANTAI = int(input("Masukkan total lantai: "))
BERAT_PENGGUNA_MAKSIMUM = int(input("Masukkan jumlah pengguna maksimum (Kg): "))
POSISI_AWAL_LIFT = int(input("Masukkan posisi awal lift: "))
alur_lift = [POSISI_AWAL_LIFT]
alur_lift_atas = []
alur_lift_bawah = []
arah = None   #True = Ke Atas ; False = Ke Bawah


# matrix pengguna = [posisi, posisi, posisi] => array posisi = [tujuan]
pengguna = []
for i in range(TOTAL_LANTAI+1):
  pengguna = tambahkan(pengguna, [])
pengguna = masukkan_input_user(pengguna)

print()
print("-------------------------------------------------------------")
print("Pengguna: ", pengguna)
print("-------------------------------------------------------------")
print()


# PROSES:
# Agar dapat berulang hingga tidak ada permintaan lagi
while not pengguna_kosong(pengguna):
  # cek arah dan posisi_permintaan awal
  arah, posisi_permintaan = menentukan_arah(pengguna, alur_lift)


  if arah: # Ketika lif bergerak ke atas
    print()
    alur_lift, pengguna = lift_naik(pengguna, alur_lift, alur_lift_atas)
    print("-------------------------------------------------------------")
    print("(Naik) Alur lift:", alur_lift)
    print()
    print(f"Posisi lift saat ini: lantai {alur_lift[-1]}")
    print("-------------------------------------------------------------")
    pengguna = masukkan_input_user(pengguna)
    print("Pengguna:", pengguna)
    print("-------------------------------------------------------------")


  # cek arah dan posisi_permintaan awal
  if not pengguna_kosong(pengguna):
    arah, posisi_permintaan = menentukan_arah(pengguna, alur_lift)


  if not arah: # Ketika lif bergerak ke bawah
    print()
    alur_lift, pengguna = lift_turun(pengguna, alur_lift, alur_lift_bawah)
    print("-------------------------------------------------------------")
    print("(Turun) Alur lift:", alur_lift)
    print()
    print(f"Posisi lift saat ini: lantai {alur_lift[-1]}")
    print("-------------------------------------------------------------")
    pengguna = masukkan_input_user(pengguna)
    print("Pengguna:", pengguna)
    print("-------------------------------------------------------------")


# OUTPUT:
print()
print()
print("-------------------------------------------------------------")
print("Alur_lift akhir", alur_lift)
print("Pengguna akhir", pengguna)
print("-------------------------------------------------------------")
