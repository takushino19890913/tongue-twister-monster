import unittest
import json
from app import app

class FindSimilarAndAnagramsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_find_similar_and_anagrams(self):
        # テストデータを設定
        test_data = {
            'word': 'みかん'
        }

        # POSTリクエストを送信
        response = self.app.post('/find_similar_and_anagrams', 
                                 data=json.dumps(test_data),
                                 content_type='application/json')

        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)

        # レスポンスデータを取得
        response_data = json.loads(response.data)

        # レスポンスデータがリストであることを確認
        self.assertIsInstance(response_data, list)

        # レスポンスデータの内容を確認（必要に応じて）
        print(response_data)

if __name__ == '__main__':
    unittest.main()