#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from bson.objectid import ObjectId
from pymongo import UpdateOne
import showlog
import pymongo
import time
import copy
import envx
silence_default = True


def make_con_info(
        env_file_name: str = 'mongo.env'
):
    # ---------------- 固定设置 ----------------
    inner_env = envx.read(file_name=env_file_name)
    con_info = {
        "host": inner_env['host'],
        "port": int(inner_env.get('port', '27017')),
        "username": inner_env.get('username', 'root'),
        "password": inner_env['password']
    }
    # ---------------- 固定设置 ----------------
    return con_info


class Basics:
    """
    这是一个封装了mongodb基础方法的类，方便快捷使用
    """
    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str,
            db: str = None,
            collection: str = None
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        # self.password = parse.quote(password)  # 针对pymongo==4.0.1的更新
        self.db = db
        self.collection = collection
        if self.username is None and self.password is None:
            self.connect_str = 'mongodb://{}:{}/'.format(self.host, self.port)
        elif len(self.username) == 0 and len(self.password) == 0:
            self.connect_str = 'mongodb://{}:{}/'.format(self.host, self.port)
        else:
            self.connect_str = 'mongodb://{}:{}@{}:{}/'.format(self.username, self.password, self.host, self.port)
        self.client = pymongo.MongoClient(self.connect_str)

    def insert(
            self,
            values: list,
            db: str = None,
            collection: str = None
    ) -> object:
        # 增，values 为一个list
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        if len(values) == 0:
            return
        if len(values) == 1:
            return my_collection.insert_one(values[0])
        else:
            return my_collection.insert_many(values)

    def update(
            self,
            values: list,
            db: str = None,
            collection: str = None,
            query: dict = None
    ) -> object:
        # 改（单个）
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        while True:
            try:
                my_db = self.client[query_db]
                break
            except:
                showlog.warning('连接错误，正在重连...')
                time.sleep(1)
        my_collection = my_db[query_collection]
        set_values = {"$set": values[0]}
        return my_collection.update(query, set_values, True)

    def upsert(
            self,
            values: list,  # [{'value': 1}, {'value': 2}]
            db: str = None,
            collection: str = None,
            query_keys: list = None  # ['value']
    ) -> object:
        # 改（批量）
        """
        这是针对多条数据的批量插入/更新方法
        主键在query_keys参数设定，作为主键名列表，将会根据设定的主键规则去执行
        """
        if len(values) == 0:
            return
        else:
            pass

        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        while True:
            try:
                my_db = self.client[query_db]
                break
            except:
                showlog.warning('连接错误，正在重连...')
                time.sleep(1)
        my_collection = my_db[query_collection]

        arr = list()  # 初始化一个空列表
        for line in values:
            query_dict = dict()
            if query_keys is None:
                pass
            else:
                for query_key in query_keys:
                    query_data = line.get(query_key)
                    if query_data is not None:
                        query_dict[query_key] = query_data
                    else:
                        continue
            one = UpdateOne(filter=copy.deepcopy(query_dict), update={"$set": copy.deepcopy(line)}, upsert=True)
            arr.append(one)
        return my_collection.bulk_write(arr)

    def update_many(
            self,
            values: list,
            db: str = None,
            collection: str = None,
            query: dict = None
    ) -> object:
        # 改（批量）
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        set_values = {"$set": values[0]}
        return my_collection.update_many(query, set_values, True)

    def delete_key(
            self,
            key_name: str,
            db: str = None,
            collection: str = None,
            query: dict = None
    ) -> object:
        # 改-删除
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        set_values = {"$unset": {key_name: None}}
        return my_collection.update(query, set_values, True)

    def delete_one(
            self,
            db: str = None,
            collection: str = None,
            query: dict = None
    ) -> object:
        # 删，只删1条
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        if query is None:
            return
        else:
            my_db = self.client[query_db]
            my_collection = my_db[query_collection]
            return my_collection.delete_one(query)

    def delete_many(
            self,
            db: str = None,
            collection: str = None,
            query: dict = None
    ) -> object:
        # 删，删除所有满足条件的记录
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        if query is None:
            return
        else:
            my_db = self.client[query_db]
            my_collection = my_db[query_collection]
            return my_collection.delete_many(query)

    def insert_or_update(
            self,
            values: list,
            db: str = None,
            collection: str = None,
            query: dict = None
    ) -> object:
        # 改，当前只支持单条数据操作
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        if query is None:
            # 无查询语句，直接插入
            self.insert(values, db=query_db, collection=query_collection)
        else:
            # 更新
            find_res, find_count = self.find(query=query, db=db, collection=collection)
            if len(find_res) == 0:
                # 未查询到数据，直接插入
                self.insert(values, db=query_db, collection=query_collection)
            else:
                set_values = {"$set": values[0]}
                return my_collection.update(query, set_values, True)

    def find_db_list(
            self
    ) -> object:
        """
        查询db列表
        """
        my_db = self.client.list_database_names()
        return my_db

    def find(
            self,
            query: dict = None,
            db: str = None,
            collection: str = None,
            show_setting: dict = None,
            sort_setting: list = None,  # 注意在python里是list，例如[('aa', 1)]
            limit_num: int = None,
            skip_num: int = None
    ) -> object:
        # 查-多条
        """
        按照查询语句查找，内置将查询结果提取到list里面
        my_query = {'_id': 'balabala'}
        show_setting = {'_id': 0}  不显示_id，显示就为1，注意为dict格式，最好新建dict
        sort_setting = {'age': 1} 1正序 -1倒序
        query={} 表示查询所有数据
        """
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        if query is None:
            query = {}
        else:
            pass
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        if show_setting is None:
            if sort_setting is None:
                if limit_num is None:
                    if skip_num is None:
                        my_doc = my_collection.find(query)
                    else:
                        my_doc = my_collection.find(query).skip(skip_num)
                else:
                    if skip_num is None:
                        my_doc = my_collection.find(query).limit(limit_num)
                    else:
                        my_doc = my_collection.find(query).limit(limit_num).skip(skip_num)
            else:
                if limit_num is None:
                    if skip_num is None:
                        my_doc = my_collection.find(query).sort(sort_setting)
                    else:
                        my_doc = my_collection.find(query).sort(sort_setting).skip(skip_num)
                else:
                    if skip_num is None:
                        my_doc = my_collection.find(query).sort(sort_setting).limit(limit_num)
                    else:
                        my_doc = my_collection.find(query).sort(sort_setting).limit(limit_num).skip(skip_num)
        else:
            if sort_setting is None:
                if limit_num is None:
                    if skip_num is None:
                        my_doc = my_collection.find(query, show_setting)
                    else:
                        my_doc = my_collection.find(query, show_setting).skip(skip_num)
                else:
                    if skip_num is None:
                        my_doc = my_collection.find(query, show_setting).limit(limit_num)
                    else:
                        my_doc = my_collection.find(query, show_setting).limit(limit_num).skip(skip_num)
            else:
                if limit_num is None:
                    if skip_num is None:
                        my_doc = my_collection.find(query, show_setting).sort(sort_setting)
                    else:
                        my_doc = my_collection.find(query, show_setting).sort(sort_setting).skip(skip_num)
                else:
                    if skip_num is None:
                        my_doc = my_collection.find(query, show_setting).sort(sort_setting).limit(limit_num)
                    else:
                        my_doc = my_collection.find(query, show_setting).sort(sort_setting).limit(limit_num).skip(skip_num)
        res_list = list()
        for doc in my_doc:
            res_list.append(doc)
        res_count = my_doc.count()
        if res_count:
            return res_list, my_doc.count()
        else:
            return res_list, 0

    def find_page(
            self,
            db: str = None,
            collection: str = None,
            query: dict = None,
            previous_tag: str = '_id',
            previous_value=None,  # 非强制类型，str/int
            where_str: str = '$gt',
            show_setting: dict = None,
            sort_setting: list = [('_id', -1)],  # 注意在python里是list，例如[('aa', 1)]，1（升序），-1（降序）
            limit_num: int = 10
    ) -> object:
        """
        提供翻页查询功能，按照上一个位置向后翻页
        条件查询：
            $lt <
            $lte <=
            $gt >
            $gte >=
        """
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection

        if previous_tag == '_id':
            if query is None:
                if previous_value is None:
                    query = {}
                else:
                    query = {previous_tag: {where_str: ObjectId(previous_value)}}
            else:
                if previous_value is None:
                    query = {}
                else:
                    query[previous_tag] = {where_str: ObjectId(previous_value)}
        else:
            if query is None:
                if previous_value is None:
                    query = {}
                else:
                    query = {previous_tag: {where_str: previous_value}}
            else:
                if previous_value is None:
                    query = {}
                else:
                    query[previous_tag] = {where_str: previous_value}
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        if show_setting is None:
            if sort_setting is None:
                my_doc = my_collection.find(query).limit(limit_num)
            else:
                my_doc = my_collection.find(query).sort(sort_setting).limit(limit_num)
        else:
            if sort_setting is None:
                my_doc = my_collection.find(query, show_setting).limit(limit_num)
            else:
                my_doc = my_collection.find(query, show_setting).sort(sort_setting).limit(limit_num)
        res_list = list()
        for doc in my_doc:
            res_list.append(doc)
        return res_list, my_doc.count()

    def find_random(
            self,
            db: str = None,
            collection: str = None,
            num: int = 1
    ) -> list:
        # 随机抽取指定量的数据
        """
        按照查询语句查找，内置将查询结果提取到list里面
        my_query = {'_id': 'balabala'}
        """
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        my_doc = my_collection.aggregate([{'$sample': {'size': num}}])
        res_list = list()
        for doc in my_doc:
            res_list.append(doc)
        return res_list

    def collection_records(
            self,
            query: dict = None,
            db: str = None,
            collection: str = None
    ) -> int:
        # 查询collection的文档数量
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection
        my_db = self.client[query_db]
        my_collection = my_db[query_collection]
        if query is None:
            collection_count = my_collection.find().count()
        else:
            collection_count = my_collection.find(query).count()
        return collection_count

    def get_page_data(
            self,
            query: dict = None,
            db: str = None,
            collection: str = None,
            show_setting: dict = None,
            sort_setting: list = None,
            previous_tag: str = None,
            page_size: int = 10,
            page: int = 1,
            _id: str = None
    ) -> object:
        """
        获取某页的数据
        """
        if db is None:
            query_db = self.db
        else:
            query_db = db
        if collection is None:
            query_collection = self.collection
        else:
            query_collection = collection

        if _id is None:
            # 不按前序步骤标记翻页，按照最新页翻页
            find_res, find_count = self.find(
                query=query,
                db=query_db,
                collection=query_collection,
                show_setting=show_setting,
                sort_setting=sort_setting,
                limit_num=page_size,
                skip_num=(page - 1) * page_size
            )
            res_new_list = list()
            for each_find in find_res:
                if each_find.get('_id') is not None:
                    each_find['_id'] = str(each_find.get('_id'))
                res_new_list.append(each_find)
            return res_new_list, find_count
        else:
            # 从指定位置向后翻页，先按照_id找到排序字段的值，然后按照这个序列翻页继续查询
            find_record, find_count = self.find(
                query={'_id': ObjectId(_id)},
                db=query_db,
                collection=query_collection,
                show_setting=show_setting
            )
            if len(find_record) == 0:
                return [], 0
            else:
                previous_value = find_record[0][previous_tag]
                find_res, find_count = self.find_page(
                    query=query,
                    db=query_db,
                    collection=query_collection,
                    show_setting=show_setting,
                    sort_setting=sort_setting,
                    previous_tag=previous_tag,
                    previous_value=previous_value,
                    limit_num=page_size
                )
                res_new_list = list()
                for each_find in find_res:
                    if each_find.get('_id') is not None:
                        each_find['_id'] = str(each_find.get('_id'))
                    res_new_list.append(each_find)
                return res_new_list, find_count


def safe_get_records(
        query: dict = None,
        db: str = None,
        collection: str = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------

    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response = mongo_basics.collection_records(
                query=query,
                db=db,
                collection=collection
            )
            return response
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def safe_find(
        query: dict = None,
        db: str = None,
        collection: str = None,
        show_setting: dict = None,
        sort_setting: list = None,  # 注意在python里是list，例如[('aa', 1)]
        limit_num: int = None,
        skip_num: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response, response_count = mongo_basics.find(
                query=query,
                db=db,
                collection=collection,
                show_setting=show_setting,
                sort_setting=sort_setting,
                limit_num=limit_num,
                skip_num=skip_num
            )
            return response
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def safe_find_page(
        db: str = None,
        collection: str = None,
        query: dict = None,
        previous_tag: str = None,
        previous_value: str = None,
        where_str: str = '$gt',
        show_setting: dict = None,
        sort_setting: list = [('_id', 1)],  # 注意在python里是list，例如[('aa', 1)]
        limit_num: int = 10,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response, response_count = mongo_basics.find_page(
                db=db,
                collection=collection,
                query=query,
                previous_tag=previous_tag,
                previous_value=previous_value,
                where_str=where_str,
                show_setting=show_setting,
                sort_setting=sort_setting,
                limit_num=limit_num
            )
            return response
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def safe_find_page_by_num(
        db: str = None,
        collection: str = None,
        query: dict = None,
        show_setting: dict = None,
        sort_setting: list = [('_id', 1)],  # 注意在python里是list，例如[('aa', 1)]
        previous_tag: str = None,
        page_size: int = 20,
        page: int = 1,
        _id: str = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    """
    按页码获取数据
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response, response_count = mongo_basics.get_page_data(
                db=db,
                collection=collection,
                query=query,
                show_setting=show_setting,
                sort_setting=sort_setting,
                previous_tag=previous_tag,
                page_size=page_size,
                page=page,
                _id=_id
            )
            return response, response_count
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def safe_insert(
        values: list,
        db: str = None,
        collection: str = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response = mongo_basics.insert(
                values=values,
                db=db,
                collection=collection
            )
            return response
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def safe_upsert(
        values: list,
        db: str = None,
        collection: str = None,
        query_keys: list = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response = mongo_basics.upsert(
                values=values,
                db=db,
                collection=collection,
                query_keys=query_keys
            )
            return response
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def safe_delete_one(
        db: str = None,
        collection: str = None,
        query: dict = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    """
    删除一条数据
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response = mongo_basics.delete_one(
                db=db,
                collection=collection,
                query=query
            )
            return response
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def safe_delete_many(
        db: str = None,
        collection: str = None,
        query: dict = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    """
    删除满足条件的所有数据
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                host=inner_host,
                port=inner_port,
                username=inner_username,
                password=inner_password,
                db=inner_db,
                collection=inner_collection
            )
            response = mongo_basics.delete_many(
                db=db,
                collection=collection,
                query=query
            )
            return response
        except ConnectionError:
            showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            showlog.error('未知错误')
            time.sleep(1)


def quick_save_log(
        values: list,
        db: str = 'log',
        collection: str = None,
        add_platform_info: bool = False,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'mongo.env',
        # silence: bool = silence_default
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(env_file_name=env_file_name)
    else:
        pass
    inner_host = con_info.get('host')
    inner_port = con_info.get('port')
    inner_username = con_info.get('username')
    inner_password = con_info.get('password')
    if db is None:
        inner_db = db
    else:
        inner_db = None
    if collection is None:
        inner_collection = collection
    else:
        inner_collection = None
    # ---------------- 固定设置 ----------------
    mongo_basics = Basics(
        host=inner_host,
        port=inner_port,
        username=inner_username,
        password=inner_password,
        db=inner_db,
        collection=inner_collection
    )
    response = mongo_basics.insert(
        values=values,
        db=db,
        collection=collection
    )
    return response
