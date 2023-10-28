from django.contrib import admin
from django.contrib.admin.options import StackedInline
from invoices.models import Invoice, InvoiceHeader, InvoiceBody, InvoicePayment, InvoiceResult
from jalali_date.widgets import AdminSplitJalaliDateTime
from django.db import models
from .actions import send_invoices, inquiry_invoices


class InvoiceHeaderAdminInline(StackedInline):
    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.invoiceresult.status == "SUCCESS":
                return [field.name for field in self.model._meta.get_fields() if field.name != 'id']
        except Exception:
            pass
        return ("taxid", "tins", "inp", "inty")
    model = InvoiceHeader
    exclude = ["ft", "tax17", "billid", "crn",
               "bid", "bpn", "scln", "scc", "todam"]
    fields = [("taxid"), ("indatim", "indati2m"), ("inno", "irtaxid"), ("inty", "inp", "ins"),
              ("tins", "tinb", "tob",), ("sbc", "bpc", "bbc",),
              ("tprdis", "tdis", "tadis"), ("setm", "cap", "insp"), ("tbill", "tvop", "tvam", )]
    formfield_overrides = {
        models.DateTimeField: {"widget": AdminSplitJalaliDateTime},
    }


class InvoiceBodyAdminInline(StackedInline):
    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.invoiceresult.status == "SUCCESS":
                return [field.name for field in self.model._meta.get_fields() if field.name != 'id']
        except Exception:
            pass
        return []
    extra = 1
    model = InvoiceBody
    exclude = ["mu", "cfee", "cut", "exr", "odt",
               "odr", "odam", "olt", "olr", "olam", "consfee", "spro", "bros", "tspbs", "bsrn"]
    fields = [("sstid", "sstt", ), ("am", "fee"), ("prdis", "dis",
                                                   "adis", ), ("vra", "vam", "tsstam"), ("cop", "vop")]


class InvoiceResultInline(admin.StackedInline):
    model = InvoiceResult
    extra = 0
    readonly_fields = ("uid", "reference_number", "error_code",
                       "error_detail", "status", "confirmation_reference_id",
                       "errors", "warnings")
    fields = ["status", ("confirmation_reference_id", "uid", "reference_number"),
              ("error_code", "error_detail"), "errors", "warnings"]


class InvoicePaymentAdminInline(StackedInline):
    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.invoiceresult.status == "SUCCESS":
                return [field.name for field in self.model._meta.get_fields() if field.name != 'id']
        except Exception:
            pass
        return []
    extra = 1
    model = InvoicePayment
    fields = [("iinn", "acn"), ("trmn", "trn"), ("pid", "pcn"), ("pdt")]


@admin.register(Invoice)
class InvoiceModelAdmin(admin.ModelAdmin):
    @admin.display(description="وضعیت استعلام")
    def get_status(self, obj):
        return obj.invoiceresult.status
    inlines = (InvoiceHeaderAdminInline, InvoiceBodyAdminInline,
               InvoicePaymentAdminInline, InvoiceResultInline)
    list_display = ["title", "get_status"]
    list_filter = ("invoiceresult__status",
                   "invoiceheader__indatim", "invoiceheader__setm")
    ordering = ['-title', ]
    actions = [send_invoices, inquiry_invoices]
