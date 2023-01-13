from django.db import models, DataError
from django.urls import reverse

from authentication.models import CustomUser
from book.models import Book
from datetime import datetime as dt, timedelta


class Order(models.Model):
    """
           This class represents an Order. \n
           Attributes:
           -----------
           param book: foreign key Book
           type book: ForeignKey
           param user: foreign key CustomUser
           type user: ForeignKey
           param created_at: Describes the date when the order was created. Can't be changed.
           type created_at: int (timestamp)
           param end_at: Describes the actual return date of the book. (`None` if not returned)
           type end_at: int (timestamp)
           param plated_end_at: Describes the planned return period of the book (2 weeks from the moment of creation).
           type plated_end_at: int (timestamp)
       """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None, verbose_name='Товар')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, verbose_name='Заказник')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')
    end_at = models.DateTimeField(default=None, null=True, blank=True, verbose_name='Кінець')
    plated_end_at = models.DateTimeField(default=dt.now() + timedelta(days=14), verbose_name='Плановий кінець')

    class Meta:
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'
        ordering = ['-created_at']
        # permissions = [
        #     ('read_orders', 'Can read orders'), # visitor(himself), librarian(all), admin(all)
        #     ('delete_orders', 'Can delete orders'),  # admin
        #     ('change_orders', 'Can change orders'),  # librarian, admin -- (open/close orders)
        #     ('add_order', 'Can add order'),  # visitor
        # ]

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        # if self.end_at == None:
        #     return f"\'id\': {self.pk}, " \
        #            f"\'user\': CustomUser(id={self.user.pk})," \
        #            f" \'book\': Book(id={self.book.pk})," \
        #            f" \'created_at\': \'{self.created_at}\'," \
        #            f" \'end_at\': {self.end_at}," \
        #            f" \'plated_end_at\': \'{self.plated_end_at}\'"
        # else:
        #     return f"\'id\': {self.pk}, " \
        #            f"\'user\': CustomUser(id={self.user.pk})," \
        #            f" \'book\': Book(id={self.book.pk})," \
        #            f" \'created_at\': \'{self.created_at}\'," \
        #            f" \'end_at\': \'{self.end_at}\'," \
        #            f" \'plated_end_at\': \'{self.plated_end_at}\'"
        return f'{self.pk}, {self.book}, {self.user}'

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self. id})'

    def to_dict(self):
        """
                :return: order id, book id, user id, order created_at, order end_at, order plated_end_at
                :Example:
                | {
                |   'id': 8,
                |   'book': 8,
                |   'user': 8',
                |   'created_at': 1509393504,
                |   'end_at': 1509393504,
                |   'plated_end_at': 1509402866,
                | }
                """
        pass

    @staticmethod
    def create(user, book, plated_end_at, end_at):
        orders = Order.objects.all()
        books = set()
        for order in orders:
            if not order.end_at:
                books.add(order.book.id)
        if book.id in books and book.count == 1:
            return None
        try:
            order = Order(user=user, book=book, plated_end_at=plated_end_at, end_at=end_at)
            order.save()
            return order
        except ValueError:
            return None
        except DataError:
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except:
            return None

    @staticmethod
    def get_by_user(user_id):
        set = Order.objects.filter(user=user_id)
        return set

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at != None:
            self.plated_end_at = plated_end_at
        if end_at != None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at=None).values()

    @staticmethod
    def delete_by_id(order_id):
        try:
            a = Order.objects.get(pk=order_id)
        except:
            return False
        else:
            a.delete()
            return True

    def get_close_url(self):
        return reverse('close_order', kwargs={"pk":self.pk})

    def get_open_url(self):
        return reverse('open_order', kwargs={"pk":self.pk})

