from abc import ABC, abstractmethod
import sqlite3
from typing import List
from lib.platform import Platform, PlatformNotFound

class DatabaseAccess(ABC):
    """Controls access to database"""
    @abstractmethod
    def find_platform(self, platform) -> bool:
        """Return if platform exists in the database"""

    @abstractmethod
    def get_admin_list(self) -> List[str]:
        """Returns a list of user IDs of all Admins"""

    @abstractmethod
    def get_owner_platforms(self, user_id) -> List[str]:
        """Get a list of all platforms owned by a user.
        """


    @abstractmethod
    def register_owner(self, user_id, platform):
        """Registers a user as an owner of a platform in PlatformOwners
        """ 

    @abstractmethod
    def add_user(self, user_id: str, name: str, email: str):
        """Add user to Users table"""

    @abstractmethod
    def delete_user(self, user_id: str):
        """Delete User from database. Foreign key management will destroy all ownership data in PlatformOwners"""

class SQLiteDatabaseAccess(DatabaseAccess):
    """Controls access to database"""

    def __init__(self, database_file: str):
        self.database = database_file
        self.build_db = sqlite3.connect(database_file)
        self.build_cursor = self.build_db.cursor()

        self.build_cursor.execute("PRAGMA foreign_keys = ON")

        self.admin_ids = self.get_admin_list()

    def find_platform(self, platform) -> bool:
        """Return if platform exists in the database"""
        self.build_cursor.execute('SELECT Platform FROM PlatformInfo WHERE Platform=?', (platform,))

        return self.build_cursor.fetchone() is not None

    def get_admin_list(self) -> List[str]:
        """Returns a list of user IDs of all Admins"""
        self.build_cursor.execute('SELECT AdminId FROM Admins')
        return [admin for admin, in self.build_cursor.fetchall()]

    def get_owner_platforms(self, user_id) -> List[str]:
        """Get a list of all platforms owned by a user.
        """
        self.build_cursor.execute('SELECT Platform FROM PlatformOwners WHERE UserId=:user_id', {'user_id':user_id})
        return [plat for plat, in self.build_cursor.fetchall()]
    
    def register_owner(self, user_id, platform):
        """Registers a user as an owner of a platform in PlatformOwners
        """
        # Add platform and user to PlatformOwners table
        with self.build_db:
            self.build_cursor.execute('INSERT INTO PlatformOwners (Platform, UserId) VALUES ( ?, ?)', (platform, user_id))    

    def add_user(self, user_id: str, name: str, email: str):
        """Add user to Users table"""
        with self.build_db:
            self.build_cursor.execute('INSERT INTO Users (UserId, UserName, UserEmail) VALUES (:user_id, :user_name, :user_email)', {'user_id':user_id, 'user_name':name, 'user_email': email})

    def delete_user(self, user_id: str):
        """Delete User from database. Foreign key management will destroy all ownership data in PlatformOwners"""

        with self.build_db:
            self.build_cursor.execute('DELETE FROM Users WHERE UserId=:userId', {'userId' : user_id})

    def get_platform(self, platform: str) -> Platform:
        """Get Platform from database"""

        self.build_cursor.execute('SELECT Platform, ChannelId, IdString FROM PlatformInfo WHERE Platform=:platform', {'platform':platform})
        platform_row = self.build_cursor.fetchone()
        if not platform_row:
            raise PlatformNotFound(message=f'Could not find platform {platform} in {self.database}')

        (platform_id, channel_id, description) = platform_row

        return Platform(rom_family=platform_id, description = description, slack_channel = channel_id)

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

if __name__ == "__main__":
    main()

