INSERT INTO sale_cartype (id, name, tag_value) VALUES (1, 'Легковые автомобили', 1);
INSERT INTO sale_cartype (id, name, tag_value) VALUES (2, 'Мотоцикл', 2);
INSERT INTO sale_cartype (id, name, tag_value) VALUES (3, 'Автобус и микроавтобусы', 3);
INSERT INTO sale_cartype (id, name, tag_value) VALUES (4, 'Грузовые автомобили', 4);
INSERT INTO sale_cartype (id, name, tag_value) VALUES (5, 'Прицепы и полуприцепы', 5);
INSERT INTO sale_cartype (id, name, tag_value) VALUES (6, 'Тракторы', 6);
INSERT INTO sale_cartype (id, name, tag_value) VALUES (7, 'Трамваи и троллейбусы', 7);


 /* car[type] */
                 1: {/* car[more] */2: {/* person */1: {/* docs */ 1: 15.5, 2: 16}, 2: {/* docs */ 1: 30, 2: 32.5}},
                    3: {
                        1: {1: 18.5, 2: 19.88},
                        2: {1: 20, 2: 22.99},
                    },
                    8: {
                        1: {1: 15.5},
                        2: {2: 21.99}
                    },
                    9: {
                        1: {1: 18.5, 2: 16}
                    }
                },
                2: {
                    /* person */
                    1: {/* docs */ 1: 18.5, 2: 19.88},
                    2: {/* docs */ 1: 20, 2: 22.99}
                },
                4: {
                    1: {1: {1: 18.5, 2: 19.88}, 2: {1: 20, 2: 22.99}},
                    3: {1: {1: 18.5, 2: 16}}
                },
                5: {1: {1: 18.5, 2: 16}},



<script type="text/javascript">
			window.saleInsurancePremiumVals = {
				/* car[make] */
				1: {
					/* car[model] */
					1: {
					    title: "Focus",
                        /* car[type] */
                        type: {
                            1: "Легковые автомобили"
                        }, more: {
                                1: "#carEngine"
                            }
					},
					2: {title: "Mondeo", /* car[type] */ type: {1: "Легковые автомобили", 5: "Прицепы и полуприцепы"}, more: {1: "#carEngine"}}
				},
				2: {
					1: {title: "Sportage", type: {1: "Легковые автомобили"}, more: {1: "#carEngine"}},
					2: {title: "Sorento", type: {1: "Легковые автомобили"}, more: {1: "#carEngine"}},
					3: {title: "Rio", type: {1: "Легковые автомобили"}, more: {1: "#carEngine"}}
				},
				3: {
					1: {title: "CL203", type: {1: "Легковые автомобили"}, more: {1: "#carEngine"}},
					2: {title: "Transporter", type: {3: "Автобус и микроавтобусы"}, more: {3: "#carSize"}}
				},
				4: {
					1: {title: "8C Spider", type: {1: "Легковые автомобили"}, more: {1: "#carEngine"}},
					2: {title: "Giulietta", type: {4: "Грузовые автомобили"}, more: {4: "#carWeight"}}
				}
			};
		</script>