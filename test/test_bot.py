import unittest
import sqlite3

from unittest.mock import patch

from bot import BuildNotification, BuildMessage
from lib.auth import UnauthorizedAction, UserAlreadyOwner
from lib.user import User

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from unittest.mock import patch

from bot import BuildNotification, BuildMessage
from db_manager import User, UnauthorizedAction, UserAlreadyOwner, PlatformError

import db_manager

DEBUG = True
CREATE_DB = False

if DEBUG:
    test_db = sqlite3.connect('test.db')
else:
    test_db = sqlite3.connect(':memory:')

cursor = test_db.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

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

class TestBuildNotifications(unittest.TestCase):
    def test_get_build_info(self):
        self.test_build_dict = BUILD_DICT
        testBuild = BuildNotification(self.test_build_dict)
        self.assertEqual(testBuild._get_build_info(), EXPECTED_BUILD_INFO)

        self.test_build_dict['platform'] =  ['H10']
        self.test_build_dict['new_rom_version'] = '1.99_09_09_9999'
        testBuild = BuildNotification(self.test_build_dict)
        self.assertEqual(testBuild._get_build_info(), {'type':'section', 'text': {'type':'mrkdwn','text':'*H10 build complete*\nBuild version: 1.99_09_09_9999'}})


class TestUserActions(unittest.TestCase):
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

    @patch('db_manager.client')
    def setUp(self, mock_client):
        # Create TEST User
        mock_client.users_info.return_value = {'profile':{'real_name':"Test User", 'email': 'test_user@hpe.com'}, 'id' : 'TEST'}
        self.test_user = User('TEST')

  
    def tearDown(self):
        with test_db:
            try:
                cursor.execute('DELETE FROM Users WHERE UserId="TEST"')
            except :
                pass  

    @patch('db_manager.client')
    def test_admin_User(self, mock_client):

        # admin user creation
        mock_client.users_info.return_value = {'profile':{'real_name':"Jack Little", 'email': 'jack.tay.little@hpe.com'}, 'id' : 'ABC123'}
        admin = User('ABC123')

        # multiple owned platforms
        self.assertEqual(admin.get_owner_platforms(), ['H10', 'U47'])

        # check admin for admin
        self.assertEqual(admin._get_admin(), True)

        # Admin - register owner
        self.assertEqual(self.test_user.get_owner_platforms(), [])

        admin.register_owner(self.test_user, 'H10')
        self.assertEqual(self.test_user.get_owner_platforms(), ['H10'])
        admin.register_owner(self.test_user, 'U47')
        self.assertEqual(self.test_user.get_owner_platforms(), ['H10', 'U47'])
        
        # Admin - register existing owner
        #       Handle UserAlreadyOwner exception
        with self.assertRaises(UserAlreadyOwner):
            admin.register_owner(self.test_user, 'H10')

        # Admin - delete user
        #       Removes user from Users which should cascade 
        #       and remove all platforms registered to the user
        #       in PlatformOwners
        admin.delete_user(self.test_user)

        cursor.execute('SELECT UserId FROM Users WHERE UserId=(?)', (self.test_user.userId, ))
        self.assertEqual(cursor.fetchone(), None)

        cursor.execute('SELECT Platform FROM PlatformOwners WHERE UserId=(?)', (self.test_user.userId, ))
        self.assertEqual(cursor.fetchall(), [])

        # Admin - register owner for platform not in DB
        #       Should throw PlatformNotFound
        with self.assertRaises(PlatformError):
            admin.register_owner(self.test_user, 'ZZZ')

        # Admin - create platform
        admin.register_platform('Z99', 'e333 New Platform')
        cursor.execute('SELECT * FROM PlatformInfo WHERE Platform="Z99"')
        self.assertEqual(cursor.fetchone(), ('Z99', None, 'e333 New Platform'))
        
        # Admin - create existing platform
        #       Should throw PlatformError
        with self.assertRaises(PlatformError):
            admin.register_platform('Z99', "Another one")

        # Admin - delete platform
        admin.delete_platform('Z99')
        cursor.execute('SELECT * FROM PlatformInfo WHERE Platform="Z99"')
        self.assertEqual(cursor.fetchone(), None)

        # Admin - delete platfrom not in DB
        with self.assertRaises(PlatformError):
            admin.delete_platform('Z99')
       

    @patch('db_manager.client')
    def test_normal_User(self, mock_client):
        
        # Make owner
        mock_client.users_info.return_value = {'profile':{'real_name':"Jack Whack", 'email': 'jack.3@hpe.com'}, 'id' : 'ABC456'}
        user = User('ABC456')

        # multiple owned platforms
        self.assertEqual(user.get_owner_platforms(), ['H10', 'U47'])

        # no owned platforms
        self.assertEqual(self.test_user.get_owner_platforms(), [])
        
        # single owned platform
        user.userId = 'ABC789'
        self.assertEqual(user.get_owner_platforms(), ['H10'])

        # check admin for non-admin
        self.assertEqual(user._get_admin(), False)

        # register user for platform as Owner
        user.register_owner(self.test_user, 'H10')
        cursor.execute('SELECT UserId FROM PlatformOwners WHERE UserId="TEST" AND Platform="H10"')
        self.assertEqual(cursor.fetchone(), ('TEST', ))

        # register user again
        #       Should raise UserAlreadyOwner
        with self.assertRaises(UserAlreadyOwner):
            user.register_owner(self.test_user, 'H10')

        # register user for platform as non-Owner
        #       Should raise UnauthorizedAction
        with self.assertRaises(UnauthorizedAction):
            user.register_owner(self.test_user, 'U47')

        # register existing platform

        # register platform not in DB


    @patch('db_manager.client')
    def test_create_User(self, mock_client):
        # user creation
        mock_client.users_info.return_value = {'profile':{'real_name':"Jack Shmack", 'email': 'jack.2@hpe.com'}, 'id' : 'ABC456'}
        user = User('ABC456')
        self.assertEqual(user.name, 'Jack Shmack')
        self.assertEqual(user.email, 'jack.2@hpe.com')
        self.assertEqual(user.userId, 'ABC456')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.owned_platforms, ['H10', 'U47'])


    
class TestDatabase(unittest.TestCase):
    def test_find_platform(self):
        # Find existing platform
        self.assertEqual(db_manager.find_platform('H10'), True)

        # Find new platform
        self.assertEqual(db_manager.find_platform('Y99'), False)


    def test_db_foreign_keys(self):
        """Test that the foreign key dependencies are working correctly
        """
        with test_db:
            cursor.execute('INSERT INTO Users VALUES (?, ?, ?)', ('TEST1', '', ''))
            cursor.execute('INSERT INTO Users VALUES (?, ?, ?)', ('TEST2', '', ''))

            cursor.execute('INSERT INTO PlatformInfo VALUES (?, ?, ?)', ('Z99', None, ''))
            cursor.execute('INSERT INTO PlatformInfo VALUES (?, ?, ?)', ('X88', None, ''))

            cursor.execute('INSERT INTO PlatformOwners VALUES (?, ?)', ('Z99', 'TEST1'))
            cursor.execute('INSERT INTO PlatformOwners VALUES (?, ?)', ('Z99', 'TEST2'))
            cursor.execute('INSERT INTO PlatformOwners VALUES (?, ?)', ('X88', 'TEST1'))
            cursor.execute('INSERT INTO PlatformOwners VALUES (?, ?)', ('X88', 'TEST2'))

        with test_db:
            cursor.execute('DELETE FROM Users WHERE UserId="TEST1"')
        
        cursor.execute('SELECT Platform FROM PlatformOwners WHERE UserId="TEST1"')
        self.assertEqual(cursor.fetchall(), [])

        with test_db:
            cursor.execute('DELETE FROM PlatformInfo WHERE Platform="X88"')
        cursor.execute('SELECT UserId FROM PlatformOwners WHERE Platform="X88"')
        self.assertEqual(cursor.fetchall(), [])

        #clean up
        cursor.execute('DELETE FROM PlatformInfo WHERE Platform="Z99"')
        cursor.execute('DELETE FROM Users WHERE UserId="TEST2"')

if __name__ == '__main__':
    db_manager.build_cursor = cursor
    db_manager.build_db = test_db
    unittest.main()