import unittest
from bot import BuildNotification, BuildMessage
import json

DEMO_JENKINS_MESSAGE = """{
  "end_sha": "89c84c410f8670a15d73e6a90b3f8007efa01cf5",
  "start_sha": "eae54533244881c411add67a7f7b00b57a48584e",
  "branch": "origin/private/Jack/H10_05_27_2021",
  "platform": [
    "H10",
    "U47"
  ],
  "new_rom_version": "1.42_05_27_2021",
  "parent_rom_version": "1.42_04_30_2021",
  "snap": "Gen10 Plus Snap 4 Latent",
  "rom_type": "release",
  "bootleg_build_type": "DEBUG",
  "bootleg_desc": "",
  "user_email": "jack.tay.little@hpe.com",
  "release_doc_enabled": true,
  "debug_build_enabled": true,
  "release_build_enabled": true,
  "test_build_enabled": false,
  "skip_build_enabled": false,
  "submission_id": "49e2dd7b-ebf1-433b-b6fd-b7793264a485"
}
"""
BUILD_DICT = {'end_sha': '89c84c410f8670a15d73e6a90b3f8007efa01cf5', 'start_sha': 'eae54533244881c411add67a7f7b00b57a48584e', 'branch': 'origin/private/Jack/H10_05_27_2021', 'platform': ['H10', 'U47'], 'new_rom_version': '1.42_05_27_2021', 'parent_rom_version': '1.42_04_30_2021', 'snap': 'Gen10 Plus Snap 4 Latent', 'rom_type': 'release', 'bootleg_build_tyild_enabled': False, 'skip_build_enabled': False, 'submission_id': '49e2dd7b-ebf1-433b-b6fd-b7793264a485'}
EXPECTED_BUILD_INFO = {
            'type': 'section',
            'text': {
                'type' : 'mrkdwn',
                'text'  : '*H10, U47 builds complete*\nBuild version: 1.42_05_27_2021'
            }
        }

class TestBot(unittest.TestCase):
    
    def setUp(self):
        self.test_build_dict = BUILD_DICT

    def test_get_build_info(self):
        testBuild = BuildNotification(self.test_build_dict)
        self.assertEqual(testBuild._get_build_info(), EXPECTED_BUILD_INFO)

        self.test_build_dict['platform'] =  ['H10']
        self.test_build_dict['new_rom_version'] = '1.99_09_09_9999'
        testBuild = BuildNotification(self.test_build_dict)
        self.assertEqual(testBuild._get_build_info(), {'type':'section', 'text': {'type':'mrkdwn','text':'*H10 build complete*\nBuild version: 1.99_09_09_9999'}})


    

if __name__ == '__main__':
    unittest.main()