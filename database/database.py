import mysql.connector
import mysql.connector.cursor
from database.db_config import DB_CONFIG

def get_db_connection() -> mysql.connector.MySQLConnection:
    return mysql.connector.connect(**DB_CONFIG)

def get_cursor(con: mysql.connector.MySQLConnection) -> mysql.connector.cursor.MySQLCursorDict:
    return con.cursor(dictionary=True)

def init_db():
    con = get_db_connection()
    cur = get_cursor(con)
    cur.execute('''
                CREATE TABLE IF NOT EXISTS Owners (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    phone VARCHAR(255)
                )
                ''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS Animals (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    age INT,
                    genus VARCHAR(255),
                    owner_id INT,
                    FOREIGN KEY (owner_id) REFERENCES Owners (id)    
                )

                ''')
    ## ACHTUNG: TODO Wenn wir mySQL integriert haben, können wir nachträglich Constraints wie die Fremdschlüsseleigenschaft hinzufügen
    # try:
    #     cur.execute('ALTER TABLE Animals ADD COLUMN owner_id INTEGER')
    #     cur.execute('ALTER TABLE Animals ADD CONSTRAINT owner_id FOREIGN KEY (owner_id) REFERENCES Owners (id);')
    # except:
    #     print("owner_id Spalte hinzugefügt")
    cur.execute('SELECT COUNT(*) AS count FROM Owners') # Ein Dictionary aus Schlüssel-Wert Paaren
    # z.B. bei 4 Datensätzen bekomme ich ein { "count": 4 } zurück
    owner_count = cur.fetchone()['count'] 
    if owner_count == 0:
        data = [
            ('Max Mustermann', 'max@email.com', '0123 456789'),
            ('Anna Schmidt', 'schmidty@mail.de', '01896 128842'),
            ('Tom Weber', 'weberknecht@spinne.at', '0189 5868463')
        ]
        cur.executemany('INSERT INTO Owners (name, email, phone) VALUES (%s,%s,%s)', data)

    cur.execute('SELECT COUNT(*) AS count FROM Animals')
    animal_count = cur.fetchone()['count']
    if animal_count == 0:
        data = [
            ('dog', 3, 'mammals', 2),
            ('cat', 2, 'mammals', 3),
            ('elephant', 20, 'mammals', 1),
            ('bird', 5, 'birds', None)
        ]
        cur.executemany('INSERT INTO Animals (name, age, genus, owner_id) VALUES (%s,%s,%s,%s)', data)
    
    con.commit()
    con.close()