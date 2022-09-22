from functools import cache
from turtle import onrelease
from akivymd.uix.datepicker import AKDatePicker
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.animation import Animation
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.utils import asynckivy
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineListItem, TwoLineListItem
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.uix.popup import Popup
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRaisedButton


# python imports
import asyncio
from contextlib import asynccontextmanager
import os
import time
import mysql
from mysql.connector import connect
from mysql.connector import errors
from smtplib import SMTP
import random
import hashlib
import urllib
from urllib.request import urlopen
from threading import Thread
from connection import DBConnection
import cloudinary
import cloudinary.uploader
import cloudinary.api

Window.size = (300, 580)

LabelBase.register(
    name="Poppins", fn_regular="assets/Poppins/Poppins-Regular.ttf")
LabelBase.register(
    name="Poppins-SemiBold", fn_regular="assets/Poppins/Poppins-SemiBold.ttf")
LabelBase.register(
    name="Poppins-Bold", fn_regular="assets/Poppins/Poppins-Bold.ttf")


class Connection:
    def internet_connected():
        try:
            urlopen('https://www.google.com', timeout=15)
            return True
        except urllib.error.URLError:
            return False


class MyPopup(MDFloatLayout):
    pass


class SojrelApp(MDApp):
    def build(self):
        # self.theme_cls.material_style = "M3"
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('splash.kv'))
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('internet_error_login.kv'))
        screen_manager.add_widget(
            Builder.load_file('internet_error_signup.kv'))
        screen_manager.add_widget(Builder.load_file('login.kv'))
        screen_manager.add_widget(Builder.load_file('signup.kv'))
        screen_manager.add_widget(Builder.load_file('sendotp.kv'))
        screen_manager.add_widget(Builder.load_file('resetpassword.kv'))
        screen_manager.add_widget(Builder.load_file('homepage.kv'))
        screen_manager.add_widget(Builder.load_file('userprofile.kv'))
        screen_manager.add_widget(Builder.load_file('contact.kv'))
        screen_manager.add_widget(Builder.load_file('chat.kv'))
        screen_manager.add_widget(Builder.load_file('about.kv'))
        screen_manager.add_widget(Builder.load_file('verification.kv'))
        screen_manager.add_widget(Builder.load_file('add_nextofkin.kv'))
        screen_manager.add_widget(
            Builder.load_file('registereduserprofile.kv'))
        screen_manager.add_widget(Builder.load_file('faqs.kv'))
        screen_manager.add_widget(Builder.load_file('nextofkins.kv'))
        screen_manager.add_widget(Builder.load_file('loaneligibility.kv'))
        screen_manager.add_widget(Builder.load_file('loanproducts.kv'))
        screen_manager.add_widget(Builder.load_file('updateprofile.kv'))
        screen_manager.add_widget(Builder.load_file('flash_loan.kv'))
        screen_manager.add_widget(Builder.load_file('flash_loan_status.kv'))
        screen_manager.add_widget(Builder.load_file('loans_in_progress.kv'))
        screen_manager.add_widget(Builder.load_file('view_members.kv'))
        screen_manager.add_widget(Builder.load_file('applied_loans.kv'))
        screen_manager.add_widget(Builder.load_file('loan_application.kv'))
        screen_manager.add_widget(Builder.load_file('add_guarantors.kv'))
        screen_manager.add_widget(Builder.load_file('guarantee_loan.kv'))
        screen_manager.add_widget(Builder.load_file('guarantee_amount.kv'))
        return screen_manager
    # data = {
    #     'Python': 'language-python',
    #     'PHP': 'language-php',
    #     'C++': 'language-cpp',
    # }
    db = DBConnection.db_cnx
    cursor = DBConnection.get_connection(DBConnection, db)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.binary_kra_file = None
        self.binary_photo = None
        self.agreed_terms = False
        self.binary_back_image = None
        self.binary_front_image = None
        self.gender = None
        self.reset_email = None
        self.data_tables = None
        self.login_pwd_hash = None
        self.manager_open = None
        self.back_home = None
        self.date_dialog = None
        self.has_been_called = False
        self.regdatepicker = AKDatePicker(callback=self.regcallback,
                                          year_range=([2020, 2030]))
        self.dobdatepicker = AKDatePicker(callback=self.dobcallback,
                                          year_range=([1979, 2030]))
        self.fromdatepicker = AKDatePicker(callback=self.fromcallback,
                                           year_range=([2020, 2030]))
        self.todatepicker = AKDatePicker(callback=self.tocallback,
                                         year_range=([2020, 2030]))
        self.show_loan_datepicker = AKDatePicker(
            callback=self.loan_date_callback, year_range=([2021, 2030]))

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_photo_path,
            # preview=True
        )
        self.kra_file_mng = MDFileManager(
            exit_manager=self.exit_kra_manager,
            select_path=self.select_kra_path,
        )

    # def complete_kin_detail(self):

    def client_login(self, email, password):
        # cursor = DBConnection.get_connection(DBConnection, self.db)
        global user_login_email
        user_login_email = email.text
        # print(user_login_email)
        # if self.cursor:
        pass1 = password.text.encode()

        pwd = hashlib.sha256(pass1)
        login_pwd_hash = pwd.hexdigest()

        try:
            sql = "SELECT email, password0 FROM user where email = %(email)s and password0 = %(password)s"
            login_data = {
                'email': email.text.lower(),
                'password': login_pwd_hash
            }
            self.cursor.execute(sql, login_data)
            data = self.cursor.fetchone()
            email_list = []
            for k in self.cursor.fetchall():
                email_list.append(k[0])

            sql1 = "SELECT active FROM user WHERE email = %(email)s"

            user_email = {
                'email': email.text.lower()
            }
            self.cursor.execute(sql1, user_email)
            active_list = []
            for k in self.cursor.fetchall():
                active_list.append(k[0])

            if data is not None:
                if active_list[0] == 1:
                    email.text = ''
                    password.text = ''
                    # print(active_list[0])
                    self.load_screen('registered_members')
                    self.load_profile_image()
                    self.get_membership_no()
                    # self.root.get_screen(
                    #     'registered_members').ids.user_mail.text = user_login_email
                    toast('Login successful')

                    # self.add_member()

                else:
                    self.root.get_screen(
                        'my_profile-screen').ids.mail.text = user_login_email
                    email.text = ''
                    password.text = ''
                    toast('Login successful')
                    self.load_screen('homepage')

            else:
                self.open_dialog(
                    'Incorrect login credentials. Check and try again')
                email.text = ''
                password.text = ''

            #     email_list2 = []
            #     for k in cursor.fetchall():
            #         email_list2.append(k[0])
            #         # print(email_list2)

            #     cursor.execute(sql, (email.text, login_pwd_hash))
            #     data = cursor.fetchone()
            #     # for row in data:
            #     # print(row)
            #     if data is not None and email.text in email_list2:
            #         # print('data is found')

            #         MDApp.get_running_app().root.current = 'registered_members'
            #         self.root.get_screen(
            #             'my_profile-screen').ids.mail.text = email.text
            #         self.root.get_screen(
            #             'registered_members').ids.user_mail.text = email.text
            #         self.load_profile_image(email.text)
            #         self.add_member()
            #         email.text = ''
            #         password.text = ''
            #         Clock.schedule_interval(self.logout, 600)
            #     elif data is not None and email.text not in email_list2:
            #         MDApp.get_running_app().root.current = 'homepage'
            #         self.root.get_screen(
            #             'my_profile-screen').ids.mail.text = email.text
            #         self.root.get_screen(
            #             'registered_members').ids.user_mail.text = email.text

            #         email.text = ''
            #         password.text = ''
            #         Clock.schedule_interval(self.logout, 600)
            #     else:
            #         self.open_dialog(
            #             "Invalid credentials. \nCheck and try again")
            #         email.text = ''
            #         password.text = ''
        except UnboundLocalError as err:
            self.load_screen('internet_error_login')
            print(err)

    def get_membership_no(self):
        try:
            sql = "SELECT membership_no FROM member WHERE email=%(mail)s"
            data = {
                'mail': user_login_email
            }
            self.cursor.execute(sql, data)
            member_data = self.cursor.fetchall()
            for row in member_data:
                for col in row:
                    # print(col)
                    self.root.get_screen(
                        'apply_loan').ids.mem_no.text = str(col)
                    self.root.get_screen(
                        'registered_members').ids.member_no.text = str(col)
                    self.root.get_screen(
                        'flash_loan').ids.members_no.text = str(col)
                    self.root.get_screen(
                        'nextofkins').ids.membership_no.text = str(col)
        except errors.Error as e:
            toast('Unable to get membership number')
            print(e)

    def apply_loan(self, membership_no, category, principal, instalments):
        if principal.text == "":
            toast('Amount cannot be empty')
        elif instalments.text == "":
            toast('Repayment period cannot be empty')
        else:
            try:
                sql = "INSERT INTO loan(membership_no, category, principal, interest, instalments, loan_status) VALUES (%(member_no)s,%(category)s,%(principal)s,%(interest)s,%(instalments)s,%(loan_status)s)"
                loan_data = {
                    'member_no': membership_no.text,
                    'category': category.text,
                    'principal': principal.text,
                    'interest': 2,
                    'instalments': instalments.text,
                    'loan_status': 'Applied'
                }
                self.cursor.execute(sql, loan_data)
                self.db.commit()
                toast('Loan application successful')
                self.load_screen('guarantors')
            except errors.Error as e:
                toast('Loan application not successful')
                self.db.rollback()
                print(e)

    def fetch_loan_id(self):
        try:
            sql = "SELECT loan_id from loan WHERE membership_no = (SELECT membership_no FROM member WHERE email = %(mail)s) AND loan_status = %(status)s"
            data = {
                'mail': user_login_email,
                'status': 'Applied'
            }
            self.cursor.execute(sql, data)
            id_data = self.cursor.fetchall()
            if id_data is not None:
                for row in id_data:
                    for col in row:
                        self.root.get_screen(
                            'guarantors').ids.loanid.text = str(col)
            else:
                self.root.get_screen(
                    'guarantors').ids.loanid.text = ''
        except errors.Error as e:
            toast('Loan id not found')
            print(e)

    def load_loan_page(self, loan_category):
        try:
            sql = "SELECT total_shares from loan_qualifiers WHERE email = %(mail)s"
            data = {
                'mail': user_login_email
            }
            self.cursor.execute(sql, data)
            qualifier = self.cursor.fetchall()
            print(f'qualified > {qualifier}')
            if qualifier == []:
                self.open_dialog(
                    'Sorry, we regret to inform you that you do not qualify for a loan at this moment. Please try gain later.')
            else:
                for row in qualifier:
                    print(row[0])
                    for col in row:
                        if int(col) < 10000:
                            print(f'amount {col}')
                            self.open_dialog(
                                'Sorry, we regret to inform you that you do not qualify for a loan at this moment. Please try gain later.')
                        else:
                            self.root.get_screen(
                                'apply_loan').ids.loan_cat.text = loan_category.text
                            self.load_screen('apply_loan')
        except errors.Error as e:
            print(e)
            # toast()

    def load_guarantor_requests(self, loan_id, guarantor_no):
        if guarantor_no.text == '':
            toast('You must enter the membership no of your guarantor')
        else:
            guarator_list = []
            while True:
                guarantor = ()

                guarantor = guarantor + \
                    (int(loan_id.text), int(guarantor_no.text))
                print(guarantor)

                guarator_list.append(guarantor)
                print(guarator_list)

                for i in guarator_list:
                    print(i)
                    'insert into guarantors values(i)'
                    item = TwoLineListItem(
                        text=f'Loan ID: {str(i[0])}',
                        secondary_text=f'Membership No: {str(i[1])}'
                    )
                    self.root.get_screen(
                        'guarantors').ids.list.add_widget(item)
                # break

                    try:
                        sql = "INSERT INTO guarantor(loan_id, membership_no) VALUES (%(loan_id)s,%(member_no)s)"
                        guarantor_data = {
                            'loan_id': int(i[0]),
                            'member_no': int(i[1])
                        }
                        self.cursor.execute(sql, guarantor_data)
                        self.db.commit()
                        toast('Guarantor added successfully')
                        guarantor_no.text == ''
                    except errors.Error as e:
                        guarantor_no.text == ''
                        print(e)
                        self.db.rollback()
                        toast('Guarantor with this id does not exist')
                        self.root.get_screen(
                            'guarantors').ids.list.remove_widget(item)
                break

    def load_toguarantee_loans(self):
        self.loanid_list = []
        self.guarantorlist = []
        sql = 'SELECT loan_id, membership_no  FROM guarantor WHERE membership_no = ((SELECT membership_no FROM member WHERE email = %(email)s) AND amount IS NULL)'

        data = {
            'email': user_login_email,
        }
        self.cursor.execute(sql, data)
        loans = self.cursor.fetchall()
        if loans == []:
            toast('There are not loans for this account')
        else:
            for row in loans:
                parentbox = MDCard(
                    orientation='vertical',
                    size_hint_y=None,
                    height='50dp',
                    spacing=10,
                    padding=10,
                    md_bg_color=(9/255, 178/255, 159/255, 1),
                    radius='5dp',
                    on_release=self.load_guarantee_page
                )
                loanbox = MDBoxLayout(
                    spacing=5,
                    padding=10,

                )
                parentbox.add_widget(loanbox)
                loan_label = MDLabel(
                    text='Membership No.',
                    theme_text_color='Custom',
                    text_color=(1, 1, 1, 1),
                    font_style='Subtitle2',
                    halign='left'
                )
                actual_loan_label = MDLabel(
                    text=str(row[0]),
                    theme_text_color='Custom',
                    text_color=(1, 1, 1, 1),
                    font_style='Caption',
                    halign='right'
                )
                loanbox.add_widget(loan_label)
                loanbox.add_widget(actual_loan_label)
                memberbox = MDBoxLayout(
                    spacing=5,
                    padding=10
                )
                parentbox.add_widget(memberbox)
                memberno_label = MDLabel(
                    text='Loan ID',
                    theme_text_color='Custom',
                    text_color=(1, 1, 1, 1),
                    font_style='Subtitle2',
                    halign='left'
                )
                actual_memberno_label = MDLabel(
                    text=str(row[1]),
                    theme_text_color='Custom',
                    text_color=(1, 1, 1, 1),
                    font_style='Caption',
                    halign='right'
                )
                memberbox.add_widget(memberno_label)
                memberbox.add_widget(actual_memberno_label)

                # self.guarantee_item = TwoLineListItem(
                #     text=str(row[0]),
                #     secondary_text=str(row[1]),
                #     on_release=self.load_guarantee_page
                # )
                self.root.get_screen(
                    'guarantee_loan').ids.loan_guarantee_list.add_widget(parentbox)

                self.loanid_list.append(actual_loan_label.text)
                print(self.loanid_list)
                self.guarantorlist.append(actual_memberno_label.text)
                print(self.guarantorlist)

    def load_guarantee_page(self, *args):
        self.root.get_screen(
            'guarantee_amount').ids.lid.text = self.loanid_list[0]
        self.root.get_screen(
            'guarantee_amount').ids.member_no.text = self.guarantorlist[0]
        self.load_screen('guarantee_amount')

    def load_applied_loans(self):
        self.loan_id_list = []
        try:
            sql = 'SELECT loan_id, category, principal, loan_status FROM loan_details WHERE membership_no = ((SELECT membership_no FROM member WHERE email = %(email)s) AND loan_status != %(status1)s OR loan_status != %(status2)s)'
            data = {
                'email': user_login_email,
                'status1': 'Completed',
                'status2': 'Repaying'
            }
            self.cursor.execute(sql, data)
            loans = self.cursor.fetchall()
            # print(loans)
            if loans == []:
                self.open_dialog(
                    'There are not applied loans for this account')
            else:
                for row in loans:
                    # print(row)
                    parentbox = MDCard(
                        orientation='vertical',
                        size_hint_y=None,
                        height='100dp',
                        spacing=10,
                        padding=10,
                        md_bg_color=(9/255, 178/255, 159/255, 1),
                        radius='5dp',
                    )
                    loanbox = MDBoxLayout(
                        spacing=5,
                        padding=10,

                    )
                    parentbox.add_widget(loanbox)
                    loan_label = MDLabel(
                        text='Loan ID',
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='left'
                    )
                    actual_loan_label = MDLabel(
                        text=str(row[0]),
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='right'
                    )
                    loanbox.add_widget(loan_label)
                    loanbox.add_widget(actual_loan_label)
                    categorybox = MDBoxLayout(
                        spacing=5,
                        padding=10
                    )
                    parentbox.add_widget(categorybox)
                    category_label = MDLabel(
                        text='Loan Type',
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='left'
                    )
                    actual_category_label = MDLabel(
                        text=str(row[1]),
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='right'
                    )
                    categorybox.add_widget(category_label)
                    categorybox.add_widget(actual_category_label)
                    amountbox = MDBoxLayout(
                        spacing=5,
                        padding=10
                    )
                    parentbox.add_widget(amountbox)
                    amount_label = MDLabel(
                        text='Loan Amount',
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='left'
                    )
                    actual_amount_label = MDLabel(
                        text=f'Ksh. {str(row[2])}',
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='right'
                    )
                    amountbox.add_widget(amount_label)
                    amountbox.add_widget(actual_amount_label)

                    statusbox = MDBoxLayout(
                        spacing=5,
                        padding=10
                    )
                    parentbox.add_widget(statusbox)
                    status_label = MDLabel(
                        text='Loan Status',
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='left'
                    )
                    actual_status_label = MDLabel(
                        text=str(row[3]),
                        theme_text_color='Custom',
                        text_color=(1, 1, 1, 1),
                        font_style='Subtitle2',
                        halign='right'
                    )
                    statusbox.add_widget(status_label)
                    statusbox.add_widget(actual_status_label)

                    self.root.get_screen(
                        'applied_loans').ids.applied_loan_list.add_widget(parentbox)

                    self.loan_id_list.append(actual_loan_label.text)
        except errors.Error as e:
            print(e)
            toast('Error in loading loans applied')

    def postloader(self, *args):
        screen_manager.current = 'applied_loans'

    # def sync_page_load(self):
    #     self.()
    #     screen_manager.current = 'anim_loading'
    #     Clock.schedule_once(self.postloader, 10)

    def guarantee(self, loanid, guarantorno, id_no, amount):
        sql = "UPDATE guarantor SET guarantor_idno=%(idno)s, amount=%(amount)s WHERE loan_id =%(loanid)s AND membership_no=%(member_no)s"
        data = {
            'loanid': loanid.text,
            'member_no': guarantorno.text,
            'idno': id_no.text,
            'amount': amount.text,
        }
        if id_no.text == "":
            toast('Please enter your ID No.')
        elif amount.text == "":
            toast('Please enter amount to guarantee')
        else:
            try:
                self.cursor.execute(sql, data)
                self.db.commit()
                toast('Loan guaranteed successfully')
                self.load_screen('guarantee_loan')
            except errors.Error as e:
                toast('Failed to guarantee')
                self.db.rollback()
                print(e)

    def reject_guarantee(self, loanid, guarantorno):
        sql = 'UPDATE guarantor SET amount = %(amount)s WHERE loan_id=%(loanid)s AND membership_no = %(member_no)s'
        data = {
            'loanid': loanid.text,
            'member_no': guarantorno.text,
            'amount': 0000
        }
        try:
            self.cursor.execute(sql, data)
            self.db.commit()
            toast('Guarantee rejected successfully')
            self.load_screen('guarantee_loan')
        except errors.Error as e:
            toast('Failed to reject')
            self.db.rollback()
            print(e)

    def load_loan_details(self, loanid, member_no):
        sql = "SELECT first_name, mid_name, category, principal, instalments FROM loan_details WHERE loan_id=%(loanid)s AND membership_no=%(mem_no)s"

        data = {
            'loanid': loanid.text,
            'mem_no': member_no.text
        }
        try:
            self.cursor.execute(sql, data)
            loan_detail = self.cursor.fetchall()
            for row in loan_detail:
                self.root.get_screen(
                    'guarantee_amount').ids.name.text = f"{str(row[0])} {str(row[1])}"
                self.root.get_screen(
                    'guarantee_amount').ids.category.text = str(row[2])
                self.root.get_screen(
                    'guarantee_amount').ids.amount.text = str(row[3])
                self.root.get_screen(
                    'guarantee_amount').ids.instalment.text = str(row[4])
        except errors.Error as e:
            print(e)
            self.db.rollback()
            toast('Could not load loan details')

    # def guarantee_loan(self, id_no, amount):
    #     try:
    #         sql = 'UPDATE guarantor SET guarantor_idno=%(idno)s AND amount = %(amount)s WHERE loan_id=%(id)s AND membership_no =%(member_no)s'
    #         data = {
    #             'idno': id_no,
    #             'amount': amount,
    #             'id': self.guarantee_item.text,
    #             'member_no': self.guarantee_item.secondary_text
    #         }
    #         self.cursor.execute(sql, data)
    #         self.db.commit()
    #         toast('Loan guaranteed successfully')
    #     except errors.Error as e:
    #         self.db.rollback()
    #         toast('Gurantee details not submitted')
    #         print(e)

        # def show_popup(self, kin_id):
    #     show = MyPopup()
    #     popupWindow = Popup(title="Add Next of Kin",
    #                         content=show, size_hint=(.8, .6))
    #     show.md_bg_color = (1, 1, 1, 1)
    #     idlb = Label(
    #         text=f'ID No.: {kin_id.text}',
    #         pos_hint={'center_x': .5, 'center_y': .85},
    #         halign='center',
    #         color=(9/255, 178/255, 159/255, 1)
    #     )
        # print(idlb.text)  # printing
        # member_txt = MDTextField(
        #     hint_text='Membership No.',
        #     pos_hint={'center_x': .5, 'center_y': .65},
        #     size_hint_x=.8
        # )
        # print(member_txt.text)  # not printing
        # perc_txt = MDTextField(
        #     hint_text='Percentage(optional)',
        #     pos_hint={'center_x': .5, 'center_y': .45},
        #     size_hint_x=.8
        # )
        # print(f'% is... {perc_txt.text}')
        # add_btn = MDRaisedButton(
        #     text='Add',
        #     pos_hint={'center_x': .5, 'center_y': .25},
        #     size_hint_x=.4,
        #     md_bg_color=(9/255, 178/255, 159/255, 1),
        #     on_release=self.add_next_of_kin(idlb, member_txt, perc_txt)
        # )
        # show.add_widget(idlb)
        # show.add_widget(member_txt)
        # show.add_widget(perc_txt)
        # show.add_widget(add_btn)
        # popupWindow.open()

    def add_next_of_kin_details(self, membership_no, id_no, fname, mname, lname, percentage):
        if membership_no.text == "":
            toast('Please enter your membership no.')
        elif id_no.text == "":
            toast('Please fill the ID No.')
        elif fname.text == "":
            toast('First Name cannot be empty')
        elif lname.text == "":
            toast('Last Name cannot be empty')
        else:
            try:
                sql1 = "INSERT INTO next_of_kin(id_no, first_name, mid_name,last_name) VALUES(%(id_no)s,%(fname)s,%(mname)s,%(lname)s)"
                kin_data = {
                    'id_no': id_no.text,
                    'fname': fname.text,
                    'mname': mname.text,
                    'lname': lname.text
                }
                self.cursor.execute(sql1, kin_data)

                sql = "INSERT INTO member_kin(kin_id, membership_no, percentage) VALUES(%(kin_id_no)s,%(membership_no)s,%(percentage)s)"
                data = {
                    'kin_id_no': id_no.text,
                    'membership_no': membership_no.text,
                    'percentage': percentage.text
                }
                self.cursor.execute(sql, data)
                self.db.commit()
                toast('Next of kin added successfully')
                membership_no.text = ""
                id_no.text = ""
                fname.text = ""
                mname.text = ""
                lname.text = ""
                percentage.text = ""
            except errors.Error as e:
                self.db.rollback()
                self.open_dialog(
                    'Sorry next of kin could not be added\nCheck your details and try again')
                print(e)

    def load_contributions_history(self):
        sql = "SELECT contribution_date, contribution, amount FROM members_contributions WHERE email=%(email)s ORDER BY contribution_date DESC"
        data = {
            'email': user_login_email
        }
        try:
            self.cursor.execute(sql, data)
            contr_data = self.cursor.fetchall()
        except errors.Error as e:
            toast('Failed to load contribution details')
        for row in contr_data:
            contribution_item = ThreeLineListItem(
                text=f'Date: {row[0]}',
                theme_text_color='Custom',
                text_color=(9/255, 178/255, 159/255, 1),
                secondary_text=f'Type: {row[1]}',
                tertiary_text=f'Amount: Ksh.{row[2]}',
                tertiary_theme_text_color='Custom',
                tertiary_text_color=(0, 0, 0, 1),
            )
            self.root.get_screen('registered_members').ids.contribution_view.add_widget(
                contribution_item)

        sql1 = "SELECT SUM(amount) FROM members_contributions WHERE contribution=%(share)s AND email=%(email)s"
        share_data = {
            'share': 'Shares',
            'email': user_login_email
        }
        self.cursor.execute(sql1, share_data)
        shares = self.cursor.fetchall()
        for row in shares:
            self.root.get_screen(
                'registered_members').ids.tshares.text = f'Total Shares:  Ksh.{str(row[0])}'

        sql2 = "SELECT SUM(amount) FROM members_contributions WHERE contribution=%(saving)s AND email=%(email)s"
        saving_data = {
            'saving': 'Savings',
            'email': user_login_email
        }
        self.cursor.execute(sql2, saving_data)
        savings = self.cursor.fetchall()
        for row in savings:
            self.root.get_screen(
                'registered_members').ids.tsavings.text = f'Total Savings:  Ksh.{str(row[0])}'

        sql3 = "SELECT SUM(amount) FROM members_contributions WHERE email=%(email)s"
        contr_data = {
            'email': user_login_email
        }
        self.cursor.execute(sql3, contr_data)
        contributions = self.cursor.fetchall()
        for row in contributions:
            self.root.get_screen(
                'registered_members').ids.tcontributions.text = f'Total Contributions:  Ksh.{str(row[0])}'

    def add_member(self):
        try:
            sql = "SELECT membership_no, photo, first_name, mid_name,residence FROM active_members_information ORDER BY membership_no"
            self.cursor.execute(sql)
            member_data = self.cursor.fetchall()
            for row in member_data:
                parentbox = MDBoxLayout(
                    size_hint_y=None,
                    height='60dp',
                    spacing=10,
                    padding=10,
                    md_bg_color=(9/255, 178/255, 159/255, 1),
                    radius='5dp',

                )
                imagebox = MDBoxLayout(
                    size_hint_x=None,
                    width='50dp',
                )
                img = FitImage(
                    radius='50dp',
                    source=str(row[1])
                )
                imagebox.add_widget(img)
                detailbox = MDBoxLayout(
                    orientation='vertical',
                    spacing=5,
                    padding=10
                )
                name_label = MDLabel(
                    text=str(f'{row[0]}: {row[2]} {row[3]}'),
                    theme_text_color='Custom',
                    text_color=(1, 1, 1, 1),
                    font_style='Subtitle2'
                )
                residence_label = MDLabel(
                    text=str(row[4]),
                    theme_text_color='Custom',
                    text_color=(1, 1, 1, 1),
                    font_style='Caption'
                )
                detailbox.add_widget(name_label)
                detailbox.add_widget(residence_label)

                parentbox.add_widget(imagebox)
                parentbox.add_widget(detailbox)

                self.root.get_screen(
                    'view_members').ids.members_list.add_widget(parentbox)

                # self.root.get_screen(
                #     'view_members').ids.image.source = str(row[1])
                # self.root.get_screen(
                #     'view_members').ids.name.text = str(f'{row[0]}: {row[2]} {row[3]}')
                # self.root.get_screen(
                #     'view_members').ids.residence.text = str(row[4])

                # image = ImageLeftWidget(source=str(row[1]), radius='20dp')
                # self.member_item = ThreeLineAvatarListItem(
                #     text=f'Member No.: {row[0]}',
                #     secondary_text=f'{row[2]} {row[3]}',
                #     secondary_theme_text_color='Custom',
                #     secondary_text_color=(9/255, 178/255, 159/255, 1),
                #     tertiary_text=f'Residence: {row[4]}',
                #     bg_color=(9/255, 178/255, 159/255, .05),
                #     divider_color=(9/255, 178/255, 159/255, 1)
                # )
                # self.member_item.add_widget(image)
                # self.root.get_screen(
                #     'view_members').ids.members_list.add_widget(self.member_item)

        except TypeError as e:
            print(e)
            toast('Members data not found')

    def loans_table(self):
        loan_item = ThreeLineListItem(
            text='Loan Type: Emergency',
            secondary_text='Loan Amount: 10,000',
            tertiary_text='Oustanding balance: 2,500'
        )
        self.root.get_screen(
            'loans_in_progress').ids.loans.add_widget(loan_item)

    # page pre-loader
    def animate_circle(self, widget):
        anim = Animation(size_hint=(0, 0), opacity=0, pos_hint={
                         'center_x': .5, 'center_y': 1}, duration=.5)
        anim += Animation(size_hint=(2, .6), opacity=1, pos_hint={
            'center_x': .5, 'center_y': .925}, duration=.5)
        anim.start(widget)

    angle = 45

    def load_animation(self, *args):
        anim = Animation(height=80, width=80, spacing=[10, 10], duration=0.3)
        anim += Animation(height=60, width=60, spacing=[5, 5], duration=0.5)
        anim += Animation(angle=self.angle, duration=0.3)
        anim.bind(on_complete=self.load_animation)
        # anim.start(widget)
        anim.start(screen_manager.get_screen('anim_loading').ids.loading)
        self.angle += 45

    dialog = None

    # functions for displaying date-picker

    def show_date_picker(self):
        self.regdatepicker.open()

    def regcallback(self, date):
        self.root.get_screen(
            'my_profile-screen').ids.date.text = '' if not date else f'{date.year}-{date.month}-{date.day}'

    def show_dob(self):
        self.dobdatepicker.open()

    def dobcallback(self, date):
        self.root.get_screen(
            'my_profile-screen').ids.birth_date.text = '' if not date else f'{date.year}-{date.month}-{date.day}'

    def show_from_date(self):
        self.fromdatepicker.open()

    def fromcallback(self, date):
        self.root.get_screen(
            'contribution_history').ids.txt_from_date.text = '' if not date else f'{date.year}-{date.month}-{date.day}'

    def show_to_date(self):
        self.todatepicker.open()

    def tocallback(self, date):
        self.root.get_screen(
            'contribution_history').ids.txt_to_date.text = '' if not date else f'{date.year}-{date.month}-{date.day}'

    def show_loan_date(self):
        self.show_loan_datepicker.open()

    def loan_date_callback(self, date):
        self.root.get_screen(
            'apply_loan').ids.loan_date.text = '' if not date else f'{date.year}-{date.month}-{date.day}'

    def next(self):
        self.root.get_screen(
            'my_profile-screen').ids.slide.load_next(mode="next")

    def prev(self):
        self.root.get_screen('my_profile-screen').ids.slide.load_previous()

    # capturing image with Camera
    def capture(self, camera_obj):
        camera_obj.play = True

    # upload image to folder
    def upload(self, camera_obj):
        # saving captured image
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera_obj.export_to_png(
            'assets/images/id_{}.png'.format(timestr))
        photo_path = os.path.abspath('assets/images/id_{}.png'.format(timestr))
        print(photo_path)
        camera_obj.play = False
        return photo_path
        # return

    # convert captured images into binary data
    def get_front_id(self):
        image = self.root.get_screen('my_profile-screen').ids.id_front
        id_front_path = self.upload(image)
        print(id_front_path)
        file_size = os.path.getsize(id_front_path)/1000000
        print(file_size)
        if file_size < 10:
            return id_front_path
        else:
            toast('File size exceeds 10MB')

        # with open(filename, 'rb') as file:
        #     binary_front_image = file.read()

    def get_back_id(self):
        image = self.root.get_screen('my_profile-screen').ids.id_back
        id_back_path = self.upload(image)
        print(id_back_path)
        file_size = os.path.getsize(id_back_path)/1000000
        print(file_size)
        if file_size < 10:
            return id_back_path
        else:
            toast('File size exceeds 10MB')
        # with open(filename, 'rb') as file:
        #     binary_back_image = file.read()
        #
    # Selecting image from filemanager

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_photo_path(self, path):
        self.image_path = path
        print(self.image_path)
        file_size = os.path.getsize(path)/1000000
        print(file_size)
        if file_size < 10:
            self.root.get_screen(
                'my_profile-screen').ids.profile_image.source = self.image_path
        else:
            toast('File size exceed 10MB')
        self.exit_manager()

        # self.root.get_screen(
        #     'registered_members').ids.profile_image.source = path
        # with open(path, 'br') as file:
        #     self.binary_image = file.read()
        # self.profile_url = f'https://realgreatapps.online/assets/images/{os.path.basename(path)}'
        # self.profile_url = f'{os.getcwd()}/uploads/profile_images/{os.path.basename(path)}'
        # print(self.profile_url)
        # print(self.profile_url1)
        # print(os.path.basename(path))
        # with open(self.profile_url, 'wb') as f:
        #     f.write(self.binary_image)

        # return self.binary_image

        # print(self.profile_url)
        # return self.profile_url
    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def kra_file_manager_open(self):
        self.kra_file_mng.show('/')
        self.manager_open = True

    def select_kra_path(self, path):
        self.kra_file_path = path
        print(self.kra_file_path)
        file_size = os.path.getsize(path)/1000000
        print(file_size)
        if file_size < 10:
            self.root.get_screen(
                'my_profile-screen').ids.file_selected.text = os.path.basename(path)
        else:
            toast('File size exceed 10MB')
        self.exit_kra_manager()
        # with open(path, 'br') as file:
        #     self.binary_kra_file = file.read()
        #
        # print(path)
        # return self.binary_kra_file

        # self.kra_url = f'{os.getcwd()}/uploads/kra/{os.path.basename(path)}'
        # with open(self.kra_url, 'bw') as f:
        #     f.write(binary_kra_file)
        #     print(self.kra_url)
        # return self.kra_url

    def exit_kra_manager(self, *args):
        self.manager_open = False
        self.kra_file_mng.close()

    def spinner_clicked(self, value):
        self.root.get_screen('my_profile-screen').ids.category.text = value

    def check_email(self, email):
        self.cursor.execute('SELECT email from user')
        print('cursor executed')
        email_list = []
        emails = self.cursor.fetchall()
        print(f'printing.. {emails}')
        if emails is []:
            for i in emails:
                email_list.append(i[0])
                print('email appended')
                print(email_list)
                if email_list == [] or email.text not in email_list:
                    print('emails empty')

    def insert_client(self, first_name, middle_name, last_name, email, password, password1):

        if first_name.text == "":
            toast("First name cannot be empty")
            print('fname checked')
        elif last_name.text == "":
            toast("Last name cannot be empty")
            print('lname checked')
        elif email.text == "":
            toast("Email cannot be empty")
            print('email checked')
        elif password.text == "":
            toast("Password cannot be empty")
            print('password checked')
        elif password1.text == "":
            toast("Password cannot be empty")
            print('password checked')
        elif password.text != password1.text:
            toast("Passwords do not match")
            print('passwd match checked')
        else:

            # registration details
            insert_client_query = ("INSERT INTO user (first_name, mid_name, last_name, email, password0, password1, "
                                   "active) "
                                   "VALUES(%(firstname)s,%(midname)s, %(lastname)s, %(email)s, %(pass)s, %(pass1)s, "
                                   "%(active)s)")

            pass1 = password.text.encode()
            pass2 = password1.text.encode()

            p1 = hashlib.sha256(pass1)
            p2 = hashlib.sha256(pass2)

            p1hash = p1.hexdigest()
            p2hash = p2.hexdigest()

            client_data = {
                'firstname': first_name.text.title(),
                'midname': middle_name.text.title(),
                'lastname': last_name.text.title(),
                'email': email.text.lower(),
                'pass': p1hash,
                'pass1': p2hash,
                'active': False
            }
            sql_commit = 'SET autocommit = 0'
            print('auto_commit set to false')
            self.cursor.execute(sql_commit)
            try:
                self.cursor.execute(
                    insert_client_query, client_data)
                print('cursor executed')
                self.db.commit()
                print('committed')
                toast('Account created successfully')
                self.load_screen('login-screen')
                self.empty_fields()
            except errors.Error as e:
                toast("Oops! Account not created")
                self.load_screen('signup-screen')
                self.empty_fields()
                print(e)
                self.db.rollback()
                print('rolledback')
            # finally:
            #     self.cursor.close()
            #     self.db.close()
        # else:
        #     toast(
        #         'This email is already registered. \nLogin or try another one')

            # self.send_OTP()
            # if e == UnboundLocalError:
            #     self.open_dialog(
            #         "Please fill the fields before submitting")

            # finally:
            #     cursor.close()
            #     self.db.close()

    """
    generated_otp = random.randint(100000, 999999)

    def send_OTP(self):
        receiver_email = self.root.get_screen('signup-screen').ids.mail.text
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('sojrelsacco@gmail.com', password='wjaokodcmhadubaj')
        msg = f'If you are getting this message, your tried to create account with Sojrel App. \nYour OTP is {self.generated_otp}.'
        print(self.generated_otp)
        server.sendmail('sojrelsacco@gmail.com', receiver_email, msg)
        server.quit()
        MDApp.get_running_app().root.current = 'user_verification'

    def verify_OTP(self, entered_otp):
        # cursor = self.get_dbconnection()
        # email = self.root.get_screen('signup-screen').ids.mail.text
        # entered_otp = self.root.get_screen('user_verification').ids.otp.text
        if str(entered_otp.text) == str(self.generated_otp):
            print(self.generated_otp)
            print(entered_otp.text)
            # self.db.commit()
            self.open_dialog("Account created successfully")
            MDApp.get_running_app().root.current = 'login-screen'
            # self.cursor.close()
            # self.db.close()
        else:
            self.open_dialog("OTPs do not match.\nCheck and enter again")
            # self.send_OTP()
            self.root.get_screen('user_verification').ids.otp.text = ""
            self.root.get_screen('user_verification').ids.otp.focus = True
    """

    def logout(self, *args):
        self.root.get_screen(
            'view_members').ids.members_list.clear_widgets()
        self.load_screen('login-screen')

    def send_reset_otp(self):
        self.cursor = self.get_dbconnection()
        self.reset_email = self.root.get_screen(
            'send_reset_otp').ids.reset_email.text.lower()
        sql = "SELECT email FROM user"
        self.cursor.execute(sql)
        email_list = []
        for i in self.cursor.fetchall():
            email_list.append(i[0])
            if self.reset_email in email_list:
                if self.reset_email != '':
                    server = SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login('sojrelsacco@gmail.com',
                                 password='wjaokodcmhadubaj')
                    msg = f'Your OTP is {self.generated_otp}.'
                    server.sendmail('sojrelsacco@gmail.com',
                                    self.reset_email, msg)
                    server.quit()
                    MDApp.get_running_app().root.current = 'reset_password'
                else:
                    self.open_dialog("Please enter your email")
            else:
                self.open_dialog("The email does not exist")
        # return self.reset_email

    def reset_password(self, sent_reset_otp, passwd1, passwd2):
        # cursor = self.get_dbconnection()
        reset_password_query = ("UPDATE user SET password = %(pass)s, password1=%(pass1)s"
                                "WHERE email = %(email)s")

        pass1 = passwd1.text.encode()
        pass2 = passwd2.text.encode()

        p1 = hashlib.sha256(pass1)
        p2 = hashlib.sha256(pass2)

        p1hash = p1.hexdigest()
        p2hash = p2.hexdigest()

        update_data = {
            "email": self.reset_email,
            "pass": p1hash,
            "pass1": p2hash
        }
        print(self.reset_email)
        print(passwd1.text)
        print(self.generated_otp)
        print(sent_reset_otp.text)
        if str(sent_reset_otp.text) == str(self.generated_otp):
            if passwd1.text == "":
                self.open_dialog("Password cannot be empty")
            elif passwd2.text == "":
                self.open_dialog(" Password cannot be empty")
            elif passwd1.text != passwd2.text:
                self.open_dialog("Passwords do not match")
            else:
                try:
                    self.cursor.execute(reset_password_query, update_data)
                except mysql.connector.errors.IntegrityError:
                    self.open_dialog("Password reset failed")
                self.db.commit()
                self.open_dialog("Password changed successfully")
                MDApp.get_running_app().root.current = 'login-screen'
        else:
            self.open_dialog("Incorrect OTP")
            self.reset_password(sent_reset_otp, passwd1, passwd2)

    def empty_fields(self):
        self.root.get_screen('signup-screen').ids.fname.text = ''
        self.root.get_screen('signup-screen').ids.mname.text = ''
        self.root.get_screen('signup-screen').ids.lname.text = ''
        self.root.get_screen('signup-screen').ids.mail.text = ''
        self.root.get_screen('signup-screen').ids.pwd.text = ''
        self.root.get_screen('signup-screen').ids.pwd1.text = ''

    def binary_to_file(self, binarydata, filename):
        with open(filename, 'wb') as file:
            converted_file = file.write(binarydata)
        return converted_file

    def load_profile_image(self):
        sql = "SELECT photo FROM member WHERE email = %(email)s"
        data = {
            'email': user_login_email
        }
        self.cursor.execute(sql, data)
        row_data = self.cursor.fetchall()
        for row in row_data:
            for col in row:
                self.root.get_screen(
                    'registered_members').ids.profile_image.source = str(col)
                # path = os.getcwd()
                # filepath = '{}/assets/images/profile_image.png'.format(path)
                # for row in row_data:
                #     self.binary_to_file(col, filepath)
                # print(file_path)
                # widget.source = filepath

            # print(str(file_path/{}.format(photo)))

    def load_homepage_details(self):
        sql = "SELECT membership_no, first_name, mid_name, SUM(amount) FROM members_contributions WHERE email = %(mail)s"
        data = {
            'mail': user_login_email
        }
        self.cursor.execute(sql, data)
        user_data = self.cursor.fetchall()
        for row in user_data:
            self.root.get_screen(
                'registered_members').ids.member_no.text = f'Membership No: {str(row[0])}'
            self.root.get_screen(
                'registered_members').ids.username.text = f'Name: {str(row[1])} {str(row[2])}'
            self.root.get_screen(
                'registered_members').ids.totalcontributions.text = f'Contributions: {str(row[3])}'

    def open_dialog(self, text):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Alert!",
                text=text,
                buttons=[MDFlatButton(
                    text="OK", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, args):
        # Close alert box
        self.dialog.dismiss()

    def check_gender(self):
        male = self.root.get_screen('my_profile-screen').ids.male
        female = self.root.get_screen('my_profile-screen').ids.female
        if male.active:
            self.gender = 'Male'

        if female.active:
            self.gender = 'Female'

    def check_terms(self):
        self.agreed_terms = True

    def uploader(self, path):
        cloudinary.config(
            cloud_name="dmhovenqz",
            api_key="373784732193682",
            api_secret="62F0PCb4A19ZrbTiMThUhGh1-7E",
        )

        result = cloudinary.uploader.upload(
            file=path, use_filename=True, unique_filename=False, folder='sacco_files')
        print(result['secure_url'])
        return result['secure_url']
        # else:
        #     toast('File size too large')

    def update_profile(self, reg_date, id_no, dob, kra_pin, phone, email, residence):
        print(f'{reg_date.text} {id_no.text} {dob.text} {kra_pin.text} {phone.text} {email.text.lower()} {residence.text.title()}')
        photo = self.uploader(str(self.image_path))
        print(f'printing photo....')
        gender = self.gender
        print(gender)
        kra_file = self.uploader(str(self.kra_file_path))
        print(f'printing kra_file...')
        id_front = self.uploader(str(self.get_front_id()))
        print(f'printing id_front...')
        id_back = self.uploader(str(self.get_back_id()))
        print(f'printing id_back...')
        agreed_terms = self.agreed_terms
        print(agreed_terms)

        profile_sql = ("INSERT INTO member (photo, reg_date, id_no, dob, gender, kra_pin, kra_file, id_front, id_back, "
                       "phone,email,residence, agreed_terms)"
                       "VALUES (%(photo)s, %(date)s, %(id_no)s, %(dob)s, %(gender)s, %(kra_pin)s, %(kra_file)s,%(id_front)s, "
                       " %(id_back)s, %(phone)s,%(email)s,%(residence)s, %(agreed_terms)s)")
        profile_data = {
            'photo': photo,
            'date': reg_date.text,
            'id_no': id_no.text,
            'dob': dob.text,
            'gender': gender,
            'kra_pin': kra_pin.text.upper(),
            'kra_file': kra_file,
            'id_front': id_front,
            'id_back': id_back,
            'phone': phone.text,
            'email': email.text.lower(),
            'residence': residence.text.title(),
            'agreed_terms': agreed_terms
        }
        # email_sql = "SELECT email FROM user"
        # self.cursor.execute(email_sql)
        # email_list = []
        # for i in self.cursor.fetchall():
        #     email_list.append(i[0])
        #     if email.text not in email_list:
        #         self.load_screen('my_profile-screen')
        #         toast("The email used does not exist")
        #     else:
        try:
            sql_commit = 'SET autocommit = 0'
            print('auto_commit set to false')
            self.cursor.execute(sql_commit)
            id_sql = "SELECT id_no FROM member"
            self.cursor.execute(id_sql)
            id_list = []
            for i in self.cursor.fetchall():
                id_list.append(i[0])
            phone_sql = "SELECT phone FROM member"
            self.cursor.execute(phone_sql)
            phone_list = []
            for i in self.cursor.fetchall():
                phone_list.append(i[0])
            if photo is None:
                toast('You must upload a photo of yourself')
            elif id_no.text in id_list:
                toast('Your ID No is already registered')
            elif phone.text in phone_list:
                toast('Your phone number is already registered')
            elif reg_date.text == '':
                toast("Please select registration date")
            elif id_no.text == '':
                toast("Id No. must not be empty")
            elif dob.text == '':
                toast("Date of birth must not be empty")
            elif gender is None:
                toast("Please select your gender")
            elif id_front is None:
                toast("Please upload front face of your id")
            elif id_back is None:
                toast("Please upload back face of your id")
            elif phone.text == '':
                toast("Please enter your phone no.")
            elif email.text == '':
                toast("Please enter your email")
            elif residence.text == '':
                toast("Please enter your place of residence")
            elif not agreed_terms:
                toast("Please agree to terms before submitting")
            else:
                sql_commit = 'SET autocommit = 0'
                print('auto_commit set to false')
                self.cursor.execute(sql_commit)
                self.cursor.execute(profile_sql, profile_data)
                self.db.commit()
                print('commmitted')
                toast("Registration successful")
                reg_date.text = ""
                id_no.text = ""
                dob.text = ""
                kra_pin.text = ""
                phone.text = ""
                email.text = ""
                residence.text = ""
                self.load_screen('registered_members')
                # self.load_profile_image(email.text)
        except errors.Error as e:
            self.db.rollback()
            print('....rolledback')
            self.load_screen('my_profile-screen')
            toast("Oops! Registration not successful. Try again")
            print(e)

    def load_screen(self, screen_name):
        screen_manager.current = screen_name

    def load_login(self):
        if Connection.internet_connected() == False:
            self.load_screen('internet_error_login')
        else:
            MDApp.get_running_app().root.current = 'login-screen'

    def load_signup(self):
        if Connection.internet_connected() == False:
            self.load_screen('internet_error_signup')
        else:
            MDApp.get_running_app().root.current = 'signup-screen'

    def load_images(self, widget, *args):
        anim = Animation(
            pos_hint={'center_x': .5, 'center_y': .5}, opacity=1, duration=60)
        anim += Animation(pos_hint={'center_x': 1.5,
                          'center_y': .5}, opacity=0, duration=60)
        anim += Animation(pos_hint={'center_x': 2.5,
                          'center_y': .5}, opacity=0, duration=60)
        anim.repeat = True
        anim.start(widget)

    def load_image2(self, widget, *args):
        anim = Animation(pos_hint={'center_x': -.5,
                                   'center_y': .5}, opacity=0, duration=60)
        anim += Animation(pos_hint={'center_x':
                          .5, 'center_y': .5}, opacity=1, duration=60)
        anim += Animation(pos_hint={'center_x':
                          1.5, 'center_y': .5}, opacity=1, duration=60)
        anim.repeat = True
        anim.start(widget)

    def load_image3(self, widget, *args):
        anim = Animation(pos_hint={'center_x': -1.5,
                                   'center_y': .5}, opacity=0, duration=60)
        anim += Animation(pos_hint={'center_x': -.5,
                          'center_y': .5}, opacity=0, duration=60)
        anim += Animation(pos_hint={'center_x': .5,
                          'center_y': .5}, opacity=1, duration=60)
        anim.repeat = True
        anim.start(widget)

    def animateError(self, widget, *args):
        anim = Animation(opacity=0, duration=.75)
        anim += Animation(opacity=1, duration=.75)
        anim.repeat = True
        anim.start(widget)

    def load_main(*args):
        screen_manager.current = 'main-screen'

    def flash_loan_amount(self, principal):
        amount = (int(principal.text)*0.135) + (int(principal.text))
        self.root.get_screen('flash_loan').ids.amount.text = str(
            format(amount, '.1f'))

    def loan_amount_calculator(self, principal, period):
        try:
            amount = ((int(principal.text)*.02)*(pow(1.02, int(period.text))) /
                      ((pow(1.02, int(period.text)))-1))*int(period.text)
            self.root.get_screen(
                'apply_loan').ids.amount.text = str(round(int(amount), -1))
        except ValueError as e:
            toast('Please enter the loan amount')
            print(e)
        except ZeroDivisionError:
            toast('Instalment cannot be 0')

    def flash_loan_application(self, mem_no, principal):
        sql = "INSERT INTO flash_loans (membership_no, principal, interest,status) VALUES (%(mem_no)s,%(principal)s,%(interest)s,%(status)s)"
        data = {
            'mem_no': mem_no.text,
            'principal': principal.text,
            'interest': 13.5,
            'status': 'Reviewing'
        }
        if principal.text == "":
            self.open_dialog('Please enter a minimum amount of Ksh 1000')
        else:
            try:
                self.cursor.execute(sql, data)
                self.db.commit()
                self.open_dialog('Application submitted successfully')
                # self.load_screen('')
            except errors.Error as e:
                self.db.rollback()
                self.open_dialog('Loan application failed')
                print(e)

    def on_start(self):
        DBConnection.create_database(DBConnection)
        self.load_animation()
        Clock.schedule_once(self.load_main, 30)
        self.loans_table()
        # self.load_toguarantee_loans()


if __name__ == '__main__':
    SojrelApp().run()


# class ScreenManager(ScreenManager):
#     manager = SojrelApp.build.screen_manager
#     manager.add_widget(MDBottomNavigationItem(name="main-screen"))
