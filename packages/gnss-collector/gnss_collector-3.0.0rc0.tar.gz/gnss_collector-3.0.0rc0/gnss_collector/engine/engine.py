# stdlilb python
import datetime
import asyncio
from asyncio import shield, wait_for
from tasktools.taskloop import TaskLoop
import time
import os
import traceback
import socket
import functools
import concurrent.futures
import multiprocessing as mp
import time
from functools import reduce
from pathlib import Path
# contrib @dpineda
from networktools.time import timestamp, now
from networktools.colorprint import gprint, bprint, rprint
from networktools.library import my_random_string
from basic_queuetools.queue import read_queue_gen
from dataprotocols import Gsof, Eryo
from data_rdb import Rethink_DBS
from orm_collector.manager import SessionCollector, object_as_dict
from networktools.library import check_type

from networktools.library import (pattern_value,
                                  fill_pattern, context_split,
                                  gns_loads, gns_dumps)
from networktools.time import gps_time, now

# Tasktools
from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out
from tasktools.scheduler import TaskScheduler
# GSOF Protocol
import multiprocessing
from .steps import (CollectSteps as CSteps, DBSteps, Logger, ORMSteps,
                    ControlActions)
from datetime import timedelta, datetime
# DBS Rethinkdb
from rethinkdb import RethinkDB
from rich import print
import sys 
from tblib import pickling_support
pickling_support.install()
# same module
from basic_logtools.filelog import LogFile as FileLog
from .subscribe import SubscribeData
from .message import MessageManager
# from .async_mongo import AsyncMongoDB
import itertools

rdb = RethinkDB()
import logging
# base settings
try:
    from .conf.settings import COMMANDS, groups, dirs

except:
    from conf.settings import COMMANDS, groups, dirs


def load_stations(server_name, datadb, log_path='~/log'):
    print("Obteniendo estaciones....", server_name, datadb)
    dbmanager = SessionCollector(
        log_path=log_path, 
        active='true', 
        server=server_name, 
        **datadb)
    u = dbmanager.get_station_data(server=server_name)
    print(u)
    dbmanager.close()
    return u


def load_databases(datadb, log_path='~/log'):
    print("Obteniendo datadb lista")
    dbmanager = SessionCollector(
        log_path=log_path, 
        **datadb)
    u = dbmanager.get_dbdata_data()
    print("Resultado...", u)
    dbmanager.close()
    return u


def active_server(server_name, datadb, log_path='~/log'):
    print("Activando server", server_name, datadb)
    dbmanager = SessionCollector(
        log_path=log_path, 
        **datadb)
    u = dbmanager.get_server_id(server_name)
    if u:
        dbmanager.active_server(u)
    dbmanager.close()
    return u


def deactive_server(server_name, datadb, log_path='~/log'):
    dbmanager = SessionCollector(log_path=log_path, **datadb)
    u = dbmanager.get_server_id(server_name)
    if u:
        dbmanager.deactive_server(u)
    dbmanager.close()
    return u


"""
Engine basic for collector
"""


class Aux:
    async def stop(self):
        pass


class Engine(TaskScheduler):
    """
    A class for data adquisition, receive meshttp://www.cursodeprogramacion.cl/sages from anageser and
    save data on db

    """
    log_manager = {}

    def __init__(self,
                 set_queue,
                 sleep_time,
                 est_by_proc,
                 stations,
                 dbtype,
                 protocol,
                 status_sta,
                 db_instances_sta,
                 status_conn,
                 db_data,
                 dump_list,
                 proc_tasks,
                 assigned_tasks,
                 free_ids,
                 wait,
                 inc_msg,
                 ids,
                 idd,
                 ipt,
                 idm,
                 ico,
                 changes,
                 gsof_timeout,
                 sta_init,
                 db_init,
                 db_connect,
                 status_tasks,
                 nproc,
                 idc,
                 rdb_address=None,
                 uin=8, *args, **kwargs):

        # init taskschduler
        self.server_name = kwargs.get('server', "atlas")
        self.log_path = Path(kwargs.get('log_path', '~/log'))
        self.timeout = kwargs.get("timeout", 5)
        self.datadb = kwargs.get("dbdata", {})        
        self.raise_timeout = kwargs.get("raise_timeout", False)
        args = []
        kwargs_extra = {
            'ipt': ipt,
            'ico': ico,
            'assigned_tasks': assigned_tasks,
            'nproc': nproc,
            'sta_init': sta_init
        }
        kwargs.update(kwargs_extra)
        super().__init__(*args, **kwargs)
        #
        self.sep = '|'
        self.rq = set_queue[0]
        self.queue_n2t = self.rq
        self.wq = set_queue[1]
        self.queue_t2n = self.wq
        self.queue_process = set_queue[2]
        self.queue_ans_process = set_queue[3]
        self.queue_db = set_queue[4]
        self.queue_log = set_queue[-1]
        self.time = sleep_time
        self.status_sta = status_sta
        self.status_tasks = status_tasks
        self.stations = stations
        self.dbtype = dbtype
        self.protocol = protocol
        self.instances = dict()
        self.db_instances_sta = db_instances_sta
        self.status_conn = status_conn
        self.db_data = db_data
        self.db_instances = dict()
        self.free_ids = free_ids
        self.wait = wait
        self.uin = uin
        self.folder = 'data'
        self.nproc = mp.cpu_count()
        # list of objects
        self.collect_objects = dict(
            GSOF=Gsof,
            ERYO=Eryo
        )
        self.database_objects = dict(
            RethinkDB=Rethink_DBS,
            #Mongo=AsyncMongoDB
        )
        self.dump_list = dump_list

        # LOAD DATA TO STATIONS
        self.tasks = dict()
        self.proc_tasks = proc_tasks
        self.status_tasks = status_tasks
        self.lnproc = est_by_proc
        self.inc_msg = inc_msg
        self.ids = ids
        self.idd = idd
        self.ipt = ipt
        self.ico = ico
        self.idm = idm
        self.changes = changes
        self.first_time = dict()
        self.gsof_timeout = gsof_timeout
        self.rethinkdb_address = rdb_address
        self.rethinkdb = {}
        self.rethinkdb_address = rdb_address
        self.idc = idc  # dict shared
        self.dt_criteria = kwargs.get('dt_criteria',3)
        self.db_init = db_init
        self.db_connect = db_connect
        # set the main task
        coros_callback_dict = {
            'run_task': self.process_data,
        }
        # must be in every new process ATENTION!
        self.message_manager = MessageManager(self)
        self.subscribe_data = SubscribeData(
            'collector_subscribe', self.queue_t2n)
        self.LOG_STA = check_type(os.environ.get('LOG_STA', False))
        ###############################################
        self.set_new_run_task(**coros_callback_dict)
        self.server = active_server(self.server_name, self.datadb)


    def set_datafolder(self, folder):
        """
        Set another, different, folder to save data
        """
        self.folder = folder

    def set_id(self, lista):
        """
        Defines a new id for stations, check if exists
        """
        ids = my_random_string(self.uin)
        while True:
            if ids not in lista:
                lista.append(ids)
                break
            else:
                ids = my_random_string(self.uin)
        return ids

    def set_ids(self):
        """
        Defines a new id for stations, check if exists
        """
        return self.set_id(self.ids)

    def set_idd(self):
        """
        Defines a new id for stations, check if exists
        """
        return self.set_id(self.idd)

    def set_ipt(self, ipt=""):
        """
        Defines a new id for relation process-collect_task, check if exists
        """
        if ipt:
            self.ipt.append(ipt)
        else:
            ipt = self.set_id(self.ipt) 
        return ipt

    def set_ico(self, ico):
        """
        Defines a new id for task related to collect data insice a worker, check if exists
        """
        if ico:
            self.ipt.append(ico)
        else:
            ico = self.set_id(self.ipt) 

        return ico

    def set_idm(self):
        """
        Defines a new id for relation incoming messages, check if exists
        """
        return self.set_id(self.idm)

    def load_stations(self):
        u = load_stations(self.server_name, self.datadb, log_path=self.log_path/"orm")  # ok
        for m in u:
            # print(m)
            keys = ['id', 'code', 'db', 'dblist', 'ECEF_X', 'ECEF_Y', 'protocol_host',
                    'ECEF_Z', 'port', 'protocol', 'host', 'dbname']
            try:
                station = dict(
                    id=m['id'],
                    code=m['st_code'],
                    name=m['st_name'],
                    ECEF_X=m['ecef_x'],
                    ECEF_Y=m['ecef_y'],
                    ECEF_Z=m['ecef_z'],
                    db=m['db_code'],
                    dblist=m['db_list'],
                    port=m['st_port'],
                    protocol=m['prt_name'],
                    protocol_host=m['protocol_host'],
                    host=m['st_host'],
                    on_db=True
                )
                (ids, sta) = self.add_station(**station)
                # print(station)
            except Exception as exc:
                raise exc

    def add_station(self, **sta):
        """
        Add station to list for data adquisition
        """
        try:
            keys = ['id',
                    'code',
                    'name',
                    'ECEF_X',
                    'ECEF_Y',
                    'ECEF_Z',
                    'host',
                    'port',
                    'interface_port',
                    'db',
                    'dblist',
                    'protocol',
                    'protocol_host',
                    'on_db',
                    'ipt']
            ids = self.set_ids()

            # if ids in self.enqueued:
            #     self.enqueued.remove(ids)
            # self.enqueued.add(ids)

            station = dict(ids=ids)

            for k in keys:
                if k in sta.keys():
                    if k == 'protocol':
                        station[k] = sta.get(k, 'None').upper()
                    else:
                        station[k] = sta.get(k, None)
                else:
                    if k == 'host':
                        station[k] = 'localhost'
                    elif k == 'port' or k == 'interface_port':
                        station[k] = 0
                    elif k in  [f'ECEF_{v}' for v in ("X", "Y", "Z")]:
                        station[k] = 0
                    else:
                        station[k] = None
            self.stations.update({ids: station})
            self.status_sta.update({ids: False})
            self.first_time.update({ids: True})
            return (ids, sta)
        except Exception as ex:
            raise ex

    def update_station(self, ids, **sta):
        """
        Add station to list for data adquisition
        """
        try:
            keys = ['id',
                    'code',
                    'name',
                    'ECEF_X',
                    'ECEF_Y',
                    'ECEF_Z',
                    'host',
                    'port',
                    'interface_port',
                    'db',
                    'dblist',
                    'protocol',
                    'protocol_host',
                    'on_db',
                    'ipt']
            station = dict(ids=ids)

            for k in keys:
                if k in sta.keys():
                    if k == 'protocol':
                        station[k] = sta.get(k, 'None').upper()
                    else:
                        station[k] = sta.get(k, None)
                else:
                    if k == 'host':
                        station[k] = 'localhost'
                    elif k == 'port' or k == 'interface_port':
                        station[k] = 0
                    elif k in  [f'ECEF_{v}' for v in ("X", "Y", "Z")]:
                        station[k] = 0
                    else:
                        station[k] = None
            self.stations.update({ids: station})
            self.status_sta.update({ids: False})
            self.first_time.update({ids: True})
            return (ids, sta)
        except Exception as ex:
            raise ex


    def get_stations_keys(self):
        return list(self.stations.keys())

    def load_databases(self):
        u = load_databases(self.datadb, log_path=self.log_path/"orm")
        # ok
        groups = {}
        for m in u:
            dbtype = m['type_name']
            kwargs = dict(
                id=m['id'],
                code=m['code'],
                path=m['path'],
                host=m['host'],
                port=m['port'],
                user=m['user'],
                passw=m['passw'],
                info=m['info'],
                type_name=m['type_name'],
                type_db=m['type_db'],
                url=m['url'],
                data_list=m['data_list'],
                dbname=m["dbname"].rstrip(),
                address=(m['host'], m['port']),
                log_path=self.log_path/"rdb",
                on_db=True)
            groups[(m["host"], m["port"])] = kwargs
        print("Different db destinies", len(groups), groups.keys())
        for opts in groups.values():
            self.new_datadb(dbtype, **opts)

    def new_datadb(self, dbtype, **kwargs):
        """
        Here you give the argument for every type engine for store data colected
        and instantiate the db for enable query on that
        """
        # generate a idd= database instance identifier
        try:
            keys = [
                'id',
                'user',
                'passw',
                'code',
                'host',
                'port',
                'name',
                'path',
                'data_list',
                'type_name',
                'dbname',
                'type_db,'
                'url',
                'info',
                'address',
                'on_db',
                'log_path']
            uin = 4
            idd = self.set_idd()
            db_data = dict(idb=idd, name=dbtype, args={})
            for k in keys:
                if k in keys:
                    if k in kwargs.keys():
                        db_data['args'][k] = kwargs[k]
                    else:
                        if k == 'localhost':
                            db_data['args'][k] = 'localhost'
                        elif k == 'port':
                            db_data['args'][k] = 0
                        else:
                            db_data['args'][k] = ''
            self.db_data[idd] = db_data
            return idd, db_data
        except Exception as ex:
            raise ex

    def mod_station(self, ids, key, value):
        """
        Modify some value in station info

        """
        if key in self.stations.get(ids).keys():
            self.stations[ids][key] = value

    def del_station(self, ids):
        """
        Delete a station from list
        """
        del self.stations[ids]
        del self.status_sta[ids]
        del self.status_conn[ids]
        del self.instances[ids]
        k = self.ids.index(ids)
        del self.ids[k]

    def save_db(self, dbmanager, tname, args):
        """
        Save data to tname with args
        """
        # TODO: actualizar la lista de campos port table
        # TODO: añadir serverinstance
        input_args = dict(
            station=[
                'code',
                'name',
                'position_x',
                'position_y',
                'position_z',
                'host',
                'port',
                'interface_port',
                'db',
                'protocol'],
            dbdata=[
                'code',
                'path',
                'host',
                'port',
                'user',
                'passw',
                'info',
                'dbtype'],
            dbtype=['typedb', 'name', 'url', 'data_list'],
            protocol=['name', 'red_url', 'class_name', 'git_url']
        )
        name_args = input_args[tname]
        my_args = []
        id_instance = None
        if dbmanager == None:
            dbmanager = SessionCollector()
            instance = object
            if tname == 'station':
                instance = dbmanager.station(**args)
            elif tname == 'dbdata':
                instance = dbmanager.dbdata(**args)
            elif tname == 'dbtype':
                instance = dbmanager.dbtype(**args)
            elif tname == 'protocol':
                instance = dbmanager.protocol(**args)
            id_instance = instance.id
            return id_instance

    def save_station(self, ids):
        """
        Save station to database
        """
        # check if exists
        # if exist get data and compare
        # then update
        # if not, save
        pass

    def drop_station(self, ids):
        """
        Delete station from database
        """
        # get id from station ids
        # delete on database
        pass

    def del_db(self, varlist):
        """
        Delete element from database identified by idx in varlist
        """
        pass
###############

    def add_sta_instance(self, ids, loop):
        """
        Crear la instancia que accederá a los datos
        a través del socket
        """
        station =  self.stations.get(ids)
        if station:
            protocol = self.stations[ids]['protocol']
            kwargs = self.stations[ids]
            self.stations[ids].update({'on_collector': True})
            kwargs['code'] = self.stations[ids]['code']
            kwargs['host'] = self.stations[ids]['protocol_host']
            kwargs['port'] = self.stations[ids]['port']
            kwargs['sock'] = None
            kwargs['timeout'] = self.gsof_timeout
            kwargs["raise_timeout"] = False
            kwargs['loop'] = loop
            kwargs['log_path'] = self.log_path/"protocols"
            instance = self.collect_objects[protocol](**kwargs)
            code = kwargs["code"]
            table_name = f"{code}_{protocol}"
            return instance, table_name

            # bprint(f"Instance ok {instance}")
            # # self.instances.update(
            # #     {ids: instance})
            # try:
            # code = self.stations[ids]['code']
            # code_db = self.stations[ids]['db']
            # idd = self.get_id_by_code('DBDATA', code_db)
            # args = []
            # # activate engine to save date:
            # if self.db_data[idd]['name'].upper() == 'TIMESERIE':
            #     # check if gsof
            #     folder = self.folder + "/" + idd
            #     args = [code, idd, folder, self.sep]
            # self.db_instances_sta[ids] = idd
            # self.first_time[ids] = True
            # self.sta_init[ids] = True
            # self.set_status_conn(ids, False)
            # gprint(f"Returning sta instance {instance}")
            # return instance
        else:
            print("No station")

    def set_status_sta(self, ids, value):
        if isinstance(value, bool):
            self.status_sta[ids] = value
            # True: connect to sta
            # False: maintain status_conn01

    def set_status_conn(self, ids, value):
        if isinstance(value, bool):
            self.status_conn[ids] = value
            # True: connected
            # False: unconnected

    def del_sta(self, ids):
        del self.instances[ids]
        del self.status_sta[ids]
        del self.status_conn[ids]
        del self.first_time[ids]
        # del self.db_instances[ids]
        del self.ids

    def get_tname(self, varname):
        assert isinstance(varname, str)
        if varname == 'STA' or varname == 'STATION':
            return 'station'
        elif varname == 'DB' or varname == 'DBDATA':
            return 'database'
        elif varname == 'PROT' or varname == 'PROTOCOL':
            return 'protocol'
        elif varname == 'DBTYPE':
            return 'dbtype'
        else:
            return None

    def get_id_by_code(self, varname, code):
        if varname == 'STATIONS':
            this_var = self.stations
            for k in this_var.keys():
                if this_var[k]['code'] == code:
                    return k

        elif varname == 'DBDATA':
            this_var = self.db_data
            # variable in function dbtype
            for k in this_var.keys():
                # code_r=''
                try:
                    if this_var[k]['args']['code'] == code:
                        return k
                except Exception as ex:
                    raise ex

    def get_var(self, varname):
        varin = ''
        if varname == 'STA':
            varin = self.stations
        elif varname == 'DB':
            varin = self.db_data
        else:
            varin = None
        return varin

    async def connect(self, ids):
        if self.status_sta[ids]:
            await self.instances[ids].connect()
            self.set_status_conn(ids, True)
            self.set_status_sta(ids, False)
            self.first_time[ids] = False

    async def stop(self, ipt, ids):
        if self.status_sta[ids]:
            icos = [ico_dict for ipt, ico_dict in self.assigned_tasks.items()]
            ico_list = []
            for ico_dict in icos:
                ico_list += [ico for ico, _ids in ico_dict.items()
                             if _ids == ids]
            for ico in ico_list:
                self.unset_sta_assigned(ipt, ico, ids)
                instance_obj = self.instances.get(ids, Aux())
                await instance_obj.stop()
                self.set_status_conn(ids, False)
                self.set_status_sta(ids, False)

    async def reset_station_conn(self, sta_insta, ids, idc):
        self.set_status_sta(ids, False)
        self.set_status_conn(ids, False)
        self.first_time[ids] = True       
        v = 1
        message = ""
        if idc:
            try:
                await sta_insta.close(idc)
                message = f"Station {sta_insta.station} closed at {idc}"
            except Exception as e:
                print("sta insta yet closed")
            except asyncio.TimeoutError as te:
                print("sta insta yet closed")
        return message, logging.INFO

    def connect_to_sta(self, ids):
        return self.sta_init[ids] and not self.status_conn[ids] and self.first_time[ids]

    def is_connected(self, ids):
        return self.sta_init[ids] and self.status_conn[ids] and not self.first_time[ids]        

    def add_db_instance(self, ipt):
        """
        Create a new instance for ending database to save the raw data

        """
        try:
            if self.db_data:
                rdbs_destinies = [key for key in self.db_data.keys()]
                key_data = rdbs_destinies.pop()
                data = self.db_data.get(key_data)
                name_db = data['name']
                object_db = self.database_objects[name_db]
                data.update({
                    "dbname": data["args"]["dbname"],
                    'address': data["args"]["address"],            
                    'hostname': 'atlas'})
                db_insta = object_db(**data)
                self.rethinkdb[ipt] = False
                self.db_init[ipt] = True
                self.db_connect[ipt] = True
                if data['name'] == 'RethinkDB':
                    self.rethinkdb[ipt] = True

                self.db_instances[ipt]  = db_insta

                return db_insta 
            else:
                print("Ipt not in DB_DATA")
                return None
        except Exception as ex:
            print("Error creando instancia database %s" % format(self.db_data))
            raise ex


    def db_task(self):
        # enable db task
        loop = asyncio.get_event_loop()
        queue_db = self.queue_db
        control = {f"DB_{i}":DBSteps.CREATE for i in range(24)}        
        counter = {}
        task_name = f"db_task"
        ipt = "DB_PROCESS"
        flags = {key:True for key in control}
        db_instances = {}
        assigned = {key:{} for key in control}
        backup = {key:{} for key in control}
        db_args = [ipt, control, queue_db, db_instances,
                   counter, now(), now(), flags, assigned, backup]
        db_task = TaskLoop(self.db_work, db_args, {},
                           name=task_name)
        db_task.set_name(f"db_task_{ipt}")
        db_task.create()
        
        if not loop.is_running():
            loop.run_forever()


    async def db_work(self, ipt, control, queue_db, 
                      db_instances, counter,
                      last_data, last_time, flags, assigned, backup, **kwargs):
        """
        TODO: Control exceptions
        """
        # task_name = asyncio.Task.current_task()
        level = Logger.INFO
        messages = []
        message = ""
        kwargs["dataset"] = []
        now_check = now()
        task_name = f"db_task_{ipt}"
        loop = asyncio.get_event_loop()

        control_changes = {}
        cnow = now()
        free = set()
        for key, futures in assigned.items():
            db_insta = db_instances.get(key)
            task_group = all(map(lambda f:f.done(), futures.values()))
            falses = {t:f for t,f in futures.items() if not f.done()}
            if task_group:
                flags[key] = True
                free.add(key)
            elif falses:  
                print(now(), "Falses", falses)
                tosend = {}
                for table_name, future in falses.items():
                    bk = backup.get(key,{}).get(table_name)
                    time = bk.get("time")
                    dataset = bk.get("dataset")
                    if (not future.done()) and (cnow >= time +timedelta(seconds=15)):
                        await db_insta.close()
                        future.cancel()
                        tosend[table_name] = dataset
                        #await queue_db.put([])
                        # TODO
                        print(now(),"Cancel fut", key)
                        control[key] = DBSteps.CONNECT
                        exc = {}
                        try:
                            future.exception()
                        except Exception as e:
                            exc = dict(
                                zip(
                                    ("exc_type","exc_value","exc_traceback"), 
                                    sys.exc_info()))
                        message  = f"Task cancelled for {key}->{table_name}"
                        level = Logger.ERROR
                        messages.append((level, message, exc))

                if tosend:
                    queue_db.put(tosend)
        for key in free:
            assigned[key] = {}

        for key, dbcontrol in control.items():
            db_insta = db_instances.get(key)
            if dbcontrol == DBSteps.CREATE and db_insta:
                print(now(),"closign db insta?", db_insta)
                if db_insta:
                    await db_insta.close()
                    del db_insta
                db_insta = None
                message = f"Deleted weird db instance at ipt {ipt}, db {key}"
                level = Logger.WARNING
                messages.append((level, message, {}))

        for key, dbcontrol in control.items():
            #print("KEY", key,"CONTROL", dbcontrol)
            db_insta = db_instances.get(key)
            if dbcontrol == DBSteps.CREATE or not db_insta:
                db_insta = self.add_db_instance(ipt)
                db_instances[key] =  db_insta
                kwargs["instance"] = db_insta
                if db_insta:
                    control_changes[key] = DBSteps.CONNECT
                    message = f"RDB  {db_insta} at {ipt} created and passed to connect, db {key}"
                else:
                    message = f"RDB  {db_insta} at {ipt} can't created and try to recreate, db {key}"
                    level = Logger.WARNING
                    rprint("cannot create db object")
                messages.append((level, message, {}))

        control.update(control_changes)
        #print({k:db.active for k, db in db_instances.items()})

        for key, dbcontrol in control.items():
            db_insta = db_instances.get(key)
            if db_insta and dbcontrol == DBSteps.CONNECT:
                if not db_insta.active:
                    exc = {}
                    try:
                        address = db_insta.client_address
                        if db_insta.active:
                            await db_insta.close()
                            db_insta.clean_client()

                        future = asyncio.create_task(db_insta.async_connect())
                        stage = "connect"

                        # await queue_control.put((
                        #     task_name, 
                        #     now(), 
                        #     stage, 
                        #     future))

                        coro = await wait_for(
                            shield(future), 
                            timeout=20)

                        await asyncio.shield(db_insta.list_dbs())
                        await asyncio.shield(db_insta.create_db(db_insta.default_db))
                        await asyncio.shield(db_insta.list_tables())
                        message = f"RDB {db_insta} at {ipt} was connected, then passed to save data, db {key}"
                        level = Logger.INFO
                        control_changes[key] = DBSteps.SAVE
                    except asyncio.CancelledError as e:
                        exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                        message = f"RDB {db_insta} at {ipt} has canceled task, but protected by shield"
                        level = Logger.ERROR
                        control_changes[key] = DBSteps.CONNECT
                        gprint(f"Reconnect to db  IPT -> {ipt}")
                        await db_insta.close()
                    except Exception as e:
                        exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                        message = f"RDB  {db_insta} at {ipt} has an exception {e}"
                        level = Logger.CRITICAL
                        control_changes[key] = DBSteps.CONNECT
                        gprint(f"Exception connecting to db  IPT -> {ipt}, {e}")
                        await asyncio.sleep(3)
                        await db_insta.close()

                    print(now(),f"{ipt} Rethinkdb connection", db_insta.client_address)
                    messages.append((level, message, exc))
                else:
                    exc = {}
                    message = f"At {ipt} tried to connect but active {db_insta.active}"
                    level = Logger.WARNING
                    messages.append((level, message, exc))
                    control_changes[key] = DBSteps.SAVE
        control.update(control_changes)

        tasks = []

        for key, dbcontrol in control.items():
            db_insta = db_instances.get(key)
            db_flag = flags.get(key, True)
            opts = {}
            #print(now(), f"Saving data db {key}, flag {db_flag}")
            if db_insta.active and dbcontrol == DBSteps.SAVE and (not queue_db.empty()) and db_flag:
                """
                Leer la cola queue que debe ser una tupla (table_name,
                data)
                chequear si existe, si no crear
                """
                print(now(), f"Reading new data from process_data and save, db {key}")

                dataset = {}
                for i in range(queue_db.qsize()):
                    item = queue_db.get()
                    for t, array in item.items():
                        if t not in dataset:
                            dataset[t] = []
                        dataset[t]+= array
                queue_db.task_done()

                i = 0
                # maybe group by table_name and then save as bulk
                flags[key] = False
                opts[key] = True
                assigned[key] = {}
                for table_name, items in dataset.items():
                    message = ""
                    dataset = items
                    if table_name:
                        exc = {}
                        try:
                            if table_name not in db_insta.tables:
                                create = await db_insta.create_table(table_name)
                                await db_insta.create_index(
                                    table_name,
                                    index='DT_GEN')
                            print(now(), f"Saving to {table_name}"+\
                                  f"#{len(dataset)}, {db_insta.client_address}")
                            future = asyncio.create_task(db_insta.save_data(
                                table_name, dataset), name=f"save_data_{key}_{table_name}_{len(dataset)}")
                            tasks.append(future)
                            assigned[key][table_name] = future
                           
                            backup[key][table_name] = {
                                "time":now(),
                                "dataset": dataset}
                            if table_name in counter:
                                counter[table_name] += len(dataset)
                            else:
                                counter[table_name] = 0

                            if counter[table_name] == 60:
                                message = f"At ipt {ipt} saved successfully last {counter[table_name]}"+\
                                    f" messages for {table_name}, last " +\
                                    f"result"
                                level = Logger.INFO
                                counter[table_name] = 0

                            last_data = now()
                        except asyncio.CancelledError as e:
                            exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                            message = f"RDB {db_insta} at {ipt} has canceled task, but protected by shield"
                            level = Logger.ERROR
                            control_changes[key] = DBSteps.CONNECT
                            gprint(f"Reconnect to db  IPT -> {ipt}")
                            await db_insta.close()
                            break
                        except Exception as e:
                            exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                            message = f"RDB {db_insta} at {ipt} has an exception {e}"
                            level = Logger.CRITICAL
                            control_changes[key] = DBSteps.CONNECT
                            gprint(f"Exception connecting to db {db_insta.client_address} IPT -> {ipt}, {e}")
                            await db_insta.close()
                            break

                        if message:
                            messages.append((level, message, exc))
        control.update(control_changes)
        print(tasks)
        asyncio.gather(*tasks, return_exceptions=True)
            # stage = "free"

            # await queue_control.put((
            #     task_name, 
            #     now(), 
            #     stage, 
            #     {}))

        #gprint(f"No data on queue, db_insta {db_insta}")
        if queue_db.empty():
            await asyncio.sleep(1)
        # do log
        if messages:
            for level, message, exc in messages:
                #log.save(level, message)
                self.queue_log.put(("db_work", message, level, exc))
        if level not in {logging.INFO, logging.DEBUG}:
            await asyncio.sleep(5)

        return [ipt, control, queue_db,  
                db_instances, counter, 
                last_data, last_time, flags, assigned, backup], kwargs
    
    async def process_data(self, ipt, ico, control, sta_insta,
                           last_data, last_time, counter, queue_control, 
                           *args, **kwargs):
        loop = asyncio.get_event_loop()
        ids = self.assigned_tasks.get(ipt, {}).get(ico, None)
        assigned_tasks = self.assigned_tasks.get(ipt, {})
        ids = assigned_tasks.get(ico)
        level = Logger.INFO
        messages = []
        message = ""
        task_name = f"process_sta_task:{ipt}:{ico}"

        if now() >= last_time + timedelta(seconds=5):
            stage = "update"
            # await queue_control.put((task_name, now(), stage, sta_insta))
            # counter["DB_WORK"] = 0       

        if ids:
            if self.changes.get(ids, False):
                """
                Linked to db_loop, if there are a new change then
                create new instance, 
                """
                del sta_insta 
                sta_insta = None
                control = CSteps.CREATE

            code_db = self.stations.get(ids, {}).get('db')
            code = self.stations.get(ids, {}).get('code')
            idd = self.get_id_by_code('DBDATA', code_db)
            idc = self.idc.get(ids)
            if idc and sta_insta:
                if idc not in sta_insta.clients:
                    del sta_insta
                    sta_insta = None
                    control = CSteps.CREATE
            #############
            # For some actions that modify status of
            # the variables on this coroutine
            # self.free_ids[ids] = False
            # while self.wait.get(ids, False):
            #     await asyncio.sleep(.01)

            # if not self.status_sta[ids]:
            #     v = 1
            ##############
            """
            Si no se ha creado instancia de conexion a estación
            se crea

            sta_init un diccionario  {ids:bool}

            indice si la estación fue inicializada
            """        
            if control == CSteps.CREATE:
                # step 0 initialize the objects, source and end
                exc ={}
                try:
                    sta_insta, table_name = self.add_sta_instance(ids, loop)
                    kwargs["table_name"] = table_name
                    message = f"Station instance {sta_insta} created "+\
                        f"for {table_name}, control {control.value}"
                    level = Logger.INFO
                    if sta_insta:
                        control = CSteps.CONNECT
                        self.changes[ids] = False
                except Exception as ex:
                    exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                    message = f"PD_00: Conexión de estación con falla-> {ids}:{code}"
                    level = Logger.ERROR
                    idc = self.idc.get(ids, None)
                    msg, close_level = await self.reset_station_conn(sta_insta, ids, idc)
                    control = CSteps.CREATE
                    kwargs["origin_exception"] = f"PD_00 + {code}"
                if message:
                    messages.append((level, message, {}))
            """
            Si no se ha creado la instanca de database:
            se crea la db instancia
            """
            """
            En caso que instancia de collect a estacion se haya iniciado
            1° conectar
            2° extraer datos
            """
        else:
            await asyncio.sleep(5)

        if sta_insta:
            queue_db = kwargs.get("queue_db")
            table_name = kwargs.get("table_name")

            if control == CSteps.CONNECT:
                # step 1
                # si es primera vez de acceso
                # conectar al socket correspondiente
                # step 1.a connect and set flags to run data
                code = sta_insta.station            
                idc = None
                exc = {}
                try:

                    future = asyncio.create_task(sta_insta.connect())
                    stage = "connect"

                    await queue_control.put((
                        task_name,
                        now(),
                        stage,
                        future))

                    idc = await wait_for(
                        shield(future),
                        timeout=20)

                    try:
                        future.exception()
                    except Exception as e:
                        exc = dict(
                            zip(
                                ("exc_type","exc_value","exc_traceback"), 
                                sys.exc_info()))

                        msg = f"Excepcion at {ipt} tipo {e} for {sta_insta}"
                        messages.append((Logger.ERROR, msg, exc))

                    if idc:
                        self.idc[ids] = idc
                        self.set_status_sta(ids, True)
                        self.set_status_conn(ids, True)
                        self.first_time[ids] = False
                        control = CSteps.COLLECT
                        message = f"Station {sta_insta} connected at"+\
                            f" {ipt} "+\
                            f" to address {sta_insta.address}"
                        level = Logger.INFO
                    else:
                        control = CSteps.CONNECT
                        message = f"Station {sta_insta} not connected at"+\
                            f" {ipt} "+\
                            f" to address {sta_insta.address}"
                        level = Logger.WARNING

                except asyncio.TimeoutError as e:
                    exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                    message = f"Tiempo fuera para conectar instancia " +\
                        f"de estación {sta_insta} en ipt {ipt}, idc <{idc}>"
                    level = Logger.ERROR               
                    control = CSteps.CONNECT
                    msg, lvl = await self.reset_station_conn(
                        sta_insta,
                        ids,
                        idc)
                    control = CSteps.CONNECT
                    messages.append((lvl, msg, {}))


                except Exception as ex:
                    exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                    message = f"PD_02: Error al conectar estación {sta_insta}, ids {ids}, ipt  {ipt}, {ex}"
                    level = Logger.ERROR
                    control = CSteps.CONNECT
                    msg, lvl = await self.reset_station_conn(
                        sta_insta,
                        ids,
                        idc)
                    control = CSteps.CONNECT
                    messages.append((lvl, msg, {}))

                # si ya esta conectado :), obtener dato
                if message:
                    messages.append((level, message, exc))

            """
            Si ya está inicializado y conectad
            proceder a obtener datos
            """
            sta_dict = {}
            if control == CSteps.COLLECT and table_name:
                code = sta_insta.station
                idc = self.idc.get(ids)
                exc = {}
                # just for checking
                # step 1.b collect data and process to save the raw data
                try:
                    # set idc and header
                    # set_header =
                    # wait_for(sta_insta.get_message_header(idc),
                    #          timeout=self.timeout)
                    set_header = sta_insta.get_message_header(idc)
                    await shield(set_header)
                    get_records = wait_for(
                        sta_insta.get_records(),
                        timeout=10)

                    future = asyncio.create_task(get_records)
                    # stage = "collect"

                    # await queue_control.put((
                    #     task_name, 
                    #     now(), 
                    #     stage, 
                    #     future))

                    # TODO ADD STAGE GET RECORD
                    done, sta_dict = await shield(future)
                    dt0 = gps_time(sta_dict, sta_insta.tipo)
                    dt_iso = rdb.iso8601(dt0.isoformat())
                    rnow = now()
                    recv_now = rdb.iso8601(rnow.isoformat())
                    # print(rnow)
                    delta = (rnow - dt0).total_seconds()
                    sta_dict.update({
                        'DT_GEN': dt_iso,
                        'DT_RECV': recv_now,
                        "DELTA_TIME": delta})
                    last_data = recv_now
                    # Control criteria
                    await queue_db.put((table_name, sta_dict))
                    # queue_db.put((table_name, sta_dict))

                    stage = "sendq"

                    # await queue_control.put((
                    #     task_name, 
                    #     now(), 
                    #     stage, 
                    #     {"DT_GEN":dt0.isoformat(),"station":table_name}))

                    counter += 1
                    if counter == 60:
                        message = f"At ipt {ipt} ico {ico} sended successfully last {counter}"+\
                            f" messages for {code} at {rnow}"
                        level = Logger.INFO
                        messages.append((level, message, {}))   
                        counter = 0
                    await sta_insta.heart_beat(idc)
                    control = CSteps.COLLECT                    

                except asyncio.IncompleteReadError as incomplete_read:
                    exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                    message = f"At ipt {ipt} ico {ico} imcomplete read {incomplete_read},"+\
                        f"station {sta_insta}"
                    level = Logger.ERROR
                    msg, lvl = await self.reset_station_conn(
                        sta_insta,
                        ids,
                        idc)
                    control = CSteps.CONNECT
                    messages.append((level, message, exc))
                    messages.append((lvl, msg, {}))

                except Exception as e:
                    exc = dict(zip(("exc_type","exc_value","exc_traceback"), sys.exc_info()))
                    message = f"At ipt {ipt} ico {ico} error al obtener dato de estación {e},"+\
                        f"station {sta_insta}"
                    level = Logger.ERROR
                    msg, lvl = await self.reset_station_conn(
                        sta_insta,
                        ids,
                        idc)
                    control = CSteps.CONNECT
                    messages.append((level, message, exc))
                    messages.append((lvl, msg, {}))

                except asyncio.TimeoutError as e:
                    exc = dict(
                        zip(("exc_type","exc_value","exc_traceback"), 
                            sys.exc_info()))
                    message = f"At ipt {ipt}, ico {ico} tiempo fuera para"+\
                        f"obtener datos de estación {sta_insta}"
                    level = Logger.ERROR
                    kwargs["origin_exception"] = f"PD_T12_00 + {sta_insta}"                                     
                    msg, lvl = await self.reset_station_conn(
                        sta_insta,
                        ids,
                        idc)
                    messages.append((level, message, exc))
                    messages.append((lvl, msg, {}))
                    control = CSteps.CONNECT
                except asyncio.ConnectionError as e:
                    exc = dict(
                        zip(
                            ("exc_type","exc_value","exc_traceback"), 
                            sys.exc_info()))
                    message = f"At ipt {ipt}, ico {ico} Error de conexión para conectar instancia de estación {sta_insta}"
                    level = Logger.ERROR
                    kwargs["origin_exception"] = f"PD_T13_00 + {sta_insta}"                                     
                    msg, lvl = await self.reset_station_conn(sta_insta, ids, idc)
                    messages.append((level, message, exc))
                    messages.append((lvl, msg, {}))
                    control = CSteps.CONNECT


            if ids in self.first_time:
                idd = self.db_instances_sta.get(ids)
                self.first_time[ids] = False
            else:
                idd = self.db_instances_sta.get(ids)

            if not table_name:
                message = f"There are no table name for {code} " +\
                    +f"instance {sta_insta}"
                level = Logger.WARNING
                rprint(message)
                messages.append((level, message, {}))

            # control last data received
            # si aun no hay last_data
            if not last_data:
                control = CSteps.CONNECT
            elif isinstance(last_data, datetime):
                rnow = now()
                if last_data + timedelta(seconds=60) <= rnow:
                    code = sta_insta.station
                    idc = self.idc.get(ids)
                    message, level = await self.reset_station_conn(
                        sta_insta,
                        ids,
                        idc)
                    messages.append((level, message, {}))
                    message = f"Last data was along time"+\
                        f" ago... <{last_data}>, try reconnect for {sta_insta}"
                    level  = Logger.WARNING
                    messages.append((level, message, {}))
                    control = CSteps.CONNECT
            else:
                message = f"last data for station {sta_insta} doesn't"+\
                    " exists or isn't a datetime object"

            """
            Procesar los datos
            """
            """
            Conclusión del cliclo
            esta tarea se termina. ... (por un momento)
            se preparan los parámetros de retorno

            Si todo va bien debería llegar hasta acá:
            """
            # [input, output] controls
            #self.free_ids[ids] = True
        else:
            message = "Sleeping because there are no task, table name {table_name}"
            level = Logger.WARNING
        if now() >= last_time + timedelta(seconds=10):
            last_time = now()
        out = [ipt, ico,  control, 
               sta_insta, last_data, 
               last_time, counter, queue_control]
        if not self.status_sta.get(ids):
            out = [ipt, ico,  control, 
                   sta_insta, last_data,
                   last_time, counter, queue_control]

        if messages:
            for level, message, exc in messages:
                #log.save(level, message)
                self.queue_log.put(("process_data", message, level, exc))
            #log.save(level, message)
        if level not in {logging.INFO, logging.DEBUG}:
            await asyncio.sleep(5)
        return out, kwargs

    async def status_proc_task(self, ipt, loop, ipt_result_dict):
        """
        Coroutine que chequea el status
        """
        log = self.log_manager[ipt]
        ids_list = self.proc_tasks[ipt]
        if len(ids_list) > 0:
            print("Recolectando %s" % format(ids_list))
        results_dict = {}
        for ids in ids_list:
            """
            Check stop queue
            """
            # print("Status to collect: %s "%self.status_task[ids])
            # bprint("Task %s in %s" % (format(self.stations[ids]), ipt))
            try:
                if ids not in ipt_result_dict.keys():
                    v = 1
                    args = [[ids, v], loop]
                    ipt_result_dict.update({ids: args})
                # args=[[ids,v],loop]
                args = ipt_result_dict[ids]
                result = await self.process_data(*args)
                self.tasks[ids] = result
                results_dict.update({ids: result})
            except Exception as ex:
                log.exception("Falla al registrar status, %s" % ex)
                raise ex
        await asyncio.sleep(5)

        return [ipt, loop, results_dict]

    def check_iteration(self, maxv, task, coro):
        """
        Is a demo fn to create a hyperiteration and possible add new stations
        ->not impletented yet
        """
        result = task.result()
        value = result[0][1]
        if value <= maxv:
            renew(task, coro, simple_fargs_out)

    def set_init_args_kwargs(self, ipt):
        """
        This definition is for collector instance
        """
        return [ipt, (None, None)], {}

    def set_pst(self, ids, args, kwargs):
        """
        This definition is for collector instance
        """
        return [args[0], ids, *args[1:]], kwargs

    def msg_network_task(self):
        # get from queue status
        # read_queue -> rq
        # process msg -> f(
        queue_list = [self.queue_n2t, self.queue_t2n]
        loop = asyncio.get_event_loop()
        try:
            args = [queue_list]
            kwargs = {}
            # Create instances
            task_name = "check_status_task"
            task = TaskLoop(
                    self.check_status,
                    args, kwargs, name=task_name)
            task.create()
            self.status_tasks["status_check"] = task_name
            ## log task
            self.manage_log_task()
            rprint("MANAGE DB LOOP")
            self.manage_db_loop()
            self.status_task_monitor_task()
            if not loop.is_running():
                loop.run_forever()
        except Exception as ex:
            print("Error o exception que se levanta con %s" %
                  format(queue_list))
            raise ex

    def manage_db_loop(self):
        args = [ORMSteps.CONNECT, None]
        task_name = "db_loop_task"
        task = TaskLoop(self.db_loop, args, {}, name=task_name)
        task.create()
        self.status_tasks["db_loop"] = task_name
        
    async def db_loop(self, control, session, *args, **kwargs):
        keys = ['id', 'code', 'db', 'dblist', 'ECEF_X', 'ECEF_Y', 'protocol_host',
                'ECEF_Z', 'port', 'protocol', 'host', 'dbname']
        bprint(f"Db_loop {control.name}  {session}, {now()}")

        if control == ORMSteps.CONNECT:
            session = SessionCollector(
                log_path=self.log_path/"orm", 
                active='true', 
                server=self.server_name,
                **self.datadb)
            control = ORMSteps.DISTRIBUTE
        if session and control == ORMSteps.DISTRIBUTE:
            control = ORMSteps.EXECUTE
        if session and control == ORMSteps.EXECUTE:
            """
            Needs:
            - list of stations
            - assignation of stations 
            - check for new stations
            - drop if not listed in new list of databases
            """
            # Obtener las estaciones
            ids_stations = {station.get("code"):ids for ids, station in self.stations.items()}
            base_stations = [station for station in self.stations.values()]
            codes = [station.get("code") for station in base_stations]
            set_codes = set(codes)
            address = {
                station.get("code"):(station.get("host"),station.get("port")) 
                for station in base_stations
            }
            # obtain all ids assigned
            assigned_tasks  = set()      # 
            if self.assigned_tasks:
                assigned_tasks = reduce(
                    lambda a,b: a|b, 
                    [set(ids_set.values()) for ipt, ids_set in
                     self.assigned_tasks.items()])
            assigned_ids = set(filter(lambda e:e,[self.stations.get(ids, {}).get("code") for
                            ids in assigned_tasks]))

            try:
                stations = session.get_station_data(server=self.server_name)
                new_codes = set()
                for m in stations:
                    station = dict(
                        id=m['id'],
                        code=m['st_code'],
                        name=m['st_name'],
                        ECEF_X=m['ecef_x'],
                        ECEF_Y=m['ecef_y'],
                        ECEF_Z=m['ecef_z'],
                        db=m['db_code'],
                        dblist=m['db_list'],
                        port=m['st_port'],
                        protocol=m['prt_name'].upper(),
                        protocol_host=m['protocol_host'],
                        host=m['st_host'],
                        on_db=True
                    )
                    code = station["code"]
                    new_codes.add(code)
                    if code not in assigned_ids:
                        """
                        add new station to list, and send by queue to assignator
                        """
                        ids, station = self.add_station(**station)
                        message = f"New station added to collector {station}"
                        level = Logger.INFO
                        self.queue_log.put(("db_loop",  message,
                                            level, {}))
          
                        self.queue_process.put(ids)
                        self.changes[ids] = True
                    else:
                        """
                        if there is in codes, but check address data
                        is the important information for this use case
                        """
                        base_address = address.get(code)
                        if base_address:
                            now_address = (station["host"],
                                           station["port"])
                            ids = ids_stations.get(code)
                            if now_address != base_address:
                                """
                                If new info is correct, the connection
                                will raise and check for new info
                                (check control)
                                """
                                station = self.update_station(**station)
                                self.changes[ids] = True
                # drop deactivated codes
                dropped = set_codes - new_codes
                ids_drop = [ids_stations.get(code) for code in
                            dropped]
                for ids in ids_drop:
                    self.changes[ids] = True
                    if ids in self.stations:
                        station = self.stations.get(ids)
                        del self.stations[ids]
                        for ipt, task_set in self.assigned_tasks.items():
                            if ids in task_set.values():
                                for ico, nids in task_set.items():
                                    if ids == nids:
                                        message = f"Station {station} with ids {ids},"+\
                                            "ico {ico}, ipt {ipt}  dropped"
                                        level = Logger.INFO                        
                                        self.queue_log.put(("db_loop",  message,
                                                            level, {}))                    
                                        self.unset_sta_assigned(ipt,
                                                                ico, 
                                                                ids)
            except Exception as e:
                message = f"At db_loop the session is disconnected"
                level = Logger.ERROR
                self.queue_log.put(("db_loop",  message, level))
                control = ORMSteps.CONNECT
        await asyncio.sleep(30)
        return (control, session), kwargs


    async def check_status(self, queue_list, *args, **kwargs):
        wq = queue_list[0]
        rq = queue_list[1]
        process = dict()
        idc = ""
        await asyncio.sleep(5)
        try:
            msg_from_source = []
            if not rq.empty():
                for i in range(rq.qsize()):
                    msg = rq.get()
                    # msg is a dict deserialized
                    msg_from_source.append(msg)
                    m = msg.get('dt', {})
                    idc = msg.get('idc', {})
                    if isinstance(msg, dict):
                        c_key = m.get('command',{}).get('action',None)
                        if c_key in self.message_manager.commands.keys():
                            result = await self.message_manager.interpreter(m)
                            wq.put({'msg': result, 'idc': idc})
                        else:
                            wq.put({'msg': "Hemos recibido %s" % m, 'idc': idc})
                    else:
                        wq.put(
                            {'msg': "Es un mensaje que no es un comando de sistema %s" % msg,
                             'idc': idc})

            # bprint(self.instances.keys())
        except Exception as ex:
            raise ex
        return [queue_list, *args], kwargs


    async def manage_data(self, queue_list, *args, **kwargs):
      
        # idd = self.get_id_by_code('DBDATA', code_db)        
        # code = None        

        # if not self.db_init.get(idd, False):
        #     db_insta = self.add_db_instance(ids, idd)

        return [queue_list, *args], kwargs

    async def status_task_monitor(self, *args, **kwargs):
        tasks_list = [task for task in asyncio.all_tasks() 
                      if task.get_name() in
                      self.status_tasks.values()]
        for task in tasks_list:
            print(now(), "Monitor ::", task.get_name(), "Cancelled", task.cancelled(),
                  "Done", task.done())
        await asyncio.sleep(20)
        return args, kwargs

    def status_task_monitor_task(self):
        loop = asyncio.get_event_loop()
        task_name = "status_task_monitor_task"
        task = TaskLoop(self.status_task_monitor, (), {}, name=task_name)
        task.create()
        self.status_tasks["status_task_monitor"] = task_name

    async def manage_log(self, log, queue_log, **kwargs):
        """
        an multiprocessing queue to manage all log messages
        """
        if not queue_log.empty():
            for i in range(queue_log.qsize()):
                (function, message, level, exc) = queue_log.get()
                print(now(), function, "::", message, exc)
                
                log.logger.log(level, f"{function} :: {message}")               
                if exc:
                    tb = exc.get("exc_traceback")
                    traceback.print_tb(tb)
                    info = tuple(exc.values())
                    log.logger.error(f"{function} :: {message}", 
                                     exc_info=info)
            queue_log.task_done()
        return (log, queue_log), kwargs


    def manage_log_task(self):
        rprint("Manage log task doing")
        loop = asyncio.get_event_loop()
        log = FileLog("Engine@Collector",
                      f"LogTask",
                      "localhost@atlas",
                      path=self.log_path/"engine",
                      max_bytes=10100204)
        args = [log, self.queue_log]
        task_name = "log_task"
        task = TaskLoop(self.manage_log, args, {}, name=task_name)
        task.create()
        self.status_tasks["log"] = task_name


    async def queue_join(self, ipt, queue_db, queue_to_db, **kwargs):

        if not queue_db.empty():
            dataset = {}
            
            for i in range(queue_db.qsize()):
                table, item = await queue_db.get()
                if table not in dataset:
                    dataset[table] = []
                dataset[table].append(item)

            queue_to_db.put(dataset)

        return (ipt, queue_db, queue_to_db), kwargs
        
    def manage_tasks(self, ipt):
        """
        A method to manage the tasks assigned to *ipt* process

        Initialize an event loop, and assign idle tasks for this process

        Create the tasks for every source assigned to this process.

        Create task for database

        Check the cases unidirectional and bidirectional.

        :param ipt: the key or identifier of a process
        """
        # loop = asyncio.get_event_loop()
        gprint(f"New ipt task {ipt}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bprint(f"New loop on ipt {ipt}")
        queue_db = asyncio.Queue()
        queue_to_db = self.queue_db

        args = [ipt, queue_db, queue_to_db]
        task_name = f"queue_db:{ipt}"
        task_db = TaskLoop(
            self.queue_join,
            args,
            {},
            **{"name": task_name})
        task_db.set_name(task_name)
        task_db.create()

        queue_control = asyncio.Queue()

        tasks = []
        self.assigned_tasks[ipt] = {}
        new_dict = {}
        # inicia n tareas en proceados
        for i in range(self.lnproc):
            ico = f"ICO_{i}"
            nd = {ico:  None}
            new_dict.update(nd)
        self.assigned_tasks[ipt] = new_dict
        tasks_on_this_ipt = self.assigned_tasks.get(ipt)
        

        #tasks.append(db_task)
        #self.status_tasks["db_task"] = task_name 
        # end db task
        for ico in tasks_on_this_ipt.keys():
            if self.run_task:
                try:
                    #ids = self.assigned_tasks.get(ipt, {}).get(ico,
                    #None)
                    control_collect = CSteps.CREATE
                    args = [ipt, ico, control_collect, None, 
                            now(), now(), 0, queue_control]
                    task_name = f"process_sta_task:{ipt}:{ico}"
                    task_1 = TaskLoop(
                        self.process_data,
                        args,
                        {"queue_db": queue_db},
                        **{"name": task_name})
                    #task_1.set_name(task_name)
                    task_1.create()
                    tasks.append(task_1)
                    key = f"collect_{ico}"
                    self.status_tasks[key] = task_name
                except Exception as ex:
                    print(
                        "Error en collect_task, gather stations, process_sta(task) %s, error %s"
                        % (ipt, ex))
                    print(ex)
                    raise ex
        try:
            args = [ipt]
            kwargs = {}
            task_4 = TaskLoop(
                self.process_sta_manager,
                args,
                kwargs,
                {"name": "task_process_sta_manager"}
            )
            task_4.create()
            # for task in tasks:
            #     bprint(f"Iniciando tarea->{task}")
            #     task.create()
            

            """
            Controller, check for the running tasks
            """
            control = ControlActions.ACTIVATE
            monitoring = {}
            counter = {}
            stages = {}
            reserva = {}
            args = [ipt, control, queue_control, tasks, monitoring,
                    counter, stages, reserva]
            kwargs = {}
            print(now(),"Creating control tasks to dynamic management")

            # control_task = TaskLoop(
            #     self.control_tasks,
            #     args,
            #     kwargs,
            #     {"name": "task_control_tasks"}
            # )
            # print(now(),"Created")
            # control_task.create()


        except Exception as exe:
            print("Error en collect_task, manager %s, error %s" % (ipt, exe))
            print(exe)
            raise exe
        if not loop.is_running():
            loop.run_forever()


    async def control_tasks(self, ipt, control,  
                            queue, 
                            tasks, 
                            monitoring, 
                            counter,
                            stages,
                            reserva,
                            **kwargs):
        DEBUG = False
        loop = asyncio.get_event_loop()
        delta_time = 5
        limit = 60
        print(now(), f"Control Tasks :: at {ipt}, {control.name}, "+\
              f"queue {queue.qsize()}") 
        messages = []
        if control == ControlActions.ACTIVATE:
            for task in tasks:
                future = task.create()#asyncio.run_coroutine_threadsafe(run_task(task), loop)
                monitoring[task.name] = {
                    "task": task,
                    "future": future,
                    "last_check": now(), 
                    "instance": None
                }
                message = f"Control Tasks At ipt {ipt} task running at threadsafe {task.name}"
                messages.append((Logger.INFO, message, {}))
                stages[task.name] = {}
            control = ControlActions.MONITOR

        observable = {}

        if control == ControlActions.MONITOR:
            if not queue.empty():
                for i in range(queue.qsize()):
                    # can get many of same source but save last
                    origin, data, stage, information = await queue.get()

                    if stage == "update":
                        client_address = information
                        if origin in monitoring:
                            last_check = monitoring[origin]["last_check"]
                            observable[origin] = data
                            #comment this to develop fast ::
                            if not DEBUG:
                                monitoring[origin]["last_check"] = data
                            monitoring[origin]["client"] = client_address
                        else:
                            message = f"Control Tasks Trash received origin :: {origin} data :: {data}"
                            messages.append((Logger.INFO, message,
                                             {}))
                    elif stage in ("connect", "save", "collect"):
                        stages[origin] = {
                            "time": data, 
                            "task": information,
                            "stage": stage
                        }
                        observable[origin] = data
                        #comment this to develop fast ::
                        if not DEBUG:
                            monitoring[origin]["last_check"] = data

                    elif stage in {"sendq", "todb"}:
                        dtgen = information.get("DT_GEN")
                        station = information.get("station")
                        if station not in counter:
                            counter[station] = {"sendq":{}, "todb":{}}
                        counter[station][stage][dtgen] = data

                    elif stage == "free":
                        reserva[origin] = True
                        for station in counter:
                            counter[station] = {"sendq":{}, "todb":{}}
                queue.task_done()
        
        # now, do the control based at the information
        factor = limit/delta_time
        
        for key, item_task in monitoring.items():
            monitoring_check = item_task["last_check"]
            # counter[key] do the control in case observable didn't
            # receive new data
            #if counter[key] >= factor:
            comp = now()
            drop_loop = False
            differences = []

            reserva_key = reserva.get(key, True)

            if key.startswith("db_task_"):
                station = ""
                for station, data in counter.items():
                    send_time = counter[station]["sendq"]
                    todb_time = counter[station]["todb"]
                    differences = []
                    discard = []
                    for dtgen, value in send_time.items():
                        todb_value = todb_time.get(dtgen)
                        final = todb_value
                        if not todb_value:
                            final = now()
                        else:
                            discard.append(dtgen)
                            dest = [dt for dt, val in
                                    todb_time.items() if val<=value]
                            discard += dest
                        check = (final - value) > timedelta(seconds=limit)
                        differences.append(check)
                        if check:
                            break
                        else:
                            discard.append(dtgen)
                    for dtkey in discard:
                        if dtkey in counter[station]["sendq"]:
                            del counter[station]["sendq"][dtkey]
                        if dtkey in counter[station]["todb"]:
                            del counter[station]["todb"][dtkey]
                    drop_loop = any(differences)
                    if drop_loop:
                        print("LOCKED -> drop", station, data)
                        break
                print(now(), key, f"LOCKED If loop locked {drop_loop}, {differences}")
                
            loop_locked = comp >= (monitoring_check +
                                   timedelta(seconds=limit))
            # if not reserva_key:
            #     item = stages[key]
            #     # here cancel the inner task that is blocked
            #     stage_task = item.get("task")
            #     if not stage_task.done():
            #         print(now(), f"Cancelling stage at {ipt}, with  delta {delta}")
            #         if not stage_task.cancelled():
            #             stage_task.cancel()
            #         exc = {}
            #         try:
            #             stage_task.exception()
            #         except Exception as e:
            #             exc = dict(
            #                 zip(
            #                     ("exc_type","exc_value","exc_traceback"), 
            #                     sys.exc_info()))


            if (loop_locked or drop_loop) and reserva_key:
                reserva[key] = False
                delta = comp - (monitoring_check + timedelta(seconds=limit))
                main_task = item_task.get("task")
                future = item_task.get("future")

                """
                works: run a new task 
                doesnt' work :: close db connection!! :S
                """
                # options :: dropped yet
                # entry here if the task is blocked, so we 
                # can redefine the callbacks, finish and give
                # one to show
                print(now(), f"The {main_task.name} is forced"+\
                                         " to  finish at ipt"+\
                                         f" {ipt} Control Tasks")
                #main_task.finish()
                if key in stages:
                    item = stages[key]
                    # here cancel the inner task that is blocked
                    stage_task = item.get("task")
                    print(now(), f"Cancelling stage at {ipt}, with  delta {delta}")
                    if stage_task:
                        if not stage_task.cancelled():
                            stage_task.cancel()
                        exc = {}
                        try:
                            stage_task.exception()
                        except Exception as e:
                            exc = dict(
                                zip(
                                    ("exc_type","exc_value","exc_traceback"), 
                                    sys.exc_info()))
                        # close rdb conn
                        result_args, result_kwargs = future.result()
                        for i, elem in result_kwargs.items():
                            if isinstance(elem, Rethink_DBS):
                                instance = elem
                                flag = True
                                while flag:
                                    await instance.close()
                                    flag = instance.active
                                    print(now(), instance.client_host,
                                          instance.client_port)
                                    print(now(), 
                                          f"""Instance {instance}
                                          close connection,
                                          active
                                          {instance.active},
                                          at {ipt}, falg {flag}""")

                        # recreate future
                        datenow = now()

                        message = f"At ipt {ipt} cancel stage {stage} for {key} at"+\
                            f" {datenow}, previous future coroutine cancelled"+\
                            f" the previous result, delta time {delta}"+\
                            f" or an exception {exc}"+\
                            f" counter was at {key}"
                        level = Logger.CRITICAL
                        messages.append((level, message, exc))
                        counter[station] = {"sendq":{}, "todb":{}}

                # while not future.done():
                #     await asyncio.sleep(.1)

                # instance = None
                # position = 0
                # if future.done():
                #     result = future.result()
                #     if len(result) == 2:
                #         margs, mkwargs = result
                #         for i, elem in enumerate(margs):
                #             if isinstance(elem, Rethink_DBS):
                #                 instance = elem
                #                 while instance.active:
                #                     await instance.close()
                #                     await asyncio.sleep(1)
                #                     print(now(), instance.client_host,
                #                           instance.client_port)
                #                     print(now(), 
                #                           f"""Instance {instance}
                #                           close connection,
                #                           active
                #                           {instance.active},
                #                           at {ipt}""")
                #                 #main_task.coro_args[i] = elem
                #             if isinstance(elem, DBSteps):
                #                 #main_task.coro_args[i] = DBSteps.SAVE
                #                 pass

                #             if isinstance(elem,Gsof):
                #                 instance = elem
                #                 while instance.status:
                #                     await instance.close()
                #                     await asyncio.sleep(.1)
                #                     print(now(), 
                #                           f"""Instance {instance}
                #                           close connection,
                #                           active
                #                           {instance.active},
                #                           at {ipt}""")

                # if key.startswith("db_task_"):
                #     # pass
                #     if isinstance(instance, Rethink_DBS):
                #         message = f"Control Tasks Closing rethinkdb {instance} "+\
                #               f" to spawn another at {ipt}"
                #         print(now(), message)
                #         address = instance.client_address
                #         # await instance.close()
                #         # await asyncio.sleep(3)
                #         # print(now(), f"Control Tasks ipt {ipt} Closing to client port"+\
                #         #       f" address {address}")
                #         # del instance
                #         messages.append((Logger.INFO, message,
                #                          {}))

                #     future = main_task.create()

                #     datenow = now()

                #     monitoring[main_task.name] = {
                #         "task": main_task,
                #         "future": future,
                #         "last_check": datenow
                #     }

                #     message = f"At ipt {ipt} spawned new task for {key} at"+\
                #         f" {datenow}, previous future coroutine cancelled"+\
                #         f" the previous result"+\
                #         f" or an exception {exc}"+\
                #         f" counter was at {key}"
                #     level = Logger.CRITICAL
                #     messages.append((level, message, exc))


                # if key.startswith("process_sta_task_"):
                #     task.coro_args[1] = CSteps.CREATE 
                #     instance = mkwargs.get("instance")

                #     if isinstance(instance, Gsof):
                #         message = f"Control Tasks Closing protocol {instance}"+\
                #               f" to spawn another at {ipt}"
                #         print(now(), message)
                #         del instance
                #         messages.append((Logger.INFO, message, {}))


                #     # create new future task at threadsafe

                #     # future = asyncio.run_coroutine_threadsafe(
                #     #     run_task(main_task), 
                #     #     loop)

                #     future = main_task.create()

                #     datenow = now()

                #     monitoring[main_task.name] = {
                #         "task": main_task,
                #         "future": future,
                #         "last_check": datenow
                #     }

                #     message = f"At ipt {ipt} spawned new task for {key} at"+\
                #         f" {datenow}, previous future coroutine cancelled"+\
                #         f" the previous result"+\
                #         f" or an exception {exc}"+\
                #         f" counter was at {counter[key]}"
                #     level = Logger.CRITICAL
                #     messages.append((level, message, exc))

                # else:
                # task = item_task.get("task")
                # future = item_task.get("future")
                # if not future.cancelled():
                #     future.cancel()

                # r_kwargs = {}
                # instance = None

                # if future.done():
                #     result = future.result()
                #     r_args, r_kwargs = result
                #     for i, elem in enumerate(r_args):
                #         if isinstance(elem, Rethink_DBS):
                #             instance = elem
                #     await asyncio.sleep(1)
                # exc = {}
                # try:
                #     future.exception()
                # except Exception as e:
                #     exc = dict(
                #         zip(
                #             ("exc_type", "exc_value", "exc_traceback"), 
                #             sys.exc_info()))


                # if key.startswith("db_task_"):
                #     task.coro_args[1] = DBSteps.CREATE 
                #     instance = r_kwargs.get("instance")

                #     if isinstance(instance, Rethink_DBS):
                #         message = f"Control Tasks Closing rethinkdb {instance} "+\
                #               f"to spawn another at {ipt}"
                #         print(now(), message)
                #         address = instance.client_address
                #         await instance.close()
                #         await asyncio.sleep(5)
                #         print(now(), f"Control Tasks ipt {ipt} Closing to client port"+\
                #               f" address {address}")
                #         del instance
                #         close_socket(address)
                #         messages.append((Logger.INFO, message, {}))
                # if key.startswith("process_sta_task_"):
                #     task.coro_args[1] = CSteps.CREATE 
                #     instance = r_kwargs.get("instance")

                #     if isinstance(instance, Gsof):
                #         message = f"Control Tasks Closing protocol {instance}"+\
                #               f" to spawn another at {ipt}"
                #         print(now(), message)
                #         await instance.close()
                #         del instance
                #         messages.append((Logger.INFO, message, {}))



                # task = monitoring[key]["task"]
                # future = task.create()#asyncio.run_coroutine_threadsafe(
                #     #run_task(task), 
                #     #loop)

                # datenow = now()

                # monitoring[task.name] = {
                #     "task": task,
                #     "future": future,
                #     "last_check": datenow
                # }

                # message = f"At ipt {ipt} spawned new task for {key} at"+\
                #     f" {datenow}, previous future coroutine cancelled"+\
                #     f" the previous result"+\
                #     f" or an exception {exc}"+\
                #     f" counter was at {counter[key]}"
                # level = Logger.CRITICAL
                # messages.append((level, message, exc))
            # elif last_check:
            #     monitoring[key]["last_check"] = last_check
            #     counter[key] = 0
            # else:
            #     counter[key] += 1


        # 5 is a period reasonable to check operation
        # at every object observed the period is multiplied by 5

        if messages:
            for level, message, exc in messages:
                #log.save(level, message)
                self.queue_log.put(("control_tasks", message, level, exc))

        await asyncio.sleep(delta_time)
        return [ipt, control, queue, tasks, monitoring, counter,
                stages, reserva], kwargs





async def run_task(task):
    task.create()


import socket

from contextlib import closing
   
def close_socket(address):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex(address) == 0:
            print(f"Port is open {address}")
        else:
            print(f"Port is not open {address}")
