from mapreduce import operation as op


def update_entity(entity):
    entity.user_id = entity.userinfo.user_id()
    entity.meta_version = '1'
    yield op.db.Put(entity)
