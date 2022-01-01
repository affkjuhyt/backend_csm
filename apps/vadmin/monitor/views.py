from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from rest_framework.request import Request

from apps.vadmin.monitor.filters import ServerFilter, MonitorFilter
from apps.vadmin.monitor.models import Server, Monitor, SysFiles
from apps.vadmin.monitor.serializers import ServerSerializer, MonitorSerializer, UpdateServerSerializer
from apps.vadmin.op_drf.response import SuccessResponse, ErrorResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission
from apps.vadmin.system.models import ConfigSettings


class ServerModelViewSet(CustomModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    update_serializer_class = UpdateServerSerializer
    filter_class = ServerFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'


class MonitorModelViewSet(CustomModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    filter_class = MonitorFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'

    def get_rate_info(self, request: Request, *args, **kwargs):
        pk = kwargs.get("pk")
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(server__id=pk).order_by("create_datetime")
        queryset_count = queryset.count()
        Interval_num = 1 if queryset_count < 200 else int(queryset_count / 100)
        queryset = queryset.values('cpu_sys', 'mem_num', 'mem_sys', 'create_datetime')[::Interval_num][:100]
        data = {
            "cpu": [],
            "memory": [],
            "datetime": [],
        }
        for ele in queryset:
            data["cpu"].append(round(float(ele.get('cpu_sys', 0)), 2))
            data["datetime"].append(ele.get('create_datetime').strftime('%Y-%m-%d %H:%M:%S'))
            data["memory"].append(round(float(ele.get('mem_num', 0)), 4) and round(float(ele.get('mem_sys', 0)) /
                                                                                   float(ele.get('mem_num', 0)) * 100,
                                                                                   2))
        return SuccessResponse(data=data)

    def get_monitor_info(self, request: Request, *args, **kwargs):
        pk = kwargs.get("pk")
        instance = Monitor.objects.filter(server__id=pk).order_by("-create_datetime").first()
        if not instance:
            return ErrorResponse(msg="Không tìm thấy id thông tin máy chủ")
        serializer = self.get_serializer(instance)
        data = serializer.data
        return SuccessResponse(data={
            "cpu": {
                "total": int(data.get('cpu_num'), 0),
                "used": "",
                "rate": float(data.get('cpu_sys', 0)) / 100,
                "unit": "核心",
            },
            "memory": {
                "total": int(int(data.get('mem_num', 0)) / 1024),
                "used": int(int(data.get('mem_sys', 0)) / 1024),
                "rate": int(data.get('mem_num', 0)) and round(int(data.get('mem_sys', 0)) /
                                                              int(data.get('mem_num', 0)), 4),
                "unit": "MB",
            },
            "disk": [{
                "dir_name": ele.get('dir_name'),
                "total": int(int(ele.get('total', 0)) / 1024 / 1024 / 1024),
                "used": int(int(ele.get('disk_sys', 0)) / 1024 / 1024 / 1024),
                "rate": int(ele.get('total', 0)) and round(int(ele.get('disk_sys', 0)) / int(ele.get('total', 0)),
                                                           4),
                "unit": "GB",
            } for ele in SysFiles.objects.filter(monitor=instance).values('dir_name', 'total', 'disk_sys')]
        })

    def enabled_monitor_info(self, request: Request, *args, **kwargs):
        enabled = request.query_params.get('enabled', None)
        save_days = request.query_params.get('save_days', None)
        interval = request.query_params.get('interval', None)
        periodictask_obj = PeriodicTask.objects.filter(task='apps.vadmin.monitor.tasks.get_monitor_info').first()
        if not periodictask_obj:
            intervalschedule_obj, _ = IntervalSchedule.objects.get_or_create(every=5, period="seconds")
            periodictask_obj = PeriodicTask()
            periodictask_obj.task = "apps.vadmin.monitor.tasks.get_monitor_info"
            periodictask_obj.name = "Obtain system monitoring information regularly"
            periodictask_obj.interval = intervalschedule_obj
            periodictask_obj.enabled = False
            periodictask_obj.save()

        clean_task_obj = PeriodicTask.objects.filter(
            task='apps.vadmin.monitor.tasks.clean_surplus_monitor_info').first()
        if not clean_task_obj:
            crontab_obj, _ = CrontabSchedule.objects.get_or_create(day_of_month="*", day_of_week="*", hour="1",
                                                                   minute="0", month_of_year="*")
            clean_task_obj = PeriodicTask()
            clean_task_obj.task = "apps.vadmin.monitor.tasks.clean_surplus_monitor_info"
            clean_task_obj.name = "Regularly clean up redundant-system monitoring information"
            clean_task_obj.crontab = crontab_obj
            clean_task_obj.enabled = True
            clean_task_obj.save()
        config_obj = ConfigSettings.objects.filter(configKey='sys.monitor.info.save_days').first()
        if not config_obj:
            config_obj = ConfigSettings()
            config_obj.configKey = "sys.monitor.info.save_days"
            config_obj.configName = "Regularly clean up redundant system monitoring information"
            config_obj.configValue = "30"
            config_obj.configType = "Y"
            config_obj.status = "1"
            config_obj.remark = "Clean up redundant information regularly-system monitoring information, 30 days by default"
            config_obj.save()

        if enabled:
            periodictask_obj.enabled = True if enabled == "1" else False
            periodictask_obj.save()

            clean_task_obj.enabled = True if enabled == "1" else False
            clean_task_obj.save()
        if save_days and config_obj:
            config_obj.configValue = save_days
            config_obj.save()
        if interval:
            periodictask_obj.interval.every = interval
            periodictask_obj.interval.save()
        return SuccessResponse(data={
            "enabled": periodictask_obj.enabled,
            "interval": periodictask_obj.interval.every,
            "save_days": config_obj.configValue if config_obj else "30",
        })

    def clean_all(self, request: Request, *args, **kwargs):
        self.get_queryset().delete()
        return SuccessResponse(msg="Empty successfully")
