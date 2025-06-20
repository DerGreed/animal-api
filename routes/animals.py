from flask import request, jsonify
from database.database import get_db_connection
from routes.owners import get_owner_by_id


## Hilfsfunktionen für die Entitäten
def get_animal_by_id(animal_id):
    con = get_db_connection()
    cur = con.cursor()
    animal = cur.execute('SELECT * FROM Animals WHERE id = ?', (animal_id,)).fetchone()
    con.close()
    return animal

def register_animal_routes(app):
    ## GET-Route implementieren, d.h. Daten abrufen bzw. alle Tiere anzeigen
    @app.route("/api/animals", methods=['GET'])
    def show_animals():
        """
        Liste aller Tiere
        ---
        responses:
            200:
                description: JSON-Liste aller Tiere
                examples:
                    application/json:
                        - id: 1
                          name: Dog
                          age: 3
                          genus: mammals
                          owner_id: 2
                        - id: 2
                          name: Cat
                          age: 2
                          genus: mammals
                          owner_id: 3
        """
        # Daten abrufen von der DB
        con = get_db_connection() # Verbindung mit der DB
        cur = con.cursor()
        animals = cur.execute('SELECT * FROM Animals').fetchall()
        con.close()
        return jsonify([dict(animal) for animal in animals]), 200

    ## GET-Route implementieren, um Daten von einem Tier anzuzeigen
    @app.route("/api/animals/<int:animal_id>", methods=['GET'])
    def show_animal(animal_id):
        """
        Anzeigen eines Tieres
        ---
        parameters:
            - name: animal_id
              in: path
              type: integer
              required: true
              description: Die ID des anzuzeigenden Tieres
        responses:
            200:
                description: JSON-Objekt von einem Tier
                examples:
                    application/json:
                        - id: 1
                          name: Dog
                          age: 3
                          genus: mammals
                          owner_id: 2
            404:
                description: Ti¥er wurde nicht gefunden
                examples:
                    application/json:
                        - message: Tier mit der ID 7 existiert nicht
        """
        animal = get_animal_by_id(animal_id)
        if animal is None:
            return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
        return jsonify(dict(animal)), 200
    
    ## POST-Route implementieren, d.h. neue Tier hinzufügen
    @app.route("/api/animals", methods=['POST'])
    def add_animal():
        """
        Neues Tier hinzufügen
        ---
        consumes:
            - application/json
        parameters:
            - in: body
              name: tier
              required: true
              schema:
                type: object
                properties:
                    name:
                        type: string
                        example: Elephant
                    age:
                        type: integer
                        example: 10
                    genus:
                        type: string
                        example: mammals
                    owner_id:
                        type: integer
                        example: 2
        responses:
            201:
                description: Tier hinzugefügt
                examples:
                    application/json:
                        - message: Tier wurde erfolgreich hinzugefügt
            400:
                description: Keine oder fehlerhafte Daten
                examples:
                    application/json:
                        - message: Keine oder fehlerhafte Daten übertragen
        """
        new_animal = request.get_json() # {"name": "turtle", "age:": 100, "genus": "reptile"}
        if not new_animal or 'name' not in new_animal:
            return jsonify({"message": "Keine oder fehlerhafte Daten übertragen"}), 400
        con = get_db_connection() # Schritt 1: DB-Verbindung
        cur = con.cursor() # Schritt 2: Cursor-Objekt definieren
        # Schritt 3: Befehl ausführen
        cur.execute('INSERT INTO Animals (name, age, genus) VALUES (?,?,?)', 
                    (new_animal['name'],
                    new_animal['age'],
                    new_animal['genus'])
                    ) # An dieser Stelle SQL-Befehl zum Hinzufügen des neuen Objektes
        con.commit() # Schritt 4: Persistieren der Veränderungen
        con.close() # Schritt 5: Verbindung zur DB wieder schließen
        return jsonify({"message": "Tier wurde erfolgreich hinzugefügt"}), 201

    ## DELETE-Route, um ein Tier aus der Liste zu löschen
    @app.route("/api/animals/<int:animal_id>", methods=['DELETE'])
    def delete_animal(animal_id):
        """
        Ein Tier löschen
        ---
        parameters:
            - name: animal_id
              in: path
              type: integer
              required: true
              description: Die ID des zu löschenden Tieres
        responses:
            200:
                description: Tier wurde gelöscht
                examples:
                    application/json:
                        - message: Tier wurde erfolgreich gelöscht
            404:
                description: Tier wurde nicht gefunden
                examples:
                    application/json:
                        - message: Tier mit der ID 7 existiert nicht
        """
        con = get_db_connection() 
        cur = con.cursor()
        # Überprüfe, ob das Tier mit der angegebenen ID überhaupt existiert
        animal = cur.execute('SELECT * FROM Animals WHERE id = ?', (animal_id,)).fetchone() # 4 OR 1=! --
        if animal is None:
            return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
        cur.execute('DELETE FROM Animals WHERE id = ?', (animal_id,) )
        ## Achtung: Nutz bitte die ?-Funktion, um SQL-Injection zu verhindern, sonst sähe es so aus:
        # cur.execute(f'DELETE FROM Animals WHERE id = {animal_id}') # 4 OR 1=! --
        con.commit()
        con.close()
        return jsonify({"message": "Tier wurde erfolgreich gelöscht"}), 200

    ## PUT-Route -> Ersetze alle Eigenschaften eines Tieres, d.h. hier schicken wir alle Eigenschaften im Body als JSON mit
    @app.route("/api/animals/<int:animal_id>", methods=['PUT'])
    def put_animal(animal_id):
        """
        Ganzes Tier ersetzen
        ---
        parameters:
            - name: animal_id
              in: path
              type: integer
              required: true
              description: Die ID des Tiers, das ersetzt werden soll
            - in: body
              name: tier
              required: true
              schema: 
                type: object
                properties:
                    name:
                        type: string
                        example: elephant
                    age:
                        type: integer
                        example: 20
                    genus:
                        type: string
                        example: mammals
                    owner_id:
                        type: integer
                        example: 2
        responses:
            200:
                description: Tier wurde aktualisiert
                examples:
                    application/json:
                        - message: Tier wurde komplett aktualisiert
            404:
                description: Tier wurde nicht gefunden
                examples:
                    application/json:
                        - message: Tier mit der ID 7 existiert nicht
        """
        updated_animal = request.get_json() # Speichere dir das Objekt im Body aus dem Request des Clients
        if not updated_animal or 'name' not in updated_animal:
            return jsonify({"message": "Fehlende Daten"}), 400
        # Überprüfe, ob das Tier überhaupt existiert in der DB mit dieser ID
        con = get_db_connection() # Schritt 1
        cur = con.cursor() # Schritt 2
        # Schritt 3
        animal = cur.execute('SELECT * FROM Animals WHERE id = ?', (animal_id,)).fetchone()
        if animal is None:
            return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
        # Update jetzt das Tier mit der übergebenen ID und mit den übergebenen Daten
        cur.execute('UPDATE Animals SET name = ?, age = ?, genus = ? WHERE id = ?', (updated_animal['name'], updated_animal['age'], updated_animal['genus'], animal_id))
        con.commit()
        con.close()
        return jsonify({"message": "Tier wurde komplett aktualisiert"}), 200


    ## PATCH-Route -> Ersetze spezifisch einzelne Eigenschaften, d.h. hier schicken wir nur die zu ändernden Eigenschaften im Body als JSON mit
    @app.route("/api/animals/<int:animal_id>", methods=["PATCH"])
    def patch_animal(animal_id):
        """
        Tier teilweise ändern (z.B. nur das Alter)
        ---
        parameters:
            - name: animal_id
              in: path
              type: integer
              required: true
              description: Die ID des Tiers, das aktualisiert werden soll
            - in: body
              name: tier
              required: anyOf
              schema: 
                type: object
                properties:
                    id:
                        type: integer
                        example: 3
                    name:
                        type: string
                        example: elephant
                    age:
                        type: integer
                        example: 20
                    genus:
                        type: string
                        example: mammals
        responses:
            200:
                description: Tier wurde geupdated
                examples:
                    application/json:
                        - message: Tier wurde geupdated
            404:
                description: Tier wurde nicht gefunden
                examples:
                    application/json:
                        - message: Tier mit der ID 7 existiert nicht
        """
        updated_animal = request.get_json() # name, age, genus
        if not updated_animal:
            return jsonify({"message": "Fehlende Daten"}), 400
        con = get_db_connection()
        cur = con.cursor()
        animal = cur.execute('SELECT * FROM Animals WHERE id = ?', (animal_id,)).fetchone()
        if animal is None:
            return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
        # Leere Liste, wo wir die Felder mitgeben, die wir speziell updaten wollen
        update_fields = [] # Notizzettel, wo wir alle Spalten reinschreiben, die der Client updaten möchte, z.B. nur name: elephant Joel, age = 24
        # Leere Liste, wo wir die Werte der Felder mitgeben, die wir updaten wollen
        update_values = [] # Notizzettel, wo wir die entsprechenden Werte reinschreiben von den Spalten, die wir aktualisieren wollen

        for field in ['name', 'age', 'genus']: # Iteriere über alle möglichen, vorhandenen Spalte der Tabelle
            if field in updated_animal:
                update_fields.append(f'{field} = ?') # name = ?, age = ?
                update_values.append(updated_animal[field]) # elephant Joel, 24
        
        if update_fields:
            update_values.append(animal_id)
            query = f'UPDATE Animals SET {", ".join(update_fields)} WHERE id = ?' # UPDATE Animals SET name = ?, age = ? WHERE id = ?
            cur.execute(query, update_values)
            con.commit()
        con.close()
        return jsonify({"message": "Tier wurde geupdated"}), 200
    
    # Anzeigen, welcher Owner zum Tier gehört
    # GET /api/animals/<int:animal_id>/owner
    @app.route("/api/animals/<int:animal_id>/owner", methods=["GET"])
    def get_owner_of_animal(animal_id):
        """
        Zeigt den Owner eines Tieres an
        ---
        parameters:
            - name: animal_id
              in: path
              type: integer
              required: true
              description: Die ID des Tieres
        responses:
            200:
                description: Besitzer-Daten oder ggf. eine Info, dass kein Besitzer zugeordnet ist
        """
        animal = get_animal_by_id(animal_id)
        if animal is None:
            return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
        if animal["owner_id"] is None:
            return jsonify({"message": "Tier hat keinen Besitzer und kann adoptiert werden"}), 200
        owner = get_owner_by_id(animal["owner_id"])
        if owner is None:
            return jsonify({"message": "Besitzer nicht gefunden"}), 404
        
        return jsonify({
            "animal": animal["name"],
            "owner": dict(owner)
        }), 200
    
    ## TODO: JOIN 
    @app.route("/api/animals/<int:animal_id>/owner/join", methods=["GET"])
    def get_owner_of_animal_by_join(animal_id):
        """
        Zeigt den Owner eines Tieres an (Mit JOIN)
        ---
        parameters:
            - name: animal_id
              in: path
              type: integer
              required: true
              description: Die ID des Tieres
        responses:
            200:
                description: Besitzer-Daten oder ggf. eine Info, dass kein Besitzer zugeordnet ist
        """
        con = get_db_connection()
        cur = con.cursor()
        result = cur.execute('''
                SELECT 
                    a.name AS animal_name,
                    o.id AS owner_id,
                    o.name AS owner_name,
                    o.email AS owner_email,
                    o.phone AS owner_phone
                FROM Animals a JOIN Owners o ON a.owner_id = o.id
                WHERE a.id = ?
                ''', (animal_id,)).fetchone()
        con.close()

        if result:
            return jsonify({
                "animal": result["animal_name"],
                "owner": {
                    "id": result["owner_id"],
                    "name": result["owner_name"],
                    "email": result["owner_email"],
                    "phone": result["owner_phone"]
                }
            }), 200
        else:
            animal = get_animal_by_id(animal_id)
            if animal is None:
                return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
            return jsonify({"message": "Tier hat keinen Besitzer"}), 200

        
    # POST /api/animals/<int:animal_id>/release
    # Tier wird wieder freigegeben, d.h. der Besitzer bzw. die owner_id wird auf Null esetzt
    @app.route("/api/animals/<int:animal_id>/release", methods=["POST"])
    def release_animal(animal_id):
        animal = get_animal_by_id(animal_id)
        if animal is None:
            return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
        if animal["owner_id"] is None:
            return jsonify({"message": f"Tier mit der ID {animal_id} hat keinen Besitzer"}), 400

        old_owner = get_owner_by_id(animal["owner_id"])
        con = get_db_connection()
        cur = con.cursor()
        cur.execute('UPDATE Animals SET owner_id = NULL WHERE id = ?', (animal_id,))
        con.commit()
        con.close()

        return jsonify({"message": f"{animal["name"]} wird nicht mehr besessen von {old_owner["name"]}"}), 200