import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("myapp", "0009_alter_farmerprofile_phone"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Order", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("product_name", models.CharField(max_length=200)),
            ("quantity", models.PositiveIntegerField()),
            ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ("total_amount", models.DecimalField(decimal_places=2, max_digits=12)),
            ("contact_phone", models.CharField(max_length=20)),
            ("delivery_address", models.TextField()),
            ("status", models.CharField(choices=[(x, x.title()) for x in ("pending", "accepted", "completed", "rejected", "cancelled")], default="pending", max_length=12)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("buyer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="purchases", to=settings.AUTH_USER_MODEL)),
            ("seller", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="sales", to=settings.AUTH_USER_MODEL)),
            ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="myapp.product")),
        ]),
        migrations.CreateModel(name="Notification", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("message", models.CharField(max_length=255)),
            ("is_read", models.BooleanField(default=False)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("order", models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="myapp.order")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ]),
    ]
