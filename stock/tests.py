from django.test import TestCase
from django.test import TestCase
from stock.models import Comment
from django.urls import reverse
# Create your tests here.
import os
FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"
class HomepageViewTests(TestCase):
        def test_homepageview_with_no_pages(self):
            """
      if there is no pages on the homepage，we will see a statement
            """
            response = self.client.get(reverse('stock:index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "There are no News post currently.")
            self.assertQuerysetEqual(response.context['pages'], [])

