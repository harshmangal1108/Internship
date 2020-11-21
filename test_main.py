import unittest
import main as m
import config as cfg

test_length = 10
test_fields = ["name", "is_groupby", "is_active", "field_name", "new_sheet_name", "collection_name",
                       "interval_date", "interval_time", "group_by", "filter"]


class check_fields(unittest.TestCase):
    def test_check_fields(self):
        self.assertEqual(m.check_field_length, test_length)
        self.assertEqual(m.fields, test_fields)
        for test_key, test_val in cfg.configuration_count.items():
            # print(m.check_fields(test_key,test_val))
            self.assertEqual(m.check_fields(test_key, test_val), True)


class from_main(unittest.TestCase):
    def test_from_main(self):
        pass


if __name__ == '__main__':
    unittest.main()
