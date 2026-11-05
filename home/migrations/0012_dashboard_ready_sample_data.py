from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.db import migrations, models


def normalize_shipment_costs(apps, schema_editor):
    """Make legacy text costs safe to convert to a numeric database column."""
    Sample = apps.get_model('home', 'Sample')
    for sample in Sample.objects.exclude(shipment_cost__isnull=True).iterator():
        raw = str(sample.shipment_cost).strip()
        if not raw:
            sample.shipment_cost = None
            sample.save(update_fields=['shipment_cost'])
            continue

        value = raw.replace('R$', '').replace('$', '').replace(' ', '')
        if ',' in value and '.' in value:
            if value.rfind(',') > value.rfind('.'):
                value = value.replace('.', '').replace(',', '.')
            else:
                value = value.replace(',', '')
        elif ',' in value:
            value = value.replace(',', '.')

        try:
            amount = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            if not amount.is_finite() or amount < 0 or amount.adjusted() > 9:
                raise InvalidOperation
            sample.shipment_cost = format(amount, 'f')
        except (InvalidOperation, ValueError):
            # Values that cannot be trusted as money must not distort aggregates.
            sample.shipment_cost = None
        sample.save(update_fields=['shipment_cost'])


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_sample_gross_weight_sample_gross_weight_unit_and_more'),
    ]

    operations = [
        migrations.RunPython(normalize_shipment_costs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='sample',
            name='shipment_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='shipment_currency',
            field=models.CharField(choices=[('BRL', 'Real brasileiro (BRL)')], default='BRL', max_length=3),
        ),
        migrations.AlterField(
            model_name='sample',
            name='courier',
            field=models.CharField(blank=True, choices=[('FedEx', 'FedEx'), ('Correios', 'Correios'), ('DHL', 'DHL'), ('UPS', 'UPS')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_type',
            field=models.CharField(blank=True, choices=[('Pré embarque', 'Pré Embarque'), ('Embarque', 'Embarque'), ('Amostra Comercial', 'Amostra Comercial')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='status',
            field=models.CharField(blank=True, choices=[('Pendente', 'Pendente'), ('Aguardando coleta', 'Aguardando coleta'), ('Em Trânsito', 'Em Trânsito'), ('Concluído', 'Concluído')], max_length=100, null=True),
        ),
        migrations.AddIndex(
            model_name='sample',
            index=models.Index(fields=['shipping_date'], name='home_sample_shippin_0e663d_idx'),
        ),
        migrations.AddIndex(
            model_name='sample',
            index=models.Index(fields=['delivery_date'], name='home_sample_deliver_0f0479_idx'),
        ),
        migrations.AddIndex(
            model_name='sample',
            index=models.Index(fields=['status'], name='home_sample_status_f1c979_idx'),
        ),
        migrations.AddIndex(
            model_name='sample',
            index=models.Index(fields=['courier'], name='home_sample_courier_ac62b2_idx'),
        ),
        migrations.AddIndex(
            model_name='sample',
            index=models.Index(fields=['client', 'shipping_date'], name='home_sample_client__fb582b_idx'),
        ),
    ]
