from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from namespace.models import Namespace
from .models import Account, Currency

class AccountTests(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        
        # Create namespace
        self.namespace = Namespace.objects.create(user=self.user, name='personal')
        
        # Base URL
        self.create_url = '/api/accountsb/create/'
        self.list_url = '/api/accountsb/'
        self.retrieve_url = '/api/accountsb/retrieve-by-name/'
        self.update_url = '/api/accountsb/update/'
        self.delete_url = '/api/accountsb/delete/'
        self.list_by_ns_url = '/api/accountsb/list-by-namespace/'

    def test_create_account(self):
        data = {
            "namespace_name": "personal",
            "name": "Main USD Account",
            "currency": "USD"
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, "Main USD Account")

    def test_create_duplicate_account_name(self):
        # Create first account
        Account.objects.create(user=self.user, namespace=self.namespace, name="Savings", currency="USD")
        
        # Try to create another with same name (even in different namespace if we had one, but constraint is per user)
        data = {
            "namespace_name": "personal",
            "name": "Savings",
            "currency": "EUR"
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verify message if possible, but status code is key

    def test_list_accounts(self):
        Account.objects.create(user=self.user, namespace=self.namespace, name="Acc1", currency="USD")
        Account.objects.create(user=self.user, namespace=self.namespace, name="Acc2", currency="EUR")
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_account_by_name(self):
        Account.objects.create(user=self.user, namespace=self.namespace, name="Target Account", currency="USD")
        
        data = {"account_name": "Target Account"}
        response = self.client.post(self.retrieve_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Target Account")

    def test_update_account(self):
        Account.objects.create(user=self.user, namespace=self.namespace, name="Old Name", currency="USD")
        
        # Update name
        data = {"name": "New Name"}
        response = self.client.patch(f"{self.update_url}?account_name=Old Name", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Account.objects.filter(name="New Name").exists())
        self.assertFalse(Account.objects.filter(name="Old Name").exists())

    def test_delete_account(self):
        Account.objects.create(user=self.user, namespace=self.namespace, name="To Delete", currency="USD")
        
        response = self.client.delete(f"{self.delete_url}?account_name=To Delete")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)

    def test_list_accounts_by_namespace(self):
        Account.objects.create(user=self.user, namespace=self.namespace, name="In NS", currency="USD")
        
        data = {"namespace_name": "personal"}
        response = self.client.post(self.list_by_ns_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
