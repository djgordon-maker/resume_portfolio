'''
Functions to interface with the user and status information
in the social network project
'''
from datetime import date
import logging
import csv
import users
import user_status

today = date.today()
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FILENAME = f"log_{today.strftime('%m_%d_%Y')}.log"
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler(FILENAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def init_user_collection():
    '''
    Creates and returns a new instance
    of UserCollection
    '''
    logger.info('Creating a new UserCollection')
    return users.UserCollection()


def init_status_collection():
    '''
    Creates and returns a new instance
    of UserStatusCollection
    '''
    logger.info('Createing a new UserStatusCollection')
    return user_status.UserStatusCollection()


def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    logger.debug('Entering load_users(%s, %s)', filename, user_collection)
    if not filename.endswith('.csv'):
        logger.error('User files must be in csv format')
        return False
    with open(filename, newline='') as userfile:
        logger.info('Loading users from %s', filename)
        data = csv.reader(userfile)
        next(data)  # Eat header data
        for row in data:
            # There should be four parameters
            if len(row) != 4:
                logger.error('Users need four parameters')
                return False
            # Empty strings, 0, and None are all considered empty fields
            for item in row:
                if not item:
                    logger.error('Users can not have empty fields')
                    return False  # I'm inclinded to raise a ValueError here
            # Should only be called with four non-empty parameters
            logger.debug('Calling add_user(%s)', row)
            user_collection.add_user(*row)
    logger.debug('load_users() returns true')
    return True


def save_users(filename, user_collection):
    '''
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    '''
    header = ['USER_ID', 'EMAIL', 'NAME', 'LASTNAME']
    if not filename.endswith('.csv'):
        logger.error('User files must be in csv format')
        return False
    with open(filename, 'w', newline='') as userfile:
        logger.info('Saving users to %s', filename)
        writer = csv.writer(userfile)
        writer.writerow(header)
        for user in user_collection.database.values():
            user_data = [user.user_id, user.email, user.user_name,
                         user.user_last_name]
            writer.writerow(user_data)
    return True


def load_status_updates(filename, status_collection):
    '''
    Opens a CSV file with status data and
    adds it to an existing instance of
    UserStatusCollection

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    if not filename.endswith('.csv'):
        logger.error('UserStatus files must be in csv format')
        return False
    with open(filename, newline='') as statusfile:
        logger.info('Saving statuses to %s', filename)
        data = csv.reader(statusfile)
        next(data)  # Eat header data
        for row in data:
            # There should be three parameters
            if len(row) != 3:
                logger.error('UserStatus needs three parameters')
                return False
            # Empty strings, 0, and None are all considered empty fields
            for item in row:
                if not item:
                    logger.error('UserStatus can not have empty fields')
                    return False  # I'm inclinded to raise a ValueError here
            # Should only be called with four non-empty parameters
            status_collection.add_status(*row)
    return True


def save_status_updates(filename, status_collection):
    '''
    Saves all statuses in status_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    '''
    header = ['STATUS_ID', 'USER_ID', 'STATUS_TEXT']
    if not filename.endswith('.csv'):
        logger.error('UserStatus files must be in csv format')
        return False
    with open(filename, 'w', newline='') as statusfile:
        logger.info('Saving statuses to %s', filename)
        writer = csv.writer(statusfile)
        writer.writerow(header)
        for status in status_collection.database.values():
            status_data = [status.status_id, status.user_id,
                           status.status_text]
            writer.writerow(status_data)
    return True


def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    logger.info('Adding a new User')
    return user_collection.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    logger.info('Updating an User')
    return user_collection.modify_user(
        user_id, email, user_name, user_last_name)


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    logger.info('Deleting an User')
    return user_collection.delete_user(user_id)


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    '''
    logger.info('Searching for an User')
    user = user_collection.search_user(user_id)
    if user.user_id:
        return user
    return None


def add_status(user_id, status_id, status_text, status_collection):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    logger.info('Adding an UserStatus')
    return status_collection.add_status(status_id, user_id, status_text)


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    logger.info('Updating an UserStatus')
    return status_collection.modify_status(status_id, user_id, status_text)


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    logger.info('Deleting an UserStatus')
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    logger.info('Searching for an UserStatus')
    status = status_collection.search_status(status_id)
    if status.status_id:
        return status
    return None
