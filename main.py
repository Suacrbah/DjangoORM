from django.db.models import *

from app.config import * 
from app.models import *

#You can now use the User model as needed as well as user 
if __name__=="__main__":
  # Test query
  q = Shippers.objects.all()
  print(q.query)
  for shipper in q:
    print(shipper.shipperid, shipper.companyname, shipper.phone)

  # 6
  q = OrderDetails.objects.select_related('productid').annotate(
          ProductName=F('productid__productname'),
          ExtendedPrice=Sum(F('unitprice') * F('quantity') * (1 - F('discount')))
        ).values(
            'orderid', 'productid', 'ProductName', 'unitprice', 'quantity', 'discount', 'ExtendedPrice'
        ).order_by('orderid')
  print(q.query)
  print(len(q))

  # 8
  q = Products.objects.annotate(
        Ten_Most_Expensive_Products=F('productname'),
        UnitPrice=F('unitprice')
      ).order_by('-unitprice')[:10]
  print(q.query)
  print(len(q))

  # 9
  q = Products.objects.filter(
      discontinued='N'
    ).select_related('categoryid').order_by(
      'categoryid__categoryname', 'productname'
    ).values(
      'categoryid__categoryname', 'productname', 'quantityperunit',
      'unitsinstock', 'discontinued'
    ).distinct()
  print(q.query)
  print(len(q))

  # 10
  # Define queries for Customers and Suppliers separately
  customers_query = Customers.objects.annotate(Relationship=Value('Customers', output_field=CharField()))
  suppliers_query = Suppliers.objects.annotate(Relationship=Value('Suppliers', output_field=CharField()))
  # Combine queries using union operator
  union_query = customers_query.union(suppliers_query)
  # Specify columns to select and order by
  q = union_query.values('city', 'companyname', 'contactname', 'Relationship').order_by('city', 'companyname')
  print(q.query)
  print(len(q))

  # 11
  q = Products.objects.filter(unitprice__gt=Products.objects.aggregate(avg_price=Avg('unitprice'))['avg_price']).order_by('unitprice').values('productname', 'unitprice').distinct()
  print(q.query)
  print(len(q))
