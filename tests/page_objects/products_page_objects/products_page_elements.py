class ProductElements:
    home_page_header_xpath = "//span[normalize-space()='Home']"
    best_sellers_header_xpath = "//a[@class='blockbestsellers']"
    all_products_xpath = "//ul[contains(@class, 'product_list')]//li"
    product_name_xpath = "//a[@class='product-name']"
    product_price_xpath = "//div[@class='right-block']//span[@class='price product-price']"

    all_names_xpath = "//ul[contains(@class, 'product_list')]//li//a[@class='product-name']"
    all_prices_xpath = "//ul[contains(@class, 'product_list')]//li//div[@class='right-block']//span[@class='price product-price']"