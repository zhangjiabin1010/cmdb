from django.db import models
# Create your models here.


class IDC(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='IDC')
    comment = models.CharField(max_length=200, null=True, blank=True, help_text='注释')

    def __str__(self):
        return self.name

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self._meta.fields:
    #         setattr(self, '{0}_help_text'.format(field.name), field.help_text)


class BusinessLine(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='业务线')
    comment = models.CharField(max_length=200, null=True, blank=True, help_text='注释')

    def __str__(self):
        return self.name

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, db_index=True, help_text='用户名')
    realname = models.CharField(max_length=20, null=True, blank=True, help_text='姓名')
    password = models.CharField(max_length=100, help_text='密码')
    email = models.EmailField(max_length=254, help_text='邮箱')
    mobile = models.CharField(max_length=11, null=True, blank=True, help_text='手机号')
    wechat = models.CharField(max_length=12, null=True, blank=True, help_text='微信号')

    def __str__(self):
        return self.username

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class Asset(models.Model):
    STATE_CHOICE = (
        (0, 'offline'),
        (1, 'online')
    )

    serialnum = models.CharField(max_length=100, unique=True, help_text='资产序列号')
    asset_type = models.CharField(max_length=120, help_text='资产类型')
    idc = models.ForeignKey(IDC, default=1, on_delete=models.SET_DEFAULT, help_text='IDC')
    cabinet_number = models.IntegerField(null=True, blank=True, help_text="机柜号")
    cabinet_position = models.IntegerField(null=True, blank=True, help_text="机柜U位")
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建日期')
    update_time = models.DateTimeField(auto_now=True, help_text='更新日期')
    contact = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, help_text='负责人')
    business_line = models.ManyToManyField(BusinessLine, null=True, blank=True, help_text='业务线')
    use = models.CharField(max_length=120, help_text="用途")
    state = models.SmallIntegerField(db_index=True, choices=STATE_CHOICE, default=1, help_text='状态')
    comment = models.CharField(max_length=200, null=True, blank=True, help_text='注释')

    def __str__(self):
        return self.serialnum

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class Server(models.Model):
    hostname = models.CharField(max_length=100, help_text='主机名')
    lan_ip = models.GenericIPAddressField(protocol='IPv4', db_index=True, unique=True, help_text='内网IP')
    wan_ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, help_text='外网IP')
    logical_cpu = models.CharField(max_length=100, help_text='CPU信息')
    logical_disk = models.CharField(max_length=50, help_text='磁盘容量')
    logical_memory = models.CharField(max_length=50, help_text='内存容量')
    os = models.CharField(max_length=100, help_text='操作系统')
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    phost_ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True,
                                            help_text='宿主机IP')

    def __str__(self):
        return self.hostname

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class NetworkDevice(models.Model):
    name = models.CharField(max_length=30, help_text='设备名')
    manufacturer = models.CharField(max_length=200, blank=True, null=True, help_text='生产厂商')
    product_name = models.CharField(max_length=200, help_text='机器型号')
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, help_text='ip地址')
    mac = models.CharField(max_length=50, null=True, blank=True, help_text='MAC 地址')

    def __str__(self):
        return self.name

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class NetworkInterface(models.Model):
    STATE_CHOICE = (
        (0, 'disable'),
        (1, 'enable')
    )
    name = models.CharField(max_length=30, help_text='网卡名')
    mac = models.CharField(max_length=50, help_text='MAC地址')
    ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, help_text='ip地址')
    state = models.SmallIntegerField(db_index=True, choices=STATE_CHOICE, default=0, help_text='网卡状态')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='networkinterface')

    def __str__(self):
        return self.name

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class Memory(models.Model):
    serialnum = models.CharField(max_length=100, null=True, blank=True, help_text='内存序列号')
    part_number = models.CharField(max_length=100, null=True, blank=True, help_text='内存条物理号码')
    speed = models.CharField(max_length=50, help_text='内存速率')
    manufacturer = models.CharField(max_length=100, help_text='生产厂商', null=True, blank=True)
    locator = models.CharField(max_length=20, help_text='安装位置')
    size = models.CharField(max_length=20, help_text='内存大小')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='memory')

    def __str__(self):
        return self.size

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class CPU(models.Model):
    socket = models.CharField(max_length=20, help_text='CPU槽位')
    family = models.CharField(max_length=10, help_text='系列')
    version = models.CharField(max_length=80, blank=True, null=True,
                               help_text='型号')
    speed = models.CharField(max_length=50, help_text='CPU 速率')
    cores = models.SmallIntegerField(help_text='cpu 核心数')
    characteristics = models.CharField(max_length=200, help_text='特性')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='cpu')

    def __str__(self):
        return self.family

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class Disk(models.Model):
    size = models.CharField(max_length=50, help_text='磁盘大小')
    serialnum = models.CharField(max_length=100, null=True, blank=True, help_text='序列号')
    speed = models.CharField(max_length=50, help_text='转速', null=True, blank=True)
    manufacturer = models.CharField(max_length=100, help_text='生产厂商', null=True, blank=True)
    locator = models.CharField(max_length=20, help_text='安装位置')
    interface_type = models.CharField(max_length=20, help_text='接口类型', null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='disk')

    def __str__(self):
        return self.size

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class HWSystem(models.Model):
    serialnum = models.CharField(max_length=100, help_text='序列号')
    manufacturer = models.CharField(max_length=100, help_text='生产厂商')
    product_name = models.CharField(max_length=100, help_text='机器型号')
    uuid = models.CharField(max_length=50, help_text='UUID', null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='hw_system')

    def __str__(self):
        return self.product_name

    @classmethod
    def get_help_text(cls, field_name):
        for field in cls._meta.fields:
            if field.name == field_name:
                return field.help_text
        return field_name


class History(models.Model):
    OP_CHOICE = (
        ('d', 'delete'),
        ('u', 'update'),
        ('a', 'add')
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    old = models.CharField(max_length=200, null=True, blank=True)
    new = models.CharField(max_length=200, null=True, blank=True)
    operate = models.CharField(max_length=6, choices=OP_CHOICE)

    def __str__(self):
        return self.field

