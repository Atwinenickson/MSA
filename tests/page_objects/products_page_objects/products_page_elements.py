class ProductElements:
    home_page_header_xpath = "//span[normalize-space()='Home']"
    best_sellers_header_xpath = "//a[@class='blockbestsellers']"
    all_products_xpath = "//ul[contains(@class, 'product_list')]//li"
    product_name_xpath = "//a[@class='product-name']"
    product_price_xpath = "//div[@class='right-block']//span[@class='price product-price']"

    all_names_xpath = "//ul[contains(@class, 'product_list')]//li//a[@class='product-name']"
    all_prices_xpath = "//ul[contains(@class, 'product_list')]//li//div[@class='right-block']//span[@class='price product-price']"

    women_section_xpath = "//a[@title='Women']"
    dresses_section_xpath = "//div[@class='block']//li[@class='last']//a[normalize-space()='Dresses']"
    evening_dresses_section_xpath = "//div[@class='block_content']//a[normalize-space()='Evening Dresses']"

    medium_xpath = "//input[@id='layered_id_attribute_group_2']"
    pink_xpath = "//input[@id='layered_id_attribute_group_24']"
    range_xpath = "//label[@for='price']"
    slider_xpath = "//div[@class='layered_slider ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all']//a"

    more_xpath = "//span[normalize-space()='More']"
    dress_xpath = "//img[@title='Printed Dress']"
    quantity_label_xpath = "//label[normalize-space()='Quantity']"   
    quantity_xpath = "//input[@id='quantity_wanted']"
    size_select_xpath = "//select[@id='group_1']"
    select_pink_xpath = "//a[@id='color_7']"

    size_selected_xpath = "//span[@id='layer_cart_product_attributes']"
    product_quantity_xpath = "//span[@id='layer_cart_product_quantity']"
    product_price_xpath = "//span[@id='layer_cart_product_price']"
    total_title_xpath = "//span[@class='ajax_cart_product_txt_s ']"

    total_product_cost_xpath = "//span[@class='ajax_block_products_total']"
    total_shipping_cost_xpath = "//span[@class='ajax_cart_shipping_cost']"
    total_cost_xpath = "//span[@class='ajax_block_cart_total']"