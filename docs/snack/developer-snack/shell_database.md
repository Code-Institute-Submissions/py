## Manipulate Database from the Django Shell

You can interact with your Django database using the shell. Here's a step-by-step guide on how to manipulate data using the shell.

1. Access the Django Shell:
   Open a terminal and navigate to your Django project directory. Then, run the following command to start the Django shell:

   ```bash
   python3 manage.py shell
   ```

2. Import the Relevant Model:
   Import the model you want to work with. In this example, we'll use the `Product` model from the `products` app:

   ```python
   from products.models import Product
   ```

3. Filter Products:
   Suppose you want to work with products that are not in the categories 'kitchen-dining room' or 'bed_bathroom'. You can filter the products as follows:

   ```python
   kdbb = ['kitchen-dining room', 'bed_bathroom']
   clothes = Product.objects.exclude(category__name__in=kdbb)
   ```

   This code creates a queryset called `clothes` containing products that are not in the specified categories.

4. Count Filtered Products:
   You can check the number of products in the `clothes` queryset using the `count()` method:

   ```python
   clothes_count = clothes.count()
   ```

   This code stores the count in the variable `clothes_count`.

5. Update Product Attributes:
   Let's assume you want to update the `has_sizes` attribute for each product in the `clothes` queryset. You can loop through the queryset and set the `has_sizes` attribute to `True` for each item:

   ```python
   for item in clothes:
       item.has_sizes = True
       item.save()
   ```

   This code iterates through the products and updates their `has_sizes` attribute.

6. Query Products with Updated Attribute:
   Finally, you can query and retrieve products that have the `has_sizes` attribute set to `True`:

   ```python
   sized_products = Product.objects.filter(has_sizes=True)
   ```

   This code creates a new queryset called `sized_products` containing products with the updated attribute.

This is a basic example of how to manipulate your Django database using the shell. Be cautious when making changes in the shell, as they will affect your database. Always make sure you have a backup or are working in a development environment.

## Complete Code

```bash
python3 manage.py shell
```

```python

from products.models import Product
kdbb = ['kitchen-dining room', 'bed_bathroom']
clothes = Product.objects. exclude (category__name__in=kdbb)
clothes.count()
for item in clothes:
    item.has_sizes = True
element.save()
Product.objects.filter(has_sizes=True)
```