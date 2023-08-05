import os
import jsonsh.aiojson as aiojson
import asyncio
from uuid import uuid4
from pydantic import BaseModel

class Instance:
    def __init__(self,folder,*,cache_state = False,cache_capacity = 100):
        self.main_folder = folder
        aiojson.setcache(on=cache_state,capacity=cache_capacity)

    def setcache(self,on:bool,capacity:int):
        aiojson.setcache(on=on,capacity=capacity)

    def file_list(self,dir):
        return os.listdir(dir)

    def match(self,details:dict,data:dict):
        for key,value in details.items():
            if key not in data:
                return False
            if value != data.get(key):
                return False
        return True

    def register(self,temp):
        temp.__instance__ = self
        return temp
                    
        

class Template(BaseModel):
    __instance__ = None

    @classmethod
    async def find_one(cls,**details:str):
        ins = cls.__instance__
        if ins is None:
            raise NotImplementedError("Instance is not yet registered")
        if (id:=details.get("id")):
            try:
                data = await aiojson.open_and_load(f"{ins.main_folder}/{cls.__name__}/{id}.json")
            except FileNotFoundError:
                return None
            if ins.match(details,data):
                return cls(**data)
            else:
                return None
        else:
            try:
                for file in await asyncio.to_thread(ins.file_list,f"{ins.main_folder}/{cls.__name__}"):
                    data = await aiojson.open_and_load(f"{ins.main_folder}/{cls.__name__}/{file}")
                    if ins.match(details,data):
                        return cls(**data)
            except FileNotFoundError:
                return None
            return None

    @classmethod
    async def find_many(cls,**details:str):
        ins = cls.__instance__
        results = []
        try:
            for file in await asyncio.to_thread(ins.file_list,f"{ins.main_folder}/{cls.__name__}"):
                data = await aiojson.open_and_load(f"{ins.main_folder}/{cls.__name__}/{file}")
                if ins.match(details,data):
                    results.append(cls(**data))
        except FileNotFoundError:
            pass
        return results

    async def save(self):
        ins = self.__instance__
        if ins is None:
            raise NotImplementedError("Instance is not yet registered")
        dic = self.dict()
        if not os.path.exists(f"{ins.main_folder}/{self.__class__.__name__}"):
            os.makedirs(f"{ins.main_folder}/{self.__class__.__name__}",exist_ok=True)
        id = dic.get("id",uuid4().hex)
        dic["id"] = id
        await aiojson.open_and_dump(dic,f"{ins.main_folder}/{self.__class__.__name__}/{id}.json",indent = 4)
        return id