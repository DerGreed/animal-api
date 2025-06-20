import sqlite3

DATABASE = "./database/animals.db"

def get_db_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row 
    return con

def init_db():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS Owners (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT
                )
                ''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS Animals (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    genus TEXT,
                    owner_id INTEGER,
                    FOREIGN KEY (owner_id) REFERENCES Owners (id)    
                )

                ''')
    ## ACHTUNG: TODO Wenn wir mySQL integriert haben, können wir nachträglich Constraints wie die Fremdschlüsseleigenschaft hinzufügen
    # try:
    #     cur.execute('ALTER TABLE Animals ADD COLUMN owner_id INTEGER')
    #     cur.execute('ALTER TABLE Animals ADD CONSTRAINT owner_id FOREIGN KEY (owner_id) REFERENCES Owners (id);')
    # except:
    #     print("owner_id Spalte hinzugefügt")
    owner_count = cur.execute('SELECT COUNT(*) FROM Owners').fetchone()[0] 
    if owner_count == 0:
        data = [
            ('Max Mustermann', 'max@email.com', '0123 456789'),
            ('Anna Schmidt', 'schmidty@mail.de', '01896 128842'),
            ('Tom Weber', 'weberknecht@spinne.at', '0189 5868463')
        ]
        cur.executemany('INSERT INTO Owners (name, email, phone) VALUES (?,?,?)', data) 
    animal_count = cur.execute('SELECT COUNT(*) FROM Animals').fetchone()[0] 
    if animal_count == 0:
        data = [
            ('dog', 3, 'mammals', 2),
            ('cat', 2, 'mammals', 3),
            ('elephant', 20, 'mammals', 1),
            ('bird', 5, 'birds', None)
        ]
        cur.executemany('INSERT INTO Animals (name, age, genus, owner_id) VALUES (?,?,?,?)', data) 
        con.commit() 
    
    con.close()