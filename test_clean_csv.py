import csv
import tempfile
import unittest
from pathlib import Path
from clean_csv import clean_csv


class CleanerTests(unittest.TestCase):
    def test_clean_and_keep_chinese(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'input.csv'
            output = Path(folder) / 'output.csv'
            source.write_text('姓名, 城市\n 小明 , 台北 \n小明,台北\n , \n小華,高雄\n', encoding='utf-8-sig')
            result = clean_csv(source, output)
            self.assertEqual(result, {'rows_read': 4, 'rows_written': 2, 'blank_removed': 1, 'duplicates_removed': 1})
            with output.open(encoding='utf-8-sig', newline='') as stream:
                self.assertEqual(list(csv.reader(stream)), [['姓名', '城市'], ['小明', '台北'], ['小華', '高雄']])

    def test_reject_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'data.csv'
            path.write_text('a\n1\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                clean_csv(path, path)

    def test_reject_malformed_row(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'input.csv'
            output = Path(folder) / 'output.csv'
            source.write_text('a,b\n1\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                clean_csv(source, output)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
