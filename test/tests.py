import unittest
from satcounter import satnum as sn


class GeneralTests(unittest.TestCase):
    def test_res4(self):
        date = [2020, 12, 25, 18, 00, 00]
        exp = 1500
        cords = [45.0, 45.0]
        field_of_view = 600
        self.assertEqual(sn.satnum(date, exp, cords, field_of_view), 4, "Wrong Answer")

    def test_res1(self):
        date = [2020, 12, 27, 18, 00, 00]
        exp = 1500
        cords = [45.0, 45.0]
        field_of_view = 600
        self.assertEqual(sn.satnum(date, exp, cords, field_of_view), 1, "Wrong Answer")

    def test_res0(self):
        date = [2020, 12, 27, 18, 00, 00]
        exp = 150
        cords = [45.0, 45.0]
        field_of_view = 60
        self.assertEqual(sn.satnum(date, exp, cords, field_of_view), 0, "Wrong Answer")

    def test_date(self):
        date = "2020-10-10 19:00"
        exp = 150
        cords = [45.0, 45.0]
        field_of_view = 60
        with self.assertRaises(TypeError, msg='argument should be a list'):
            sn.satnum(date, exp, cords, field_of_view)

    def test_exp(self):
        date = [2020, 12, 27, 18, 00, 00]
        exp = -27.5
        cords = [45.0, 45.0]
        field_of_view = 60
        with self.assertRaises(ValueError, msg='argument should be an integer'):
            sn.satnum(date, exp, cords, field_of_view)

    def test_cords(self):
        date = [2020, 12, 27, 18, 00, 00]
        exp = 150
        cords = ["45deg", 45.0]
        field_of_view = 60
        with self.assertRaises(ValueError, msg='argument should be a float'):
            sn.satnum(date, exp, cords, field_of_view)

    def test_fov(self):
        date = [2020, 12, 27, 18, 00, 00]
        exp = 150
        cords = [45.0, 45.0]
        field_of_view = -45.5
        with self.assertRaises(ValueError, msg='argument should be an integer'):
            sn.satnum(date, exp, cords, field_of_view)


def test_suite():
    suite = unittest.defaultTestLoader.loadTestsFromName(__name__)
    return suite


if __name__ == '__main__':
    unittest.main()
