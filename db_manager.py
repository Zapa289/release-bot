import sqlite3
import slack
import os

build_db = sqlite3.connect('build_database.db')
build_cursor = build_db.cursor()
build_cursor.execute("PRAGMA foreign_keys = ON")

client = slack.WebClient(token=os.environ['SLACKBOT_TOKEN'])

#Owner table indexes
# ONWER_USER_ID = 0 
# OWNER_USER_EMAIL = 1
# OWNER_PLATFORMS = 2

class UnauthorizedAction(Exception):
    def __init__(self, message='You do not have permisson to do that'):
        super().__init__(self.message)

class UserAlreadyOwner(Exception):
    def __init__(self, user_id, platform, message=''):
        self.message = f'User ({user_id}) is already an owner of {platform}'
        super().__init__(self.message)

class User:
    def __init__(self, userId):
        try:
            userInfo = client.users_info(user=userId)
        except slack.errors.SlackApiError:
            pass

        userProfile = userInfo.get('profile', "")

        self.userId = userInfo.get('id')
        self.name = userProfile.get("real_name", "")
        self.email = userProfile.get("email", "")

        self.is_admin  = self._get_admin()

        #list of platforms owned by a user; can be empty
        self.get_owner_platforms()

    def get_owner_platforms(self):
        """Get a list of all platforms owned by a user.

        Returns [] if none.
        """
        build_cursor.execute('SELECT Platform FROM PlatformOwners WHERE UserId=:user_id', {'user_id':self.userId})
        self.owned_platforms = [plat[0] for plat in build_cursor.fetchall()]
        return self.owned_platforms


    # def _find_user(self):
    #     """Get an owner from the database.

    #     Returns None if user is not found.
    #     """
    #     build_cursor.execute('SELECT UserId, UserName, UserEmail FROM Owners WHERE UserId=:user_id', {'user_id':self.userId})
    #     return build_cursor.fetchone()
        
    def _get_admin(self):
        """Returns True if user exists in admins table, otherwise false
        """
        build_cursor.execute('SELECT AdminId FROM Admins WHERE AdminID=:user_id', {'user_id':self.userId})
        return False if build_cursor.fetchone() == None else True

    def register_owner(self, user, platform):
        """Registers a user as an owner of a platform. Admins are implied
        owners of all platforms.

        If a user is already registered then an UserAlreadyOwner exception
        will be raised.
        """
        if self.is_admin:
            # Admin
            if user.owned_platforms == []:
                # Add new user to the User table
                with build_db:
                    try:
                        build_cursor.execute('INSERT INTO Users (UserId, UserName, UserEmail) VALUES (:user_id, :user_name, :user_email)', {'user_id':user.userId, 'user_name':user.name, 'user_email': user.email})
                    except sqlite3.IntegrityError:
                        pass
                user.owned_platforms = user.owned_platforms.append(platform)

            # Add platform and user to PlatformOwners table
            with build_db:
                build_cursor.execute('INSERT INTO PlatformOwners (Platform, UserId) VALUES ( ?, ?)', (platform, user.userId))
        else:
            # non-admin
            pass

        # if not self.owned_platforms:
        #     print (f'User {self.name} ({self.email}) not found, adding to database')
        #     with build_db:
        #         build_cursor.execute('INSERT INTO owners VALUES (:user_id, :user_email, :platform)',{'user_id':self.name, 'user_email':self.email, 'platform': platform})
        # else:
        #     if platform not in self.owned_platforms:
        #         new_plat_list = self.owned_platforms + f', {platform}'
        #         print(f'Updating ({self.name}) to have new platform ownership ({new_plat_list})')
        #         with build_db:
        #             build_cursor.execute('UPDATE owners SET Platforms=:platforms WHERE User_id=:user_id AND User_email=:user_email',{'user_id': self.name, 'user_email': self.email, 'platforms': new_plat_list} )
        #         self.owned_platforms = new_plat_list
        #     else:
        #         raise UserAlreadyOwner(user, platform)

    def verify_owner(self, platform):
        """Returns True or False based on if the user is an owner of
        a given platform.
        """
        return True if platform in self.owned_platforms else False

        # if platform in self.owned_platforms:
        #     return True
        # else:
        #     return False

    def delete_user(self, user):
        """Delete User from database.
        
        Will destroy all records in PlatformOwners belonging to the User"""
        if not self.is_admin:
            raise UnauthorizedAction(message=f'User {self.name} (user ID : {self.userId}) does not have permission to delete a user') 

        with build_db: 
            build_cursor.execute('DELETE FROM Users WHERE UserId=:userId', {'userId' : user.userId})
        

def  find_platform(platform):
    """Find a platform in PlatformInfo table
    Return True/False that it exists"""
    build_cursor.execute('SELECT Platform FROM PlatformInfo WHERE Platform=?', (platform,))
    return False if build_cursor.fetchone() == None else True

class BuildMessage:
    def __init__(self,id):
        pass

    def _store_build_message(self):
        pass

    def _get_build_message(self, platform, rom_version):
        pass

if(__name__ == "__main__"):
    demo_owners = [ ('Jack', 'jack.tay.little@hpe.com', 'H10'),
                    ('Joe',  'joe@hpe.com', 'U46')]
    for owner in demo_owners:
        user_id, user_email, platforms = owner
        user = User(user_id)
        try:
            is_owner = user.verify_owner(platforms)
            print(is_owner)
        except UserAlreadyOwner:
            print(f'User ({user_id}) already in data base for platform "{platforms}"')




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
