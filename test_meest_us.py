from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

class TestUnityApp(object):

    @classmethod
    def setup_class(cls):
        cls.browser = webdriver.Chrome(executable_path='/./chromedriver')
        cls.browser.get('https://my.meest.us/en')
        cls.browser.implicitly_wait(10)

    def setup_method(self, method):
        self.browser.refresh()
        self.browser.execute_script("window.scrollTo(0, 0)")


    def test_calculation_battomn_click(self):
        self.__return_visible_element__(By.LINK_TEXT, 'Calculate delivery cost').click()
        sleep(2)
        calculation_battomn = self.__return_visible_element__(By.CSS_SELECTOR,
                                        '* div.hidden-xs > button.submit-calculation-form')
        calculation_battomn.click()
        country_error = self.\
            __return_visible_element__(By.CSS_SELECTOR,
                                       '* div.field-calculatedeliveryform-country > p.help-block-error').text
        assert country_error == 'This field can’t be blank'
        shipping_method_error = self. \
            __return_visible_element__(By.CSS_SELECTOR,
                                       '* div.field-calculatedeliveryform-shipping_method > p.help-block-error').text
        assert shipping_method_error == 'This field can’t be blank'
        weight_error = self. \
            __return_visible_element__(By.CSS_SELECTOR,
                                       '* div.field-calculatedeliveryform-weight > p.help-block-error').text
        assert weight_error == 'This field can’t be blank'
        cost_of_delivery = self. \
            __return_visible_element__(By.CSS_SELECTOR, '* .cost-of-delivery').text
        assert cost_of_delivery == '$ 0.00'
        summary_calculation = self. \
            __return_visible_element__(By.CSS_SELECTOR, '* .summary-calculation').text
        assert summary_calculation == '$ 0.00'
        assert calculation_battomn.is_enabled

    def test_appearance_of_shipping_type_dropdown(self):
        self.__return_visible_element__(By.LINK_TEXT, 'Calculate delivery cost').click()
        sleep(2)
        country_type_dropdown = self.__return_visible_element__(By.CSS_SELECTOR,
                                                                'select#calculatedeliveryform-country.form-control')
        Select(country_type_dropdown).select_by_visible_text('Ukraine')
        shipping_method_dropdown = self.__return_visible_element__(By.CSS_SELECTOR,
                                                                'select#calculatedeliveryform-shipping_method.form-control')
        Select(shipping_method_dropdown).select_by_visible_text('Air')
        shipping_type_dropdown = self.__return_visible_element__(By.CSS_SELECTOR,
                                                        'div > #calculatedeliveryform-shipping_type')
        assert shipping_type_dropdown.is_displayed()
        select_shipping_type = self.__return_visible_element__(By.CSS_SELECTOR,
                                                        '#calculatedeliveryform-shipping_type > option[value="-1"]')
        assert select_shipping_type.is_selected()

        amount_of_shipping_types = self.browser.find_elements_by_css_selector(
            '#calculatedeliveryform-shipping_type > option')
        assert len(amount_of_shipping_types) == 3
        assert 'Select shipping type' == amount_of_shipping_types[0].text
        assert 'Home delivery' == amount_of_shipping_types[1].text
        assert 'Branch' == amount_of_shipping_types[2].text
        shipping_type_error = self.browser.\
            find_element_by_css_selector('.field-calculatedeliveryform-shipping_type > .help-block-error').text
        assert shipping_type_error == ''

    def test_check_calculation(self):
        self.__return_visible_element__(By.LINK_TEXT, 'Calculate delivery cost').click()
        sleep(2)
        country_type_dropdown = self.__return_visible_element__(By.CSS_SELECTOR,
                                                                'select#calculatedeliveryform-country.form-control')
        Select(country_type_dropdown).select_by_visible_text('Ukraine')
        shipping_method_dropdown = self.__return_visible_element__(By.CSS_SELECTOR,
                                                                   'select#calculatedeliveryform-shipping_method.form-control')
        Select(shipping_method_dropdown).select_by_visible_text('Sea')
        shipping_type_dropdown = self.__return_visible_element__(By.CSS_SELECTOR,
                                                                 'div > #calculatedeliveryform-shipping_type')
        Select(shipping_type_dropdown).select_by_visible_text('Home delivery')
        weight_input_form = self.browser. \
            find_element_by_css_selector('#calculatedeliveryform-weight.form-control')
        weight_input_form.send_keys('22')
        calculation_battomn = self.__return_visible_element__(By.CSS_SELECTOR,
                                                              '* div.hidden-xs > button.submit-calculation-form')
        calculation_battomn.click()
        sleep(1)
        country_error = self.browser. \
            find_element_by_css_selector('.field-calculatedeliveryform-country > .help-block-error').text
        assert country_error == ''
        shipping_method_error = self.browser. \
            find_element_by_css_selector('.field-calculatedeliveryform-shipping_method > .help-block-error').text
        assert shipping_method_error == ''
        shipping_type_error = self.browser. \
            find_element_by_css_selector('.field-calculatedeliveryform-shipping_type > .help-block-error').text
        assert shipping_type_error == ''
        cost_of_delivery = self. \
            __return_visible_element__(By.CSS_SELECTOR, '* .cost-of-delivery').text
        assert cost_of_delivery == '$ 76.16'
        summary_calculation = self. \
            __return_visible_element__(By.CSS_SELECTOR, '* .summary-calculation').text
        assert summary_calculation == '$ 76.16'

    @classmethod
    def teardown_class(cls):
        sleep(1)
        cls.browser.close()

    def __return_visible_element__(self, locator_type, locator):
        return WebDriverWait(self.browser, 5) \
            .until(EC.visibility_of_element_located((locator_type, locator)))
