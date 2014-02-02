'''
Runs selenium based unit/system tests.
'''
import time
import datetime
import getpass
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

class SeleniumTests(unittest.TestCase):
    '''
    Runs the selenium tests.
    '''
    @classmethod
    def setUpClass(cls):
        if 'jenkins' in getpass.getuser():
            vis = 0
        else:
            vis = 1
        print(getpass.getuser())
        cls.display = Display(visible=vis, size=(1024, 768))
        cls.display.start()
        cls.driver = webdriver.Firefox()
        cls.driver.set_window_size(1000, 700)
        cls.driver.implicitly_wait(30)
        cls.base_url = 'http://localhost:9000'
        cls.add_users()

    def setUp(self):
        self.verificationErrors = []

    def is_text_present(self, text):
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while curr_time < (start_time + datetime.timedelta(seconds=30)):
            if str(text) in self.driver.page_source:
                return True
            self.driver.refresh()
            time.sleep(1)
            curr_time = datetime.datetime.now()
        return False

    def verifyTextPresent(self, text):
        try:
            self.assertTrue(self.is_text_present(text))
        except AssertionError as e:
            self.verificationErrors.append(str(e) + ' did not find %s' % text)
            print(self.driver.page_source)

    def retry_select_xpath(self, xpath, text):
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while curr_time < (start_time + datetime.timedelta(seconds=30)):
            try:
                Select(self.driver.find_element_by_xpath(xpath)).select_by_visible_text(text)
                return True
            except NoSuchElementException:
                print('current url %s' % self.driver.current_url)
                print('failed to find %s. curr_time %s start_time %s' % (
                    xpath, curr_time, start_time))
                time.sleep(1)
                curr_time = datetime.datetime.now()
        print(self.driver.page_source)
        return False

    def retry_click_link(self, link_text):
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while curr_time < (start_time + datetime.timedelta(seconds=30)):
            try:
                self.driver.find_element_by_link_text(link_text).click()
                return True
            except NoSuchElementException:
                print('current url %s' % self.driver.current_url)
                print('failed to find %s. curr_time %s start_time %s' % (
                    link_text, curr_time, start_time))
                time.sleep(1)
                curr_time = datetime.datetime.now()

        print(self.driver.page_source)
        return False

    def retry_select_id(self, select_id, text):
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while curr_time < (start_time + datetime.timedelta(seconds=30)):
            try:
                Select(self.driver.find_element_by_id(select_id)).select_by_visible_text(text)
                return True
            except NoSuchElementException:
                print('current url %s' % self.driver.current_url)
                print('failed to find %s. curr_time %s start_time %s' % (
                    select_id, curr_time, start_time))
                time.sleep(1)
                curr_time = datetime.datetime.now()

        print(self.driver.page_source)
        return False

    def retry_click_id(self, item_id):
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while curr_time < (start_time + datetime.timedelta(seconds=30)):
            try:
                self.driver.find_element_by_id(item_id).click()
                return True
            except NoSuchElementException:
                print('current url %s' % self.driver.current_url)
                print('failed to find %s. curr_time %s start_time %s' % (
                    item_id, curr_time, start_time))
                time.sleep(1)
                curr_time = datetime.datetime.now()

        print(self.driver.page_source)
        return False

    @classmethod
    def add_users(cls):
        driver = cls.driver
        driver.get(cls.base_url + "/_ah/login?continue=http%3A//localhost%3A9000/administrator")
        cls.users_added = True
        driver.find_element_by_id("admin").click()
        driver.find_element_by_id("submit-login").click()
        driver.find_element_by_id("id_user_email_address").clear()
        driver.find_element_by_id("id_user_email_address").send_keys("test@example.com")
        driver.find_element_by_css_selector("input[type=submit]").click()
        driver.find_element_by_id("id_user_email_address").clear()
        driver.find_element_by_id("id_user_email_address").send_keys("test2@example.com")
        driver.find_element_by_css_selector("input[type=submit]").click()

    def add_login_steps_user1(self):
        driver = self.driver
        driver.get(self.base_url + "/_ah/login?continue=http%3A//localhost%3A9000/")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("test@example.com")
        driver.find_element_by_css_selector("input[type=submit]").click()

    def add_login_steps_user2(self):
        driver = self.driver
        driver.get(self.base_url + "/_ah/login?continue=http%3A//localhost%3A9000/")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("test2@example.com")
        driver.find_element_by_css_selector("input[type=submit]").click()


    def test_add_client(self):
        self.add_login_steps_user1()
        driver = self.driver
        driver.find_element_by_link_text("Add New Client").click()
        driver.find_element_by_id("id_lastname").clear()
        driver.find_element_by_id("id_lastname").send_keys("test_last_name")
        driver.find_element_by_id("id_firstname").clear()
        driver.find_element_by_id("id_firstname").send_keys("test_first_name")
        driver.find_element_by_id("id_cellnumber").clear()
        driver.find_element_by_id("id_cellnumber").send_keys("test_cell")
        driver.find_element_by_id("id_homenumber").clear()
        driver.find_element_by_id("id_homenumber").send_keys("test_home")
        driver.find_element_by_id("id_worknumber").clear()
        driver.find_element_by_id("id_worknumber").send_keys("test_work")
        driver.find_element_by_id("id_emailaddress").clear()
        driver.find_element_by_id("id_emailaddress").send_keys("test_email")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("test_addr")
        driver.find_element_by_id("id_address2").clear()
        driver.find_element_by_id("id_address2").send_keys("test_addr2")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("test_city")
        driver.find_element_by_id("id_zipcode").clear()
        driver.find_element_by_id("id_zipcode").send_keys("test_zip")
        Select(driver.find_element_by_id(
            "id_dob_month")).select_by_visible_text("January")
        Select(driver.find_element_by_id(
            "id_dob_day")).select_by_visible_text("1")
        Select(driver.find_element_by_id(
            "id_dob_year")).select_by_visible_text("1915")
        driver.find_element_by_id("id_guardians_name").clear()
        driver.find_element_by_id("id_guardians_name").send_keys(
            "test_guardian")
        driver.find_element_by_id("id_guardians_phone_number").clear()
        driver.find_element_by_id("id_guardians_phone_number").send_keys(
            "test_guardian_phone")
        driver.find_element_by_id("id_emergency_contact").clear()
        driver.find_element_by_id("id_emergency_contact").send_keys(
            "test_emerg_cont")
        driver.find_element_by_id("id_emergency_contact_phone_number").clear()
        driver.find_element_by_id(
            "id_emergency_contact_phone_number").send_keys(
            "test_emerg_cont_phone")
        driver.find_element_by_id("id_referrer").click()
        driver.find_element_by_id('referrer_choice_other').clear()
        driver.find_element_by_id("referrer_choice_other").send_keys(
            "test_refer")
        driver.find_element_by_id('OK_referrer_dlg').click()
        driver.find_element_by_id("id_dsm_code").clear()
        driver.find_element_by_id("id_dsm_code").send_keys("test_dsm")
        driver.find_element_by_id('id_reason_for_visit').click()
        driver.find_element_by_id('reason_for_visit_choice_other').clear()
        driver.find_element_by_id('reason_for_visit_choice_other').send_keys(
            'test_other_rfv')
        driver.find_element_by_id('OK_reason_for_visit_dlg').click()
        self.assertEqual(driver.find_element_by_id('id_reason_for_visit').get_attribute('value'),
                         'test_other_rfv')
        driver.find_element_by_css_selector("input[type=submit]").click()

    def test_update_client(self):
        self.add_login_steps_user1()
        driver = self.driver
        driver.find_element_by_link_text("Clients").click()
        driver.find_element_by_link_text("test_last_name, test_first_name").click()
        driver.find_element_by_link_text('Edit Client Info').click()
        driver.find_element_by_id("id_cellnumber").clear()
        driver.find_element_by_id("id_cellnumber").send_keys("test_cell_update")
        driver.find_element_by_id("id_homenumber").clear()
        driver.find_element_by_id("id_homenumber").send_keys("test_home_update")
        driver.find_element_by_id("id_worknumber").clear()
        driver.find_element_by_id("id_worknumber").send_keys("test_work_update")
        driver.find_element_by_id("id_emailaddress").clear()
        driver.find_element_by_id("id_emailaddress").send_keys("test_email_update")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("test_addr_update")
        driver.find_element_by_id("id_address2").clear()
        driver.find_element_by_id("id_address2").send_keys("test_addr2_update")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("test_city_update")
        driver.find_element_by_id("id_zipcode").clear()
        driver.find_element_by_id("id_zipcode").send_keys("test_zip_update")
        driver.find_element_by_css_selector("input[type=submit]").click()
        self.verifyTextPresent('test_cell_update')


    def test_add_client2(self):
        self.add_login_steps_user2()
        driver = self.driver
        driver.find_element_by_link_text("Add New Client").click()
        driver.find_element_by_id("id_lastname").clear()
        driver.find_element_by_id("id_lastname").send_keys("test_last_name2")
        driver.find_element_by_id("id_firstname").clear()
        driver.find_element_by_id("id_firstname").send_keys("test_first_name2")
        driver.find_element_by_id("id_cellnumber").clear()
        driver.find_element_by_id("id_cellnumber").send_keys("test_cell")
        driver.find_element_by_id("id_homenumber").clear()
        driver.find_element_by_id("id_homenumber").send_keys("test_home")
        driver.find_element_by_id("id_worknumber").clear()
        driver.find_element_by_id("id_worknumber").send_keys("test_work")
        driver.find_element_by_id("id_emailaddress").clear()
        driver.find_element_by_id("id_emailaddress").send_keys("test_email")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("test_addr")
        driver.find_element_by_id("id_address2").clear()
        driver.find_element_by_id("id_address2").send_keys("test_addr2")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("test_city")
        driver.find_element_by_id("id_zipcode").clear()
        driver.find_element_by_id("id_zipcode").send_keys("test_zip")
        Select(driver.find_element_by_id("id_dob_month")).select_by_visible_text("January")
        Select(driver.find_element_by_id("id_dob_day")).select_by_visible_text("1")
        Select(driver.find_element_by_id("id_dob_year")).select_by_visible_text("1915")
        driver.find_element_by_id("id_guardians_name").clear()
        driver.find_element_by_id("id_guardians_name").send_keys("test_guardian")
        driver.find_element_by_id("id_guardians_phone_number").clear()
        driver.find_element_by_id("id_guardians_phone_number").send_keys("test_guardian_phone")
        driver.find_element_by_id("id_emergency_contact").clear()
        driver.find_element_by_id("id_emergency_contact").send_keys("test_emerg_cont")
        driver.find_element_by_id("id_emergency_contact_phone_number").clear()
        driver.find_element_by_id("id_emergency_contact_phone_number").send_keys("test_emerg_cont_phone")
        driver.find_element_by_id("id_referrer").click()
        driver.find_element_by_id('referrer_choice_other').clear()
        driver.find_element_by_id("referrer_choice_other").send_keys(
            "test_refer")
        driver.find_element_by_id('OK_referrer_dlg').click()
        driver.find_element_by_id("id_dsm_code").clear()
        driver.find_element_by_id("id_dsm_code").send_keys("test_dsm")
        driver.find_element_by_css_selector("input[type=submit]").click()


    def add_dos(self, client_name):
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/02/06/00/calendar/")
        self.assertTrue(self.retry_select_xpath("//select[@id='id_clientinfo']", client_name))
        driver.find_element_by_css_selector("input[type=submit]").click()
        time.sleep(10)

    def add_rep_1_day(self, client_name):
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/02/07/00/calendar/")
        self.assertTrue(self.retry_select_xpath("//select[@id='id_clientinfo']", client_name))
        self.assertTrue(self.retry_select_id("id_dos_repeat", "One Day"))
        driver.find_element_by_id("id_dos_repeat_end_date").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-e").click()
        driver.find_element_by_link_text("28").click()
        driver.find_element_by_css_selector("input[type=submit]").click()
        time.sleep(10)

    def add_rep_1_week(self, client_name):
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/02/08/00/calendar/")
        self.assertTrue(self.retry_select_xpath("//select[@id='id_clientinfo']", client_name))
        self.assertTrue(self.retry_select_id("id_dos_repeat", "One Week"))
        driver.find_element_by_id("id_dos_repeat_end_date").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-e").click()
        driver.find_element_by_link_text("28").click()
        driver.find_element_by_css_selector("input[type=submit]").click()
        time.sleep(10)

    def add_rep_2_weeks(self, client_name):
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/02/09/00/calendar/")
        self.assertTrue(self.retry_select_xpath("//select[@id='id_clientinfo']", client_name))
        self.assertTrue(self.retry_select_id("id_dos_repeat", "Two Weeks"))
        driver.find_element_by_id("id_dos_repeat_end_date").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-e").click()
        driver.find_element_by_link_text("28").click()
        driver.find_element_by_css_selector("input[type=submit]").click()
        time.sleep(10)

    def add_rep_3_weeks(self, client_name):
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/02/10/00/calendar/")
        self.assertTrue(self.retry_select_xpath("//select[@id='id_clientinfo']", client_name))
        self.assertTrue(self.retry_select_id("id_dos_repeat", "Three Weeks"))
        driver.find_element_by_id("id_dos_repeat_end_date").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-e").click()
        driver.find_element_by_link_text("28").click()
        driver.find_element_by_css_selector("input[type=submit]").click()
        time.sleep(10)

    def add_rep_4_weeks(self, client_name):
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/02/11/00/calendar/")
        self.assertTrue(self.retry_select_xpath("//select[@id='id_clientinfo']", client_name))
        self.assertTrue(self.retry_select_id("id_dos_repeat", "Four Weeks"))
        driver.find_element_by_id("id_dos_repeat_end_date").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-e").click()
        driver.find_element_by_link_text("28").click()
        driver.find_element_by_css_selector("input[type=submit]").click()


    def test_add_dos(self):
        self.add_login_steps_user1()
        self.add_dos("test_last_name, test_first_name")
        self.add_rep_1_day("test_last_name, test_first_name")
        self.add_rep_1_week("test_last_name, test_first_name")
        self.add_rep_2_weeks("test_last_name, test_first_name")
        self.add_rep_3_weeks("test_last_name, test_first_name")
        self.add_rep_4_weeks("test_last_name, test_first_name")

    def test_zz_00_update_balance(self):
        self.add_login_steps_user1()
        driver = self.driver
        driver.find_element_by_link_text("test_last_name, test_first_name").click()
        driver.find_element_by_link_text("Update DOS").click()
        driver.find_element_by_id("id_amt_due").clear()
        driver.find_element_by_id("id_amt_due").send_keys("100")
        driver.find_element_by_css_selector("input[type=submit]").click()
        self.verifyTextPresent('Balance: 100.0')
        driver.find_element_by_link_text("Update DOS").click()
        driver.find_element_by_id("id_amt_paid").clear()
        driver.find_element_by_id("id_amt_paid").send_keys("95")
        driver.find_element_by_css_selector("input[type=submit]").click()
        self.verifyTextPresent('Balance: 5.0')


    def test_sel_search(self):
        self.add_login_steps_user1()
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2/show_specific_client/")
        driver.find_element_by_id("id_search_input").clear()
        driver.find_element_by_id("id_search_input").send_keys("last_name first_name")
        elem = driver.find_element_by_id("id_search_input")
        elem.send_keys("selenium\n")
        self.verifyTextPresent('test_last_name')

    def test_sel_generate_invoices(self):
        self.add_login_steps_user1()
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/26/calendar/")
        driver.find_element_by_class_name('fc-button-month').click()

    def test_zz_01_ask_permission(self):
        self.add_login_steps_user1()
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/show_client/")
        driver.find_element_by_link_text("Settings").click()
        driver.find_element_by_link_text("Permission Settings").click()
        driver.find_element_by_id("id_permitted_user_email").clear()
        driver.find_element_by_id("id_permitted_user_email").send_keys("test2@example.com")
        driver.find_element_by_css_selector("input[type=submit]").click()

    def test_zz_02_grant_permission(self):
        self.add_login_steps_user2()
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/show_client/")
        driver.find_element_by_link_text("Settings").click()
        driver.find_element_by_link_text("Permission Settings").click()
        self.retry_click_link('Change')
        self.retry_select_id('id_user_approved', 'Approved')
        self.retry_click_id('id_submit_update_request')
        time.sleep(5)
        #driver.find_element_by_id('id_submit_update_request').click()


    def act_as_user2(self):
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/show_client/")
        self.verifyTextPresent('test2@example.com')
        Select(driver.find_element_by_id("permitted_user")).select_by_visible_text("test2@example.com")

    def test_zz_04_add_dos_client2(self):
        self.add_login_steps_user1()
        self.act_as_user2()
        self.add_dos("test_last_name2, test_first_name2")
        self.add_rep_1_day("test_last_name2, test_first_name2")
        self.add_rep_1_week("test_last_name2, test_first_name2")
        self.add_rep_2_weeks("test_last_name2, test_first_name2")
        self.add_rep_3_weeks("test_last_name2, test_first_name2")
        self.add_rep_4_weeks("test_last_name2, test_first_name2")

    def test_zz_05_update_balance(self):
        self.add_login_steps_user1()
        self.act_as_user2()
        driver = self.driver
        driver.find_element_by_link_text("test_last_name2, test_first_name2").click()
        driver.find_element_by_link_text("Update DOS").click()
        driver.find_element_by_id("id_amt_due").clear()
        driver.find_element_by_id("id_amt_due").send_keys("100")
        driver.find_element_by_css_selector("input[type=submit]").click()
        self.verifyTextPresent('Balance: 100.0')
        driver.find_element_by_link_text("Update DOS").click()
        driver.find_element_by_id("id_amt_paid").clear()
        driver.find_element_by_id("id_amt_paid").send_keys("95")
        driver.find_element_by_css_selector("input[type=submit]").click()
        self.verifyTextPresent('Balance: 5.0')

    def test_zz_06_run_reports(self):
        self.add_login_steps_user1()
        self.act_as_user2()
        driver = self.driver
        driver.find_element_by_link_text("Reports").click()
        driver.find_element_by_link_text("Provider Invoices").click()
        Select(driver.find_element_by_id("id_start_invoice_date_month")).select_by_visible_text("January")
        Select(driver.find_element_by_id("id_start_invoice_date_day")).select_by_visible_text("1")
        Select(driver.find_element_by_id("id_start_invoice_date_year")).select_by_visible_text("2009")
        Select(driver.find_element_by_id("id_end_invoice_date_month")).select_by_visible_text("January")
        Select(driver.find_element_by_id("id_end_invoice_date_day")).select_by_visible_text("1")
        Select(driver.find_element_by_id("id_end_invoice_date_year")).select_by_visible_text("2020")
        driver.find_element_by_css_selector("input[type=submit]").click()
        time.sleep(5)
        driver.refresh()
        self.verifyTextPresent('test_last_name2, test_first_name2')
        self.verifyTextPresent('100')
        self.verifyTextPresent('95')
        self.verifyTextPresent('Other Total: 95.0')
        self.verifyTextPresent('Total: 95.0')
        self.verifyTextPresent('Cash Total: 0')
        self.verifyTextPresent('Check Total: 0')
        self.verifyTextPresent('100')
        driver.find_element_by_link_text("Reports").click()
        driver.find_element_by_link_text("Provider Statistics").click()
        driver.find_element_by_link_text("2011").click()
        self.verifyTextPresent('95.0')

#    def test_zz_07_mark_dos_attended_client2(self):
#        self.add_login_steps_user1()
#        self.act_as_user2()
#        driver = self.driver
#        driver.get(self.base_url + "/Mindwell/2011/05/23/calendar/")
#        driver.find_element_by_link_text("test_last_name2, test_first_name2").click()
#        Select(driver.find_element_by_id("id_session_result")).select_by_visible_text("Attended")
#        driver.find_element_by_css_selector("input[type=submit]").click()

#    def test_zz_08_generate_reports_client2(self):
#        self.add_login_steps_user1()
#        self.act_as_user2()
#        driver = self.driver
#        driver.get(self.base_url + "/Mindwell/2011/05/23/calendar/")
#        Select(driver.find_element_by_id("generate_report")).select_by_visible_text("Current Week")
#        driver.find_element_by_link_text("[View in MindWell]").click()
#        # the report in mindwell doesn't have a login button so go back
#        # to a page that does
#        driver.get(self.base_url + "/Mindwell/2011/05/23/calendar/")

    def test_zz_09_add_client2a(self):
        self.add_login_steps_user2()
        driver = self.driver
        driver.find_element_by_link_text("Add New Client").click()
        driver.find_element_by_id("id_lastname").clear()
        driver.find_element_by_id("id_lastname").send_keys("test_last_name2a")
        driver.find_element_by_id("id_firstname").clear()
        driver.find_element_by_id("id_firstname").send_keys("test_first_name2a")
        driver.find_element_by_id("id_cellnumber").clear()
        driver.find_element_by_id("id_cellnumber").send_keys("test_cell")
        driver.find_element_by_id("id_homenumber").clear()
        driver.find_element_by_id("id_homenumber").send_keys("test_home")
        driver.find_element_by_id("id_worknumber").clear()
        driver.find_element_by_id("id_worknumber").send_keys("test_work")
        driver.find_element_by_id("id_emailaddress").clear()
        driver.find_element_by_id("id_emailaddress").send_keys("test_email")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("test_addr")
        driver.find_element_by_id("id_address2").clear()
        driver.find_element_by_id("id_address2").send_keys("test_addr2")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("test_city")
        driver.find_element_by_id("id_zipcode").clear()
        driver.find_element_by_id("id_zipcode").send_keys("test_zip")
        Select(driver.find_element_by_id("id_dob_month")).select_by_visible_text("January")
        Select(driver.find_element_by_id("id_dob_day")).select_by_visible_text("1")
        Select(driver.find_element_by_id("id_dob_year")).select_by_visible_text("1915")
        driver.find_element_by_id("id_guardians_name").clear()
        driver.find_element_by_id("id_guardians_name").send_keys("test_guardian")
        driver.find_element_by_id("id_guardians_phone_number").clear()
        driver.find_element_by_id("id_guardians_phone_number").send_keys("test_guardian_phone")
        driver.find_element_by_id("id_emergency_contact").clear()
        driver.find_element_by_id("id_emergency_contact").send_keys("test_emerg_cont")
        driver.find_element_by_id("id_emergency_contact_phone_number").clear()
        driver.find_element_by_id("id_emergency_contact_phone_number").send_keys("test_emerg_cont_phone")
        driver.find_element_by_id("id_referrer").clear()
        driver.find_element_by_id("id_referrer").send_keys("test_refer")
        driver.find_element_by_id("id_dsm_code").clear()
        driver.find_element_by_id("id_dsm_code").send_keys("test_dsm")
        driver.find_element_by_css_selector("input[type=submit]").click()

    def test_zz_10_add_dos_client2a(self):
        self.add_login_steps_user2()
        self.add_dos("test_last_name2a, test_first_name2a")
        self.add_rep_1_day("test_last_name2a, test_first_name2a")

    def test_zz_11_provider_stats_all_time(self):
        self.add_login_steps_user2()
        driver = self.driver
        driver.get(self.base_url + "/Mindwell/2011/05/02/calendar/")
        driver.find_element_by_link_text("Reports").click()
        driver.find_element_by_link_text("Provider Statistics").click()
        driver.find_element_by_link_text("View All Time Stats").click()

#    def test_zz_12_running_balance(self):
#        self.add_login_steps_user2()
#        driver = self.driver
#        driver.get(self.base_url + "/Mindwell/provider_stats_all_time/")
#        driver.find_element_by_link_text("Show Clients").click()
#        driver.find_element_by_link_text("test_last_name2, test_first_name2").click()
##        driver.find_element_by_xpath("//div[@id='content']/table/tbody/tr[4]/td/a").click()
#        driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[4]/td/a").click()
#
#        driver.find_element_by_id("id_amt_due").clear()
#        driver.find_element_by_id("id_amt_due").send_keys("150")
#        driver.find_element_by_css_selector("input[type=submit]").click()
##        driver.find_element_by_xpath("//div[@id='content']/table/tbody/tr[3]/td/a").click()
#        driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[3]/td/a").click()
#        driver.find_element_by_id("id_amt_due").clear()
#        driver.find_element_by_id("id_amt_due").send_keys("33")
#        driver.find_element_by_css_selector("input[type=submit]").click()
#        self.verifyTextPresent('150.0')
#        self.verifyTextPresent('183.0')
#        self.verifyTextPresent('188.0')


#    def test_zz_13_provider_stats_all_time(self):
#        self.add_login_steps_user2()
#        driver = self.driver
#        driver.get(self.base_url + "/Mindwell/2011/05/02/calendar/")
#        driver.find_element_by_link_text("Reports").click()
#        driver.find_element_by_link_text("Customer Invoices").click()
#        self.verifyTextPresent("test_last_name2, test_first_name2")

    def tearDown(self):
        if self.verificationErrors:
            print(self.driver.page_source)
            self.driver.find_element_by_link_text("Logout").click()
            self.driver.quit()
            self.display.stop()
        else:
            self.driver.find_element_by_link_text("Logout").click()
#        self.driver.quit()
#        self.display.stop()
        self.assertEqual([], self.verificationErrors)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.display.stop()
