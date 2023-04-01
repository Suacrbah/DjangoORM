from django.db.models import *

from app.config import *
from app.models import *


def orderSubTotals():
    """
        select OrderID, format(sum(UnitPrice * Quantity * (1 - Discount)), 2) as Subtotal
        from orderdetails
        group by OrderID
        order by OrderID;
        """
    subtotal_by_order = (
        Orderdetails.objects
        .values('orderid')
        .annotate(
            Subtotal=Sum(F('unitprice') * F('quantity') * (1 - F('discount')), output_field=models.FloatField())
        )
        .order_by('orderid')
    )
    print(subtotal_by_order.query)
    print(subtotal_by_order)
    return


def salesByYear():
    """
    select distinct date(a.ShippedDate) as ShippedDate,
                a.OrderID,
                b.Subtotal,
                year(a.ShippedDate) as Year
    from Orders a
             inner join
         (
             select distinct OrderID,
                             format(sum(UnitPrice * Quantity * (1 - Discount)), 2) as Subtotal
             from orderdetails
             group by OrderID) b on a.OrderID = b.OrderID
    where a.ShippedDate is not null
      and a.ShippedDate between date('1996-12-24') and date('1997-09-30')
    order by a.ShippedDate;
    :return:
    """
    orders = Orderdetails.objects.select_related('OrderID_id').filter(
        OrderID_id__shippeddate__isnull=False,
        OrderID_id__shippeddate__range=['1996-12-24', '1997-09-30']
    ) \
        .annotate(year=ExtractYear('OrderID_id__shippeddate')) \
        .annotate(ShippedDate=TruncDate('OrderID_id__shippeddate')) \
        .annotate(
        Subtotal=Sum(F('unitprice') * F('quantity') * (1 - F('discount')),
                     output_field=models.FloatField())). \
        values('OrderID_id__shippeddate', 'OrderID_id__orderid', 'Subtotal', 'year'). \
        order_by('ShippedDate')
    print(orders.query)
    print(orders)
    return


def employeeSalesByCountry():
    """
    select distinct b.*, a.CategoryName
    from Categories a
    inner join Products b on a.CategoryID = b.CategoryID
    where b.Discontinued = 'N'
    order by b.ProductName;
    :return:
    """
    categories = (
        Categories.objects.filter(
            products__discontinued=1
        )
        .annotate(
            CategoryName=F('categoryname'),
        )
        .values(
            'products__productid',
            'products__productname',
            'products__supplierid',
            'products__categoryid',
            'products__quantityperunit',
            'products__unitsinstock',
            'products__unitsonorder',
            'products__reorderlevel',
            'products__discontinued',
            'CategoryName'
        )
        .order_by('products__productname')
    )

    print(categories.query)
    print(categories)


def listOfProducts():
    """
    select distinct b.*, a.CategoryName
    from Categories a
    inner join Products b on a.CategoryID = b.CategoryID
    where b.Discontinued = 1
    order by b.ProductName;
    :return:
    """

    categories = Products.objects.filter(discontinued=1) \
        .select_related('categoryid').annotate().order_by('productname') \
        .values('id', 'productname', 'categoryid__categoryid', 'categoryid__categoryname')
    print(categories.query)
    print(categories)


def currentProductList():
    """
    select ProductID, ProductName
    from products
    where Discontinued = 1
    order by ProductName;
    :return:
    """
    products = (
        Products.objects.filter(
            discontinued=1
        )
        .values(
            'productid',
            'productname'
        )
        .order_by('productname')
    )
    print(products.query)
    print(len(products.values()))

def sql_function_6():
    # 6
    q = OrderDetails.objects.select_related('productid').annotate(
        ProductName=F('productid__productname'),
        ExtendedPrice=Sum(F('unitprice') * F('quantity') * (1 - F('discount')))
    ).values(
        'orderid', 'productid', 'ProductName', 'unitprice', 'quantity', 'discount', 'ExtendedPrice'
    ).order_by('orderid')
    print(q.query)
    print(len(q))


def sql_function_8():
    # 8
    q = Products.objects.annotate(
        Ten_Most_Expensive_Products=F('productname'),
        UnitPrice=F('unitprice')
    ).order_by('-unitprice')[:10]
    print(q.query)
    print(len(q))


def sql_function_9():
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


def sql_function_10():
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


def sql_function_11():
    # 11
    q = Products.objects.filter(
        unitprice__gt=Products.objects.aggregate(avg_price=Avg('unitprice'))['avg_price']).order_by('unitprice').values(
        'productname', 'unitprice').distinct()
    print(q.query)
    print(len(q))


# You can now use the User model as needed as well as user
if __name__ == "__main__":
    sql_function_6()