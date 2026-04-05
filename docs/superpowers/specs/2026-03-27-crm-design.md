# 顧客管理システム 設計書

**作成日:** 2026-03-27
**ステータス:** 承認済み

---

## 概要

メールアドレス・パスワード認証を備えた社内向け顧客管理Webアプリケーション。ローカル環境で起動し、将来的にサーバーへ移行できる構成とする。

---

## 技術スタック

| 項目 | 選定 |
|------|------|
| バックエンド | Django 5.x |
| フロントエンド | Django テンプレート + Tailwind CSS (CDN) |
| データベース（開発） | SQLite |
| データベース（本番） | PostgreSQL（`DATABASE_URL` 切り替えのみ） |
| 認証 | Django 組み込み認証 (`django.contrib.auth`) |
| Python | 3.11以上 |

---

## データモデル

### CustomUser

Django の `AbstractBaseUser` を拡張。

| フィールド | 型 | 備考 |
|------------|----|------|
| id | AutoField | PK |
| email | EmailField | ユニーク・ログインID |
| name | CharField | 表示名 |
| role | CharField | `admin` / `user` |
| is_active | BooleanField | デフォルト True |
| is_staff | BooleanField | Django admin用 |
| date_joined | DateTimeField | 自動 |

### Customer

| フィールド | 型 | 備考 |
|------------|----|------|
| id | AutoField | PK |
| customer_id | CharField | ユニーク・必須（例: C-0001） |
| name | CharField | 必須 |
| attribute | CharField | `corporate`/`individual`/`government` |
| corporate_number | CharField | 任意・法人のみ（13桁） |
| industry | CharField | 任意・選択式 |
| phone | CharField | 任意 |
| email | EmailField | 任意 |
| address | TextField | 任意 |
| note | TextField | 任意 |
| assigned_user | ForeignKey(CustomUser) | 担当者・NULL可 |
| created_at | DateTimeField | 自動 |
| updated_at | DateTimeField | 自動 |

### 業種選択肢

IT・通信 / 製造業 / 医療・福祉 / 建設・不動産 / 小売・流通 / 金融・保険 / 教育・研究 / 行政・自治体 / 農業・水産 / その他

---

## 権限設計

| 機能 | 管理者 | 一般ユーザー |
|------|--------|-------------|
| 顧客一覧・検索 | ✅ | ✅ |
| 顧客登録・編集・削除 | ✅ | ✅ |
| ユーザー一覧 | ✅ | ❌ |
| ユーザー登録・編集・削除 | ✅ | ❌ |

- ユーザー管理画面は `role == admin` のみアクセス可（ビューレベルで制御）
- 自分自身のアカウントは削除不可

---

## 画面一覧

| 画面 | URL | アクセス |
|------|-----|---------|
| ログイン | `/login/` | 全員（未認証） |
| ダッシュボード | `/` | 要ログイン |
| 顧客一覧 | `/customers/` | 要ログイン |
| 顧客登録 | `/customers/new/` | 要ログイン |
| 顧客編集 | `/customers/<id>/edit/` | 要ログイン |
| 顧客削除 | `/customers/<id>/delete/` | 要ログイン |
| ユーザー一覧 | `/users/` | 管理者のみ |
| ユーザー登録 | `/users/new/` | 管理者のみ |
| ユーザー編集 | `/users/<id>/edit/` | 管理者のみ |
| ユーザー削除 | `/users/<id>/delete/` | 管理者のみ |

---

## UI方針

- サイドバーナビ＋メインコンテンツのレイアウト
- Tailwind CSS CDNでレスポンシブ対応（スマートフォン閲覧可）
- 削除操作は確認ダイアログ（`confirm()`）を表示
- 顧客フォームの法人番号フィールドは属性「法人」選択時のみ表示（JS制御）
- フラッシュメッセージ（登録完了・エラー等）を画面上部に表示

---

## 顧客一覧フィルター

- キーワード検索（顧客名）
- 属性フィルター（全て / 法人 / 個人 / 自治体）
- 担当者フィルター（プルダウン）
- 業種フィルター（プルダウン）
- ページネーション（1ページ20件）

---

## プロジェクト構成

```
crm/
├── manage.py
├── requirements.txt
├── .env.example
├── crm_project/          # Django設定
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/             # 認証・ユーザー管理アプリ
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── customers/            # 顧客管理アプリ
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
└── templates/
    ├── base.html
    ├── accounts/
    └── customers/
```
