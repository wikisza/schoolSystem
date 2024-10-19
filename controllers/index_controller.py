import sqlite3


def get_reservations():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        query = '''
            SELECT imie||' '||nazwisko AS gosc, data_od, data_do, id_pokoju
            FROM rezerwacje
        '''
        cursor.execute(query)
        rezerwacje = cursor.fetchall()
        return rezerwacje
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_old_reservations():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        query = '''
            SELECT imie||' '||nazwisko AS gosc, data_od, data_do, id_pokoju
            FROM historia_rezerwacji
        '''
        cursor.execute(query)
        stare = cursor.fetchall()
        return stare
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
