"""初期データ作成スクリプト"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from accounts.models import CustomUser
from customers.models import Customer

# 管理者アカウント
if not CustomUser.objects.filter(email='admin@example.com').exists():
    admin = CustomUser.objects.create_user(
        email='admin@example.com',
        password='admin1234',
        name='管理者',
        role='admin',
        is_staff=True,
        is_superuser=True,
    )
    print(f'管理者作成: {admin.email}')

# 一般ユーザー
users_data = [
    ('yamada@example.com', 'pass1234', '山田 太郎'),
    ('suzuki@example.com', 'pass1234', '鈴木 花子'),
]
created_users = {}
for email, pw, name in users_data:
    if not CustomUser.objects.filter(email=email).exists():
        u = CustomUser.objects.create_user(email=email, password=pw, name=name, role='user')
        print(f'ユーザー作成: {name}')
    created_users[name] = CustomUser.objects.get(email=email)

# サンプル顧客
customers_data = [
    ('C-0001', '株式会社サンプル商事', 'corporate', 'manufacturing', '03-1234-5678', '山田 太郎'),
    ('C-0002', '田中 健一', 'individual', 'other', '090-1234-5678', '鈴木 花子'),
    ('C-0003', '○○市役所', 'government', 'government', '0120-000-000', '山田 太郎'),
    ('C-0004', '合同会社テック', 'corporate', 'it', '06-9876-5432', '鈴木 花子'),
    ('C-0005', '△△医療法人', 'corporate', 'medical', '052-111-2222', '山田 太郎'),
]
for cid, name, attr, industry, phone, assignee in customers_data:
    if not Customer.objects.filter(customer_id=cid).exists():
        Customer.objects.create(
            customer_id=cid,
            name=name,
            attribute=attr,
            industry=industry,
            phone=phone,
            assigned_user=created_users.get(assignee),
        )
        print(f'顧客作成: {name}')

print('\n完了！')
print('管理者ログイン: admin@example.com / admin1234')
print('一般ユーザー:   yamada@example.com / pass1234')
