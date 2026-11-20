from database import get_connection
from psycopg2.extras import RealDictCursor
import logging

logger = logging.getLogger(__name__)

def kunden_abrufen(country=None):
    connection = get_connection()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            logger.info("Starte Datenbankabfrage für Kunden")
            if country is None:
                cursor.execute("""
                    SELECT
                        customerkey,
                        givenname,
                        surname,
                        city,
                        country,
                        age,
                        occupation
                    FROM customer
                    LIMIT 10;
                """)
            else:
                cursor.execute("""
                            SELECT
                                customerkey,
                                givenname,
                                surname,
                                city,
                                country,
                                age,
                                occupation
                            FROM customer
                            WHERE country = %s
                            LIMIT 10;
                        """, (country,))
            results = cursor.fetchall()
            logger.info("Datenbankabfrage erfolgreich: %s Datensätze", len(results))
            return results
        finally:
            cursor.close()
    finally:
        connection.close()

def kunden_anlegen(kunde):
    connection = get_connection()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            logger.info("Kundenerstellung gestartet %s", kunde.customerkey)
            cursor.execute("""
                INSERT INTO customer (
                    customerkey,
                    givenname,
                    surname,
                    city,
                    country,
                    age,
                    occupation
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    customerkey,
                    givenname,
                    surname,
                    city,
                    country,
                    age,
                    occupation;
            """, (
                kunde.customerkey,
                kunde.givenname,
                kunde.surname,
                kunde.city,
                kunde.country,
                kunde.age,
                kunde.occupation
            ))
            neuer_kunde = cursor.fetchone()
            connection.commit()
            logger.info("Kundenerstellung erfolgreich %s", kunde.customerkey)
            return neuer_kunde
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
    finally:
        connection.close()

def auftraege_abrufen(kunde=None):
    connection = get_connection()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            logger.info("Starte Datenbankabfrage für Aufträge")
            if kunde is None:
                cursor.execute("""
                    SELECT
                        orderkey,
                        linenumber,
                        orderdate,
                        deliverydate,
                        customerkey,
                        quantity,
                        unitprice,
                        netprice,
                        unitcost
                    FROM sales
                    LIMIT 10;
                """)
            else:
                cursor.execute("""
                            SELECT
                                orderkey,
                                linenumber,
                                orderdate,
                                deliverydate,
                                customerkey,
                                quantity,
                                unitprice,
                                netprice,
                                unitcost
                            FROM sales
                            WHERE customerkey = %s
                            LIMIT 10;
                        """, (kunde,))
            results = cursor.fetchall()
            logger.info("Datenbankabfrage erfolgreich: %s Datensätze", len(results))
            return results
        finally:
            cursor.close()
    finally:
        connection.close()

def auftrag_anlegen(auftrag):
    connection = get_connection()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            logger.info("Erstellung in Datenbank gestartet %s", auftrag.orderkey)
            cursor.execute("""
                INSERT INTO sales (
                    orderkey,
                    linenumber,
                    orderdate,
                    deliverydate,
                    customerkey,
                    quantity,
                    unitprice,
                    netprice,
                    unitcost
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    orderkey,
                    linenumber,
                    orderdate,
                    deliverydate,
                    customerkey,
                    quantity,
                    unitprice,
                    netprice,
                    unitcost;
            """, (
                auftrag.orderkey,
                auftrag.linenumber,
                auftrag.orderdate,
                auftrag.deliverydate,
                auftrag.customerkey,
                auftrag.quantity,
                auftrag.unitprice,
                auftrag.netprice,
                auftrag.unitcost
            ))
            neuer_auftrag = cursor.fetchone()
            connection.commit()
            logger.info("Erstellung in Datenbank erfolgreich %s", auftrag.orderkey)
            return neuer_auftrag
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
    finally:
        connection.close()