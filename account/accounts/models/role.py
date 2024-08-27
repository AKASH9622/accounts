from . import utils
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import user

class RolePermissions(utils.TimeStamp):
    name = models.CharField(max_length=50)
    value = models.TextField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'user_role_permissions'

class Role(utils.TimeStamp):
    name = models.CharField(_("Role Name"), max_length=50)
    permissions = models.ManyToManyField(RolePermissions)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'user_roles'
        
class UserRole(utils.TimeStamp):
    user_id = models.OneToOneField(user.User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.user_id}"
    
    class Meta:
        db_table = 'user_roles_detail'

    @property
    def get_permissions(self):
        if not self.role_id:
            return []
        
        permissions = self.role_id.permissions.all()
        permissions_list = [{"name": perm.name, "value": perm.value} for perm in permissions]
        return permissions_list