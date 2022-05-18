import sqlite3
import aiosqlite


class DataTool:
    """
    Singleton class to interactions with database
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, db_name):
        self.__base: aiosqlite.core.Connection
        self.__cursor: aiosqlite.Cursor

        self.__db_name, self.__base, self.__cursor = db_name, None, None
        self.__create_tables()

    def __create_tables(self):
        with sqlite3.connect(self.__db_name) as db:
            db.execute(
                'CREATE TABLE IF NOT EXISTS {}(id PRIMARY KEY, readable_channels, forwarding_group, activity)'
                .format('data')
            )
            db.execute(
                'CREATE TABLE IF NOT EXISTS {}(id PRIMARY KEY, name, subscribed_users)'.format('groups_names'))
            db.commit()
            print('create table')

    async def __connect(self):
        if (self.__base is None) and (self.__cursor is None):
            self.__base: aiosqlite.core.Connection = await aiosqlite.connect(self.__db_name)
            self.__cursor: aiosqlite.core.Cursor = await self.__base.cursor()
            print('data connect is success')

    async def add_to_data(self,
                          user_id: int,
                          readable_channels: set | tuple | list | None = None,
                          forwarding_group: int | None = None,
                          activity: bool = True
                          ) -> bool:

        await self.__connect()

        activity = int(activity)
        if readable_channels is not None:
            readable_channels = list(readable_channels)
            readable_channels = '_'.format(readable_channels)
        try:

            await self.__cursor.execute('INSERT INTO data VALUES(?, ?, ?, ?)',
                                        (user_id, readable_channels, forwarding_group, activity))
            await self.__base.commit()
            return True
        except aiosqlite.IntegrityError:
            return False

    async def get_activity(self, user_id: int) -> bool:
        """Return current user activity"""
        await self.__connect()

        activity = await self.__cursor.execute('SELECT activity FROM data WHERE id == ?', (user_id,))
        activity = await activity.fetchone()
        activity = activity[0]
        return bool(activity)

    async def change_activity(self, user_id: int) -> bool:
        """Change user activity and return current user activity"""
        await self.__connect()
        if await self.get_activity(user_id=user_id):
            await self.__cursor.execute('UPDATE data SET activity == ? WHERE id = ?', (0, user_id))
            await self.__base.commit()
            return False
        else:
            await self.__cursor.execute('UPDATE data SET activity == ? WHERE id = ?', (1, user_id))
            await self.__base.commit()
            return True

    async def get_readable_channels(self, user_id: int) -> tuple | None:
        """
        Return user readable channels as tuple of channels id
        if user does not read any chanel, then return None
        Elements in tuple are str
        """
        await self.__connect()

        channels = await self.__cursor.execute('SELECT readable_channels FROM data WHERE id == ?', (user_id,))
        channels = await channels.fetchone()
        if (channels is None) or (channels[0] is None):
            return None
        else:
            channels = channels[0].split('_')
            return tuple(channels)

    async def get_id_and_readable_channels(self):
        """
        :return: in dict{key: user_id, value: [readable_channels]}

        """
        await self.__connect()

        ids = await self.__cursor.execute(
            'SELECT id FROM data'
        )

        ids_channels = []
        ids = [i[0] for i in ids]
        for user_id in ids:
            channels = await self.get_readable_channels(user_id=user_id)
            if channels is None:
                continue

            channels = list(channels)
            id_channel = list()
            id_channel.append(user_id)
            id_channel.append(channels)

            ids_channels.append(id_channel)

        ids_channels = dict(ids_channels)
        return ids_channels

    async def clear_readable_channels(self, user_id: int):
        """Set user readable channels as None"""
        await self.__connect()

        readable_channels = await self.get_readable_channels(user_id=user_id)

        for channel in readable_channels:
            await self.__remove_subscriber(user_id=user_id, group_id=int(channel))

        await self.__cursor.execute('UPDATE data SET readable_channels == ? WHERE id == ?', (None, user_id))
        await self.__base.commit()

    async def add_chanel_to_readable_channels(self, user_id: int, channel_id: int) -> bool:
        """
        Add new chanel to user readable_channels
        :param user_id: user id
        :param channel_id: id channel to add
        :returns
        True: if chanel success added;
        False: if chanel already in readable_channels
        """
        await self.__connect()

        current_channels = await self.get_readable_channels(user_id=user_id)

        # if user has no readable channels just add new and return True
        if current_channels is None:
            channel_id = str(channel_id)

            await self.__cursor.execute('UPDATE data SET readable_channels == ? WHERE id == ?', (channel_id, user_id))
            await self.__base.commit()
            await self.__add_subscribers(user_id=user_id, group_id=int(channel_id))
            return True

        # check for chanel already in readable_channels
        if str(channel_id) in current_channels:
            return False

        current_channels = list(current_channels)
        current_channels.append(str(channel_id))
        current_channels = '_'.join(current_channels)

        await self.__cursor.execute('UPDATE data SET readable_channels == ? WHERE id == ?', (current_channels, user_id))
        await self.__base.commit()
        await self.__add_subscribers(user_id=user_id, group_id=int(channel_id))
        return True

    async def remove_chanel_from_readable_channels(self, user_id: int, chanel_id: int) -> bool:
        """
        Remove channel from user readable_channels in database
            :param user_id: user id
            :param chanel_id: id channel to remove
            :returns
            True: if channel remove success;
            False: not found channel in user readable_channels
        """
        await self.__connect()

        readable_channels = await self.get_readable_channels(user_id=user_id)
        chanel_id = str(chanel_id)

        if readable_channels is None:
            return False

        readable_channels = list(readable_channels)

        try:
            readable_channels.remove(chanel_id)

            if not readable_channels:
                await self.clear_readable_channels(user_id=user_id)
                await self.__remove_subscriber(user_id=user_id, group_id=int(chanel_id))
                return True
            else:
                readable_channels = '_'.join(readable_channels)

                await self.__cursor.execute(
                    'UPDATE data SET readable_channels == ? WHERE id == ?', (readable_channels, user_id)
                )
                await self.__base.commit()
                await self.__remove_subscriber(user_id=user_id, group_id=int(chanel_id))
            return True

        except ValueError:
            return False

    async def get_forwarding_group(self, user_id: int) -> int | None:
        """
        Return from bd user forwarding_group

        :return: id group in int: witch set like user forwarding group;
                 None: if user has not set group already
        """
        await self.__connect()

        forwarding_group = await self.__cursor.execute('SELECT forwarding_group FROM data WHERE id == ?', (user_id,))
        forwarding_group = await forwarding_group.fetchone()
        forwarding_group = forwarding_group[0]

        if forwarding_group is None:
            return forwarding_group

        return int(forwarding_group)

    async def clear_forwarding_group(self, user_id: int):
        """Set in db user forwarding_group as None"""
        await self.__connect()

        await self.__cursor.execute(
            'UPDATE data SET forwarding_group == ? WHERE id == ?', (None, user_id)
        )
        await self.__base.commit()

    async def set_forwarding_group(self, user_id: int, group_id) -> bool:
        """
        Set new group in bd to bot forwarding new posts

        :param user_id: User id
        :param group_id: Group id need to set as new forwarding group
        :returns: True: If success changed;
                  False: If new group already set as forwarding group
        """
        await self.__connect()

        current_group = await self.get_forwarding_group(user_id=user_id)

        if current_group == group_id:
            return False

        group_id = str(group_id)
        await self.__cursor.execute(
            'UPDATE data SET forwarding_group == ? WHERE id == ?', (group_id, user_id)
        )
        await self.__base.commit()
        return True

    async def add_to_groups_names(self, group_id: int, name: str, subscribed_users: list | None = None) -> bool:
        """
        Add new (id, name, subscribed_users) to table group_names in bd

        :param subscribed_users:
        :param group_id: group to add id
        :param name: group name
        :return: True: If group success added;
                 False: If group or id already id bd
        """
        await self.__connect()

        if subscribed_users is not None:
            subscribed_users = '_'.join(subscribed_users)

        try:
            await self.__cursor.execute('INSERT INTO groups_names VALUES(?, ?, ?)', (group_id, name, subscribed_users))
            await self.__base.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    async def get_group_name_by_id(self, group_id: int) -> str | None:
        """
        :return: group name as str, if no id in bd -> return None
        """
        await self.__connect()

        try:
            name = await self.__cursor.execute('SELECT name FROM groups_names WHERE id == ?', (group_id,))
            name = await name.fetchone()
            return name[0]
        except TypeError:
            return None

    async def get_grop_id_by_name(self, name: str) -> tuple | None:
        """
        :return: group ids in tuple, if no name in bd -> return None
        """
        await self.__connect()

        try:
            group_ids = await self.__cursor.execute('SELECT id FROM groups_names WHERE name == ?', (name,))
            group_ids = await group_ids.fetchall()
            ids = [i[0] for i in group_ids]
            ids = tuple(ids)
            return ids
        except TypeError:
            return None

    async def delete_from_data(self, user_id):
        await self.__connect()

        await self.__cursor.execute(
            'DELETE FROM data WHERE id == ?', (user_id,)
        )
        await self.__base.commit()

    async def delete_from_groups_name(self, group_id):
        await self.__connect()

        await self.__cursor.execute(
            'DELETE FROM groups_names WHERE id == ?', (group_id,)
        )
        await self.__base.commit()

    async def get_subscribers(self, group_id: int) -> tuple | None:
        """ return all users' id in int, who reading this group"""
        await self.__connect()

        subscribers = await self.__cursor.execute(
            'SELECT subscribed_users FROM groups_names WHERE id == ?', (group_id,)
        )
        subscribers = await subscribers.fetchone()
        if subscribers is None:
            return None
        else:
            subscribers = subscribers[0]

        if subscribers is None:
            return None
        else:
            subscribers = subscribers.split('_')
            subscribers = [int(user) for user in subscribers]
            return tuple(subscribers)

    async def __add_subscribers(self, user_id: int, group_id: int) -> bool:
        """
        Add user to group subscribers

        :param user_id: id user need to add
        :param group_id: id group user need subscribe
        :return: True: If user success added
                 False: If user already reading this channel
        """
        await self.__connect()

        subscribers = await self.get_subscribers(group_id=group_id)

        if subscribers is None:
            user_id = str(user_id)
            await self.__cursor.execute(
                'UPDATE groups_names SET subscribed_users == ? WHERE id == ?', (user_id, group_id)
            )
            await self.__base.commit()
            return True

        elif str(user_id) in subscribers:
            return False

        else:
            subscribers = list(subscribers)
            subscribers.append(str(user_id))
            subscribers = '_'.join(subscribers)

            await self.__cursor.execute(
                'UPDATE groups_names SET subscribed_users == ? WHERE id == ?', (subscribers, group_id)
            )
            await self.__base.commit()
            return True

    async def __remove_subscriber(self, user_id: int, group_id: int) -> bool:
        """
        Remove user id from subscribed_users in database

        :param user_id: User id need to remove
        :param group_id: Group id need to remove user id
        :return: True: If user id success removed
                 False: If not found user id in group subscribers
        """
        await self.__connect()

        subscribers = await self.get_subscribers(group_id=group_id)
        user_id = str(user_id)

        if subscribers is None:
            return False

        subscribers = list(subscribers)

        try:
            subscribers.remove(user_id)

            if not subscribers:
                await self.__cursor.execute(
                    'UPDATE groups_names SET subscribed_users == ? WHERE id == ?', (None, group_id)
                )
                await self.__base.commit()
                return True
            else:
                subscribers = '_'.join(subscribers)

                await self.__cursor.execute(
                    'UPDATE groups_names SET subscribed_users == ? WHERE id == ?', (subscribers, group_id)
                )
                await self.__base.commit()
            return True
        except ValueError:
            return False

    async def get_all_id_from_data(self) -> tuple:
        await self.__connect()

        ids = await self.__cursor.execute(
            'SELECT id FROM data'
        )
        ids = await ids.fetchall()
        ids = [i[0] for i in ids]
        ids = tuple(ids)
        return ids

    async def get_groups_names(self, in_dict: bool = False) -> list | dict:
        """
        :param in_dict: If true, return dict {key:group_id, value: name}
        """
        await self.__connect()

        bd = await self.__cursor.execute('SELECT * FROM groups_names')
        bd = await bd.fetchall()
        if in_dict:
            bd = dict(bd)
        return bd

    async def get_all_active_subscribers_and_forwarding_group(self, group_id: int) -> dict | None:
        """
        :return: dict where  key: int users_id whom active and subscribe group with id 'group_id';
                 value: user forwarding_group
                 If no users matching the conditions, return 'None'
        """
        await self.__connect()

        subscribers = await self.get_subscribers(group_id=group_id)
        if subscribers is None:
            return None

        subscriber_forwarding_group: dict = {}
        for sub_id in subscribers:
            if await self.get_activity(user_id=sub_id):
                forwarding_group = await self.get_forwarding_group(user_id=sub_id)
                subscriber_forwarding_group[sub_id] = forwarding_group

        return subscriber_forwarding_group
