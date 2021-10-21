from abc import ABC, abstractmethod
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from lib.platform import Platform, PlatformNotFound

class DatabaseAccess(ABC):
    """Controls access to database"""
    @abstractmethod
    def find_platform(self, platform) -> bool:
        """Return if platform exists in the database"""

    @abstractmethod
    def _get_admin_list(self) -> list[str]:
        """Returns a list of user IDs of all Admins"""

    @abstractmethod
    def get_owner_platforms(self, user_id) -> list[str]:
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

    @abstractmethod
    def _get_platforms(self) -> list[Platform]:
        """Get platfrom data from PlatformInfo table"""

class SQLiteDatabaseAccess(DatabaseAccess):
    """Controls access to database"""

    def __init__(self, database_file: str):
        self.database = database_file
        # self.build_db = sqlite3.connect(database_file)
        # self.cur = self.build_db.cursor()

        # self.cur.execute("PRAGMA foreign_keys = ON")

        self.admin_ids = self._get_admin_list()
        self.platforms = self._get_platforms()

    def make_cursor(self, connection: Connection) -> Cursor:
        """Make a new cursor for the SQLite connection"""
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        return cursor

    def find_platform(self, platform) -> bool:
        """Return if platform exists in the database"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('SELECT Platform FROM PlatformInfo WHERE Platform=?', (platform,))
            platform = cur.fetchone()
        return platform is not None

    def _get_admin_list(self) -> list[str]:
        """Returns a list of user IDs of all Admins"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('SELECT AdminId FROM Admins')
            admins = cur.fetchall()
        return [admin for admin, in admins]

    def get_owner_platforms(self, user_id) -> list[str]:
        """Get a list of all platforms owned by a user.
        """
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('SELECT Platform FROM PlatformOwners WHERE UserId=:user_id', {'user_id':user_id})
            owners_platforms = cur.fetchall()
        return [plat for plat, in owners_platforms]
    
    def register_owner(self, user_id, platform):
        """Registers a user as an owner of a platform in PlatformOwners
        """
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('INSERT INTO PlatformOwners (Platform, UserId) VALUES ( ?, ?)', (platform, user_id))    

    def add_user(self, user_id: str, name: str, email: str):
        """Add user to Users table"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('INSERT INTO Users (UserId, UserName, UserEmail) VALUES (:user_id, :user_name, :user_email)', {'user_id':user_id, 'user_name':name, 'user_email': email})

    def delete_user(self, user_id: str):
        """Delete User from database. Foreign key management will destroy all ownership data in PlatformOwners"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('DELETE FROM Users WHERE UserId=:userId', {'userId' : user_id})

    def _get_platforms(self) -> Platform:
        """Get list of all platforms in database"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('SELECT Platform, ChannelId, IdString FROM PlatformInfo')
            platforms = cur.fetchall()

        platform_list = []
        for platform in platforms:
            (platform_id, channel_id, description) = platform
            platform_list.append(Platform((platform_id, channel_id, description)))

        return platform_list

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

