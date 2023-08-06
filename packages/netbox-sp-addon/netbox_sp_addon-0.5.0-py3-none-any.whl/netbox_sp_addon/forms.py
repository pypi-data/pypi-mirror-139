from dcim.forms import DeviceFilterForm
from dcim.models import RackRole
from utilities.forms import DynamicModelMultipleChoiceField


class SPDeviceFilterForm(DeviceFilterForm):
    fieldsets = (
        (None, ('q', 'tag')),
        ('Location', ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_role', 'rack_id')),
        ('Operation', ('status', 'role_id', 'airflow', 'serial', 'asset_tag', 'mac_address')),
        ('Hardware', ('manufacturer_id', 'device_type_id', 'platform_id')),
        ('Tenant', ('tenant_group_id', 'tenant_id')),
        ('Components', (
            'console_ports', 'console_server_ports', 'power_ports', 'power_outlets', 'interfaces', 'pass_through_ports',
        )),
        ('Miscellaneous', ('has_primary_ip', 'virtual_chassis_member', 'local_context_data'))
    )

    rack_role = DynamicModelMultipleChoiceField(
        queryset=RackRole.objects.all(),
        required=False,
        label="Rack role",
    )
