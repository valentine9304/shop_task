from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


from .models import Category, Product, ShoppingCart
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ShoppingCartSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        """
        Список покупок. Добавление, удаления продукта у пользователя.
        """
        product = get_object_or_404(Product, id=pk)
        user = self.request.user

        if request.method == "POST":
            quantity = request.query_params.get("quantity", 1)
            if int(quantity) < 1:
                return Response(
                    "Количество дожно быть больше 1", status=status.HTTP_400_BAD_REQUEST
                )

            if ShoppingCart.objects.filter(
                user=user, product=product, quantity=int(quantity)
            ).exists():
                return Response(
                    "Продукт уже в списке покупок, вы можете изменить его количество.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Создаем продукт в корзине или обновляем его количество
            shopping_cart_entry, created = ShoppingCart.objects.get_or_create(
                user=user, product=product
            )
            serializer = ShoppingCartSerializer(
                shopping_cart_entry, data={"quantity": quantity}, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not ShoppingCart.objects.filter(user=user, product=product).exists():
            return Response(
                "Продукта нет в списке покупок.",
                status=status.HTTP_404_NOT_FOUND,
            )
        ShoppingCart.objects.get(user=user, product=product).delete()
        return Response(
            "Продукт удалён из списка покупок.",
            status=status.HTTP_204_NO_CONTENT,
        )


class ShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShoppingCart.objects.all()
    pagination_class = CustomPagination
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        # Возвращаем только продукты пользователя
        return ShoppingCart.objects.filter(user=self.request.user)

    def delete(self, request):
        # Удаляем все продукты из корзины
        queryset = self.get_queryset()
        queryset.delete()
        return Response(
            "Все продукты удалены из корзины.",
            status=status.HTTP_204_NO_CONTENT,
        )

    def destroy(self, request, *args, **kwargs):
        # Удаляем определённый продукт из корзины
        instance = self.get_object()
        if instance.user != self.request.user:
            return Response(
                "Вы не можете удалить этот продукт из корзины.",
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response("Продукт удален из корзины.", status=status.HTTP_204_NO_CONTENT)
