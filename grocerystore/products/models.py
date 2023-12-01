import sys
import os
from io import BytesIO

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey
from pytils.translit import slugify
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="category_images/")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Используем автоматичнское формирования слак поля из имени
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="subcategory_images/")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    def save(self, *args, **kwargs):
        # Используем автоматичнское формирования слак поля из имени
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя",
    )
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите Категорию перед выбор Подкатегорий",
    )
    subcategory = ChainedForeignKey(
        "SubCategory",
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name="Подкатегория",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=10,
        decimal_places=2,
        help_text="Цена указывается в Int или Float",
    )
    image = models.ImageField(upload_to="product_images/")
    image2 = models.ImageField(upload_to="product_images/", blank=True)
    image3 = models.ImageField(upload_to="product_images/", blank=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Прикрепляем 1 изображение ,и автоматически формируются два других с другим разрешением. Так же изображение конвертируется в JPG
        self.slug = slugify(self.name)
        base, extension = os.path.splitext(self.image.name)
        name = slugify(base)
        self.image.name = name + extension
        output_thumb = BytesIO()
        output_thumb2 = BytesIO()

        img = Image.open(self.image)

        if img.mode != "RGB":
            output = BytesIO()
            img.convert("RGB").save(output, "JPEG")
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                "ImageField",
                "%s.jpg" % self.image.name.split(".")[0],
                "image/jpeg",
                output.tell(),
                None,
            )

        img = Image.open(self.image)
        img2 = Image.open(self.image)

        img.thumbnail((200, 200))
        img.save(output_thumb, format="JPEG", quality=90)
        self.image2 = InMemoryUploadedFile(
            output_thumb,
            "ImageField",
            f"{name}_image2.jpg",
            "image/jpeg",
            sys.getsizeof(output_thumb),
            None,
        )

        img2.thumbnail((400, 400))
        img2.save(output_thumb2, format="JPEG", quality=90)

        self.image3 = InMemoryUploadedFile(
            output_thumb2,
            "ImageField",
            f"{name}_image3.jpg",
            "image/jpeg",
            sys.getsizeof(output_thumb2),
            None,
        )

        super(Product, self).save(*args, **kwargs)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("user",)
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_cart")
        ]

    def __str__(self):
        return f"{self.user} {self.product} {self.quantity} шт."
