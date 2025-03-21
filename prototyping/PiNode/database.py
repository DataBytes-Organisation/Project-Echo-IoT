import datetime
import sqlite3
import time
import os


class Database:


    def __init__(self):


        self.connection = None
        self.config = None
        self.cursor = None

        self.connected = False

    def connect(self):

        if not self.connected:

            self.connection = sqlite3.connect('node.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute('PRAGMA journal_mode=wal')
            self.connected = True

    def disconnect(self):

        if self.connected:
            self.cursor.close()
            self.connection.close()
            self.connected = False
            self.cursor = None
            self.connection = None

    def insert_piece(self, piece, piece_id, image_id):

        self.connect()

        self.cursor.execute('INSERT INTO Pieces (Image_id, Piece_id, piece) VALUES (?, ?, ?)',(image_id, piece_id, piece))

        self.connection.commit()

        self.disconnect()
        return True


    def insert_header(self, header):

        self.connect()

        self.cursor.execute('INSERT INTO Headers (Image_id, numberofpieces, filename) VALUES (?, ?, ?)',
                            (header[0], header[1], header[2]))

        self.connection.commit()
        self.disconnect()
        return True

    def get_unsent_header(self):

        self.connect()

        for row in self.cursor.execute('SELECT * FROM Headers WHERE received = ? LIMIT 1', (0,)):
            return row
        self.disconnect()
        return None

    def get_unsent_request(self):

        self.connect()

        for row in self.cursor.execute('SELECT * FROM Pieces WHERE requested = ? LIMIT 1', (1,)):
            return row
        self.disconnect()
        return None


    def request_piece(self, image_id, piece_id):

        self.connect()

        self.cursor.execute('UPDATE Pieces SET requested = 1 WHERE Image_id = (?) and Piece_id = (?);',(image_id,piece_id))
        self.connection.commit()
        self.disconnect()
    def reset_request(self, image_id, piece_id):

        self.connect()

        self.cursor.execute('UPDATE Pieces SET requested = 0 WHERE Image_id = (?) and Piece_id = (?);',(image_id,piece_id))
        self.connection.commit()
        self.disconnect()
    def ack_header(self, image_id):

        self.connect()

        self.cursor.execute('UPDATE Headers SET received = 1 WHERE Image_id = (?);',(image_id,))
        self.connection.commit()
        self.disconnect()
    def insert_battery_status(self, status):

        self.connect()

        timestamp = datetime.datetime.now()

        self.cursor.execute('INSERT INTO battery_log (timestamp, status) VALUES (?,?);', (timestamp, status))
        self.connection.commit()
        self.disconnect()