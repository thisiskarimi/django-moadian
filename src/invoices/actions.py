from django.forms.models import model_to_dict
from django.conf import settings
from django.shortcuts import render
from moadian import Moadian
from invoices.models import InvoiceResult


with open(settings.PATH_TO_PRIVATE_KEY, "r") as f:
    key = f.read()


def send_invoices(modeladmin, request, queryset):
    result = []
    for obj in queryset:
        try:
            invoice_result = InvoiceResult.objects.get(invoice=obj)
            inv_res_exists = True
            if invoice_result.status == "SUCCESS":
                result.append(
                    {"invoice": obj.title, "result": "صورتحساب قبلا ارسال شده و تایید شده است", "code": 2})
                allow_to_send = False
            elif invoice_result.status == "PENDING":
                result.append(
                    {"invoice": obj.title, "result": "صورتحساب قبلا ارسال شده و منتظر بررسی است", "code": 3})
                allow_to_send = False
            elif invoice_result.status == "FAILED":
                allow_to_send = True
            elif invoice_result.status is None:
                allow_to_send = True
        except InvoiceResult.DoesNotExist:
            inv_res_exists = False
            allow_to_send = True
        if allow_to_send:
            try:
                bodies = []
                payments = []
                header = model_to_dict(obj.invoiceheader)
                header.pop('id')
                header.pop('invoice')
                header["indatim"] = int(header['indatim'].timestamp() * 1000)
                header["indati2m"] = int(header['indati2m'].timestamp() * 1000)
                header['inno'] = str(f'{int(header["inno"]):x}').rjust(10, '0')
                for body in obj.invoicebody_set.all():
                    _ = model_to_dict(body)
                    _.pop('id')
                    _.pop('invoice')
                    bodies.append(_)
                for payment in obj.invoicepayment_set.all():
                    _ = model_to_dict(payment)
                    _.pop('id')
                    _.pop('invoice')
                    payments.append(_)
                invoice = {**{"header": header}, **
                           {"body": bodies}, **{"payments": payments}}
                m = Moadian(settings.FISCAL_ID, key)
                res = m.send_invoice(invoice)
                res = res['result'][0]
                if inv_res_exists:
                    InvoiceResult.objects.get(invoice=obj).delete()
                InvoiceResult.objects.create(invoice=obj, uid=res['uid'],
                                             reference_number=res['referenceNumber'],
                                             error_code=res['errorCode'], error_detail=res['errorDetail'])
                result.append(
                    {"invoice": obj.title, "result": "با موفقیت ارسال شد", "code": 1})
            except Exception as e:
                result.append(
                    {"invoice": obj.title, "result": "خطا: "+str(e), "code": 4})
        del allow_to_send
    return render(request, 'invoice_result.html', {'result': result})


send_invoices.short_description = 'ارسال صورتحساب های انتخاب شده به سامانه مودیان'


def inquiry_invoices(modeladmin, request, queryset):
    result = []
    for obj in queryset:
        try:
            invoice_result = InvoiceResult.objects.get(invoice=obj)
            m = Moadian(settings.FISCAL_ID, key)
            last_status = invoice_result.status
            if last_status is not None and last_status != "PENDING":
                result.append(
                    {"invoice": obj.title, "result": "استعلام قبلا گرفته شده", "code": 2})
            else:
                res = m.inquiry_by_reference_number(
                    str(invoice_result.reference_number))
                res = res['result']['data'][0]
                invoice_result.status = res['status']
                if res['data'] is not None:
                    if res['data'].get('confirmationReferenceId'):
                        invoice_result.confirmation_reference_id = res['data']['confirmationReferenceId']
                    invoice_result.errors = ''
                    for i in res['data']['error']:
                        invoice_result.errors += i['code'] + \
                            ': ' + i['message'] + '\n'
                    invoice_result.warnings = ''
                    for i in res['data']['warning']:
                        invoice_result.warnings += i['code'] + \
                            ': ' + i['message'] + '\n'
                invoice_result.save()
                result.append(
                    {"invoice": obj.title, "result": "استعلام گرفته شد و نتیجه ذخیره شد", "code": 1})
        except InvoiceResult.DoesNotExist:
            result.append(
                {"invoice": obj.title, "result": "قبلا ارسال نشده که حالا بخواهد استعلام شود", "code": 3})
        except Exception as e:
            result.append(
                {"invoice": obj.title, "result": "خطا: "+str(e), "code": 4})
    return render(request, 'invoice_result.html', {'result': result})


inquiry_invoices.short_description = 'استعلام صورتحساب های ارسال شده به سامانه مودیان'
