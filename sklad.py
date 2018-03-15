# !/usr/bin/python3
import sqlite3
import datetime
import re
import unittest

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
        self.find_article_list = []
        self.ware_to_list = []
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
        self.deleted_position = ""
        self.ar_view_table_list = []
        self.am_view_table_list = []
        self.su_view_table_list = []
        self.ar_view_table_list = []
        self.po_view_table_list = []
        self.da_view_table_list = []
        self.list_of_repeat = []
        self.total = 0
        self.full_locations = 0
        self.empty_locations = 0

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
        """"Method checks on full positions than reserves position for pallet"""
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
                self.position_reserved = self.free_position[counter]
                break

        return self.position_reserved

    def new_store_unit(self):
        """Method generates range and reserves store_unit for a pallet"""
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
        """Calls methods: full_position, a new_store unit to get position and
store unit for pallet, than makes record into the database."""
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
            self.Ware_in_error = ("Wrong parameter entered (both article and amount must be entered)\n"
                                  "Article must be a string in format one capital letter followed by six numbers"
                                  ". Amount must be an positive integer")

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

            self.ware_to_list = []
            self.cursor.execute("SELECT * FROM warehouse WHERE store_unit  = ?", (store_unit,))
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute("INSERT INTO warehouse (article,amount,position, store_unit, date) "
                                    "VALUES(?,?,?,?,?)",
                                    (article, amount, row[3], store_unit, self.time))
                db.commit()
                self.message = "Amount {} of article {} successfully stored to the store unit {}, position {}" \
                    .format(amount, article, store_unit, row[3])
                self.ware_to_list.append(self.message)
            else:
                self.message = "Store unit not found"
                self.ware_to_list.append(self.message)

            return self.ware_to_list

        except (AssertionError, AttributeError):
            self.Ware_to_error = ("Wrong parameter entered (article, amount and store unit must be entered)\n"
                                  "Article must be a string in format one letter followed by six numbers\n"
                                  "Amount must be positive an integer\n"
                                  "Store unit must be a positive six character number, existing in database")

    def ware_out(self, article, amount):
        """Method filtrates data from database to get right amount of the article
from the store. First priority is removing all goods from location, then removing article by the oldest
date"""
        self.Ware_out_error = ""
        self.mo = self.regexp.search(article)
        self.deleted_position = ""
        try:
            assert (article == self.mo.group())
            assert(amount > 0)
            self.ware_out_list = []
            self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount <= ? ORDER BY date",
                                (article, amount))
            row = self.cursor.fetchone()

            while row and amount:
                amount_in_pallet = row[1]
                amount -= amount_in_pallet
                self.message = ("Removing from the store amount " + str(amount_in_pallet) + " of article " + article +
                                " position: " + row[3] + " store_unit: " + str(row[2]))
                self.ware_out_list.append(self.message)
                self.cursor.execute("DELETE FROM warehouse WHERE store_unit = ? and amount = ?", (row[2], row[1]))
                self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount <= ? ORDER BY date",
                                    (article, amount))

                row = self.cursor.fetchone()
                db.commit()

            self.cursor.execute("SELECT * FROM warehouse WHERE article = ? and amount >= ? ORDER BY date",
                                (article, amount))
            row = self.cursor.fetchone()

            if amount:
                if row:
                    amount_in_pallet = row[1]
                    rest_in_palett = amount_in_pallet - amount
                    self.cursor.execute("UPDATE warehouse SET amount = ? WHERE store_unit = ? and amount = ?",
                                        (rest_in_palett, row[2], amount_in_pallet))
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

            return self.ware_out_list

        except (AssertionError, AttributeError):
            self.Ware_out_error = ("Wrong parameter entered (both article and amount must be entered)\n"
                                   "Article must be a string in format one capital letter followed by six numbers.\n"
                                   "Amount must be an positive integer")

    def find_article(self, article):
        """Method filtrates data from database by the user's input. It searches article and counts total amount"""
        self.find_article_list = []
        self.find_article_error = ""
        self.mo = self.regexp.search(article)
        self.total = 0
        try:
            assert (article == self.mo.group())
            self.cursor.execute("SELECT * FROM warehouse WHERE article = ?", (article,))
            row = self.cursor.fetchone()
            if row:
                self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                " store_unit: " + str(row[2]))
                self.find_article_list.append(self.message)
                self.total += row[1]
                for row in self.cursor:
                    self.message = ("Article: " + row[0] + " amount: " + str(row[1]) + " position: " + row[3] +
                                    " store_unit: " + str(row[2]))
                    self.find_article_list.append(self.message)
                    self.total += row[1]
                self.find_article_list.append("Total amount of article {} is {}".format(row[0], self.total))
            else:
                self.message = "Article not found"
                self.find_article_list.append(self.message)

            return self.find_article_list

        except (AssertionError, AttributeError):
            self.find_article_error = ("Wrong parameter entered (article must be entered). Article must be a string in"
                                       " format one capital letter followed by six numbers")

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

            return self.ware_out_list

        except (AssertionError, AttributeError):
            self.find_store_unit_error = ("Wrong parameter entered (Store unit field must be entered)\n"
                                          "Store unit must be a positive six character number, existing in database")

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

            return self.ware_out_list

        except (AssertionError, AttributeError):
            self.find_position_error = ("Wrong parameter entered (position field must be entered)\n"
                                        "Position must be a string with length more than 4 characters but less "
                                        "than 9 characters")

    def view_table(self,):
        """Method displays all data in database warehouseDB with possibility of data sorting """
        self.ar_view_table_list = []
        self.am_view_table_list = []
        self.su_view_table_list = []
        self.ar_view_table_list = []
        self.po_view_table_list = []
        self.da_view_table_list = []
        self.list_of_repeat = []
        self.full_locations = 0
        self.empty_locations = 0

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
            if row[3] not in self.list_of_repeat:
                self.full_locations += 1
                self.list_of_repeat.append((row[3]))
            row = ("{:<8}{:>13}{:>13}{:>10}{:>15}".format(row[0], row[1], row[2], row[3], row[4]))
            self.po_view_table_list.append(row)

        self.empty_locations = 2820 - self.full_locations
        self.po_view_table_list.append("Full locations: {}, Empty "
                                       "locations: {}".format(self.full_locations, self.empty_locations))

        self.cursor.execute("SELECT * FROM warehouse ORDER BY Date")
        for row in self.cursor:
            row = ("{:<8}{:>13}{:>13}{:>10}{:>15}".format(row[0], row[1], row[2], row[3], row[4]))
            self.da_view_table_list.append(row)


zbozi = Warehouse()
zbozi.new_position()


class TestSkladWrongInputs(unittest.TestCase):

    def test_wrong_article_input(self):
        article = ["", " ", "0", "a", "aaaaaaa", "-1", "n10010", "n100100", "N10010", "N1001001"]
        amount = 1
        store_unit = 1
        for i in article:
            self.assertEqual(zbozi.ware_in(i, amount), None)
            self.assertEqual(zbozi.ware_to(i, amount, store_unit), None)
            self.assertEqual(zbozi.ware_out(i, amount), None)
            self.assertEqual(zbozi.find_article(i), None)

    def test_wrong_amount_input(self):
        article = "N100100"
        amount = [0, -1]
        store_unit = 1
        for i in amount:
            self.assertEqual(zbozi.ware_in(article, i), None)
            self.assertEqual(zbozi.ware_to(article, i, store_unit), None)
            self.assertEqual(zbozi.ware_out(article, i), None)

    def test_wrong_store_unit_input(self):
        article = "N100100"
        amount = 1
        store_unit = [0, -1]
        for i in store_unit:
            self.assertEqual(zbozi.ware_to(article, amount, i), None)
            self.assertEqual(zbozi.find_store_unit(i), None)

    def test_wrong_position_input(self):
        position = ["", " ", "0", "a", "-1", "1.1.", "1.1.1.1.1", "10.10.10."]
        for i in position:
            self.assertEqual(zbozi.find_position(i), None)


class TestSkladGoodInputs(unittest.TestCase):

    def test_good_input(self):
        article = "N100100"
        amount = 1
        store_unit = 1
        position = "1.1.1"
        self.assertTrue(zbozi.ware_in(article, amount), not None)
        self.assertTrue(zbozi.ware_to(article, amount, store_unit), not None)
        self.assertTrue(zbozi.ware_out(article, amount), not None)
        self.assertTrue(zbozi.find_article(article), not None)
        self.assertTrue(zbozi.find_position(position), not None)
        self.assertTrue(zbozi.find_store_unit(store_unit), not None)


if __name__ == '__main__':
    unittest.main()
