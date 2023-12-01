from django.contrib import admin
from .models import Category, SubCategory, Product, ShoppingCart


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    fields = ["name", "image"]
    list_filter = ("id",)
    search_fields = ("name",)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "category")
    fields = ["name", "image", "category"]
    list_filter = ("id",)
    search_fields = ("name",)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "category", "subcategory", "price")
    fields = ["name", "category", "subcategory", "price", "image"]
    list_filter = ("id",)
    search_fields = ("name",)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")
    fields = ("user", "product", "quantity")
    list_filter = ("user",)
    search_fields = ("user",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
