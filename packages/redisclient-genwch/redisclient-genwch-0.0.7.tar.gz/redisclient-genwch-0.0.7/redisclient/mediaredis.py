from abc import ABC


class Media(ABC):
    def __init__(self, redis_host: str, source: str) -> None:
        import redis
        _redishost = redis_host.split(":")
        _host = _redishost[0]
        _port = int(_redishost[1]) if len(_redishost) > 1 else 6379
        _db = int(_redishost[2]) if len(_redishost) > 2 else 0
        self._redis = redis.Redis(host=_host, port=_port, db=_db)
        self._table = {"root": "media", "index": "_idx",
                       "running": "_rkey", "update": "_upd"}
        self._source = source
        pass

    def _sysdate(self, date: str = None) -> float:
        import time
        from datetime import datetime
        if date is None:
            _now = datetime.now()
        else:
            _now = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return time.mktime(_now.timetuple())

    def get_table(self, type: str, opt: str = None) -> str:
        if opt is None:
            _rtn = "{}:{}".format(self._table.get("root"), type)
        else:
            _rtn = "{}:{}:{}".format(self._table.get(
                "root"), self._table.get(opt), type)
        return _rtn

    def get_uid(self, type: str, value: str, col: str = None, source: str = None, usesource: bool = True, addnew: bool = True) -> list:
        _rtn = []
        _col = col if col is not None else "id"
        _source = source if source is not None else self._source
        _tbl = "{}{}:{}".format(self.get_table(
            type, "index"), f":{_source}" if usesource else "", _col) if col is not None else self.get_table(type, "index")
        _iter = self._redis.zscan_iter(name=_tbl, match=value)
        for _, _idx in _iter:
            _rtn.append(int(_idx))
        if len(_rtn) == 0 and addnew:
            _rtbl = self.get_table(type, "running")
            _rtn = [self._redis.incr(name=_rtbl)]
        return _rtn

    def _get_last_upd(self, type: str, page: int = None, count: int = None) -> list:
        page = 0 if page is None else page
        count = 50 if count is None else count
        _tbl = self.get_table(type, "update")
        _rtn = [int(_c.decode("UTF-8")) for _c in self._redis.zrevrangebyscore(
            name=_tbl, min=0, max=9999999999, start=page * count, num=count)]
        return _rtn

    def get_index(self, type: str, match: str, stype: str = None) -> list:
        _rtn = []
        _tbl = "{}{}".format(self.get_table(type, "index"),
                             f":{stype}" if stype is not None else "")
        _iter = self._redis.zscan_iter(name=_tbl, match=match)
        for _, _idx in _iter:
            _rtn.append(int(_idx))
        return _rtn

    def get(self, type: str, value: str = None, col: str = None, usesource: bool = False, uid: int = None, incluid: bool = True, count: int = 500, addnew: bool = False) -> list:
        _rtn = []
        if uid is None:
            if value is not None:
                uid = self.get_uid(type=type, value=value,
                                   col=col, addnew=addnew)
            else:
                uid = self._get_last_upd(type=type, count=count)
        if uid is not None:
            _tbl = "{}{}".format(self.get_table(
                type), f":{self._source}" if usesource else "")
            for _u in uid if isinstance(uid, list) else [uid]:
                _tmp = {_k.decode("UTF-8"): _v.decode("UTF-8")
                        for _k, _v in self._redis.hgetall(f"{_tbl}:{_u}").items() if _k is not None and _v is not None}
                if incluid:
                    _tmp.update({"uid": _u})
                _rtn.append(_tmp)
                if len(_rtn) >= count:
                    break
        return _rtn

    def _conv_data(self, data: dict) -> dict:
        return {_k: _v if not isinstance(_v, bool) else 1 if _v else 0 for _k, _v in data.items() if not isinstance(_v, list) if _v is not None}

    def _add_uid(self, type: str, data: dict, keycol: str) -> tuple:
        _uid = None
        _exists = self.get(type=type, value=data.get(keycol), usesource=True)
        if len(_exists) > 0:
            _tmp_data = _exists[0]
            _uid = _tmp_data.get("uid")
            _tmp_data.pop("uid")
            if data == _tmp_data:
                return _uid, True
        if _uid is None:
            _uid = self.get_uid(
                type=type, value=data.get(keycol), addnew=True)[0]
        return _uid, False

    def _add_data(self, type: str, data: dict, uid: int, excl: list = [], usesource: bool = True):
        _tbl = "{}:{}".format(self.get_table(type), uid)
        data = self._conv_data(data)
        _mod_cat = data.copy()
        for _x in excl:
            try:
                _mod_cat.pop(_x)
            except:
                pass
        self._redis.hset(name=_tbl, mapping=_mod_cat)
        if usesource:
            _tbl = "{}:{}:{}".format(
                self.get_table(type), self._source, uid)
            self._redis.hset(name=_tbl, mapping=data)

    def _add_index(self, type: str, data: dict, uid: int, keycol: str = None, sourcecol: list = [], source: str = None):
        _source = source if source is not None else self._source
        if keycol is not None:
            if data.get(keycol) is not None:
                _tbl = self.get_table(type, "index")
                self._redis.zadd(name=_tbl, mapping={data.get(keycol): uid})
        for _c in sourcecol:
            if data.get(_c, None) is None:
                continue
            _tbl = "{}:{}:{}".format(self.get_table(
                type, "index"), _source, _c)
            self._redis.zadd(name=_tbl, mapping={data.get(_c): uid})

    def _add_group_index(self, type: str, data: dict, keycol: str, uid: int, group: dict = {}, source: str = None, unique: bool = False):
        _source = f":{source}" if source is not None else ""
        for _k, _v in group.items():
            if _k is None or _v is None:
                continue
            _tbl = "{}{}:{}:{}".format(
                self.get_table(type, "index"), _source, _k, _v)
            self._redis.zadd(name=_tbl, mapping={data.get(keycol): uid})
            if unique:
                _tbl = "{}{}:{}".format(
                    self.get_table(type, "index"), _source, _k)
                self._redis.zadd(name=_tbl, mapping={data.get(keycol): _v})

    def _add_upd(self, type: str, uid: str, now: str = None):
        _tbl = self.get_table(type, "update")
        _now = self._sysdate() if now is None else now
        self._redis.zadd(name=_tbl, mapping={uid: _now})

    def add_cats(self, cats: list) -> None:
        _now = self._sysdate()
        _type = "cats"
        _keycol = "cat"
        _exclcol = ["id"]
        for _data in cats:
            _uid, _skip = self._add_uid(type=_type, data=_data, keycol=_keycol)
            if _skip:
                continue
            self._add_data(type=_type, data=_data, uid=_uid, excl=_exclcol)
            self._add_index(type=_type, data=_data, keycol=_keycol,
                            uid=_uid, sourcecol=_exclcol)
            self._add_upd(type=_type, uid=_uid, now=_now)
        pass

    def add_scats(self, scats: list, catid: str) -> None:
        _now = self._sysdate()
        _type = "scats"
        _keycol = "scat"
        _exclcol = ["id"]
        _catuid = self.get_uid(
            type="cats", value=catid, col="id", addnew=False)
        if len(_catuid) < 1:
            return
        _group = {"cats": _catuid[0]}
        for _data in scats:
            _uid, _skip = self._add_uid(type=_type, data=_data, keycol=_keycol)
            if _skip:
                continue
            self._add_data(type=_type, data=_data, uid=_uid, excl=_exclcol)
            self._add_index(type=_type, data=_data, keycol=_keycol,
                            uid=_uid, sourcecol=_exclcol)
            self._add_group_index(type=_type, data=_data,
                                  keycol=_keycol, uid=_uid, group=_group, unique=True)
            self._add_upd(type=_type, uid=_uid, now=_now)
        pass

    def add_src_videos(self, videos, scatid: str = None):
        _now = self._sysdate()
        _type = self._source
        _keycol = "title"
        _exclcol = ["id"]
        _group = {}
        if scatid is not None:
            _scatuid = self.get_uid(
                type="scats", value=scatid, col="id", addnew=False)
            if len(_scatuid) >= 1:
                _group.update({"scats": _scatuid[0]})
        for _data in videos if isinstance(videos, list) else [videos]:
            _uid, _skip = self._add_uid(type=_type, data=_data, keycol=_keycol)
            if _skip:
                continue
            self._add_data(type=_type, data=_data, uid=_uid,
                           excl=[], usesource=False)
            self._add_index(type=_type, data=_data, keycol=_keycol,
                            uid=_uid, sourcecol=_exclcol)
            self._add_group_index(type=_type, data=_data,
                                  keycol=_keycol, uid=_uid, group=_group, unique=True)
            self._add_upd(type=_type, uid=_uid, now=_now)

    def add_tmdb(self, videos, videoid: str = None):
        _now = self._sysdate()
        _type = "videos"
        _keycol = "title"
        _exclcol = ["tmdb_id"]
        _group = {}
        if videoid is not None:
            _videouid = self.get_uid(
                type=self._source, value=videoid, col="id", addnew=False)
            if len(_videouid) >= 1:
                _group.update({"id": _videouid[0]})

        for _data in videos if isinstance(videos, list) else [videos]:
            if _data.get("title", None) is None:
                _data.update({"title": _data.get("name", None)})
                _data.update(
                    {"original_title": _data.get("original_name", None)})
                try:
                    _data.pop("name")
                    _data.pop("original_name")
                except:
                    pass
            if _data.get("id", None) is not None:
                _data.update({"tmdb_id": _data.get("id", None)})
                _data.pop("id")
            _uid, _skip = self._add_uid(type=_type, data=_data, keycol=_keycol)
            if _skip:
                continue
            self._add_data(type=_type, data=_data, uid=_uid,
                           excl=[], usesource=False)
            self._add_index(type=_type, data=_data, keycol=_keycol,
                            uid=_uid, sourcecol=_exclcol, source="tmdb")
            self._add_index(type=_type, data=_data, keycol="original_title",
                            uid=_uid)
            self._add_group_index(type=_type, data=_data,
                                  keycol=_keycol, uid=_uid, group=_group, source=self._source)
            self._add_upd(type=_type, uid=_uid, now=_now)

    def add_people(self, people, videoid: str = None):
        _now = self._sysdate()
        _type = "people"
        _keycol = "name"
        _exclcol = []
        _group = {}
        _videouid = []
        if videoid is not None:
            _videouid = self.get_uid(
                type=self._source, value=videoid, col="id", addnew=False)
            if len(_videouid) >= 1:
                _group.update({"id": _videouid[0]})
        for _data in people if isinstance(people, list) else [people]:
            _uid, _skip = self._add_uid(type=_type, data=_data, keycol=_keycol)
            if _skip:
                continue
            self._add_data(type=_type, data=_data, uid=_uid,
                           excl=_exclcol, usesource=False)
            self._add_index(type=_type, data=_data, keycol=_keycol,
                            uid=_uid, sourcecol=_exclcol)
            self._add_index(type=_type, data=_data, keycol="en_name",
                            uid=_uid)
            self._add_index(type=_type, data=_data, keycol="oth_name",
                            uid=_uid)
            self._add_group_index(type=_type, data=_data,
                                  keycol=_keycol, uid=_uid, group=_group, source=self._source)
            if len(_videouid) >= 1:
                self._add_group_index(type=_type, data={"vid": videoid},
                                      keycol="vid", uid=_videouid[0], group={"people": _uid}, source=self._source)
            self._add_upd(type=_type, uid=_uid, now=_now)

    def _search(self, type: str, keyval: str = None, id: str = None, uid: str = None, page: int = 0, count: int = 50):
        if uid is None or (isinstance(uid, list) and len(uid) == 0):
            if id is not None:
                _uids = self.get_uid(
                    type=type, value=id, col="id", addnew=False)
            elif keyval is not None:
                _uids = self.get_uid(
                    type=type, value=keyval, col=None, usesource=False, addnew=False)
            else:
                _uids = self._get_last_upd(
                    type=type, page=page, count=count)
        else:
            _uids = uid if isinstance(uid, list) else [uid]
        return self.get(type=type, uid=_uids, addnew=False)

    def cats(self, *args, **kwargs) -> list:
        _rtn = []
        _cat = kwargs.get("cat", None)
        _catid = kwargs.get("catid", None)
        _uid = kwargs.get("uid", None)
        _page = kwargs.get("page", None)
        _count = kwargs.get("count", None)
        _type = "cats"
        _rtn = self._search(type=_type, keyval=_cat, id=_catid,
                            uid=_uid, page=_page, count=_count)
        return _rtn

    def scats(self, *args, **kwargs) -> list:
        _rtn = []
        _scat = kwargs.get("scat", None)
        _scatid = kwargs.get("scatid", None)
        _uid = kwargs.get("uid", None)
        _exclcols = ["scat", "scatid", "uid"]
        _page = kwargs.get("page", None)
        _count = kwargs.get("count", None)
        _type = "scats"
        _uids = []
        if _uid is not None:
            _uids = _uid if isinstance(_uid, list) else [_uid]
        if _scat is None and _scatid is None and _uid is None:
            _param = kwargs.copy()
            for _x in _exclcols:
                try:
                    _param.drop(_x)
                except:
                    pass
            _param.update(
                {"page": 0, "count": 500 if _count is None else _count * 10})
            _param.update({"uid": _param.get("catuid", None)})
            _cats = self.cats(**_param)
            _table = "{}:{}".format(self.get_table(
                type="scats", opt="index"), "cats")
            for _c in _cats:
                for _a, _suid in self._redis.zscan_iter(name="{}:{}".format(_table, _c.get("uid")), match="*"):
                    _uids.append(int(_suid))
                break
        _rtn = self._search(type=_type, keyval=_scat, id=_scatid,
                            uid=_uids, page=_page, count=_count)
        return _rtn

    def people(self, *args, **kwargs) -> list:
        _rtn = []
        _people = kwargs.get("name", None)
        _peopleid = kwargs.get("id", None)
        _uid = kwargs.get("uid", None)
        _page = kwargs.get("page", None)
        _count = kwargs.get("count", None)
        _type = "people"
        _rtn = self._search(type=_type, keyval=_people, id=_peopleid,
                            uid=_uid, page=_page, count=_count)
        return _rtn

    def tmdb(self, *args, **kwargs) -> list:
        _rtn = []
        _video = kwargs.get("title", None)
        _videoid = kwargs.get("tmdbid", None)
        _uid = kwargs.get("uid", None)
        _page = kwargs.get("page", None)
        _count = kwargs.get("count", None)
        _type = "videos"
        _rtn = self._search(type=_type, keyval=_video, id=_videoid,
                            uid=_uid, page=_page, count=_count)
        return _rtn

    def videos(self, *args, **kwargs) -> list:
        _rtn = []
        _video = kwargs.get("video", None)
        _videoid = kwargs.get("videoid", None)
        _uid = kwargs.get("uid", None)
        _exclcols = ["video", "videoid", "uid"]
        _page = kwargs.get("page", None)
        _count = kwargs.get("count", None)
        _type = self._source
        _uids = []
        if _uid is not None:
            _uids = _uid if isinstance(_uid, list) else [_uid]
        if _video is None and _videoid is None and _uid is None:
            _param = kwargs.copy()
            for _x in _exclcols:
                try:
                    _param.drop(_x)
                except:
                    pass
            _param.update(
                {"page": 0, "count": 500 if _count is None else _count * 10})
            _param.update({"uid": _param.get("scatuid", None)})

            _scats = self.scats(**_param)
            _table = "{}:{}".format(self.get_table(
                type=_type, opt="index"), "scats")
            for _s in _scats:
                for _a, _suid in self._redis.zscan_iter(name="{}:{}".format(_table, _s.get("uid")), match="*"):
                    _uids.append(int(_suid))
                break
        _table = "{}:{}:{}".format(self.get_table(
            type="videos", opt="index"), self._source, "id")
        _ppl_table = "{}:{}:{}".format(self.get_table(
            type="people", opt="index"), self._source, "id")
        _pg = 0 if _page is None else int(_page)
        _cnt = 50 if _count is None else int(_count)
        _uids = _uids[(_pg * _cnt):((_pg + 1) * _cnt)]
        for _v in self._search(type=_type, keyval=_video, id=_videoid,
                               uid=_uids, page=_page, count=_count):
            _ppl_lst = []
            for _, _puid in self._redis.zscan_iter(name="{}:{}".format(_ppl_table, _v.get("uid")), match="*"):
                _p = self.people(uid=int(_puid))
                if len(_p) > 0:
                    _ppl_lst += _p
            if len(_ppl_lst) > 0:
                _v.update({"people": _ppl_lst})
            for _, _vuid in self._redis.zscan_iter(name="{}:{}".format(_table, _v.get("uid")), match="*"):
                for _t in self.tmdb(uid=int(_vuid)):
                    if _t != {}:
                        _t.update(
                            {"{}_uid".format(self._source): _v.get("uid")})
                        _v.update(_t)
                        break
                break
            _rtn.append(_v)
        return _rtn
