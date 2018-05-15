from .application import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('internal', 'created', 'active', 'name', 'user_name',
                  'user_email', 'company', 'occupation')

user_schema = UserSchema()
