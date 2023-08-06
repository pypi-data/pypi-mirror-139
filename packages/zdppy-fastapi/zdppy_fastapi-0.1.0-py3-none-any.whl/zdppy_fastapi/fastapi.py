from typing import Any, List

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from fastapi import Depends, FastAPI, HTTPException, Query
from zdppy_log import Log
from .exceptions import ParamError
import pymysql

pymysql.install_as_MySQLdb()


class FastAPI(FastAPI):
    """
    FastAPI核心对象，继承原本的FastAPI
    """

    def __init__(self,
                 log_file_path: str = "logs/zdppy/zdppy_fastapi.log",
                 db_type: str = "sqlite",
                 db_host: str = "127.0.0.1",
                 db_username: str = "root",
                 db_password: str = "root",
                 db_port: int = 3306,
                 db_database: str = "test",
                 **extra: Any) -> None:
        super().__init__(**extra)
        self.table_router_dict = {}  # 表格的路由映射字典

        # 初始化日志
        self.log_file_path = log_file_path
        self.log = Log(log_file_path=log_file_path)

        # 初始化数据库引擎
        self.engine = None
        self.set_engine(db_type, db_host, db_port, db_username, db_password, db_database)

    def add_router_add(self, *, table: str, response_model=None, tags: List[str], summary: str, db_model_class,
                       create_model_class):
        """
        添加新增路由
        """
        # 添加路由
        if table not in self.table_router_dict.keys():
            self.table_router_dict[table] = APIRouter(tags=tags)
        router = self.table_router_dict.get(table)

        # 创建路由方法
        @router.post(f"/{table}", response_model=response_model, tags=tags, summary=summary)
        def router_method(*, session: Session = Depends(self.get_session), model: create_model_class):
            """
            路由方法
            """
            db_model = db_model_class.from_orm(model)
            session.add(db_model)
            session.commit()
            session.refresh(db_model)
            return db_model

    def add_router_find_by_page(self, *,
                                table: str,
                                response_model=None,
                                tags: List[str],
                                summary: str,
                                db_model_class):
        """
        添加根据分页查询路由
        """
        # 添加路由
        if table not in self.table_router_dict.keys():
            self.table_router_dict[table] = APIRouter(tags=tags)
        router = self.table_router_dict.get(table)

        # 创建路由方法
        @router.get(f"/{table}", response_model=response_model, tags=tags, summary=summary)
        def router_method(*, session: Session = Depends(self.get_session),
                          offset: int = 0,
                          limit: int = Query(default=100, lte=100)):
            """
            路由方法
            """
            self.log.info(f"根据分页查询数据 offset={offset} limit={limit}")
            db_model = session.exec(select(db_model_class).offset(offset).limit(limit)).all()
            self.log.info(f"根据分页查询数据成功 db_model = {db_model}")
            return db_model

    def add_router_find_by_id(self, *,
                              table: str,
                              response_model=None,
                              tags: List[str],
                              summary: str,
                              db_model_class):
        """
        添加根据分页查询路由
        """
        # 添加路由
        if table not in self.table_router_dict.keys():
            self.table_router_dict[table] = APIRouter(tags=tags)
        router = self.table_router_dict.get(table)

        # 创建路由方法
        @router.get(f"/{table}/" + "{id}", response_model=response_model, tags=tags, summary=summary)
        def router_method(*, session: Session = Depends(self.get_session), id: int = 0):
            """
            路由方法
            """
            db_model = session.get(db_model_class, id)
            if not db_model:
                raise HTTPException(status_code=404, detail="Student not found")
            return db_model

    def set_engine(self,
                   db_type: str = "sqlite",
                   db_host: str = "127.0.0.1",
                   db_port: int = 3306,
                   db_username: str = "root",
                   db_password: str = "root",
                   db_database: str = None, ):
        # 参数校验
        if db_database is None:
            raise ParamError(f"数据库名称不能为空： db_database={db_database}")

        # 生成sqlite类型的数据库引擎
        if db_type == "sqlite":
            sqlite_file_name = f"{db_database}.db"
            sqlite_url = f"sqlite:///{sqlite_file_name}"
            connect_args = {"check_same_thread": True}
            self.engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

        # 生成mysql类型的数据库引擎
        elif db_type == "mysql":
            # 参数校验
            url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
            self.engine = create_engine(url, echo=True)
        else:
            raise ParamError(f"不支持的数据库类型： db_type={db_type}")

    def add_router_update_by_id(self, *,
                                table: str,
                                response_model=None,
                                tags: List[str],
                                summary: str,
                                db_model_class,
                                update_model_class):
        """
        添加根据ID更新路由
        """
        # 添加路由
        if table not in self.table_router_dict.keys():
            self.table_router_dict[table] = APIRouter(tags=tags)
        router = self.table_router_dict.get(table)

        # 创建路由方法
        @router.patch(f"/{table}/" + "{id}", response_model=response_model, tags=tags, summary=summary)
        def router_method(*, session: Session = Depends(self.get_session), id: int = 0, update: update_model_class):
            """
            路由方法
            """
            db_model = session.get(db_model_class, id)
            if not db_model:
                raise HTTPException(status_code=404, detail="Not found")
            model_data = update.dict(exclude_unset=True)
            for key, value in model_data.items():
                setattr(db_model, key, value)
            session.add(db_model)
            session.commit()
            session.refresh(db_model)
            return db_model

    def add_router_delete_by_id(self, *,
                                table: str,
                                response_model=None,
                                tags: List[str],
                                summary: str,
                                db_model_class):
        """
        添加根据ID删除路由
        """
        # 添加路由
        if table not in self.table_router_dict.keys():
            self.table_router_dict[table] = APIRouter(tags=tags)
        router = self.table_router_dict.get(table)

        # 创建路由方法
        @router.delete(f"/{table}/" + "{id}", response_model=response_model, tags=tags, summary=summary)
        def router_method(*, session: Session = Depends(self.get_session), id: int = 0):
            """
            路由方法
            """
            db_model = session.get(db_model_class, id)
            if not db_model:
                raise HTTPException(status_code=404, detail="Not found")
            session.delete(db_model)
            session.commit()
            return {"ok": True}

    def add_router_table_crud(self, *,
                              table: str,
                              chinese_name: str,
                              response_model=None,
                              tags: List[str] = None,
                              db_model_class,
                              create_model_class,
                              update_model_class):
        """
        添加表格的路由
        """
        if tags is None:
            tags = [f"{chinese_name}管理"]
        self.add_router_add(
            table=table,
            response_model=response_model,
            tags=tags,
            summary=f"创建{chinese_name}",
            db_model_class=db_model_class,
            create_model_class=create_model_class)
        self.add_router_find_by_page(
            table=table,
            response_model=List[response_model],
            tags=tags,
            summary=f"根据分页查询{chinese_name}",
            db_model_class=db_model_class)
        self.add_router_find_by_id(
            table=table,
            response_model=response_model,
            tags=tags,
            summary=f"根据ID查询{chinese_name}",
            db_model_class=db_model_class)
        self.add_router_update_by_id(
            table=table,
            response_model=response_model,
            tags=tags,
            summary=f"根据ID修改{chinese_name}",
            db_model_class=db_model_class,
            update_model_class=update_model_class)
        self.add_router_delete_by_id(
            table=table,
            response_model=response_model,
            tags=tags,
            summary=f"根据ID删除{chinese_name}",
            db_model_class=db_model_class)

    def init_table_routers(self):
        """
        初始化表格路由
        """
        # 不存在路由，则忽略
        if not self.table_router_dict:
            return

        # 挂载所有路由
        for router in self.table_router_dict.values():
            self.include_router(router)

    def get_session(self):
        """
        获取数据库引擎上下文对象
        """
        if self.engine is None:
            raise ParamError(f"数据库引擎不能为空 engine={self.engine}")
        with Session(self.engine) as session:
            yield session

    def init_tables(self, sql_model):
        """
        初始化数据库表格
        """
        sql_model.metadata.drop_all(self.engine)
        sql_model.metadata.create_all(self.engine)

    def create_tables(self, sql_model):
        """
        创建数据库表格
        """
        sql_model.metadata.create_all(self.engine)

    def drop_tables(self, sql_model):
        """
        删除数据库表格
        """
        sql_model.metadata.drop_all(self.engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title="API接口文档",
        description="基于zdppy_fastapi开发，zdppy_fastapi是一个支持异步高并发的Python后端api快速开发框架",
        version="1.0.0",
    )  # 创建app
    app.add_middleware(  # 添加跨域中间件
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
