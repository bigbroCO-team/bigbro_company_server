from rest_framework import serializers

from .models import Order, OrderItem
from product.models import Product, ProductOption
from address.models import Address


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderWriteSerializer(serializers.Serializer):
    products = serializers.ListField()
    address = serializers.IntegerField()

    def create(self, validated_data):
        products = validated_data.pop('products')
        total_price = 0

        # Get address
        address = Address.objects.filter(id=validated_data['address']).first()
        if not address:
            raise serializers.ValidationError('Address not found')
        
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
                raise serializers.ValidationError('Product not found')
            
            option = ProductOption.objects.filter(id=p['option']).first()
            if not option:
                raise serializers.ValidationError('Option not found')
            
            total_price += product.price * product.discount

            order_items.append(OrderItem(product=product, product_option=option, order=order))
        OrderItem.objects.bulk_create(order_items)

        order.total_price = total_price
        order.save()

        return order