from django.contrib import admin

from islamoshop.models import userData, productDetails, purchasingHistory

# Register your models here.

admin.site.register(productDetails)
admin.site.register(purchasingHistory)
admin.site.register(userData)
