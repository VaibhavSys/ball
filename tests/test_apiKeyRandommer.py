from requests import get
from os import getenv
import unittest

class TestApiKeyRandommer(unittest.TestCase):
    
    def test_envVarExists(self):
        self.assertIsNotNone(getenv("RANDOMMER_API"))

    def test_keyIsValid(self):
        headers = {
        'accept': '*/*',
        'X-Api-Key': getenv("RANDOMMER_API")
        }

        params = (
            ('loremType', 'normal'),
            ('type', 'words'),
            ('number', '1'),
            )

        response = get('https://randommer.io/api/Text/LoremIpsum', headers=headers, params=params)
        self.assertEqual(response.status_code, 200)# Should be 200


if __name__ == "__main__":
    unittest.main()
