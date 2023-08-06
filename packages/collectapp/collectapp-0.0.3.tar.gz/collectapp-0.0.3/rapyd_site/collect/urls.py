from django.urls import path
from .views.paymentView import createPayment, updatePayment, capturePayment
from .views.paymentView import completPayment, cancelPayment
from .views.paymentView import listPayment, retrievePayment, getBdPayments
from .views.groupPaymentView import createGroupPayment, createGroupRefund
from .views.groupPaymentView import retrieveGroupPayment, getBdGroupPayment
from .views.groupPaymentView import cancelGroupPayment
from .views.escrowView import listEscrow, releaseEscrow, getBdEscrows
from .views.escrowView import retrieveEscrow
from .views.disputeView import listDispute, retrieveDispute, getBdDispute
from .views.checkoutView import createCheckout, getBdCheckout, retrieveCheckout
from .views.cardToCardView import addSourceCard, createCardToCardPayment
from .views.refundView import createRefund, updateRefund, completeRefund
from .views.refundView import listRefund, retrieveRefund, getBdRefunds


urlpatterns = [

    # **************Payments*************

    # Crear un pago
    path('create_payment/', createPayment, name="create_payment"),

    # actualizar un pago
    path('update_payment/<str:id>', updatePayment, name="update_payment"),

    # Capturar pago
    path('capture_payment/<str:id>', capturePayment, name="capture_payment"),

    # Completar pago
    path('complete_payment/', completPayment, name="complete_payment"),

    # Obtener datos del pago con Rapyd
    path('retrieve_payment/<str:id>',
         retrievePayment, name="retrieve_payment"),

    # Obtener todos los pagos en rapyd
    path('list_payment/<int:limit>', listPayment, name="list_payment"),

    # Cancelar pago
    path('cancel_payment/<str:id>', cancelPayment, name="cancel_payment"),

    # Obtener datos del pago de la DB
    path('get_payment/', getBdPayments, name="get_payment"),

    # ************Group Payment**************

    # Crear un pago
    path('create_group_payment/',
         createGroupPayment, name="create_group_payment"),

    # Crear refund group
    path('create_group_refund/',
         createGroupRefund, name="create_gropu_refund"),

    # Retrieve Group payment
    path('retrieve_group_payment/<str:id>',
         retrieveGroupPayment, name="retrieve_group_payment"),

    # Cancel group payment
    path('cancel_group_payment/<str:id>',
         cancelGroupPayment, name="cancel_group_payment"),

    # Obtener datos Group payment de la BD
    path('get_group_payment/', getBdGroupPayment, name="get_group_payment"),


    # ***********Escrow***************

    path('release_funds_escrow/<str:escrow_id>/<str:payment_id>',
         releaseEscrow, name="release_funds_escrow"),

    path('retrieve_escrow/<str:escrow_id>/<str:payment_id>',
         retrieveEscrow, name="retrieve_escrow"),

    path('list_escrow/<str:escrow_id>/<str:payment_id>',
         listEscrow, name="list_escrow"),

    path('get_escrow/', getBdEscrows, name="get_escrow"),


    # *************Dispute*****************

    path('list_dispute/<int:limit>', listDispute, name="list_dispute"),

    path('retrieve_dispute/<str:id>',
         retrieveDispute, name="retrieve_dispute"),

    path('get_dispute/', getBdDispute, name="get_dispute"),

    # *************Checkout Pages ************

    path('create_checkout/', createCheckout, name="create_checkout"),

    path('retrieve_checkout/<str:id>',
         retrieveCheckout, name="retrieve_checkout"),

    path('get_checkout/', getBdCheckout, name="get_checkout"),

    # **************Card to Card ****************
    # Se necesita Ewallet para que funcione
    path('add_source_card/', addSourceCard, name="add_source_card"),

    path('create_cardto_payment/',
         createCardToCardPayment, name="create_cardto_payment"),

    # ************** Refund *******************
    path('create_refund/', createRefund, name="create_refund"),
    path('update_refund/<str:id>', updateRefund, name="update_refund"),
    path('complete_refund/', completeRefund, name="complete_refund"),

    path('list_refund/<int:limit>', listRefund, name="list_refund"),
    path('retrieve_refund/<str:id>', retrieveRefund, name="retrieve_refund"),


    # Obtener datos  de la BD
    path('get_refund/', getBdRefunds, name="get_refund"),

]
