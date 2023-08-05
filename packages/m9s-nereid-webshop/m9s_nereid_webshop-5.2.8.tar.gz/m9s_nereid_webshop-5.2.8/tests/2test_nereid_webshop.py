# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import json
import unittest

from datetime import date
from decimal import Decimal
from os.path import join
from unittest.mock import patch

import pycountry

from cssutils import CSSParser

from trytond.config import config
from trytond.modules.gift_card.tests.test_gift_card import create_product
from trytond.modules.nereid_cart_b2c.tests import (
    create_countries, create_product_template, create_website)
from trytond.modules.payment_gateway.tests import create_payment_gateway
from trytond.pool import Pool
from trytond.tests.test_tryton import USER
from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import with_transaction
from trytond.transaction import Transaction

from nereid import request
from nereid.testing import NereidModuleTestCase

config.set('email', 'from', 'from@xyz.com')
css_dir = 'static/css/'


def create_test_products():
    pool = Pool()
    Category = pool.get('product.category')

    category2, = Category.create([
        {
            'name': 'Category 2',
        }])
    category3, = Category.create([
        {
            'name': 'Category 3',
        }])

    template1, = create_product_template(
        'Product 1',
        [{
            'type': 'goods',
            'salable': True,
            'list_price': Decimal('10'),
        }],
        uri='product-1',
    )
    template2, = create_product_template(
        'Product 2',
        [{
            'type': 'goods',
            'salable': True,
            'list_price': Decimal('10'),
        }],
        uri='product-2',
    )
    template3, = create_product_template(
        'Product 3',
        [{
            'type': 'goods',
            'salable': True,
            'list_price': Decimal('10'),
        }],
        uri='product-3',
    )
    template4, = create_product_template(
        'Product 4',
        [{
            'type': 'goods',
            'salable': True,
            'list_price': Decimal('10'),
        }],
        uri='product-4',
    )
    product2 = template2.products[0]
    product3 = template3.products[0]
    product4 = template4.products[0]

    product2.categories = [category2]
    product2.save()
    product3.categories = [category3]
    product3.save()
    product4.categories = [category3]
    product4.displayed_on_eshop = False
    product4.save()


def validate_css(filename):
    """
    Uses cssutils to validate a css file.
    Prints output using a logger.
    """
    CSSParser(raiseExceptions=True).parseFile(filename, validate=True)


class NereidWebshopTestCase(NereidModuleTestCase):
    'Test Nereid Webshop module'
    module = 'nereid_webshop'
    extras = ['nereid_catalog_variants', 'sale_shipment_cost']

    def setUp(self):
        self.templates = {
            'shopping-cart.jinja':
                'Cart:{{ cart.id }},{{get_cart_size()|round|int}},'
                '{{cart.sale.total_amount}}',
            'product.jinja':
                '{{ product.name }}',
            'catalog/gift-card.html':
                '{{ product.id }}',

            }

        # Patch SMTP Lib
        self.smtplib_patcher = patch('smtplib.SMTP')
        self.PatchedSMTP = self.smtplib_patcher.start()

    def tearDown(self):
        # Unpatch SMTP Lib
        self.smtplib_patcher.stop()

    @with_transaction()
    def test_0255_templates_guest_checkout(self):
        """
        Test for guest checkout.
        """
        pool = Pool()
        Company = pool.get('company.company')
        Country = pool.get('country.country')
        Sale = pool.get('sale.sale')
        SaleConfiguration = pool.get('sale.configuration')
        NereidUser = pool.get('nereid.user')
        NereidWebsite = pool.get('nereid.website')
        Product = pool.get('product.product')
        Account = pool.get('account.account')
        Party = pool.get('party.party')
        User = pool.get('res.user')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        website = create_website()
        website.save()
        gateway = create_payment_gateway()
        gateway.save()
        company, = Company.search([])

        sale_config = SaleConfiguration(1)
        sale_config.payment_authorize_on = 'sale_confirm'
        sale_config.payment_capture_on = 'sale_process'
        sale_config.gift_card_method = 'order'
        sale_config.save()

        create_countries()
        countries = Country.search([])
        website.countries = countries
        website.save()
        country = countries[0]
        subdivision = country.subdivisions[0]

        registered_user, = NereidUser.search([
                ('email', '=', 'email@example.com'),
                ])
        # Activate the user to block the email for others
        registered_user.active = True
        registered_user.email_verified = True
        registered_user.save()

        create_test_products()
        product1, = Product.search([
                ('name', '=', 'Product 1'),
                    ])
        product2, = Product.search([
                ('name', '=', 'Product 2'),
                    ])

        User.set_preferences({'current_channel': website.channel})
        User.write(
            [User(USER)], {
                'main_company': company.id,
                'company': company.id,
                'current_channel': website.channel,
                })

        # Define a new credit card payment gateway
        gateway = create_payment_gateway(method='dummy')

        websites = NereidWebsite.search([])
        NereidWebsite.write(websites, {
            'accept_credit_card': True,
            'save_payment_profile': True,
            'credit_card_gateway': gateway.id,
        })

        app = self.get_app()
        with app.test_client() as c:
            rv = c.post(
                '/en/cart/add',
                data={
                    'product': product1.id,
                    'quantity': 5
                }
            )
            self.assertEqual(rv.status_code, 302)

            rv = c.get('/en/checkout/sign-in')
            self.assertEqual(rv.status_code, 200)

            # Trying to checkout with a registered email should fail
            rv = c.post(
                '/en/checkout/sign-in',
                data={
                    'email': 'email@example.com'
                }
            )
            self.assertEqual(rv.status_code, 200)
            self.assertIn('{0}'.format(registered_user.email),
                rv.data.decode('utf-8'))
            self.assertIn(
                'is already registered with an existing account',
                rv.data.decode('utf-8'))
            # Now with a new email
            rv = c.post(
                '/en/checkout/sign-in',
                data={
                    'email': 'new@example.com',
                    'checkout_mode': 'guest'
                }
            )
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(
                rv.location.endswith('/checkout/shipping-address')
            )

            # Shipping address page should render
            rv = c.get('/en/checkout/shipping-address')
            self.assertEqual(rv.status_code, 200)

            address_data = {
                'name': 'Max Mustermann',
                'street': 'Musterstr. 26',
                'zip': '79852',
                'city': 'Musterstadt',
                'country': country.id,
                'subdivision': subdivision.id,
                'phone': '+491791234567',
            }
            # Shipping address
            rv = c.post(
                '/en/checkout/shipping-address',
                data=address_data)
            # Failing address form validation would mean 200 with no location
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(rv.location.endswith('/checkout/validate-address'))

            # Billing address
            rv = c.post(
                '/en/checkout/billing-address',
                data={
                    'name': 'Max Mustermann',
                    'street': '2J Skyline Daffodil',
                    'zip': '682013',
                    'city': 'Cochin',
                    'country': country.id,
                    'subdivision': subdivision.id,
                    'phone': '+491791234567',
                    })
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(rv.location.endswith('/checkout/delivery-method'))

            # Delivery method
            rv = c.post('/en/checkout/delivery-method',
                data={})
            # Should per default forward to payment with valid shipping address
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(rv.location.endswith('/checkout/payment'))

            context = {
                'company': company.id,
                'use_dummy': True,
                'dummy_succeed': True,
                }
            with Transaction().set_context(**context):
                # Set default receivable account
                receivable, = Account.search([
                        ('type.receivable', '=', True),
                        ])
                parties = Party.search([])
                Party.write(parties, {
                        'account_receivable': receivable,
                        })

                # Try to pay using credit card
                card_data = {
                    'owner': 'Joe Blow',
                    'number': '4111111111111111',
                    'expiry_year': '2030',
                    'expiry_month': '01',
                    'cvv': '911',
                    'add_card_to_profiles': '',
                    }
                rv = c.post(
                    '/en/checkout/payment',
                    data=card_data)

                # Run the sale and payment processing usually delegated
                # to the queue
                sale, = Sale.search([])
                Sale.quote_web_sales([sale])

                self.assertEqual(sale.state, 'quotation')
                payment_transaction, = sale.gateway_transactions
                self.assertEqual(payment_transaction.amount, sale.total_amount)

                rv = c.get('/en/order/{0}'.format(sale.id))
                self.assertEqual(rv.status_code, 302)  # Orders page redirect

    @unittest.skip('')
    @with_transaction()
    def test_0510_download_invoice(self):
        """
        Test to download invoice from a sale
        """
        pool = Pool()
        Company = pool.get('company.company')
        Country = pool.get('country.country')
        Sale = pool.get('sale.sale')
        SaleConfiguration = pool.get('sale.configuration')
        NereidUser = pool.get('nereid.user')
        NereidWebsite = pool.get('nereid.website')
        Product = pool.get('product.product')
        Account = pool.get('account.account')
        Party = pool.get('party.party')
        User = pool.get('res.user')
        Invoice = pool.get('account.invoice')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        website = create_website()
        website.save()
        gateway = create_payment_gateway()
        gateway.save()
        company, = Company.search([])

        sale_config = SaleConfiguration(1)
        sale_config.payment_authorize_on = 'sale_confirm'
        sale_config.payment_capture_on = 'sale_process'
        sale_config.gift_card_method = 'order'
        sale_config.save()

        create_countries()
        countries = Country.search([])
        website.countries = countries
        website.save()
        country = countries[0]
        subdivision = country.subdivisions[0]

        registered_user, = NereidUser.search([
                ('email', '=', 'email@example.com'),
                ])

        create_test_products()
        product1, = Product.search([
                ('name', '=', 'Product 1'),
                    ])
        product2, = Product.search([
                ('name', '=', 'Product 2'),
                    ])

        User.set_preferences({'current_channel': website.channel})
        User.write(
            [User(USER)], {
                'main_company': company.id,
                'company': company.id,
                'current_channel': website.channel,
                })

        # Define a new credit card payment gateway
        gateway = create_payment_gateway(method='dummy')

        websites = NereidWebsite.search([])
        NereidWebsite.write(websites, {
            'accept_credit_card': True,
            'save_payment_profile': True,
            'credit_card_gateway': gateway.id,
        })

        app = self.get_app()
        with app.test_client() as c:
            rv = c.post(
                '/en/cart/add',
                data={
                    'product': product1.id,
                    'quantity': 5
                }
            )
            self.assertEqual(rv.status_code, 302)

            # Now sign in to checkout.
            rv = c.post('/en/checkout/sign-in',
                data={
                    'email': 'email@example.com',
                    'password': 'password',
                    'checkout_mode': 'account'
                }
            )
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(rv.location.endswith('/shipping-address'))

            # Shipping address page should render
            rv = c.get('/en/checkout/shipping-address')
            self.assertEqual(rv.status_code, 200)

            address_data = {
                'name': 'Max Mustermann',
                'street': 'Musterstr. 26',
                'zip': '79852',
                'city': 'Musterstadt',
                'country': country.id,
                'subdivision': subdivision.id,
                'phone': '+491791234567',
            }
            # Shipping address
            rv = c.post(
                '/en/checkout/shipping-address',
                data=address_data)
            # Failing address form validation would mean 200 with no location
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(rv.location.endswith('/checkout/validate-address'))

            # Billing address
            rv = c.post(
                '/en/checkout/billing-address',
                data={
                    'name': 'Max Mustermann',
                    'street': '2J Skyline Daffodil',
                    'zip': '682013',
                    'city': 'Cochin',
                    'country': country.id,
                    'subdivision': subdivision.id,
                    'phone': '+491791234567',
                    })
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(rv.location.endswith('/checkout/delivery-method'))

            # Delivery method
            rv = c.post('/en/checkout/delivery-method',
                data={})
            # Should per default stay on delivery-method if no carrier was
            # provided
            self.assertEqual(rv.status_code, 200)
            # Check for the missing carrier selection
            self.assertIn('No shipping method found', rv.data.decode('utf-8'))
            # Check for the flash message if delievery-method was posted
            # nevertheless
            self.assertIn(
                'There was no carrier selected', rv.data.decode('utf-8'))

            context = {
                'company': company.id,
                'use_dummy': True,
                'dummy_succeed': True,
                }
            with Transaction().set_context(**context):
                # Set default receivable account
                receivable, = Account.search([
                        ('type.receivable', '=', True),
                        ])
                parties = Party.search([])
                Party.write(parties, {
                        'account_receivable': receivable,
                        })

                # Try to pay using credit card
                card_data = {
                    'owner': 'Joe Blow',
                    'number': '4111111111111111',
                    'expiry_year': '2030',
                    'expiry_month': '01',
                    'cvv': '911',
                    'add_card_to_profiles': '',
                    }
                rv = c.post(
                    '/en/checkout/payment',
                    data=card_data)

                # Run the sale and payment processing usually delegated
                # to the queue
                sale, = Sale.search([])
                Sale.quote_web_sales([sale])

                self.assertEqual(sale.state, 'quotation')
                payment_transaction, = sale.gateway_transactions
                self.assertEqual(payment_transaction.amount, sale.total_amount)

                rv = c.get('/en/order/{0}?access_code={1}'.format(
                        sale.id, sale.guest_access_code))
                self.assertEqual(rv.status_code, 200)

                Sale.process_all_pending_payments()
                Sale.confirm([sale])
                Sale.process_all_pending_payments()
                Sale.process([sale])
                Invoice.post(sale.invoices)

        with app.test_client() as c:
            # Loged in user tries to download invoice
            rv = c.post('/en/login',
                data={
                    'email': 'email@example.com',
                    'password': 'password'
                    })
            response = c.get(
                '/en/orders/invoice/%s/download' % (sale.invoices[0].id,))


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NereidWebshopTestCase))
    return suite
