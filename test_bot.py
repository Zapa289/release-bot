import unittest
import json
import sqlite3

from unittest.mock import patch

from bot import BuildNotification, BuildMessage

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

import db_manager

DEBUG = True
CREATE_DB = False

if DEBUG:
    test_db = sqlite3.connect('test.db')
else:
    test_db = sqlite3.connect(':memory:')

cursor = test_db.cursor()

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

# UNCOMMENT WHEN USING RAM DB

  @classmethod
  def setUpClass(cls):
    if not DEBUG or CREATE_DB:
        cursor.execute("""  
        CREATE TABLE "Admins" (
        "AdminId"	TEXT UNIQUE,
        "AdminName"	TEXT,
        "AdminEmail"	TEXT,
        PRIMARY KEY("AdminId")
        ) 
        """)

        cursor.execute("""  
        CREATE TABLE "Users" (
        "UserId"	TEXT DEFAULT '' UNIQUE,
        "UserName"	TEXT DEFAULT '',
        "UserEmail"	TEXT DEFAULT '',
        PRIMARY KEY("UserId")
        ) 
        """)

        cursor.execute("""  
        CREATE TABLE "PlatformInfo" (
        "Platform"	TEXT,
        "ChannelId"	TEXT,
        "IdString"	TEXT DEFAULT '',
        PRIMARY KEY("Platform")
        )
        """)

        cursor.execute("""  
        CREATE TABLE "PlatformOwners" (
        "Platform"	TEXT NOT NULL,
        "UserId"	TEXT NOT NULL,
        FOREIGN KEY("UserId") REFERENCES "Users"("UserId") ON DELETE CASCADE,
        FOREIGN KEY("Platform") REFERENCES "PlatformInfo"("Platform") ON DELETE CASCADE
        )
        """)

        with test_db:
            cursor.execute("INSERT INTO Users (UserId, UserName, UserEmail) VALUES ('ABC123','Jack Little','jack.tay.little@hpe.com')")
            cursor.execute("INSERT INTO Users (UserId, UserName, UserEmail) VALUES ('ABC456','Jack Shmack','jack.2@hpe.com')")
            cursor.execute("INSERT INTO Users (UserId, UserName, UserEmail) VALUES ('ABC789','Jack Whack','jack.3@hpe.com')")
            cursor.execute("INSERT INTO Users (UserId, UserName, UserEmail) VALUES ('ABCABC','Jack Black','jack.4@hpe.com')")
            cursor.execute("INSERT INTO Users (UserId, UserName, UserEmail) VALUES ('ABCDEF','Jack Attack','jack.5@hpe.com')") 

            cursor.execute("INSERT INTO Admins (AdminId, AdminName, AdminEmail) VALUES ('ABC123','Jack Little','jack.tay.little@hpe.com')") 

            cursor.execute("INSERT INTO PlatformInfo (Platform, ChannelId, IdString) VALUES ('H10','CHANNEL1','e920 - Carcassonne')")
            cursor.execute("INSERT INTO PlatformInfo (Platform, ChannelId, IdString) VALUES ('U47','CHANNEL2','Monterrey')") 

            cursor.execute("INSERT INTO PlatformOwners (Platform, UserId) VALUES ('H10','ABC123')")
            cursor.execute("INSERT INTO PlatformOwners (Platform, UserId) VALUES ('H10','ABC789')")
            cursor.execute("INSERT INTO PlatformOwners (Platform, UserId) VALUES ('H10','ABC456')") 
            cursor.execute("INSERT INTO PlatformOwners (Platform, UserId) VALUES ('U47','ABC123')")
            cursor.execute("INSERT INTO PlatformOwners (Platform, UserId) VALUES ('U47','ABC456')")
            cursor.execute("INSERT INTO PlatformOwners (Platform, UserId) VALUES ('U47','ABCDEF')")       

  def setUp(self):
      pass
  
  def test_get_build_info(self):
      self.test_build_dict = BUILD_DICT
      testBuild = BuildNotification(self.test_build_dict)
      self.assertEqual(testBuild._get_build_info(), EXPECTED_BUILD_INFO)

      self.test_build_dict['platform'] =  ['H10']
      self.test_build_dict['new_rom_version'] = '1.99_09_09_9999'
      testBuild = BuildNotification(self.test_build_dict)
      self.assertEqual(testBuild._get_build_info(), {'type':'section', 'text': {'type':'mrkdwn','text':'*H10 build complete*\nBuild version: 1.99_09_09_9999'}})
  
  @patch('db_manager.client')
  def test_admin_User(self, mock_client):
    # user creation
    mock_client.users_info.return_value = {'profile':{'real_name':"Jack Little", 'email': 'jack.tay.little@hpe.com'}}
    user = db_manager.User('ABC123')
    self.assertEqual(user.name, 'Jack Little')
    self.assertEqual(user.email, 'jack.tay.little@hpe.com')
    self.assertEqual(user.userId, 'ABC123')

    # multiple owned platforms
    self.assertEqual(user._get_owner_platforms(), ['H10', 'U47'])

    # check admin for admin
    self.assertEqual(user._get_admin(), True)

    # register owner as Admin
    mock_client.users_info.return_value = {'profile':{'real_name':"Test Register", 'email': 'test_register@hpe.com'}}
    test_register = db_manager.User('TEST')
    user.register_owner(test_register, 'H10')
    test_register = db_manager.User('TEST') #re-create the user to update owned platforms

    
    # register existing owner as Admin


    # register owner for platform not in DB


  def test_User(self):
    # user creation
    with patch('db_manager.client') as mock_client:
      mock_client.users_info.return_value = {'profile':{'real_name':"Jack Whack", 'email': 'jack.3@hpe.com'}}
      user = db_manager.User('ABC789')
      self.assertEqual(user.name, 'Jack Whack')
      self.assertEqual(user.email, 'jack.3@hpe.com')
      self.assertEqual(user.userId, 'ABC789')

    # multiple owned platforms
    self.assertEqual(user._get_owner_platforms(), ['H10', 'U47'])

    # single owned platform
    user.userId = 'ABC789'
    self.assertEqual(user._get_owner_platforms(), ['H10'])

    # no owned platforms
    user.userId = 'FFFFFF'
    self.assertEqual(user._get_owner_platforms(), [])

    # check admin for admin
    user.userId = 'ABC123'
    self.assertEqual(user._get_admin(), True)

    # check admin for non-admin
    user.userId = 'ABC456'
    self.assertEqual(user._get_admin(), False)

    # register platform as Admin

    # register platform as Owner

    # register platform as non-Owner

    # register existing platform

    # register platform not in DB

    

if __name__ == '__main__':
    db_manager.build_cursor = cursor
    unittest.main()