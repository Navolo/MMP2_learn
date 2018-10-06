# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-19 12:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ox', models.IntegerField(blank=True, default=None, null=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('fx', models.FloatField(blank=True, null=True)),
                ('fy', models.FloatField(blank=True, null=True)),
                ('fz', models.FloatField(blank=True, null=True)),
                ('cx', models.BooleanField(default=True)),
                ('cy', models.BooleanField(default=True)),
                ('cz', models.BooleanField(default=True)),
                ('magmom', models.FloatField(blank=True, null=True)),
                ('charge', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('occupancy', models.FloatField(default=1)),
            ],
            options={
                'db_table': 'atom',
                'default_related_name': 'atoms',
            },
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('formula', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('generic', models.CharField(blank=True, max_length=255, null=True)),
                ('mass', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'composition',
                'default_related_name': 'compositions',
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('symbol', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('z', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('group', models.IntegerField()),
                ('period', models.IntegerField()),
                ('mass', models.FloatField(null=True)),
                ('electronegativity', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'element',
                'default_related_name': 'elements',
            },
        ),
        migrations.CreateModel(
            name='MolAtom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ox', models.IntegerField(blank=True, default=None, null=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('magmom', models.FloatField(blank=True, null=True)),
                ('charge', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'molAtom',
                'default_related_name': 'atoms',
            },
        ),
        migrations.CreateModel(
            name='MolComposition',
            fields=[
                ('formula', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('generic', models.CharField(blank=True, max_length=255, null=True)),
                ('mass', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'molComposition',
                'default_related_name': 'compositions',
            },
        ),
        migrations.CreateModel(
            name='MolElement',
            fields=[
                ('symbol', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('z', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('group', models.IntegerField()),
                ('period', models.IntegerField()),
                ('mass', models.FloatField(null=True)),
                ('electronegativity', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'molElement',
                'default_related_name': 'elements',
            },
        ),
        migrations.CreateModel(
            name='MolStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=80, null=True)),
                ('natoms', models.IntegerField(blank=True, null=True)),
                ('ntypes', models.IntegerField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('volume_pa', models.FloatField(blank=True, null=True)),
                ('composition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structures', to='material.MolComposition')),
                ('elements', models.ManyToManyField(related_name='structures', to='material.MolElement')),
            ],
            options={
                'db_table': 'molStructure',
                'default_related_name': 'structures',
            },
            bases=(models.Model, object),
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'operation',
                'default_related_name': 'operations',
            },
        ),
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('name', models.CharField(max_length=80, primary_key=True, serialize=False)),
                ('composition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prototypes', to='material.Composition')),
            ],
            options={
                'db_table': 'prototype',
                'default_related_name': 'prototypes',
            },
        ),
        migrations.CreateModel(
            name='Rotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a11', models.FloatField()),
                ('a12', models.FloatField()),
                ('a13', models.FloatField()),
                ('a21', models.FloatField()),
                ('a22', models.FloatField()),
                ('a23', models.FloatField()),
                ('a31', models.FloatField()),
                ('a32', models.FloatField()),
                ('a33', models.FloatField()),
            ],
            options={
                'db_table': 'rotation',
                'default_related_name': 'rotations',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('coordiantion_number', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'site',
                'default_related_name': 'sites',
            },
        ),
        migrations.CreateModel(
            name='Spacegroup',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('hm', models.CharField(blank=True, max_length=20, null=True)),
                ('hall', models.CharField(blank=True, max_length=20, null=True)),
                ('pearson', models.CharField(blank=True, max_length=20, null=True)),
                ('schoenflies', models.CharField(blank=True, max_length=20, null=True)),
                ('lattice_system', models.CharField(blank=True, max_length=20, null=True)),
                ('centerosymmetric', models.BooleanField(default=False)),
                ('operations', models.ManyToManyField(related_name='spacegroups', to='material.Operation')),
            ],
            options={
                'db_table': 'spacegroup',
                'default_related_name': 'spacegroups',
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('name', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('ox', models.IntegerField(blank=True, null=True)),
                ('element', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='species', to='material.Element')),
            ],
            options={
                'db_table': 'species',
                'default_related_name': 'species',
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=80, null=True)),
                ('comment', models.CharField(default='', max_length=80)),
                ('natoms', models.IntegerField(blank=True, null=True)),
                ('nsites', models.IntegerField(blank=True, null=True)),
                ('ntypes', models.IntegerField(blank=True, null=True)),
                ('multiple', models.IntegerField(blank=True, null=True)),
                ('x1', models.FloatField(null=True)),
                ('y1', models.FloatField(null=True)),
                ('z1', models.FloatField(null=True)),
                ('x2', models.FloatField(null=True)),
                ('y2', models.FloatField(null=True)),
                ('z2', models.FloatField(null=True)),
                ('x3', models.FloatField(null=True)),
                ('y3', models.FloatField(null=True)),
                ('z3', models.FloatField(null=True)),
                ('volume', models.FloatField(null=True)),
                ('volume_pa', models.FloatField(null=True)),
                ('energy', models.FloatField(blank=True, null=True)),
                ('energy_per_formula', models.FloatField(blank=True, null=True)),
                ('energy_per_atom', models.FloatField(blank=True, null=True)),
                ('composition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structures', to='material.Composition')),
                ('elements', models.ManyToManyField(related_name='structures', to='material.Element')),
                ('prototype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='material.Prototype')),
                ('spacegroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structures', to='material.Spacegroup')),
                ('species', models.ManyToManyField(related_name='structures', to='material.Species')),
            ],
            options={
                'db_table': 'structure',
                'default_related_name': 'structures',
            },
            bases=(models.Model, object),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
            ],
            options={
                'db_table': 'translation',
                'default_related_name': 'translations',
            },
        ),
        migrations.CreateModel(
            name='WyckoffSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=1)),
                ('multiplicity', models.IntegerField(blank=True, null=True)),
                ('x', models.FloatField(blank=True, null=True)),
                ('y', models.FloatField(blank=True, null=True)),
                ('z', models.FloatField(blank=True, null=True)),
                ('spacegroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wyckoffSites', to='material.Spacegroup')),
            ],
            options={
                'db_table': 'wyckoffSite',
                'default_related_name': 'wyckoffSites',
            },
        ),
        migrations.AddField(
            model_name='site',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='material.Structure'),
        ),
        migrations.AddField(
            model_name='site',
            name='wyckoff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='material.WyckoffSite'),
        ),
        migrations.AddField(
            model_name='prototype',
            name='structures',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='material.Structure'),
        ),
        migrations.AddField(
            model_name='operation',
            name='rotation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='material.Rotation'),
        ),
        migrations.AddField(
            model_name='operation',
            name='translation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='material.Translation'),
        ),
        migrations.AddField(
            model_name='molcomposition',
            name='elements',
            field=models.ManyToManyField(related_name='compositions', to='material.MolElement'),
        ),
        migrations.AddField(
            model_name='molatom',
            name='element',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atoms', to='material.MolElement'),
        ),
        migrations.AddField(
            model_name='molatom',
            name='structure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atoms', to='material.MolStructure'),
        ),
        migrations.AddField(
            model_name='composition',
            name='elements',
            field=models.ManyToManyField(related_name='compositions', to='material.Element'),
        ),
        migrations.AddField(
            model_name='atom',
            name='element',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atoms', to='material.Element'),
        ),
        migrations.AddField(
            model_name='atom',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atoms', to='material.Site'),
        ),
        migrations.AddField(
            model_name='atom',
            name='species',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atoms', to='material.Species'),
        ),
        migrations.AddField(
            model_name='atom',
            name='structure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atoms', to='material.Structure'),
        ),
        migrations.AddField(
            model_name='atom',
            name='wyckoff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atoms', to='material.WyckoffSite'),
        ),
    ]
