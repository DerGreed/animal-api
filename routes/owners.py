from database.database import get_db_connection, get_cursor
from flask import jsonify, request
from lib.helper_functions import get_owner_by_id, get_animal_by_id

KEY_LIST = ['name', 'email', 'phone']
KEY_LIST.sort()

def register_owner_routes(app):
    ## GET-Route implementieren, d.h. Daten abrufen bzw. alle Owner anzeigen
    @app.route("/api/owners", methods=['GET'])
    def show_owners():
        """
        Liste aller Besitzer
        ---
        responses:
            200:
                description: JSON-Liste aller Besitzer
                examples:
                    application/json:
                    -
                        id: 1
                        name: Max Mustermann
                        email: max_mustermann@email.de
                        phone: 01234 56789
                    -
                        id: 2
                        name: Anna Schmidt
                        email: anna_schmidt@email.de
                        phone: 0987 65432
        """
        # Daten abrufen von der DB
        con = get_db_connection() # Verbindung mit der DB
        cur = get_cursor(con)
        cur.execute('SELECT * FROM Owners')
        owners = cur.fetchall()
        con.close()
        return jsonify(owners), 200


    ## GET-Route implementieren, um Daten von einem Owner anzuzeigen
    @app.route("/api/owners/<int:owner_id>", methods=['GET'])
    def show_owner(owner_id):
        """
        Anzeigen eines Besitzers
        ---
        parameters:
            - name: owner_id
              in: path
              type: integer
              required: true
              description: Die ID des anzuzeigenden Besitzers
        responses:
            200:
                description: JSON-Objekt von einem Besitzer
                examples:
                    application/json:
                        id: 1
                        name: Max Mustermann
                        email: max_mustermann@email.de 
                        phone: 01234 56789
            404:
                description: Besitzer wurde nicht gefunden
                examples:
                    application/json:
                        message: Besitzer mit der ID 5 existiert nicht
        """
        owner = get_owner_by_id(owner_id)
        if owner is None:
            return jsonify({"message": f"Besitzer mit der ID {owner_id} existiert nicht"}), 404
        return jsonify(owner), 200


    @app.route("/api/owners", methods=['POST'])
    def add_owner():
        """
        Neuen Besitzer hinzufügen
        ---
                 
        consumes: [application/json]
        parameters:
        -
            in: body
            name: Besitzer
            required: true
            description: name muss angegeben werden
            schema:
                type: object
                required: [name]
                properties:
                    name:
                        type: string
                        example: Max Mustermann
                    email:
                        type: string
                        example: max@email.com
                    phone:
                        type: string
                        example: 0123 456789
        responses:
            201:
                description: Besitzer wurde erfolgreich hinzugefügt
                examples:
                    application/json:
                        message: Besitzer wurde erfolgreich hinzugefügt
            400:
                description: Keine oder fehlerhafte Daten übertragen
                examples:
                    application/json:
                        message: Keine oder fehlerhafte Daten übertragen
        """
        new_owner: dict
        new_owner = request.get_json()
        if not new_owner or 'name' not in new_owner:
            return jsonify({"message": "Keine oder fehlerhafte Daten übertragen"}), 400
        con = get_db_connection()
        cur = get_cursor(con)
        values = [new_owner[key] if key in new_owner.keys() else None for key in KEY_LIST]
        keys = ', '.join(KEY_LIST)
        cur.execute('INSERT INTO Owners (' + keys + ') VALUES (%s,%s,%s)', (*values, ))
        con.commit()
        con.close()
        return jsonify({"message": "Besitzer wurde erfolgreich hinzugefügt"}), 201



    @app.route("/api/owners/<int:owner_id>", methods=['DELETE'])
    def delete_owner(owner_id):
        """
        Einen Besitzer löschen
        ---
        parameters:
        -
            name: owner_id
            in: path
            type: integer
            required: true
            description: Die ID des zu löschenden Besitzers
        responses:
            200:
                description: Besitzer wurde gelöscht
                examples:
                    application/json:
                        message: Besitzer wurde erfolgreich gelöscht
            404:
                description: Besitzer wurde nicht gefunden
                examples:
                    application/json:
                        message: Besitzer mit der ID 5 existiert nicht
        """
        con = get_db_connection()
        # Überprüfe, ob das Tier mit der angegebenen ID überhaupt existiert
        owner = get_owner_by_id(owner_id, con)
        if owner is None:
            con.close()
            return jsonify({"message": "Besitzer mit dieser ID existiert nicht"}), 404
        cur = get_cursor(con)
        cur.execute('DELETE FROM Owners WHERE id = %s', (owner_id,) )
        con.commit()
        con.close()
        return jsonify({"message": "Besitzer wurde erfolgreich gelöscht"}), 200

    ## Baue eine Funktion, zum Updaten

    ## PUT-Route -> Ersetze alle Eigenschaften eines Besitzers, d.h. hier schicken wir alle Eigenschaften im Body als JSON mit
    @app.route("/api/owners/<int:owner_id>", methods=['PUT'])
    def put_owner(owner_id):
        """
        Besitzer aktualisieren im Ganzen
        ---
        parameters:
        -
            name: owner_id
            in: path
            type: integer
            required: true
            description: Die ID des Besitzers, der ersetzt werden soll
        -
            in: body
            name: tier
            required: true
            description: name muss angegeben werden
            schema: 
                type: object
                required: [name]
                properties:
                    name:
                        type: string
                        example: max mustermann
                    email:
                        type: string
                        example: max@mail.de
                    phone:
                        type: string
                        example: 0123 456789
        responses:
            200:
                description: Besitzer wurde aktualisiert
                examples:
                    application/json:
                        message: Besitzer wurde komplett aktualisiert
            404:
                description: Besitzer wurde nicht gefunden
                examples:
                    application/json:
                        message: Besitzer mit der ID 7 existiert nicht
        """
        updated_owner: dict
        updated_owner = request.get_json() # Speichere dir das Objekt im Body aus dem Request des Clients
        if not updated_owner or 'name' not in updated_owner:
            return jsonify({"message": "Fehlende Daten"}), 400
        con = get_db_connection()
        owner = get_owner_by_id(owner_id, con)
        if owner is None:
            con.close()
            return jsonify({"message": f"Besitzer mit der ID {owner_id} existiert nicht"}), 404
        # Update jetzt den Besitzer mit der übergebenen ID und mit den übergebenen Daten
        cur = get_cursor(con)
        # cur.execute('UPDATE Owners SET name = %s, email = %s, phone = %s WHERE id = %s', (updated_owner['name'], updated_owner['email'], updated_owner['phone'], owner_id))
        values = [updated_owner[key] if key in updated_owner.keys() else None for key in KEY_LIST]
        keys = ', '.join([key + ' = %s' for key in KEY_LIST])
        cur.execute('UPDATE Owners SET ' + keys + ' WHERE id = %s', (*values, owner_id))
        con.commit()
        con.close()
        return jsonify({"message": "Besitzer wurde komplett aktualisiert"}), 200




    ## PATCH-Route -> Ersetze spezifisch einzelne Eigenschaften, d.h. hier schicken wir nur die zu ändernden Eigenschaften im Body als JSON mit
    ## Owners
    @app.route("/api/owners/<int:owner_id>", methods=["PATCH"])
    def patch_owner(owner_id):
        """
        Besitzer teilweise ändern (z.B. nur die Email)
        ---
        parameters:
        -
            name: owner_id
            in: path
            type: integer
            required: true
            description: Die ID des Besitzers, der aktualisiert werden soll
        -
            in: body
            name: besitzer
            required: true
            description: Es muss mindestens einer der Werte angegeben werden
            schema: 
                type: object
                required: anyOf
                properties:
                    id:
                        type: integer
                        example: 3
                    name:
                        type: string
                        example: lisa schmidt
                    email:
                        type: string
                        example: lisaschmidt@mail.de
                    phone:
                        type: string
                        example: 012-2345
        responses:
            200:
                description: Besitzer wurde geupdated
                examples:
                    application/json:
                        message: Besitzer wurde geupdated
            404:
                description: Besitzer wurde nicht gefunden
                examples:
                    application/json:
                        message: Besitzer mit der ID 7 existiert nicht
        """
        updated_owner: dict
        updated_owner = request.get_json()
        if not updated_owner:
            return jsonify({"message": "Fehlende Daten"}), 400
        con = get_db_connection()
        cur = get_cursor(con)
        owner = get_owner_by_id(owner_id, con)
        if owner is None:
            con.close()
            return jsonify({"message": f"Besitzer mit der ID {owner_id} existiert nicht"}), 404
        key_list = [key for key in KEY_LIST if key in updated_owner.keys()]
        if key_list:
            values = [updated_owner[key] for key in key_list]
            keys = ', '.join([key + ' = %s' for key in key_list])
            cur.execute('UPDATE Owners SET ' + keys + ' WHERE id = %s', (*values, owner_id))
            con.commit()
        con.close()
        return jsonify({"message": "Besitzer wurde geupdated"}), 200

    # POST /api/owners/<int:owner_id>/adopt/<int:animal_id>
    # Route, damit ein Besitzer ein Tier adoptieren kann
    @app.route("/api/owners/<int:owner_id>/adopt/<int:animal_id>", methods=["POST"])
    def adopt_animal(owner_id, animal_id):
        """
        Ein Tier durch einen Besitzer adoptieren lassen
        ---
        parameters:
        -
            name: owner_id
            in: path
            type: integer
            required: true
            description: Die ID des neuen Besitzers
        -
            name: animal_id
            in: path
            type: integer
            required: true
            description: Die ID des adoptierten Tieres
        responses:
            200:
                description: Tier wurde erfolgreich adoptiert
                examples:
                    application/json:
                        message: Max Mustermann hat Elephant adoptiert
            400:
                description: Tier gehört dem Besitzer bereits
                examples:
                    application/json:
                        message: Katze gehört bereits Anna Schmidt
            404:
                description: Tier wurde nicht gefunden oder Besitzer wurde nicht gefunden
                examples:
                    application/json:
                        message: Tier mit der ID 7 existiert nicht
        """
        con = get_db_connection()
        owner = get_owner_by_id(owner_id, con)
        if owner is None:
            con.close()
            return jsonify({"message": f"Besitzer mit der ID {owner_id} existiert nicht"}), 404
        animal = get_animal_by_id(animal_id, con)
        if animal is None:
            con.close()
            return jsonify({"message": f"Tier mit der ID {animal_id} existiert nicht"}), 404
        if animal["owner_id"] is not None:
            current_owner = get_owner_by_id(animal["owner_id"], con)
            con.close()
            return jsonify({"message": f"{animal["name"]} gehört bereits {current_owner["name"]}"}), 400
        # Falls das alles nicht zutrifft, kann die Adoption stattfinden
        cur = get_cursor(con)
        cur.execute('UPDATE Animals SET owner_id = %s WHERE id = %s', (owner_id, animal_id))
        con.commit()
        con.close()

        return jsonify({"message": f"{owner["name"]} hat {animal["name"]} adoptiert"}), 200
        
