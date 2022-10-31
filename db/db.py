import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    db='covid19_check'
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE COVID19_CHECK")

# mycursor.execute("CREATE TABLE accounts (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name varchar(50) NOT NULL, phone varchar(10) NOT NULL, email varchar(50) NOT NULL, username varchar(50) NOT NULL, password varchar(50) NOT NULL, conf_password varchar(50) NOT NULL)")

# mycursor.execute("ALTER TABLE accounts ADD status varchar(1)")

# mycursor.execute("ALTER TABLE accounts ADD id INT NOT NULL AUTO_INCREMENT")

# mycursor.execute("ALTER TABLE accounts DROP PRIMARY KEY")

# mycursor.execute("ALTER TABLE accounts ADD PRIMARY KEY (id)")

# mycursor.execute("CREATE TABLE faculties (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(255), address varchar(255))")

# mycursor.execute("ALTER TABLE faculties DROP address")

# sql = 'INSERT INTO faculties (name) VALUES (%s)'
# val = [
#         ("สถาบันวิทยาศาสตร์ทางทะเล",),
#         ("โรงเรียนสาธิตฯ",),
#         ("หอศิลปะและวัฒนธรรมภาคตะวันออก",),
#         ("ลานธรรม",),
#         ("คณะดนตรีและการแสดง",),
#         ("อาคารเฉลิมพระเกียรติฉลองสิริราชสมบัติครบ 60 ปี",),
#         ("อาคารการค้าระหว่างประเทศ",),
#         ("คณะเภสัชศาสตร์",),
#         ("อาคารสำนักงานอธิการบดี (ภปร.)",),
#         ("หอประชุมธำรง บัวศรี",),
#         ("อาคารประยูร จินดาประดิษฐ์",),
#         ("อาคารสิรินธร",),
#         ("อาคารเคมี ฟิสิกส์ คณิต",),
#         ("อาคารปฏิบัติการพื้นฐานและศูนย์เครื่องมือวิทยาศาสตร์",),
#         ("คณะโลจิสติกส์",),
#         ("อาคารวิทยาศาสตร์ชีวภาพ",),
#         ("สำนักหอสมุด",),
#         ("คณะวิทยาศาสตร์กีฬา",),
#         ("คณะแพทยศาสตร์",),
#         ("คณะสาธารณสุขศาสตร์",),
#         ("คณะพยาบาลศาสตร์",),
#         ("คณะการแพทย์แผนไทยอภัยภูเบศร",),
#         ("สำนักคอมพิวเตอร์",),
#         ("หอพักนานาชาติ",),
#         ("วิทยาลัยนานาชาติ",),
#         ("คณะศึกษาศาสตร์",),
#         ("หอพักนักศึกษาพยาบาล",),
#         ("คณะสหเวชศาสตร์",),
#         ("คณะศิลปกรรมศาสตร์",),
#         ("โครงการจัดตั้งคณะพาณิชยศาสตร์และบริหารธุรกิจ",),
#         ("คณะมนุษยศาสตร์และสังคมศาสตร์",),
#         ("วิทยาลัยวิทยาการวิจัยและวิทยาการปัญญา",),
#         ("ศูนย์กิจกรรมนิสิต+ศูนย์หนังสือจุฬาฯ",),
#         ("โรงแรมเทา-ทอง",),
#         ("อาคารศูนย์กิจกรรมนิสิต 2",),
#         ("หอพัก 14",),
#         ("หอพัก 50 ปี เทา-ทอง",),
#         ("หอพัก 15",),
#         ("หอพักเทา-ทอง 2",),
#         ("หอพักเทา-ทอง 3",),
#         ("สนามกีฬากลาง (เชาวน์ มณีวงษ์)",),
#         ("สวนนันทนาการ",),
#         ("หอพักเทา-ทอง 4",),
#         ("คณะวิทยาศาสตร์การกีฬา",),
#         ("คณะวิศวกรรมศาสตร์",),
#         ("สนามชมพูพันทิพย์",),
#         ("ลานกิจกรรม",),
#         ("คณะการจัดการและการท่องเที่ยว",),
#         ("อาคารเสนาะ อูนากุล",),
#         ("หอพักนิสิตแพทย์",),
#         ("คณะรัฐศาสตร์และนิติศาสตร์",),
#         ("คณะวิทยาการสารสนเทศ",)
#       ]
# mycursor.executemany(sql,val)

# mycursor.execute("CREATE TABLE hospital (id int PRIMARY KEY AUTO_INCREMENT, name varchar(255), phone varchar(10), address varchar(255), bed int)")

# mycursor.execute("CREATE TABLE admin (username varchar(50) PRIMARY KEY, password varchar(50), name varchar(50))")

# mycursor.execute("CREATE TABLE atk (id int PRIMARY KEY AUTO_INCREMENT, userID int, send_date date, end_date date)")
# mycursor.execute("ALTER TABLE atk CHANGE start send_date date")
# mycursor.execute("CREATE TABLE atk_img (id int PRIMARY KEY AUTO_INCREMENT, aID int, name varchar(255), FOREIGN KEY (aID) REFERENCES atk(id) ON DELETE CASCADE)")
# mycursor.execute("DROP TABLE atk_img")
# mycursor.execute("DROP TABLE atk")

# mycursor.execute("ALTER TABLE atk ADD facultyID int")
# mycursor.execute("ALTER TABLE atk add FOREIGN KEY (facultyID) REFERENCES faculties(id)")
# mycursor.execute("ALTER TABLE atk MODIFY facultyID int NOT NULL")

# mycursor.execute("ALTER TABLE atk add FOREIGN KEY (userID) REFERENCES accounts(id)")
# mycursor.execute("ALTER TABLE atk ADD end_date date")

# mycursor.execute("DROP TABLE hospital")
# mycursor.execute("INSERT INTO hospital (name, phone, address, bed) VALUES ('โรงพยาบาลมหาวิทยาลัยบูรพา','034745802','169 ถนนลงหาดบางแสน ตำบลแสนสุข อำเภอเมืองชลบุรี จังหวัดชลบุรี 20131', '450')")


# sql = 'INSERT INTO accounts (name, phone, email, username, password, conf_password) VALUES (%s, %s, %s, %s, %s, %s)'
# val = ('Natchapol Nillaphun','0624246668', 'ninencp01@gmail.com','nine','123456','123456')
# mycursor.execute(sql, val)

# mycursor.execute("INSERT INTO admin (username, password, name) VALUES ('admin','AdMiN12344321_','Admin')")

# mycursor.execute("ALTER TABLE admin ADD hospitalID int")
# mycursor.execute("ALTER TABLE admin add FOREIGN KEY (hospitalID) REFERENCES hospital(id)")

# mycursor.execute("ALTER TABLE atk_img ADD FOREIGN KEY (aID) REFERENCES atk(id)")

mydb.commit()