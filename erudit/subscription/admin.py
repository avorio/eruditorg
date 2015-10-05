from django.contrib import admin
from subscription.models import (
    Client, Product, RenewalNotice, RenewalNoticeStatus
)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description',]
    list_display = ['title', 'description', 'amount',]
    list_display_link = ['title',]
    list_editable = ['amount',]


class ClientAdmin(admin.ModelAdmin):
    pass
    search_fields = ['firstname', 'lastname', 'organisation', 'email', 'postal_code',]
    list_display = ['firstname', 'lastname', 'organisation', 'email',]
    list_display_link = ['firstname', 'lastname',]
    list_filter = ['organisation', 'city', 'province', 'country',]
    fieldsets = [
        ('Identification', {
            'fields': (
                ('firstname', 'lastname'),
                'organisation',
            )
        }),
        ('Coordonnées', {
            'fields': (
                'email',
                'address',
                ('city', 'province'),
                ('country', 'postal_code'),
            )
        }),
    ]


class RenewealNoticeAdmin(admin.ModelAdmin):
    pass
    search_fields = ['po_number', 'paying_customer', 'receiving_customer', ]
    list_display = ['po_number', 'paying_customer', 'receiving_customer', 'net_amount', 'status',]
    list_display_link = ['po_number', ]
    list_filter = ['currency', 'status',]
    list_editable = ['status',]
    fieldsets = [
        ('Identification', {
            'fields': (
                'po_number',
                ('paying_customer', 'receiving_customer'),
            )
        }),
        ('Montants', {
            'fields': (
                'currency',
                ('amount_total', 'rebate'),
                ('raw_amount',),
                ('federal_tax',),
                ('provincial_tax',),
                ('harmonized_tax',),
                ('net_amount',),
            )
        }),
        ('Produits', {
            'fields': (
                'products',
            )
        }),
        ('Suivi', {
            'fields': (
                'date_created',
                'status',
            )
        }),
    ]


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(RenewalNotice, RenewealNoticeAdmin)
admin.site.register(RenewalNoticeStatus)
