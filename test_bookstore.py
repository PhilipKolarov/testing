import unittest

from bookstore import Bookstore


class BookStoreTest(unittest.TestCase):
    BOOKS_LIMIT = 10
    BOOK = 'The Godfather'

    def setUp(self) -> None:
        self.bookstore = Bookstore(self.BOOKS_LIMIT)

    def test__init(self):
        self.assertEqual(self.bookstore.books_limit, self.BOOKS_LIMIT)
        self.assertEqual(self.bookstore.availability_in_store_by_book_titles, {})
        self.assertEqual(self.bookstore.total_sold_books, 0)

    def test_books_limit__if_less_than_zero__raise_value_error(self):
        num = -1

        with self.assertRaises(ValueError) as context:
            store = Bookstore(num)

        self.assertEqual(f"Books limit of {num} is not valid", str(context.exception))

    def test__len_bookstore(self):
        book = 'The Godfather'
        copies = 5

        self.bookstore.receive_book(book, copies)
        result = len(self.bookstore)

        self.assertEqual(result, copies)

    def test_receive_book__if_copies_greater_than_books_limit__raises(self):
        book = 'The Godfather'
        copies = 15
        with self.assertRaises(Exception) as ex:
            self.bookstore.receive_book(book, copies)

        self.assertEqual("Books limit is reached. Cannot receive more books!", str(ex.exception))

    def test_receive_book__if_book_does_not_exist_yet(self):
        book = 'The Godfather'
        copies = 5

        self.bookstore.receive_book(book, copies)

        sum = 0
        for c in self.bookstore.availability_in_store_by_book_titles.values():
            sum += int(c)

        self.assertEqual(sum, copies)

    def test_receive_book_message(self):
        book = 'The Godfather'
        copies = 5

        self.assertEqual(f"{copies} copies of {book} are available in the bookstore.", self.bookstore.receive_book(book, copies))

    def test_receive_book__if_book_already_exists(self):
        book = 'The Godfather'
        copies1 = 5
        copies2 = 3

        self.bookstore.receive_book(book, copies1)
        self.bookstore.receive_book(book, copies2)

        sum = 0
        for c in self.bookstore.availability_in_store_by_book_titles.values():
            sum += int(c)

        self.assertEqual(sum, copies1 + copies2)

    def test_sell_book__if_book_not_in_stock__raises(self):
        book = 'The Godfather'

        with self.assertRaises(Exception) as ex:
            self.bookstore.sell_book(book, 1)

        self.assertEqual(f"Book {book} doesn't exist!", str(ex.exception))

    def test_sell_book__if_book_does_not_have_enough_copies_in_stock__raises(self):
        book = 'The Godfather'
        copies = 3

        self.bookstore.receive_book(book, copies)

        with self.assertRaises(Exception) as ex:
            self.bookstore.sell_book(book, 5)

        self.assertEqual(f"{book} has not enough copies to sell. Left: {copies}", str(ex.exception))

    def test_sell_book__if_book_is_in_stock_with_enough_copies(self):
        book = 'The Godfather'
        copies = 3
        copies_sold = 2

        self.bookstore.receive_book(book, copies)
        self.bookstore.sell_book(book, copies_sold)

        copies_remaining = copies - copies_sold
        actual_remaining = self.bookstore.availability_in_store_by_book_titles[book]

        self.assertEqual(actual_remaining, copies_remaining)
        self.assertEqual(copies_sold, self.bookstore.total_sold_books)

    def test_sell_book_message(self):
        book = 'The Godfather'
        copies = 3
        copies_sold = 2

        self.bookstore.receive_book(book, copies)
        self.assertEqual(f"Sold {copies_sold} copies of {book}", self.bookstore.sell_book(book, copies_sold))

    def test__str_with_one_book(self):
        book = 'The Godfather'
        copies = 3

        self.bookstore.receive_book(book, copies)

        actual_result = f"""Total sold books: {self.bookstore.total_sold_books}
Current availability: {len(self.bookstore)}
 - {book}: {copies} copies"""

        self.assertEqual(str(self.bookstore), actual_result)

    def test__str_with_no_books(self):
        actual_result = f"""Total sold books: {self.bookstore.total_sold_books}
Current availability: {len(self.bookstore)}"""

        self.assertEqual(str(self.bookstore), actual_result)

