import sqlite3
import datetime
import re

db = sqlite3.connect("warehouseDB.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS warehouse"
           "(article TEXT, amount INTEGER, store_unit INTEGER, position TEXT, date TEXT)")


class Warehouse:
    """Contains methods for editing main database warehouseDB: new_position, full_position, new_store_unit, ware_in,
       ware_out
       and methods for query a content of the man database: view_table, find_article, find_store_unit,
       find_position."""

    def __init__(self):
        self.cursor = db.cursor()
        self.time = datetime.date.today()
        self.free_position = []
        self.ware_out_list = []
        self.position_reserved = None
        self.store_unit = None
        self.article = None
        self.amount = None
        self.message = ""
        self.position_reserved = ""
        self.Positions_error = ""
        self.Ware_in_error = ""
        self.Ware_to_error = ""
        self.Ware_out_error = ""
        self.find_article_error = ""
        self.find_store_unit_error = ""
        self.find_position_error = ""
        self.regexp = re.compile(r"[A-Z]\d{6}")
        self.mo = ""
        self.store_unit = ""
        self.ar_view_table_list = []
        self.am_view_table_list = []
        self.su_view_table_list = []
        self.ar_view_table_list = []
        self.po_view_table_list = []
        self.da_view_table_list = []

    def new_position(self):
        """Method generates all position in warehouse. 1 shelf has 47 row and 6 floor. Then it saves them in the list"""
        for i in range(1, 11):
            shelf = i
            for y in range(1, 48):
                row = y
                for x in range(1, 7):
                    floor = x
                    self.free_position.append(str(shelf) + "." + str(row) + "." + str(floor))
        return self.free_position

    def full_position(self):
        """"Method checks on all free_position and assignments reserved position"""
        self.position_reserved = ""
        counter = 0
        for position in self.free_position:
            self.cursor.execute("SELECT position FROM warehouse WHERE position = ?", (position,))
            row = self.cursor.fetchone()
            if row:
                counter += 1
                if counter == 2820:
                    self.position_reserved = "full"
                    break
                continue
            else:
                self.position_reserved = self.free_position.pop(counter)
                break

        return self.position_reserved

    def new_store_unit(self):
        """Method generates range and assignments store_unit to a pallet"""
        counter = 0
        for free_store_unit in range(1, 9999999999):
            self.cursor.execute("SELECT store_unit FROM warehouse WHERE store_unit  = ?", (free_store_unit,))
            row = self.cursor.fetchone()
            if row:
                counter += 1
                continue
            else:
                self.store_unit = free_store_unit
                break
        return self.store_unit

    def ware_in(self, article, amount):
        """Method checks on validity user's input then calls methods full_position, a new_store unit to get position and
store unit for pallet, takes arguments, than makes record into the database."""
        self.new_position()
        self.full_position()
        self.new_store_unit()
        self.Ware_in_error = ""
        self.Positions_error = ""
        self.mo = self.regexp.search(article)

        try:
            assert (article == self.mo.group())
            assert(amount > 0)
            assert(self.position_reserved is not "full")

            self.article = article
            self.amount = amount
            self.cursor.execute("INSERT INTO warehouse (article,amount,position, store_unit, date) VALUES(?,?,?,?,?)",
                                (article, amount, self.position_reserved, self.store_unit, self.time))
            ware_message = "Amount {} of article {} successfully stored in the warehouse".format(amount, article)
            db.commit()
            return ware_message
        except (AssertionError, AttributeError):
            self.Ware_in_error = ("Wrong parameter entered (both article and amount must be dialed)\n"
                                  "Article must be a string in format one letter followed by six numbers\n"
                                  "Amount must be an positive integer")

            if self.position_reserved == "full":
                self.Positions_error = "All positions are full"

    def ware_to(self, article, amount, store_unit):
        """Method enables store the goods in the pallet, on already existing store unit and location. """
        self.Ware_to_error = ""
        self.mo = self.regexp.search(article)
        try:
            assert (article == self.mo.group())
            assert(amount > 0)
            assert (store_unit > 0)

            self.ware_out_list = []
            self.cursor.execute("SELECT * FROM warehouse WHERE store_unit  = ?", (store_unit,))
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute("INSERT INTO warehouse (article,amount,position, store_unit, date) "
                                    "VALUES(?,?,?,?,?)",
                                    (article, amount, row[3], store_unit, self.time))
                db.commit()
                self.message = "Amount {} of article {} successfully stored to the store unit {}, position {}" \
                    .format(amount, article, store_unit, row[3])
                self.ware_out_list.append(self.message)
            else:
                self.message = "Store unit not found"
                self.ware_out_list.append(self.message)

            return self.ware_out_list

        except (AssertionError, AttributeError):
            self.Ware_to_error = ("Wrong parameter entered (both article and amount must be dialed)\n"
                                  "Article must be a string in format one letter followed by six numbers\n"
                                  "Amount must be positive an integer\n"
                                  "Store unit must be a positive six character number, existing in database")

    def ware_out(self, article, amount):
        """Method checks on validity user's input then filtrates data from database to get right amount of the article
from the store. First priority is removing all goods from location, then removing article by the oldest
date (FIFO)"""
        self.Ware_out_error = ""
        self.mo = self.regexp.search(article)
        try:
            assert (article == self.mo.group())
            assert(amount > 0)
            self.ware_out_list = []
            self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount <= ? ORDER BY date",
                                (article, amount))
            row = self.cursor.fetchone()

            while row and amount:
                amount_in_palett = row[1]
                amount -= amount_in_palett
                self.message = ("Removing from the store amount " + str(amount_in_palett) + " of article " + article +
                                " position: " + row[3] + " store_unit: " + str(row[2]))
                self.ware_out_list.append(self.message)
                self.cursor.execute("DELETE FROM warehouse WHERE store_unit = ? and amount = ?", (row[2], row[1]))
                self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount <= ? ORDER BY date",
                                    (article, amount))
                db.commit()
                row = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount >= ? ORDER BY date",
                                (article, amount))
            row = self.cursor.fetchone()

            if amount:
                if row:
                    amount_in_palett = row[1]
                    rest_in_palett = amount_in_palett - amount
                    self.cursor.execute("UPDATE warehouse SET amount = ? WHERE store_unit = ? and amount = ?",
                                        (rest_in_palett, row[2], amount_in_palett))
                    self.message = ("Removing from the store amount " + str(amount) + " of article " + article +
                                    " position: " + row[3] + " store_unit: " + str(row[2]))
                    self.ware_out_list.append(self.message)
                    db.commit()
                elif row is None:
                    self.message = "insufficient amount of Article!"
                    self.ware_out_list.append(self.message)
                    self.message = ("Missing amount " + str(amount) + " of article " + article)
                    self.ware_out_list.append(self.message)
            else:
                self.message = ("Article " + article + " war successfully delivered from the Store")
                self.cursor.connection.commit()
                self.ware_out_list.append(self.message)

        except (AssertionError, AttributeError):
            self.Ware_out_error = ("Wrong parameter entered (both article and amount must be dialed)\n"
                                   "Article must be a string in format one letter followed by six numbers\n"
                                   "Amount must be positive an integer")
        return self.ware_out_list

    def find_article(self, article, amount=None):
        """Method filtrates data from database by the user's input. Parameter 'amount' is optional"""
        self.ware_out_list = []
        self.find_article_error = ""
        self.mo = self.regexp.search(article)
        try:
            assert (article == self.mo.group())
            if amount:
                assert(amount > 0)
            if article and not amount:
                self.cursor.execute("SELECT * FROM warehouse WHERE article = ?", (article,))
                row = self.cursor.fetchone()
                if row:
                    self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                    " store_unit: "
                                    + str(row[2]))
                    self.ware_out_list.append(self.message)
                    for row in self.cursor:
                        self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                        " store_unit: " + str(row[2]))
                        self.ware_out_list.append(self.message)
                else:
                    self.message = "Article not found"
                    self.ware_out_list.append(self.message)

            elif article and amount:
                self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount >= ?", (article, amount))
                row = self.cursor.fetchone()
                if row:
                    self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                    " store_unit: "
                                    + str(row[2]))
                    self.ware_out_list.append(self.message)
                    for row in self.cursor:
                        self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                        " store_unit: " + str(row[2]))
                        self.ware_out_list.append(self.message)
                elif row is None:
                    self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount <= ? ORDER BY amount",
                                        (article, amount))
                    row = self.cursor.fetchone()
                    if row:
                        amount_in_palett = row[1]
                        amount -= amount_in_palett
                        self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                        " store_unit: " + str(row[2]))
                        self.ware_out_list.append(self.message)
                        for row in self.cursor:
                            amount_in_palett = row[1]
                            if (amount - amount_in_palett) >= 0:
                                amount -= amount_in_palett
                                self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: "
                                                + row[3] + " store_unit: " + str(row[2]))
                                self.ware_out_list.append(self.message)
                            elif (amount - amount_in_palett) < 0:
                                amount -= amount
                                self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: "
                                                + row[3] + " store_unit: " + str(row[2]))
                                self.ware_out_list.append(self.message)
                        if amount:
                            self.message = ("insufficient amount of article, missing: " + str(amount))
                            self.ware_out_list.append(self.message)
                    else:
                        self.message = "Article not found"
                        self.ware_out_list.append(self.message)
            else:
                self.message = "Article not found"
                self.ware_out_list.append(self.message)
        except (AssertionError, AttributeError):
            self.find_article_error = ("Wrong parameter dialed (article must be entered, amount field is optional)\n"
                                       "Article must be a string in format one letter followed by six numbers\n"
                                       "Amount must be positive an integer")
        return self.ware_out_list

    def find_store_unit(self, store_unit):
        """Method checks the database on the specific store unit"""
        self.ware_out_list = []
        self.find_store_unit_error = ""
        try:
            assert (store_unit > 0)

            self.cursor.execute("SELECT * FROM warehouse WHERE store_unit = ?", (store_unit,))
            row = self.cursor.fetchone()
            if row:
                self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                " store_unit: "
                                + str(row[2]))
                self.ware_out_list.append(self.message)
                for row in self.cursor:
                    self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                    " store_unit: " +
                                    str(row[2]))
                    self.ware_out_list.append(self.message)
            else:
                self.message = "Store_unit not found"
                self.ware_out_list.append(self.message)

        except (AssertionError, AttributeError):
            self.find_store_unit_error = ("Wrong parameter entered (Store unit field must be dialed)\n"
                                          "Store unit must be a positive six character number, existing in database")
        return self.ware_out_list

    def find_position(self, position):
        """Method checks the database on the specific position"""
        self.ware_out_list = []
        self.find_position_error = ""
        try:
            assert (len(position) >= 5)
            assert (len(position) < 9)

            self.cursor.execute("SELECT * FROM warehouse WHERE position = ?", (position,))
            row = self.cursor.fetchone()
            if row:
                self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                " store_unit: " + str(row[2]))
                self.ware_out_list.append(self.message)
                for row in self.cursor:
                    self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                    " store_unit: " + str(row[2]))
                    self.ware_out_list.append(self.message)
            else:
                self.message = "Position not found"
                self.ware_out_list.append(self.message)

        except (AssertionError, AttributeError):
            self.find_position_error = ("Wrong parameter entered (position field must be dialed)\n"
                                        "Position must be a string with length more than 4 characters but less "
                                        "than 9 characters")
        return self.ware_out_list

    def view_table(self,):
        """Method displays all data in database warehouseDB with possibility of data sorting """
        self.ar_view_table_list = []
        self.am_view_table_list = []
        self.su_view_table_list = []
        self.ar_view_table_list = []
        self.po_view_table_list = []
        self.da_view_table_list = []

        self.cursor.execute("SELECT * FROM warehouse ORDER BY Article")
        for row in self.cursor:
            row = ("{:<8}{:>13}{:>13}{:>10}{:>15}".format(row[0], row[1], row[2], row[3], row[4]))
            self.ar_view_table_list.append(row)
        self.cursor.execute("SELECT * FROM warehouse ORDER BY Amount")
        for row in self.cursor:
            row = ("{:<8}{:>13}{:>13}{:>10}{:>15}".format(row[0], row[1], row[2], row[3], row[4]))
            self.am_view_table_list.append(row)
        self.cursor.execute("SELECT * FROM warehouse ORDER BY Store_unit")
        for row in self.cursor:
            row = ("{:<8}{:>13}{:>13}{:>10}{:>15}".format(row[0], row[1], row[2], row[3], row[4]))
            self.su_view_table_list.append(row)
        self.cursor.execute("SELECT * FROM warehouse ORDER BY Position")
        for row in self.cursor:
            row = ("{:<8}{:>13}{:>13}{:>10}{:>15}".format(row[0], row[1], row[2], row[3], row[4]))
            self.po_view_table_list.append(row)
        self.cursor.execute("SELECT * FROM warehouse ORDER BY Date")
        for row in self.cursor:
            row = ("{:<8}{:>13}{:>13}{:>10}{:>15}".format(row[0], row[1], row[2], row[3], row[4]))
            self.da_view_table_list.append(row)


zbozi = Warehouse()
zbozi.new_position()
