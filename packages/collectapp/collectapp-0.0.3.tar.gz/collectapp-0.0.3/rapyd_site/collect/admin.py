from django.contrib import admin

from .models.order import Order
from .models.order import ItemOrder
from .models.orderReturn import ReturnOrder
from .models.orderReturn import ReturnOrderItem
from .models.invoice import Invoice
from .models.invoiceItem import InvoiceItem
from .models.suscriptionItem import SuscriptionItem
from .models.suscriptionCollect import SuscriptionCollect
from .models.planCollect import Plan
from .models.product import ProductCollect
from .models.SKU import SKU
from .models.usageRecord import UsageRecord

from .models.address import Address
from .models.coupon import Coupon
from .models.customer_payment_method import CustomerPaymentMethod
from .models.customer import Customer
from .models.discount import Discount
from .models.hosted_page_card_token import HostedPageCardToken
from .models.payment_method_type import PaymentMethodType

from .models.payment import Payment
from .models.refund import Refund
from .models.dispute import Dispute
from .models.escrow import Escrow
from .models.card_to_card import CardToCard
from .models.group_payment import GroupPayment
from .models.payment_method_data import PaymentMethodData
from .models.checkout_page import CheckoutPage
from .models.outcome import Outcome
from .models.paymentFees import PaymentFee
from .models.paymentFees import TransactionFee
from .models.paymentFees import FxFee
from .models.client_details import ClientDetail

# Writting inline admins:


class CardToCardInline(admin.TabularInline):
    model = CardToCard


class PaymentInline(admin.TabularInline):
    model = Payment


class RefundInline(admin.TabularInline):
    model = Refund


class OrderInline(admin.TabularInline):
    model = Order


class CheckoutPageInline(admin.TabularInline):
    model = CheckoutPage


class CustomerInline(admin.TabularInline):
    model = Customer


class DiscountInline(admin.TabularInline):
    model = Discount


class HostedPageCardTokenInline(admin.TabularInline):
    model = HostedPageCardToken


class InvoiceInline(admin.TabularInline):
    model = Invoice


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem


class ReturnOrderInline(admin.TabularInline):
    model = ReturnOrder


class PlanInline(admin.TabularInline):
    model = Plan


class SKUInline(admin.TabularInline):
    model = SKU


class SuscriptionCollectInline(admin.TabularInline):
    model = SuscriptionCollect


class SuscriptionItemInline(admin.TabularInline):
    model = SuscriptionItem


class ReturnOrderItemInline(admin.TabularInline):
    model = ReturnOrderItem


class OrderItemInline(admin.TabularInline):
    model = ItemOrder


# Writing admins

class EscrowAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]  # Se quito payment para ver relacion
    list_display = [f.name for f in Escrow._meta.fields]


class DisputeAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]   # Se quito payment para ver relacion
    list_display = [f.name for f in Dispute._meta.fields]


class GroupPaymentAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = [f.name for f in GroupPayment._meta.fields]


class PaymentMethodTypeAdmin(admin.ModelAdmin):
    inlines = []  # Se quito payment para checar
    list_display = [f.name for f in PaymentMethodType._meta.fields]


class PaymentMethodDataAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]  # Se quito payment para checar
    list_display = [f.name for f in PaymentMethodData._meta.fields]


class CustomerAdmin(admin.ModelAdmin):
    # Se quito card to card para checar
    inlines = [PaymentInline, HostedPageCardTokenInline,
               InvoiceInline, SuscriptionCollectInline]
    list_display = [f.name for f in Customer._meta.fields]


class PaymentAdmin(admin.ModelAdmin):
    inlines = []  # Se quito checkout para checar
    list_display = [f.name for f in Payment._meta.fields]


class CouponAdmin(admin.ModelAdmin):
    inlines = [OrderInline, CustomerInline, DiscountInline,
               SuscriptionCollectInline]
    list_display = [f.name for f in Coupon._meta.fields]


class SKUAdmin(admin.ModelAdmin):
    inlines = [ReturnOrderItemInline, OrderItemInline]
    list_display = [f.name for f in SKU._meta.fields]


class AddressAdmin(admin.ModelAdmin):
    inlines = [CustomerInline]
    list_display = [f.name for f in Address._meta.fields]


class SuscriptionCollectAdmin(admin.ModelAdmin):
    inlines = [InvoiceInline, SuscriptionItemInline]
    list_display = [f.name for f in SuscriptionCollect._meta.fields]


class PlanAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    list_display = [f.name for f in Plan._meta.fields]


class OrderAdmin(admin.ModelAdmin):
    inlines = [ReturnOrderInline]
    list_display = [f.name for f in Order._meta.fields]


class ProductCollectAdmin(admin.ModelAdmin):
    inlines = [SKUInline]
    list_display = [f.name for f in ProductCollect._meta.fields]


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    list_display = [f.name for f in Invoice._meta.fields]


class RefundAdmin(admin.ModelAdmin):
    inlines = []
    list_display = [f.name for f in Refund._meta.fields]


class OutcomeAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = [f.name for f in Outcome._meta.fields]


class PaymentFeeAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = [f.name for f in PaymentFee._meta.fields]


class ClientDetailAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = [f.name for f in ClientDetail._meta.fields]


# Register your models here.
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Refund, RefundAdmin)
admin.site.register(Escrow, EscrowAdmin)
admin.site.register(Dispute, DisputeAdmin)
admin.site.register(GroupPayment, GroupPaymentAdmin)
admin.site.register(CardToCard)
admin.site.register(PaymentMethodData, PaymentMethodDataAdmin)
admin.site.register(CheckoutPage)
admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(PaymentFee, PaymentFeeAdmin)
admin.site.register(TransactionFee)
admin.site.register(FxFee)
admin.site.register(ClientDetail, ClientDetailAdmin)


admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrder)
admin.site.register(ReturnOrder)
admin.site.register(ReturnOrderItem)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem)
admin.site.register(SuscriptionCollect, SuscriptionCollectAdmin)
admin.site.register(SuscriptionItem)
admin.site.register(ProductCollect, ProductCollectAdmin)
admin.site.register(SKU, SKUAdmin)
admin.site.register(Plan)
admin.site.register(UsageRecord)

admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CustomerPaymentMethod)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Discount)
admin.site.register(HostedPageCardToken)
admin.site.register(PaymentMethodType, PaymentMethodTypeAdmin)
