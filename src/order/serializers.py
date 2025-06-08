from rest_framework import serializers

from product.serializers import ProductReadSerializer, ProductOptionSerializer
from .models import Order, OrderItem
from product.models import Product, ProductOption
from address.models import Address
from product.exceptions import ProductException, ProductOptionException


class OrderItemWriteSerializer(serializers.Serializer):
    products = serializers.ListField()
    address = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderWriteSerializer(serializers.Serializer):
    products = OrderItemWriteSerializer(many=True)
    address = serializers.IntegerField()

    def create(self, validated_data):
        products = validated_data.pop('products')
        total_price = 0

        # Get address
        address = Address.objects.filter(id=validated_data['address']).first()
        if not address:
            raise AddressException.addressNotFound
        
        # Create order 
        order = Order.objects.create(
            user=validated_data['user'],
            address=address.address,
            address_detail=address.detail,
            zipcode=address.zipcode,
            request=address.request,
            phone=address.phone,
        )

        # Create order items
        order_items = []
        for p in products:
            product = Product.objects.filter(id=p['product']).first()
            if not product:
                raise ProductException.productNotFound
            
            option = ProductOption.objects.filter(id=p['option']).first()
            if not option:
                raise ProductOptionException.optionNotFound
            
            total_price += (product.price - int(product.price * product.discount / 100)) * p['quantity']

            order_items.append(OrderItem(product=product, product_option=option, order=order))

        OrderItem.objects.bulk_create(order_items)

        order.total_price = total_price
        order.save()

        return order


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()
    product_option = ProductOptionSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_option', 'quantity')


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, source='order_item')

    class Meta:
        model = Order
        fields = (
            'id', 'total_price', 'tracking_number', 'delivery_company',
            'address', 'address_detail', 'zipcode', 'request', 'phone',
            'items'
        )