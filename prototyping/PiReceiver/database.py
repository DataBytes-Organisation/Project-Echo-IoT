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

            self.connection = sqlite3.connect('gateway.db')
            self.cursor = self.connection.cursor()
            self.cursor.execute('PRAGMA journal_mode=wal')
            self.connected = True



    def insert_empty_pieces(self, node_id, number_of_pieces,image_id):

        self.connect()

        #generate and insert a new piece for each
        for i in range(number_of_pieces+1):

            self.cursor.execute('INSERT INTO Pieces (Node_id, Image_id, Piece_id) VALUES (?, ?, ?)',(node_id, image_id, i))

        self.connection.commit()

        return True

    def insert_a_piece(self, node_id, image_id, piece_id, piece):

        self.connect()

        self.cursor.execute('UPDATE Pieces SET piece = ?, received = 1 WHERE Node_id = (?) and Image_id = (?) and Piece_id = (?);',(piece,node_id,image_id,piece_id))
        self.connection.commit()



    def find_empty_piece(self):

        self.connect()

        #find any empty piece and request it from the Node

        for row in self.cursor.execute('SELECT * FROM Pieces WHERE received = ? LIMIT 1', (0,)):
            return row
        return None

    def get_all_pieces(self, node_id, image_id):

        self.connect()

        #find any empty piece and request it from the Node
        pieces = []

        for row in self.cursor.execute('SELECT * FROM Pieces WHERE Node_id = (?) and Image_id = (?)', (node_id,image_id)):
            pieces.append(row)
        return pieces