import unittest
import get_hdd as func

class HDD_Tracking_Test(unittest.TestCase):
    def test_get_MDI_files_name(self):
        number_of_sesions, sessions_list, car_name = func.get_MDI_files_name('C:/Users/zdunek/Desktop/mdiki/mdi_CW24YYGP')
        self.assertEqual(number_of_sesions,2)
        self.assertEqual(sessions_list,['CW24YYGP_2021_01_20__10_09_44','CW24YYGP_2021_01_20__13_09_44'])
        self.assertEqual(car_name,'CW24YYGP')
        self.assertRegex(sessions_list[0], r'._\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2}')
        self.assertGreater(len(sessions_list[0]),21)


if __name__=="__main__":
    unittest.main()


