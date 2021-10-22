from abc import ABC, abstractmethod
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from lib.platform import Platform, PlatformNotFound

class DatabaseAccess(ABC):
    """Controls access to database"""

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
    def _add_owner(self, user_id: str, name: str, email: str):
        """Add user to Owners table"""

    @abstractmethod
    def delete_owner(self, user_id: str):
        """Delete owner from database. Foreign key management will destroy all ownership data in PlatformOwners"""

    @abstractmethod
    def _get_platforms(self) -> list[Platform]:
        """Get platfrom data from PlatformInfo table"""

    @abstractmethod
    def get_user_subscriptions(self, user_id: str) -> list:
        """Get the list of user's subscriptions"""

class SQLiteDatabaseAccess(DatabaseAccess):
    """Controls access to database"""

    def __init__(self, database_file: str):
        self.database = database_file
        self.admin_ids = self._get_admin_list()
        self.platforms = self._get_platforms()

    def make_cursor(self, connection: Connection) -> Cursor:
        """Make a new cursor for the SQLite connection"""
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        return cursor

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
        if not self.get_owner_platforms(user_id):
            raise OwnerNotInTable(message=f"User ID '{user_id}' was not found in the Owner table.")

    def _add_owner(self, user_id: str, name: str, email: str):
        """Add user to Owners table"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('INSERT INTO Owners (UserId, UserName, UserEmail) VALUES (:user_id, :user_name, :user_email)', {'user_id':user_id, 'user_name':name, 'user_email': email})

    def delete_owner(self, user_id: str):
        """Delete user from Owners table. Foreign key management will destroy all ownership data in PlatformOwners"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('DELETE FROM Users WHERE UserId=:userId', {'userId' : user_id})

    def _get_platforms(self) -> dict[str, Platform]:
        """Get list of all platforms in database"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute('SELECT Platform, IdString, ChannelId FROM PlatformInfo')
            platforms = cur.fetchall()

        platform_list = {}
        for platform_row in platforms:
            platform_id, description, channel_id = platform_row
            platform_list[platform_id] = Platform(rom_family=platform_id, description=description, slack_channel=channel_id)

        return platform_list

    def get_user_subscriptions(self, user_id: str) -> list:
        """Get a list of user's subscriptions"""
        with sqlite3.connect(self.database) as conn:
            cur = self.make_cursor(conn)
            cur.execute("SELECT Platform FROM Subscriptions WHERE User_Id=:userId", {'userId': user_id})
            subs = cur.fetchall()
        return [platform for platform, in subs]

class OwnerNotInTable(Exception):
    """Customer exception for when a user is registered as an owner,
        but does not have an entry in the Owners table"""
    def __init__(self, message="Could not find user in Owners"):
        self.message = message
        super().__init__(message)

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
