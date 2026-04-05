from django.db import models
from django.conf import settings


class Customer(models.Model):
    ATTR_CORPORATE = 'corporate'
    ATTR_INDIVIDUAL = 'individual'
    ATTR_GOVERNMENT = 'government'
    ATTR_CHOICES = [
        (ATTR_CORPORATE, '法人'),
        (ATTR_INDIVIDUAL, '個人'),
        (ATTR_GOVERNMENT, '自治体'),
    ]

    INDUSTRY_CHOICES = [
        ('it', 'IT・通信'),
        ('manufacturing', '製造業'),
        ('medical', '医療・福祉'),
        ('construction', '建設・不動産'),
        ('retail', '小売・流通'),
        ('finance', '金融・保険'),
        ('education', '教育・研究'),
        ('government', '行政・自治体'),
        ('agriculture', '農業・水産'),
        ('other', 'その他'),
    ]

    customer_id = models.CharField(max_length=50, unique=True, verbose_name='顧客ID')
    name = models.CharField(max_length=200, verbose_name='顧客名')
    attribute = models.CharField(max_length=20, choices=ATTR_CHOICES, default=ATTR_CORPORATE, verbose_name='属性')
    corporate_number = models.CharField(max_length=13, blank=True, verbose_name='法人番号')
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, blank=True, verbose_name='業種')
    phone = models.CharField(max_length=20, blank=True, verbose_name='電話番号')
    email = models.EmailField(blank=True, verbose_name='メールアドレス')
    address = models.TextField(blank=True, verbose_name='住所')
    note = models.TextField(blank=True, verbose_name='備考')
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
        verbose_name='担当者',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='登録日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = '顧客'
        verbose_name_plural = '顧客'
        ordering = ['customer_id']

    def __str__(self):
        return f'{self.customer_id} {self.name}'

    def get_attribute_display_class(self):
        return {
            self.ATTR_CORPORATE: 'attr-corp',
            self.ATTR_INDIVIDUAL: 'attr-indiv',
            self.ATTR_GOVERNMENT: 'attr-gov',
        }.get(self.attribute, '')
