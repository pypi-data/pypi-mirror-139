from rest_framework import serializers
from .models.payment import Payment
from .models.group_payment import GroupPayment
from .models.customer import Customer
from .models.escrow import Escrow
from .models.dispute import Dispute
from .models.checkout_page import CheckoutPage
from .models.refund import Refund
from .models.payment_method_data import PaymentMethodData


class PaymentSerializer(serializers.ModelSerializer):
    ewallets = serializers.JSONField()
    instructions = serializers.JSONField()

    class Meta:
        model = Payment
        exclude = ('escrow',
                   'payment_method_data',
                   'dispute',
                   'customer',
                   'outcome',
                   'payment_fees',
                   'client_details')


class GroupPaymentSerializer(serializers.ModelSerializer):
    payments = serializers.JSONField()

    class Meta:
        model = GroupPayment
        fields = '__all__'


class EscrowSerializer(serializers.ModelSerializer):
    payment = serializers.JSONField()

    class Meta:
        model = Escrow
        fields = '__all__'


class DisputeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dispute
        fields = '__all__'


class CheckoutSerializer(serializers.ModelSerializer):
    payment_method_type_categories = serializers.JSONField(allow_null=True)
    payment_method_types_exclude = serializers.JSONField(allow_null=True)
    payment_method_types_include = serializers.JSONField(allow_null=True)

    class Meta:
        model = CheckoutPage
        fields = '__all__'


class CardToCardSerializer(serializers.ModelSerializer):
    customer_addresses = serializers.JSONField(allow_null=True)

    class Meta:
        model = CheckoutPage
        exclude = ('customer')


class RefundSerializer(serializers.ModelSerializer):
    ewallets = serializers.JSONField()

    class Meta:
        model = Refund
        exclude = ('payment')


class CustomerSerializer(serializers.ModelSerializer):
    addresses = serializers.JSONField()

    class Meta:
        model = Customer
        fields = '__all__'


class PaymentMethodDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethodData
        fields = '__all__'
