from database.database import get_db_connection, get_cursor
from flask import jsonify, request
from lib.helper_functions import get_animal_count, get_owner_count


def register_statistics_routes(app):
    # Statistik-Route, um Daten aus beiden Tabellen anzuzeigen
    @app.route("/api/stats", methods=["GET"])
    def get_statistics():
        """
        Statistiken über Tiere und Besitzer
        ---
        responses:
            200:
                description: Statistiken über Tiere und Besitzer
                examples:
                    application/json:
                        animal_by_genus:
                            birds: 1,
                            mammals: 3
                        total_animals: 5
                        total_owners: 2
        """
        con = get_db_connection()
        cur = get_cursor(con)
        animal_count = get_animal_count(con)
        owner_count = get_owner_count(con)
        # Nach Gattung filtern
        cur.execute(
            '''
            SELECT genus, COUNT(*) as count FROM Animals
            WHERE genus IS NOT NULL
            GROUP BY genus
            '''
        )

        genus_stats = cur.fetchall()

        con.close()
        stats = {
            "total_animals": animal_count,
            "total_owners": owner_count,
            "animals_by_genus": {row["genus"]: row["count"] for row in genus_stats}
        }

        return jsonify(stats), 200