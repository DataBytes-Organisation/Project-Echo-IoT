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

    # Because of the way that mqtt library uses multiple threads, we can't share
    # database cursors/connections between the threads.
    # So instead, we must connect and disconnect for every transaction.  Individual threads will make their own cursor
    # this is ok, as the database is configured in WAL mode, allowing multiple threads to access database at same time

    def connect(self):

        if not self.connected:

            self.connection = sqlite3.connect('gateway.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute('PRAGMA journal_mode=wal')
            self.connected = True

        else:
            time.sleep(1)

    def disconnect(self):

        if self.connected:
            self.cursor.close()
            self.connection.close()
            self.connected = False
            self.cursor = None
            self.connection = None


    def insert_header_and_empty_pieces(self, node_id, number_of_pieces,image_id, filename):

        self.connect()

        #First, insert the header

        self.cursor.execute('INSERT INTO Headers (Node_id, Image_id, numberofpieces, filename) VALUES (?, ?, ?, ?)',
                            (node_id, image_id, number_of_pieces, filename))

        #generate and insert a new piece for each
        for i in range(number_of_pieces+1):

            self.cursor.execute('INSERT INTO Pieces (Node_id, Image_id, Piece_id) VALUES (?, ?, ?)',(node_id, image_id, i))

        self.connection.commit()

        self.disconnect()

        return True

    def insert_a_piece(self, node_id, image_id, piece_id, piece):

        self.connect()

        self.cursor.execute('UPDATE Pieces SET piece = ?, received = 1 WHERE Node_id = (?) and Image_id = (?) and Piece_id = (?);',(piece,node_id,image_id,piece_id))
        self.connection.commit()

        self.disconnect()

    def find_empty_piece(self):

        self.connect()

        #find any empty piece and request it from the Node.  We want to random the selection of piece, in case we are waiting for a piece already requested.
        # when there are lots of pieces to request, this will be good, but as available pieces are reduced, the retries for specific pieces will be more prevalent

        row = self.cursor.execute(
            'SELECT * FROM Pieces WHERE received = ? ORDER BY RANDOM() LIMIT 1;',
            (0,)
        ).fetchone()
        self.disconnect()
        return row




    def get_unique_image_ids(self):

        #simply return a list of unique image ids
        self.connect()

        image_ids = []

        for row in self.cursor.execute('SELECT DISTINCT Image_id FROM Pieces WHERE Image_id is NOT NULL;'):
            image_ids.append(row[0])

        self.disconnect()
        return image_ids


    def find_ready_to_compile_image_ids(self):

        self.connect()

        image_ids = []
        # find not complete not received Headers
        for row in self.cursor.execute('SELECT Node_id, Image_id, filename FROM Headers WHERE complete = 0;'):
            image_ids.append(row)

        # iterate through the list
        completed_image_ids = []
        for each_image_id in image_ids:

            node_id = each_image_id[0]
            image_id = each_image_id[1]
            filename = each_image_id[2]
            if self.image_complete(node_id, image_id):

                all_pieces = self.get_all_pieces(node_id, image_id)

                with open(filename, 'wb') as file:
                    print(f"Image {image_id} from {node_id} is complete.  Writing out {filename}")
                    for chunk in all_pieces:
                        file.write(chunk[0])
                self.cursor.execute(
                    'UPDATE Headers SET complete =1 WHERE Node_id = (?) and Image_id = (?);',
                    (node_id, image_id))
                self.connection.commit()

        self.disconnect()



    def get_all_pieces(self, node_id, image_id):

        # self.connect()

        # find any empty piece and request it from the Node
        pieces = []

        for row in self.cursor.execute('SELECT piece FROM Pieces WHERE Node_id = (?) and Image_id = (?)',
                                       (node_id, image_id)):
            pieces.append(row)

        # self.disconnect()
        return pieces


    def image_complete(self, node_id, image_id):

        # self.connect()

        for row in self.cursor.execute('SELECT CASE WHEN COUNT(*) = COUNT(CASE WHEN received = 1 THEN 1 END) THEN 1 ELSE 0 END AS all_received FROM Pieces WHERE Image_id = ? and Node_id = ?;',(image_id,node_id)):
            return row[0]
        # self.disconnect()
        return False

    def delete_image(self, image_id):

        self.connect()
        self.cursor.execute(
            'DELETE from Pieces WHERE Image_id = (?)',(image_id,))
        self.connection.commit()

        self.disconnect()
