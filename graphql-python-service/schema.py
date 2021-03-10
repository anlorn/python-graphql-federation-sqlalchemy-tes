import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Store as StoreModel, db_session
from graphene_federation import build_schema


class Store(SQLAlchemyObjectType):

    class Meta:
        model = StoreModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    stores = graphene.List(Store)
    store = graphene.Field(Store, store_id=graphene.String())

    def resolve_stores(self, info):
        query = Store.get_query(info)  # SQLAlchemy query
        return query.all()

    def resolve_store(self, info, **args):
        query = Store.get_query(info)
        try:
            return query.filter_by(store_id=args.get('store_id')).one()
        except Exception:
            return None


class CreateStore(graphene.Mutation):

    class Arguments:
        store_id = graphene.String()
        tenant = graphene.String()
        working_hours = graphene.String()
        is_enabled = graphene.Boolean()
        address = graphene.String()

    ok = graphene.Boolean()
    store = graphene.Field(Store)

    def mutate(root, info, store_id, tenant, working_hours, is_enabled, address):
        try:
            new_store = StoreModel(store_id=store_id,
                                   tenant=tenant,
                                   working_hours=working_hours,
                                   is_enabled=is_enabled,
                                   address=address)
            db_session.add(new_store)
            db_session.commit()
            ok = True
            return CreateStore(ok=ok, store=new_store)
        except Exception:
            return CreateStore(ok=False)


class UpdateStore(graphene.Mutation):

    class Arguments:
        store_id = graphene.String(required=True)
        tenant = graphene.String(required=False)
        working_hours = graphene.String(required=False)
        is_enabled = graphene.Boolean(required=False)
        address = graphene.String(required=False)

    store = graphene.Field(Store)
    ok = graphene.Boolean()

    def mutate(root, info, *args, **kwargs):
        try:
            store = db_session.query(StoreModel).filter_by(store_id=kwargs['store_id']).one()
            for key, value in kwargs.items():
                setattr(store, key, value)
            db_session.commit()
            ok = True
        except Exception:
            ok = False
            return UpdateStore(ok=ok)
        return UpdateStore(ok=ok, store=store)


class Mutation(graphene.ObjectType):
    create_store = CreateStore.Field()
    update_store = UpdateStore.Field()


#schema = graphene.Schema(query=Query, mutation=Mutation)
schema = build_schema(query=Query, mutation=Mutation)
