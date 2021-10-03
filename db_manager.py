import sqlite3
from typing import List
from enum import Enum, auto

# Describes the form of all the tables in the database
class PlatformOwnersEnum(Enum):
    Platform = 0
    UserId = auto()
        
class UsersEnum(Enum):
    UserId = 0
    UserName = auto()
    UserEmail = auto()

class AdminsEnum(Enum):
    AdminId = 0
    AdminName = auto()
    AdminEmail = auto()

class PlatformInfoEnum(Enum):
    Platform = 0
    ChannelId = auto()

class Auth:
    def __init__(self):
        pass
    
class DatabaseAccess:
    def __init__(self):
        self.build_db = sqlite3.connect('build_database.db')
        self.build_cursor = self.build_db.cursor()

        self.build_cursor.execute("PRAGMA foreign_keys = ON")

    def find_platform(self, platform) -> bool:
        """Find a platform in PlatformInfo table
        Return True/False that it exists"""
        self.build_cursor.execute('SELECT Platform FROM PlatformInfo WHERE Platform=?', (platform,))

        return self.build_cursor.fetchone() != None

    def get_admin(self, userId) -> bool:
        """Returns True if user exists in admins table, otherwise false
        """
        self.build_cursor.execute('SELECT AdminId FROM Admins WHERE AdminID=:user_id', {'user_id':userId})
        return self.build_cursor.fetchone() != None

    def get_admin_list(self) -> List[str]:
        """Returns a list of user IDs of all Admins"""
        self.build_cursor.execute('SELECT AdminId FROM Admins')
        return [admin for admin, in self.build_cursor.fetchall()]

    def get_owner_platforms(self, userId) -> List[str]:
        """Get a list of all platforms owned by a user.
        """
        self.build_cursor.execute('SELECT Platform FROM PlatformOwners WHERE UserId=:user_id', {'user_id':userId})
        return [plat for plat, in self.build_cursor.fetchall()]
    
    def register_owner(self, userId, platform):
        """Registers a user as an owner of a platform in PlatformOwners
        """
        # Add platform and user to PlatformOwners table
        with self.build_db:
            self.build_cursor.execute('INSERT INTO PlatformOwners (Platform, UserId) VALUES ( ?, ?)', (platform, userId))    

    def add_user(self, userId: str, name: str, email: str):
        """Add user to Users table"""
        with self.build_db:
            self.build_cursor.execute('INSERT INTO Users (UserId, UserName, UserEmail) VALUES (:user_id, :user_name, :user_email)', {'user_id':userId, 'user_name':name, 'user_email': email})

    def delete_user(self, userId: str):
        """Delete User from database. Foreign key management will destroy all ownership data in PlatformOwners"""

        with self.build_db: 
            self.build_cursor.execute('DELETE FROM Users WHERE UserId=:userId', {'userId' : userId})


def main():
    pass
    # build_cursor.execute("""
    #     CREATE TABLE "build_database" (
    #     "Build_ID"	INTEGER UNIQUE,
    #     "Platform"	TEXT,
    #     "Build_Version"	TEXT,
    #     "Parent_Version"	TEXT,
    #     "Branch"	TEXT,
    #     "Build_Message_ID"	TEXT,
    #     PRIMARY KEY("Build_ID" AUTOINCREMENT)
    #     )
    #     """)

    # build_cursor.execute("""
    #     CREATE TABLE "build_messages" (
    #     "Message_ID"	INTEGER UNIQUE,
    #     "Message"	TEXT,
    #     PRIMARY KEY("Message_ID" AUTOINCREMENT)
    #     )
    #     """)

    # build_cursor.execute("""
    #     CREATE TABLE "owners" (
    #         "User_id"	TEXT UNIQUE,
    #         "User_email"	TEXT,
    #         "Platforms"	TEXT
    #     )
    #     """)

    # build_db.close()

if(__name__ == "__main__"):
    main()

