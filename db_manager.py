import sqlite3

build_db = sqlite3.connect('build_database.db')
build_cursor = build_db.cursor()

#Owner table indexes
ONWER_USER_ID = 0 
OWNER_USER_EMAIL = 1
OWNER_PLATFORMS = 2

class DatabaseError(Exception):
    pass

class UserAlreadyOwner(Exception):
    def __init__(self, user_id, platform, message=''):
        self.message = f'User ({user_id}) is already an owner of {platform}'
        super().__init__(self.message)

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

        #list of platforms owned by a user; can be empty
        self.owned_platforms = self.get_owner_platforms()

    def get_owner_platforms(self):
        """Get an owner from the database.

        Returns None if user is not found.
        """
        db_owner = self.find_user()
        if db_owner == None:
            return []
        else:
            _, _, platforms = db_owner
            return platforms[OWNER_PLATFORMS].split(', ')

    def find_user(self):
        """Get an owner from the database.

        Returns None if user is not found.
        """
        build_cursor.execute('SELECT * FROM owners WHERE User_id=:user_id AND User_email=:email', {'user_id':self.name, 'email':self.email})
        return build_cursor.fetchone()

    def register_owner(self, platform):
        """Registers a user as an owner of a platform.

        If a user is already registered then an UserAlreadyOwner exception
        will be raised.
        """
        owner = self.find_user()

        print(owner)
        if owner == None:
            print (f'User {self.name} ({self.email}) not found, adding to database')
            with build_db:
                build_cursor.execute('INSERT INTO owners VALUES (:user_id, :user_email, :platform)',{'user_id':self.name, 'user_email':self.email, 'platform': platform})
        else:
            if platform not in self.owned_platforms:
                new_plat_list = self.owned_platforms + f', {platform}'
                print(f'Updating ({self.name}) to have new platform ownership ({new_plat_list})')
                with build_db:
                    build_cursor.execute('UPDATE owners SET Platforms=:platforms WHERE User_id=:user_id AND User_email=:user_email',{'user_id': self.name, 'user_email': self.email, 'platforms': new_plat_list} )
                self.owned_platforms = new_plat_list
            else:
                raise UserAlreadyOwner(user, platform)

    def verify_owner(self, platform):
        """Returns True or False based on if the user is an owner of
        a given platform.
        """
        if platform in self.owned_platforms:
            return True
        else:
            return False

class BuildMessage:
    def __init__(self,id):
        pass

    def store_build_message(self):
        pass

    def get_build_message(self, platform, rom_version):
        pass

if(__name__ == "__main__"):
    demo_owners = [ ('Jack', 'jack.tay.little@hpe.com', 'H10'),
                    ('Joe',  'joe@hpe.com', 'U46')]
    for owner in demo_owners:
        user_id, user_email, platforms = owner
        user = User(user_id, user_email)
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
