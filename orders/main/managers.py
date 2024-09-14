from datetime import datetime
from django.db.models import Manager, Q
from .status import Status
from . import models
from .exceptions import(
    InvalidArgumentError,
    OrderAlreadyCompletedError,
    OrderCancellationError,
)


class OrderManager(Manager):
    def set_status(self, order, status):
          if status is None or not isinstance(status, Status):
               raise InvalidArgumentError('status')
          if order is None or not isinstance(order, models.Order):
               raise InvalidArgumentError('order')
          if order.status is Status.Completed.value:
                    raise OrderAlreadyCompletedError()
          order.status = status.value
          order.save()

    def cancel_order(self, order):
         if order is None or not isinstance(order, models.Order):
              raise InvalidArgumentError('order')
         if order.status != Status.Recieved.value:
              raise OrderCancellationError()
         self.set_status(order, Status.Cancelled)

    def get_customer_orders(self, customer_id):
         try:
              return self.filter(customer_id=customer_id
                   ).order_by('status', '-created')
         except ValueError:
              raise InvalidArgumentError('customer_id')

    def get_incomplete_orders(self, customer_id):
        try:
            return self.filter(
                ~Q(status=Status.Completed.value), 
                customer_id=customer_id           
            ).order_by('status')
        except ValueError:
            raise InvalidArgumentError('customer_id')

    def get_completed_orders(self, customer_id):
        try:
            return self.filter(
                status=Status.Completed.value,
                customer_id=customer_id
            ).order_by('status')
        except ValueError:
            raise InvalidArgumentError('customer_id')

    def get_by_status(self, status):
        if status is None or not isinstance(status, Status):
            raise InvalidArgumentError('status')
        return self.filter(status=status.value)
    
    def get_by_period(self, start_date, end_date):
        if start_date is None or not isinstance(start_date, datetime):
            raise InvalidArgumentError('start_date')
        if end_date is None or not isinstance(end_date, datetime):
            raise InvalidArgumentError('end_date')
        if start_date > end_date:
            raise InvalidArgumentError(end_date)
        return self.filter(created_range=[start_date, end_date])
    
    def set_next_status(self, order):
         if order is None or not isinstance(order, models.Order):
              raise InvalidArgumentError('order')
         if order.status is Status.Completed.value:
              raise OrderAlreadyCompletedError()
         order.status += 1
         order.save()