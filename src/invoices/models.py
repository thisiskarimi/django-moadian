from django.db import models
from django.conf import settings
from moadian.utils import generate_tax_id
import jdatetime


class Invoice(models.Model):
    title = models.CharField("عنوان", max_length=50)

    class Meta:
        verbose_name = "صورتحساب"
        verbose_name_plural = "صورتحساب ها"

    def __str__(self):
        return self.title


class InvoiceHeader(models.Model):
    class Inty(models.IntegerChoices):
        ONE = 1, "نوع اول"
        TWO = 2, "نوع دوم"
        THREE = 3, "نوع سوم"

    class Setm(models.IntegerChoices):
        ONE = 1, "نقدی"
        TWO = 2, "نسیه"
        THREE = 3, "نقدی/نسیه"

    class Inp(models.IntegerChoices):
        ONE = 1, "فروش"
        TWO = 2, "فروش ارزی"
        THREE = 3, "طلا و جواهر و پلاتین"
        FOUR = 4, "قرارداد پیمانکاری"
        FIVE = 5, "قبوض خدماتی"
        SIX = 6, "بلیت هواپیما"

    class Ins(models.IntegerChoices):
        ONE = 1, "اصلی"
        TWO = 2, "اصلاحی"
        THREE = 3, "ابطالی"
        FOUR = 4, "برگشت از فروش"

    class Tob(models.IntegerChoices):
        ONE = 1, "حقیقی"
        TWO = 2, "حقوقی"
        THREE = 3, "مشارکت مدنی"
        FOUR = 4, "اتباع غیرایرانی"
        FIVE = 5, "مصرف کننده نهایی"
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    taxid = models.CharField("شماره منحصر به فرد مالیاتی",
                             max_length=50, null=True, blank=True)
    indatim = models.DateTimeField(
        "تاریخ صدور صورتحساب", auto_now=False, auto_now_add=False, null=True, blank=True)
    indati2m = models.DateTimeField(
        "تاریخ ایجاد صورتحساب", auto_now=False, auto_now_add=False, null=True, blank=True)
    inty = models.PositiveSmallIntegerField(
        "نوع صورتحساب", choices=Inty.choices, null=True, blank=True, default=1)
    inno = models.CharField(
        "سریال صورتحساب", max_length=50, null=True, blank=True)
    irtaxid = models.CharField(
        "شماره منحصر به فرد سریال صورتحساب مرجع", max_length=50, null=True, blank=True)
    inp = models.PositiveSmallIntegerField(
        "الگوی صورتحساب", choices=Inp.choices, null=True, blank=True, default=1)
    ins = models.PositiveSmallIntegerField(
        "موضوع صورتحساب", choices=Ins.choices, null=True, blank=True, default=1)
    tins = models.CharField("شماره اقتصادی فروشنده",
                            max_length=15, null=True, blank=True, default="default value for tins")
    tinb = models.CharField("شماره اقتصادی خریدار",
                            max_length=15, null=True, blank=True)
    tob = models.PositiveSmallIntegerField(
        "نوع شخص خریدار", choices=Tob.choices, null=True, blank=True, default=2)
    bid = models.CharField(
        "شماره/شناسه ملی/شناسه مشارکت مدنی/کد فراگیر خریدار", max_length=50, null=True, blank=True)
    sbc = models.CharField(
        "کد شعبه فروشنده", max_length=15, null=True, blank=True)
    bpc = models.CharField(
        "کد پستی خریدار", max_length=15, null=True, blank=True)
    bbc = models.CharField(
        "کد شعبه خریدار", max_length=15, null=True, blank=True)
    ft = models.PositiveSmallIntegerField("نوع پرواز", null=True, blank=True)
    bpn = models.CharField("شماره گذرنامه خریدار",
                           max_length=50, null=True, blank=True)
    scln = models.CharField("شماره پروانه گمرکی",
                            max_length=50, null=True, blank=True)
    scc = models.CharField("کد گمرک محل اظهار",
                           max_length=50, null=True, blank=True)
    crn = models.CharField("شناسه یکتای ثبت قرارداد فروشنده",
                           max_length=50, null=True, blank=True)
    billid = models.CharField(
        "شناسه اشتراک/شماره قبض بهره بردار", max_length=50, null=True, blank=True)
    tprdis = models.PositiveBigIntegerField(
        "مجموع مبلغ قبل از کسر تخفیف", null=True, blank=True)
    tdis = models.PositiveBigIntegerField(
        "مجموع تخفیفات", null=True, blank=True, default=0)
    tadis = models.PositiveBigIntegerField(
        "مجموع مبلغ پس از کسر تخفیف", null=True, blank=True)
    tvam = models.PositiveBigIntegerField(
        "مجموع مالیات بر ارزش افزوده", null=True, blank=True)
    todam = models.PositiveBigIntegerField(
        "مجموع سایر مالیات، عوارض و وجوه قانونی", null=True, blank=True, default=0)
    tbill = models.PositiveBigIntegerField(
        "مجموع صورتحساب", null=True, blank=True)
    setm = models.PositiveSmallIntegerField(
        "روش تسویه", choices=Setm.choices, null=True, blank=True, default=1)
    cap = models.PositiveBigIntegerField(
        "مبلغ پرداختی نقدی", null=True, blank=True)
    insp = models.PositiveBigIntegerField(
        "مبلغ پرداختی نسیه", null=True, blank=True, default=0)
    tvop = models.PositiveBigIntegerField(
        "مجموع سهم مالیات بر ارزش افزوده از پرداخت", null=True, blank=True)
    tax17 = models.PositiveBigIntegerField(
        "مالیات موضوع ماده ۱۷", null=True, blank=True)

    class Meta:
        verbose_name = "InvoiceHeader"
        verbose_name_plural = "InvoiceHeaders"

    def save(self, *args, **kwargs):
        self.indatim = jdatetime.datetime.fromisoformat(
            self.indatim.isoformat()).togregorian()
        self.indati2m = jdatetime.datetime.fromisoformat(
            self.indati2m.isoformat()).togregorian()
        self.taxid = generate_tax_id(settings.FISCAL_ID, self.indatim, self.inno)
        super(InvoiceHeader, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.invoice)


class InvoiceBody(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    sstid = models.CharField(
        "شناسه کالا/خدمت", max_length=50, null=True, blank=True)
    sstt = models.CharField(
        "شرح کالا/خدمت", max_length=50, null=True, blank=True)
    am = models.PositiveIntegerField("تعداد/مقدار کالا", null=True, blank=True)
    mu = models.CharField("واحد اندازه گیزی",
                          max_length=4, null=True, blank=True)
    fee = models.PositiveBigIntegerField("مبلغ واحد", null=True, blank=True)
    cfee = models.PositiveBigIntegerField("میزان ارز", null=True, blank=True)
    cut = models.CharField("نوع ارز", max_length=50, null=True, blank=True)
    exr = models.PositiveBigIntegerField(
        "نرخ برابری ارز با ریال", null=True, blank=True)
    prdis = models.PositiveBigIntegerField(
        "مبلغ قبل از تخفیف", null=True, blank=True)
    dis = models.PositiveBigIntegerField(
        "مبلغ تخفیف", null=True, blank=True, default=0)
    adis = models.PositiveBigIntegerField(
        "مبلغ بعد از تخفیف", null=True, blank=True)
    vra = models.PositiveBigIntegerField(
        "نرخ مالیات بر ارزش افزوده", null=True, blank=True, default=9)
    vam = models.PositiveBigIntegerField(
        "مبلغ مالیات بر ارزش افزوده", null=True, blank=True)
    odt = models.CharField("موضوع سایر مالیات و عوارض",
                           max_length=50, null=True, blank=True)
    odr = models.PositiveBigIntegerField(
        "نرخ سایر مالیات و عوارض", null=True, blank=True)
    odam = models.PositiveBigIntegerField(
        "مبلغ سایر مالیات و عوارض", null=True, blank=True)
    olt = models.CharField("موضوع سایر وجوه قانونی",
                           max_length=50, null=True, blank=True)
    olr = models.PositiveBigIntegerField(
        "نرخ سایر وجوه قانونی", null=True, blank=True)
    olam = models.PositiveBigIntegerField(
        "مبلغ سایر وجوه قانونی", null=True, blank=True)
    consfee = models.PositiveBigIntegerField(
        "اجرت ساخت", null=True, blank=True)
    spro = models.PositiveBigIntegerField("سود فروشنده", null=True, blank=True)
    bros = models.PositiveBigIntegerField("حق العمل", null=True, blank=True)
    tcpbs = models.PositiveBigIntegerField(
        "جمع کل اجرت، حق العمل و سود فروشنده", null=True, blank=True)
    cop = models.PositiveBigIntegerField(
        "سهم نقدی از پرداخت", null=True, blank=True)
    vop = models.PositiveBigIntegerField(
        "سهم ارزش افزوده از پرداخت", null=True, blank=True)
    bsrn = models.CharField(
        "شناسه یکتای ثبت قرارداد حق العملکاری", max_length=50, null=True, blank=True)
    tsstam = models.PositiveBigIntegerField(
        "مبلغ کل کالا/خدمت", null=True, blank=True)

    class Meta:
        verbose_name = "InvoiceBody"
        verbose_name_plural = "InvoiceBodys"

    def __str__(self):
        return str(self.invoice)


class InvoicePayment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    iinn = models.CharField("شماره سوییچ پرداخت",
                            max_length=50, null=True, blank=True)
    acn = models.CharField("شماره پذیرنده فروشگاهی",
                           max_length=50, null=True, blank=True)
    trmn = models.CharField(
        "شماره پایانه", max_length=50, null=True, blank=True)
    trn = models.CharField("شماره پیگیری", max_length=50,
                           null=True, blank=True)
    pcn = models.CharField("شماره کارت پرداخت کننده صورتحساب",
                           max_length=50, null=True, blank=True)
    pid = models.CharField(
        "شماره/شناسه ملی/کد فراگیر اتباع غیر ایرانی پرداخت کننده صورتحساب", max_length=50, null=True, blank=True)
    pdt = models.DateTimeField(
        "تاریخ و زمان پرداخت صورتحساب", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "InvoicePayment"
        verbose_name_plural = "InvoicePayments"

    def __str__(self):
        return str(self.invoice)


class InvoiceResult(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    uid = models.UUIDField(null=True, blank=True)
    reference_number = models.UUIDField(null=True, blank=True)
    error_code = models.PositiveIntegerField(null=True, blank=True)
    error_detail = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    confirmation_reference_id = models.UUIDField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    warnings = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "InvoiceResult"
        verbose_name_plural = "InvoiceResults"

    def __str__(self):
        return str(self.invoice)
