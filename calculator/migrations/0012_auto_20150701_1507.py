# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0011_auto_20150701_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertycontract',
            name='d_start',
            field=models.DateField(null=True, verbose_name='contract start date', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='delivery_type',
            field=models.CharField(max_length=10, null=True, verbose_name='delivery type', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_country',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='country', choices=[(146, 'AAE'), (16, 'AFGHANISTAN'), (5, 'ALBANIA'), (6, 'ALGERIA'), (7, 'AMERICAN_SAMOA'), (10, 'ANDORRA'), (9, 'ANGOLA'), (8, 'ANGUILLA'), (251, 'ANTARCTICA'), (12, 'ANTIGUA_BARBUDA'), (13, 'ARGENTINA'), (14, 'ARMENIA'), (15, 'ARUBA'), (2, 'AUSTRALIA'), (3, 'AUSTRIA'), (4, 'AZERBAIJAN'), (257, 'All Shengen'), (256, 'All the world'), (258, 'All world, except USA, Canada, Australia, Japan'), (17, 'BAHAMAS'), (20, 'BAHRAIN'), (18, 'BANGLADESH'), (19, 'BARBADOS'), (21, 'BELARUS'), (23, 'BELGIUM'), (22, 'BELIZE'), (24, 'BENIN'), (25, 'BERMUDA'), (36, 'BHUTAN'), (27, 'BOLIVIA'), (29, 'BOSNIA'), (30, 'BOTSWANA'), (148, 'BOUVET_ISLAND'), (31, 'BRAZIL'), (32, 'BRITIS_IND_OC_TER'), (33, 'BRUNEI_DARUSSALAM'), (26, 'BULGARIA'), (34, 'BURKINA_FASO'), (35, 'BURUNDI'), (84, 'CAMBODIA'), (85, 'CAMEROON'), (86, 'CANADA'), (82, 'CAPE_VERDE'), (153, 'CAYMAN ISLANDS'), (230, 'CHAD'), (233, 'CHILE'), (92, 'CHINA'), (151, 'CHRISTMAS_ISLAND'), (93, 'COCOS_ISLANDS'), (94, 'COLOMBIA'), (95, 'COMOROS'), (97, 'CONGO_REPUBLIC'), (96, 'CONGO_ZAIRE'), (154, 'COOK_ISLANDS'), (100, 'COSTA_RICA'), (254, 'COTE_DIVOIRE'), (228, 'CROATIA'), (101, 'CUBA'), (89, 'CYPRUS'), (232, 'CZECH'), (229, 'C_AFRICAN_REP'), (62, 'DENMARK'), (64, 'DJIBOUTI'), (65, 'DOMINICA'), (66, 'DOMINICAN_REP'), (205, 'EAST_TIMOR'), (238, 'ECUADOR'), (67, 'EGYPT'), (241, 'EL_SALVADOR'), (239, 'EQUATORIAL_GUINEA'), (242, 'ERITREA'), (243, 'ESTONIA'), (244, 'ETHIOPIA'), (223, 'FALKLAND_ISLANDS'), (219, 'FAROE_ISLANDS'), (220, 'FIJI'), (222, 'FINLAND'), (224, 'FRANCE'), (225, 'FRENCH_GUIANA'), (226, 'FRENCH_POLYNESIA'), (227, 'FRENCH_S_TERRITO'), (43, 'GABON'), (46, 'GAMBIA'), (60, 'GEORGIA'), (52, 'GERMANY'), (47, 'GHANA'), (54, 'GIBRALTAR'), (59, 'GREECE'), (58, 'GREENLAND'), (57, 'GRENADINES'), (48, 'GUADELOUPE'), (61, 'GUAM'), (49, 'GUATEMALA'), (50, 'GUINEA'), (51, 'GUINEA_BISSAU'), (45, 'GUYANA'), (44, 'HAITI'), (152, 'HEARD_DONALD_ISLS'), (55, 'HONDURAS'), (56, 'HONG_KONG'), (38, 'HUNGARY'), (78, 'ICELAND'), (72, 'INDIA'), (73, 'INDONESIA'), (76, 'IRAN'), (75, 'IRAQ'), (77, 'IRELAND'), (71, 'ISRAEL'), (80, 'ITALY'), (249, 'JAMAICA'), (250, 'JAPAN'), (74, 'JORDAN'), (83, 'KAZAKHSTAN'), (88, 'KENYA'), (91, 'KIRIBATI'), (99, 'KOREA'), (98, 'KOREA_DEMOCR_REP'), (102, 'KUWAIT'), (90, 'KYRGYZSTAN'), (104, 'LAO'), (105, 'LATVIA'), (107, 'LEBANON'), (106, 'LESOTHO'), (109, 'LIBERIA'), (110, 'LIECHTENSTEIN'), (111, 'LITHUANIA'), (112, 'LUXEMBOURG'), (117, 'MACAU'), (168, 'MACEDONIA'), (115, 'MADAGASCAR'), (118, 'MALAWI'), (119, 'MALAYSIA'), (122, 'MALDIVES'), (120, 'MALI'), (123, 'MALTA'), (179, 'MARIANA_ISLANDS'), (126, 'MARSHALL_ISLANDS'), (125, 'MARTINIQUE'), (114, 'MAURITANIA'), (116, 'MAYOTTE'), (127, 'MEXICO'), (128, 'MICRONESIA'), (130, 'MOLDOVA'), (131, 'MONACO'), (132, 'MONGOLIA'), (133, 'MONTSERRAT'), (124, 'MOROCCO'), (129, 'MOZAMBIQUE'), (134, 'MYANMAR'), (135, 'NAMIBIA'), (136, 'NAURU'), (137, 'NEPAL'), (140, 'NETHERLANDS'), (144, 'NEW_CALEDONIA'), (143, 'NEW_ZEALAND'), (141, 'NICARAGUA'), (138, 'NIGER'), (139, 'NIGERIA'), (142, 'NIUE'), (150, 'NORFOLK_ISLAND'), (145, 'NORWAY'), (147, 'OMAN'), (156, 'PAKISTAN'), (157, 'PALAU'), (158, 'PALESTINA'), (159, 'PANAMA'), (161, 'PAPUA_NEW_GUINEA'), (162, 'PARAGUAY'), (163, 'PERU'), (221, 'PHILIPPINES'), (164, 'PITCAIRN'), (165, 'POLAND'), (166, 'PORTUGAL'), (167, 'PUERTO_RICO'), (87, 'QATAR'), (169, 'REUNION'), (172, 'ROMANIA'), (170, 'RUSSIA'), (171, 'RWANDA'), (184, 'SAINT_KITTS_NEVIS'), (185, 'SAINT_LUCIA'), (173, 'SAMOA'), (246, 'SANDWICH_ISLANDS'), (174, 'SAN_MARINO'), (175, 'SAO_TOME_PRINCIPE'), (176, 'SAUDI_ARABIA'), (182, 'SENEGAL'), (187, 'SERBIA_MONTENEGRO'), (188, 'SEYCHELLES'), (200, 'SIERRA_LEONE'), (189, 'SINGAPORE'), (192, 'SLOVAKIA'), (193, 'SLOVENIA'), (196, 'SOLOMON_ISLANDS'), (197, 'SOMALIA'), (245, 'SOUTH_AFRICA'), (79, 'SPAIN'), (237, 'SRI_LANKA'), (178, 'ST_HELENA'), (186, 'ST_PIERRE_MIQUELO'), (198, 'SUDAN'), (199, 'SURINAME'), (236, 'SVALBARD_ISLANDS'), (177, 'SWAZILAND'), (235, 'SWEDEN'), (234, 'SWITZERLAND'), (191, 'SYRIA'), (203, 'TAIWAN'), (201, 'TAJIKISTAN'), (204, 'TANZANIA'), (202, 'THAILAND'), (206, 'TOGO'), (207, 'TOKELAU'), (208, 'TONGA'), (209, 'TRINIDAD_TOBAGO'), (211, 'TUNISIA'), (213, 'TURKEY'), (212, 'TURKMENISTAN'), (155, 'TURKS_CAICOS_ISL'), (210, 'TUVALU'), (214, 'UGANDA'), (216, 'UKRAINE'), (194, 'UNITED_KINGDOM'), (218, 'URUGUAY'), (195, 'USA'), (121, 'US_ISLANDS'), (215, 'UZBEKISTAN'), (37, 'VANUATU'), (253, 'VATICAN'), (39, 'VENEZUELA'), (42, 'VIET_NAM'), (40, 'VIRGIN_ISL_BRIT'), (41, 'VIRGIN_ISL_US'), (217, 'WALLIS_FUT_ISLS'), (69, 'WESTERN_SAHARA'), (259, 'Western Europe'), (81, 'YEMEN'), (68, 'ZAMBIA'), (70, 'ZIMBABWE'), (181, '\u0421\u0435\u043d-\u041c\u0430\u0440\u0442\u0435\u043d'), (255, '\u0421\u0435\u043d-\u041c\u0430\u0440\u0442\u0435\u043d (\u0424\u0440\u0430\u043d\u0446\u0438\u044f)'), (180, '\u0421\u0435\u043d-\u0411\u0430\u0440\u0442\u0435\u043b\u044c\u043c\u0438'), (190, '\u0421\u0438\u043d\u0442-\u041c\u0430\u0440\u0442\u0435\u043d'), (183, '\u0421\u0435\u043d\u0442-\u0412\u0438\u043d\u0441\u0435\u043d\u0442 \u0438 \u0413\u0440\u0435\u043d\u0430\u0434\u0438\u043d\u044b'), (248, '\u042e\u0436\u043d\u044b\u0439 \u0421\u0443\u0434\u0430\u043d'), (247, '\u042e\u0436\u043d\u0430\u044f \u041e\u0441\u0435\u0442\u0438\u044f'), (53, '\u0413\u0435\u0440\u043d\u0441\u0438'), (63, '\u0414\u0436\u0435\u0440\u0441\u0438'), (149, '\u041e\u0441\u0442\u0440\u043e\u0432 \u041c\u044d\u043d'), (1, '\u0410\u0431\u0445\u0430\u0437\u0438\u044f'), (103, '\u041a\u044e\u0440\u0430\u0441\u0430\u043e'), (160, '\u041f\u0430\u043f\u0441\u043a\u0438\u0439 \u041f\u0440\u0435\u0441\u0442\u043e\u043b (\u0413\u043e\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u043e &mdash; \u0433\u043e\u0440\u043e\u0434 \u0412\u0430\u0442\u0438\u043a\u0430\u043d)'), (28, '\u0411\u043e\u043d\u0430\u0439\u0440\u0435, \u0421\u0430\u0431\u0430 \u0438 \u0421\u0438\u043d\u0442-\u042d\u0441\u0442\u0430\u0442\u0438\u0443\u0441'), (113, '\u041c\u0430\u0432\u0440\u0438\u043a\u0438\u0439'), (252, '\u0410\u043b\u0430\u043d\u0434\u0441\u043a\u0438\u0435 \u043e\u0441\u0442\u0440\u043e\u0432\u0430'), (240, '\u042d\u043b\u0430\u043d\u0434\u0441\u043a\u0438\u0435 \u043e\u0441\u0442\u0440\u043e\u0432\u0430'), (108, '\u041b\u0438\u0432\u0438\u0439\u0441\u043a\u0430\u044f \u0410\u0440\u0430\u0431\u0441\u043a\u0430\u044f \u0414\u0436\u0430\u043c\u0430\u0445\u0438\u0440\u0438\u044f'), (11, '\u0410\u043d\u0442\u0430\u0440\u043a\u0442\u0438\u0434\u0430'), (231, '\u0427\u0435\u0440\u043d\u043e\u0433\u043e\u0440\u0438\u044f')]),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_index',
            field=models.CharField(max_length=6, null=True, verbose_name='postal index (ZIP)', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_person_birthday',
            field=models.DateField(null=True, verbose_name='birthday', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_person_fname',
            field=models.CharField(max_length=50, null=True, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_person_gender',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='gender', choices=[(1, 'Male'), (2, 'Female')]),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_person_lname',
            field=models.CharField(max_length=50, null=True, verbose_name='last name', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_person_mname',
            field=models.CharField(max_length=50, null=True, verbose_name='middle name', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_person_pin',
            field=models.CharField(max_length=9, null=True, verbose_name='PIN', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_phone',
            field=models.CharField(max_length=12, null=True, verbose_name='phone', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='term_insurance',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='term insurance', choices=[(1, '1 \u0433\u043e\u0434'), (2, '1 \u043c\u0435\u0441\u044f\u0446')]),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='d_start',
            field=models.DateField(null=True, verbose_name='contract start date', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='delivery_type',
            field=models.CharField(max_length=10, null=True, verbose_name='delivery type', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_country',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='country', choices=[(146, 'AAE'), (16, 'AFGHANISTAN'), (5, 'ALBANIA'), (6, 'ALGERIA'), (7, 'AMERICAN_SAMOA'), (10, 'ANDORRA'), (9, 'ANGOLA'), (8, 'ANGUILLA'), (251, 'ANTARCTICA'), (12, 'ANTIGUA_BARBUDA'), (13, 'ARGENTINA'), (14, 'ARMENIA'), (15, 'ARUBA'), (2, 'AUSTRALIA'), (3, 'AUSTRIA'), (4, 'AZERBAIJAN'), (257, 'All Shengen'), (256, 'All the world'), (258, 'All world, except USA, Canada, Australia, Japan'), (17, 'BAHAMAS'), (20, 'BAHRAIN'), (18, 'BANGLADESH'), (19, 'BARBADOS'), (21, 'BELARUS'), (23, 'BELGIUM'), (22, 'BELIZE'), (24, 'BENIN'), (25, 'BERMUDA'), (36, 'BHUTAN'), (27, 'BOLIVIA'), (29, 'BOSNIA'), (30, 'BOTSWANA'), (148, 'BOUVET_ISLAND'), (31, 'BRAZIL'), (32, 'BRITIS_IND_OC_TER'), (33, 'BRUNEI_DARUSSALAM'), (26, 'BULGARIA'), (34, 'BURKINA_FASO'), (35, 'BURUNDI'), (84, 'CAMBODIA'), (85, 'CAMEROON'), (86, 'CANADA'), (82, 'CAPE_VERDE'), (153, 'CAYMAN ISLANDS'), (230, 'CHAD'), (233, 'CHILE'), (92, 'CHINA'), (151, 'CHRISTMAS_ISLAND'), (93, 'COCOS_ISLANDS'), (94, 'COLOMBIA'), (95, 'COMOROS'), (97, 'CONGO_REPUBLIC'), (96, 'CONGO_ZAIRE'), (154, 'COOK_ISLANDS'), (100, 'COSTA_RICA'), (254, 'COTE_DIVOIRE'), (228, 'CROATIA'), (101, 'CUBA'), (89, 'CYPRUS'), (232, 'CZECH'), (229, 'C_AFRICAN_REP'), (62, 'DENMARK'), (64, 'DJIBOUTI'), (65, 'DOMINICA'), (66, 'DOMINICAN_REP'), (205, 'EAST_TIMOR'), (238, 'ECUADOR'), (67, 'EGYPT'), (241, 'EL_SALVADOR'), (239, 'EQUATORIAL_GUINEA'), (242, 'ERITREA'), (243, 'ESTONIA'), (244, 'ETHIOPIA'), (223, 'FALKLAND_ISLANDS'), (219, 'FAROE_ISLANDS'), (220, 'FIJI'), (222, 'FINLAND'), (224, 'FRANCE'), (225, 'FRENCH_GUIANA'), (226, 'FRENCH_POLYNESIA'), (227, 'FRENCH_S_TERRITO'), (43, 'GABON'), (46, 'GAMBIA'), (60, 'GEORGIA'), (52, 'GERMANY'), (47, 'GHANA'), (54, 'GIBRALTAR'), (59, 'GREECE'), (58, 'GREENLAND'), (57, 'GRENADINES'), (48, 'GUADELOUPE'), (61, 'GUAM'), (49, 'GUATEMALA'), (50, 'GUINEA'), (51, 'GUINEA_BISSAU'), (45, 'GUYANA'), (44, 'HAITI'), (152, 'HEARD_DONALD_ISLS'), (55, 'HONDURAS'), (56, 'HONG_KONG'), (38, 'HUNGARY'), (78, 'ICELAND'), (72, 'INDIA'), (73, 'INDONESIA'), (76, 'IRAN'), (75, 'IRAQ'), (77, 'IRELAND'), (71, 'ISRAEL'), (80, 'ITALY'), (249, 'JAMAICA'), (250, 'JAPAN'), (74, 'JORDAN'), (83, 'KAZAKHSTAN'), (88, 'KENYA'), (91, 'KIRIBATI'), (99, 'KOREA'), (98, 'KOREA_DEMOCR_REP'), (102, 'KUWAIT'), (90, 'KYRGYZSTAN'), (104, 'LAO'), (105, 'LATVIA'), (107, 'LEBANON'), (106, 'LESOTHO'), (109, 'LIBERIA'), (110, 'LIECHTENSTEIN'), (111, 'LITHUANIA'), (112, 'LUXEMBOURG'), (117, 'MACAU'), (168, 'MACEDONIA'), (115, 'MADAGASCAR'), (118, 'MALAWI'), (119, 'MALAYSIA'), (122, 'MALDIVES'), (120, 'MALI'), (123, 'MALTA'), (179, 'MARIANA_ISLANDS'), (126, 'MARSHALL_ISLANDS'), (125, 'MARTINIQUE'), (114, 'MAURITANIA'), (116, 'MAYOTTE'), (127, 'MEXICO'), (128, 'MICRONESIA'), (130, 'MOLDOVA'), (131, 'MONACO'), (132, 'MONGOLIA'), (133, 'MONTSERRAT'), (124, 'MOROCCO'), (129, 'MOZAMBIQUE'), (134, 'MYANMAR'), (135, 'NAMIBIA'), (136, 'NAURU'), (137, 'NEPAL'), (140, 'NETHERLANDS'), (144, 'NEW_CALEDONIA'), (143, 'NEW_ZEALAND'), (141, 'NICARAGUA'), (138, 'NIGER'), (139, 'NIGERIA'), (142, 'NIUE'), (150, 'NORFOLK_ISLAND'), (145, 'NORWAY'), (147, 'OMAN'), (156, 'PAKISTAN'), (157, 'PALAU'), (158, 'PALESTINA'), (159, 'PANAMA'), (161, 'PAPUA_NEW_GUINEA'), (162, 'PARAGUAY'), (163, 'PERU'), (221, 'PHILIPPINES'), (164, 'PITCAIRN'), (165, 'POLAND'), (166, 'PORTUGAL'), (167, 'PUERTO_RICO'), (87, 'QATAR'), (169, 'REUNION'), (172, 'ROMANIA'), (170, 'RUSSIA'), (171, 'RWANDA'), (184, 'SAINT_KITTS_NEVIS'), (185, 'SAINT_LUCIA'), (173, 'SAMOA'), (246, 'SANDWICH_ISLANDS'), (174, 'SAN_MARINO'), (175, 'SAO_TOME_PRINCIPE'), (176, 'SAUDI_ARABIA'), (182, 'SENEGAL'), (187, 'SERBIA_MONTENEGRO'), (188, 'SEYCHELLES'), (200, 'SIERRA_LEONE'), (189, 'SINGAPORE'), (192, 'SLOVAKIA'), (193, 'SLOVENIA'), (196, 'SOLOMON_ISLANDS'), (197, 'SOMALIA'), (245, 'SOUTH_AFRICA'), (79, 'SPAIN'), (237, 'SRI_LANKA'), (178, 'ST_HELENA'), (186, 'ST_PIERRE_MIQUELO'), (198, 'SUDAN'), (199, 'SURINAME'), (236, 'SVALBARD_ISLANDS'), (177, 'SWAZILAND'), (235, 'SWEDEN'), (234, 'SWITZERLAND'), (191, 'SYRIA'), (203, 'TAIWAN'), (201, 'TAJIKISTAN'), (204, 'TANZANIA'), (202, 'THAILAND'), (206, 'TOGO'), (207, 'TOKELAU'), (208, 'TONGA'), (209, 'TRINIDAD_TOBAGO'), (211, 'TUNISIA'), (213, 'TURKEY'), (212, 'TURKMENISTAN'), (155, 'TURKS_CAICOS_ISL'), (210, 'TUVALU'), (214, 'UGANDA'), (216, 'UKRAINE'), (194, 'UNITED_KINGDOM'), (218, 'URUGUAY'), (195, 'USA'), (121, 'US_ISLANDS'), (215, 'UZBEKISTAN'), (37, 'VANUATU'), (253, 'VATICAN'), (39, 'VENEZUELA'), (42, 'VIET_NAM'), (40, 'VIRGIN_ISL_BRIT'), (41, 'VIRGIN_ISL_US'), (217, 'WALLIS_FUT_ISLS'), (69, 'WESTERN_SAHARA'), (259, 'Western Europe'), (81, 'YEMEN'), (68, 'ZAMBIA'), (70, 'ZIMBABWE'), (181, '\u0421\u0435\u043d-\u041c\u0430\u0440\u0442\u0435\u043d'), (255, '\u0421\u0435\u043d-\u041c\u0430\u0440\u0442\u0435\u043d (\u0424\u0440\u0430\u043d\u0446\u0438\u044f)'), (180, '\u0421\u0435\u043d-\u0411\u0430\u0440\u0442\u0435\u043b\u044c\u043c\u0438'), (190, '\u0421\u0438\u043d\u0442-\u041c\u0430\u0440\u0442\u0435\u043d'), (183, '\u0421\u0435\u043d\u0442-\u0412\u0438\u043d\u0441\u0435\u043d\u0442 \u0438 \u0413\u0440\u0435\u043d\u0430\u0434\u0438\u043d\u044b'), (248, '\u042e\u0436\u043d\u044b\u0439 \u0421\u0443\u0434\u0430\u043d'), (247, '\u042e\u0436\u043d\u0430\u044f \u041e\u0441\u0435\u0442\u0438\u044f'), (53, '\u0413\u0435\u0440\u043d\u0441\u0438'), (63, '\u0414\u0436\u0435\u0440\u0441\u0438'), (149, '\u041e\u0441\u0442\u0440\u043e\u0432 \u041c\u044d\u043d'), (1, '\u0410\u0431\u0445\u0430\u0437\u0438\u044f'), (103, '\u041a\u044e\u0440\u0430\u0441\u0430\u043e'), (160, '\u041f\u0430\u043f\u0441\u043a\u0438\u0439 \u041f\u0440\u0435\u0441\u0442\u043e\u043b (\u0413\u043e\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u043e &mdash; \u0433\u043e\u0440\u043e\u0434 \u0412\u0430\u0442\u0438\u043a\u0430\u043d)'), (28, '\u0411\u043e\u043d\u0430\u0439\u0440\u0435, \u0421\u0430\u0431\u0430 \u0438 \u0421\u0438\u043d\u0442-\u042d\u0441\u0442\u0430\u0442\u0438\u0443\u0441'), (113, '\u041c\u0430\u0432\u0440\u0438\u043a\u0438\u0439'), (252, '\u0410\u043b\u0430\u043d\u0434\u0441\u043a\u0438\u0435 \u043e\u0441\u0442\u0440\u043e\u0432\u0430'), (240, '\u042d\u043b\u0430\u043d\u0434\u0441\u043a\u0438\u0435 \u043e\u0441\u0442\u0440\u043e\u0432\u0430'), (108, '\u041b\u0438\u0432\u0438\u0439\u0441\u043a\u0430\u044f \u0410\u0440\u0430\u0431\u0441\u043a\u0430\u044f \u0414\u0436\u0430\u043c\u0430\u0445\u0438\u0440\u0438\u044f'), (11, '\u0410\u043d\u0442\u0430\u0440\u043a\u0442\u0438\u0434\u0430'), (231, '\u0427\u0435\u0440\u043d\u043e\u0433\u043e\u0440\u0438\u044f')]),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_index',
            field=models.CharField(max_length=6, null=True, verbose_name='postal index (ZIP)', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_person_birthday',
            field=models.DateField(null=True, verbose_name='birthday', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_person_fname',
            field=models.CharField(max_length=50, null=True, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_person_gender',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='gender', choices=[(1, 'Male'), (2, 'Female')]),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_person_lname',
            field=models.CharField(max_length=50, null=True, verbose_name='last name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_person_mname',
            field=models.CharField(max_length=50, null=True, verbose_name='middle name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_person_pin',
            field=models.CharField(max_length=9, null=True, verbose_name='PIN', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_phone',
            field=models.CharField(max_length=12, null=True, verbose_name='phone', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='term_insurance',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='term insurance', choices=[(1, '1 \u0433\u043e\u0434'), (2, '1 \u043c\u0435\u0441\u044f\u0446')]),
        ),
    ]
