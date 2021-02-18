class ViewOnlyModelAdminMixin(object):
    can_add = False
    can_delete = False

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, request, obj=None):
        return False
