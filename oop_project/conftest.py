def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'modinfo: tests dedicated for modify_info method from ScrapBrickEconomy class.'
    )

    config.addinivalue_line(
        'markers',
        'modprice: tests dedicated for modify_price method from ScrapBrickEconomy class.'
    )

    