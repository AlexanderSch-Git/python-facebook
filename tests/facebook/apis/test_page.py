import json
import unittest

import responses

import pyfacebook


class ApiPageTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/pages/"
    BASE_URL = "https://graph.facebook.com/" + pyfacebook.Api.VALID_API_VERSIONS[-1] + "/"

    with open(BASE_PATH + "single_default_page.json", "rb") as f:
        SINGLE_PAGE_INFO_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "single_fields_page.json", "rb") as f:
        SINGLE_PAGE_INFO_2 = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            long_term_token="token"
        )

    def testPage(self):
        page_id = "20531316728"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id, json=self.SINGLE_PAGE_INFO_1)
            page = self.api.get_page_info(
                page_id=page_id,
            )
            self.assertEqual(page.id, "20531316728")
            self.assertEqual(page.cover.id, "10159027219496729")
            self.assertEqual(len(page.category_list), 2)
            self.assertEqual(page.start_info.date.year, 2004)
            self.assertEqual(page.picture.height, 50)

        # test fields
        page_username = "facebookapp"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_username, json=self.SINGLE_PAGE_INFO_2)
            page = self.api.get_page_info(
                username=page_username,
                fields="id,name,username,fan_count",
                return_json=True
            )

            self.assertEqual(page["username"], page_username)
            self.assertEqual(page["fan_count"], 214507731)
