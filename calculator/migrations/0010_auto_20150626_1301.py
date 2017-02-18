# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0009_auto_20150625_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertycontract',
            name='address',
            field=models.CharField(max_length=100, null=True, verbose_name='address', blank=True),
        ),
        migrations.AddField(
            model_name='propertycontract',
            name='document_reason',
            field=models.CharField(max_length=50, null=True, verbose_name='document reason', blank=True),
        ),
        migrations.AddField(
            model_name='propertycontract',
            name='index',
            field=models.CharField(max_length=6, null=True, verbose_name='index', blank=True),
        ),
        migrations.AddField(
            model_name='propertycontract',
            name='n_reestr',
            field=models.CharField(max_length=50, null=True, verbose_name='registry number', blank=True),
        ),
        migrations.AddField(
            model_name='propertycontract',
            name='using_method',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='using method', choices=[(2, 'Istehsal sahesi'), (3, 'Yanacaqdoldruma stansiyasi'), (4, 'Restoran sebekesi'), (5, 'Magaza'), (6, 'Ofis binasi'), (7, 'Menzil'), (8, 'Bag evi'), (9, 'Ticaret'), (10, 'Kommersiya sahesu'), (11, 'Diger'), (12, 'Yasayis evi'), (1, 'Qeyri yasayis sah\u0259si')]),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='branch',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='branch', choices=[(21, 'Maliyy\u0259 v\u0259 sig\u0306orta f\u0259aliyy\u0259ti'), (22, 'Do\u0308vl\u0259t idar\u0259etm\u0259si v\u0259 mu\u0308dafi\u0259; icbari sosial t\u0259minat'), (23, 'Toxunulmazl\u0131q hu\u0308ququ olan t\u0259s\u0327kilatlar\u0131n f\u0259aliyy\u0259ti'), (24, 'Das\u0327\u0131nmaz \u0259mlakla \u0259laq\u0259dar \u0259m\u0259liyyatlar'), (25, 'I\u0307nzibati v\u0259 yard\u0131mc\u0327\u0131 xidm\u0259tl\u0259rin go\u0308st\u0259rilm\u0259si'), (26, 'T\u0259hsil'), (27, 'Pes\u0327\u0259, elmi v\u0259 texniki f\u0259aliyy\u0259t'), (28, 'I\u0307nformasiya v\u0259 rabit\u0259'), (29, 'Dig\u0259r sah\u0259l\u0259rd\u0259 xidm\u0259tl\u0259rin go\u0308st\u0259rilm\u0259si'), (30, '\u018fhaliy\u0259 s\u0259hiyy\u0259 v\u0259 sosial xidm\u0259tl\u0259rin go\u0308st\u0259rilm\u0259si'), (31, 'I\u0307stirah\u0259t, \u0259yl\u0259nc\u0259 v\u0259 inc\u0259s\u0259n\u0259t sah\u0259sind\u0259 f\u0259aliyy\u0259t'), (32, 'K\u0259nd t\u0259s\u0259rru\u0308fat\u0131, mes\u0327\u0259 t\u0259s\u0259rru\u0308fat\u0131 v\u0259 bal\u0131qc\u0327\u0131l\u0131q'), (33, 'N\u0259qliyyat v\u0259 anbar t\u0259s\u0259rru\u0308fat\u0131'), (35, 'Su t\u0259chizat\u0131; c\u0327irkli sular\u0131n v\u0259 tullant\u0131lar\u0131n t\u0259mizl\u0259nm\u0259si'), (36, 'Elektrik enerjisi, qaz, buxar v\u0259 kondisiyalas\u0327d\u0131r\u0131lm\u0131s\u0327 hava il\u0259 t\u0259chizat'), (37, 'Emal s\u0259nayesi'), (38, 'Yas\u0327ay\u0131s\u0327\u0131n t\u0259s\u0327kili v\u0259 ictimai ias\u0327\u0259'), (39, 'M\u0259d\u0259nc\u0327\u0131xarma s\u0259nayesi'), (40, 'Tikinti'), (34, 'Topdan v\u0259 p\u0259rak\u0259nd\u0259 ticar\u0259t, avtomobill\u0259rin v\u0259 motosikletl\u0259rin t\u0259miri')]),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='city',
            field=models.PositiveIntegerField(verbose_name='city', choices=[(77, 'Absheron'), (9, 'Astara'), (78, 'A\u011eDAM'), (6, 'A\u011fcab\u0259di'), (79, 'A\u011fda\u015f'), (85, 'A\u011fd\u0259r\u0259'), (8, 'A\u011fstafa'), (10, 'A\u011fsu'), (1, 'Bak\u0131'), (13, 'Balak\u0259n'), (76, 'Bebek'), (12, 'Beyl\u0259qan'), (14, 'Bil\u0259suvar'), (11, 'B\u0259rd\u0259'), (26, 'Culfa'), (25, 'C\u0259bray\u0131l'), (24, 'C\u0259lilabad'), (23, 'Da\u015fk\u0259s\u0259n'), (22, 'D\u0259lim\u0259mm\u0259dli'), (59, 'F\xfczuli'), (17, 'Goranboy'), (18, 'G\xf6yg\xf6l'), (19, 'G\xf6yt\u0259p\u0259'), (16, 'G\xf6y\xe7ay'), (35, 'G\u0259d\u0259b\u0259y'), (4, 'G\u0259nc\u0259'), (7, 'Hac\u0131qabul'), (21, 'Horadiz'), (40, 'K\xfcrd\u0259mir'), (36, 'K\u0259lb\u0259c\u0259r'), (81, 'K\u0259ng\u0259rli'), (41, 'La\xe7\u0131n'), (43, 'Lerik'), (44, 'Liman'), (42, 'L\u0259nk\u0259ran'), (45, 'Masall\u0131'), (46, 'Ming\u0259\xe7evir'), (83, 'M\u0259r\u0259z\u0259'), (84, 'Nabran'), (47, 'Naftalan'), (3, 'Nax\xe7\u0131van'), (48, 'Neft\xe7ala'), (50, 'Ordubad'), (49, 'O\u011fuz'), (34, 'Qax'), (33, 'Qazax'), (20, 'Qobustan'), (37, 'Quba'), (38, 'Qubadl\u0131'), (39, 'Qusar'), (15, 'Q\u0259b\u0259l\u0259'), (51, 'Saatl\u0131'), (52, 'Sabirabad'), (53, 'Salyan'), (54, 'Samux'), (55, 'Siy\u0259z\u0259n'), (2, 'Sumqay\u0131t'), (80, 'S\u0259d\u0259r\u0259k'), (56, 'Tovuz'), (57, 'T\u0259rt\u0259r'), (58, 'Ucar'), (60, 'Xank\u0259ndi'), (61, 'Xa\xe7maz'), (63, 'Xocal\u0131'), (62, 'Xocav\u0259nd'), (64, 'Xudat'), (66, 'X\u0131rdalan'), (65, 'X\u0131z\u0131'), (75, 'Yard\u0131ml\u0131'), (27, 'Yevlax'), (28, 'Zaqatala'), (29, 'Z\u0259ngilan'), (30, 'Z\u0259rdab'), (67, '\u015eabran'), (70, '\u015eahbuz'), (72, '\u015eamax\u0131'), (73, '\u015eirvan'), (82, '\u018fli-Bayraml\u0131'), (31, '\u0130mi\u015fli'), (32, '\u0130smay\u0131ll\u0131'), (74, '\u015eu\u015fa'), (71, '\u015e\u0259ki'), (68, '\u015e\u0259mkir'), (69, '\u015e\u0259rur')]),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='realty_type',
            field=models.PositiveIntegerField(verbose_name='realty type', choices=[(1, '\u041a\u0432\u0430\u0440\u0442\u0438\u0440\u0430 / \u0416\u0438\u043b\u043e\u0439 \u0434\u043e\u043c'), (2, '\u0410\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u0438\u0432\u043d\u043e\u0435 \u0437\u0434\u0430\u043d\u0438\u0435'), (3, '\u0414\u0440\u0443\u0433\u043e\u0435')]),
        ),
    ]
