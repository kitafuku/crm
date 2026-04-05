from django import forms
from .models import Customer
from accounts.models import CustomUser


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_id', 'name', 'attribute', 'corporate_number',
            'industry', 'assigned_user', 'phone', 'email', 'address', 'note',
        ]
        labels = {
            'customer_id': '顧客ID',
            'name': '顧客名',
            'attribute': '属性',
            'corporate_number': '法人番号',
            'industry': '業種',
            'assigned_user': '担当者',
            'phone': '電話番号',
            'email': 'メールアドレス',
            'address': '住所',
            'note': '備考',
        }
        widgets = {
            'customer_id': forms.TextInput(attrs={'placeholder': '例: C-0001'}),
            'name': forms.TextInput(attrs={'placeholder': '例: 株式会社サンプル商事'}),
            'corporate_number': forms.TextInput(attrs={'placeholder': '13桁の法人番号', 'maxlength': '13'}),
            'phone': forms.TextInput(attrs={'placeholder': '03-1234-5678'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contact@example.com'}),
            'address': forms.TextInput(attrs={'placeholder': '東京都千代田区...'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': '特記事項など'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_user'].queryset = CustomUser.objects.filter(is_active=True).order_by('name')
        self.fields['assigned_user'].empty_label = '— 選択してください —'
        self.fields['attribute'].widget.attrs['id'] = 'id_attribute'
        self.fields['corporate_number'].required = False
