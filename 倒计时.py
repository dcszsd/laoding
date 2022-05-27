# coding=utf-8
import obspython
import time

source_name = ""
a = 1
b = 0
c = 0
aa = 0
bb = 0
cc = 0
d = 0


def script_load(setting):
    obspython.script_log(obspython.LOG_INFO, "脚本载入成功")


def script_description():
    return """
    obs倒计时
        by 老丁(博客地址：106.14.134.171)
           
    (版本号：1.0.0)    
    """


def script_properties():
    global a
    global b
    global c
    pros = obspython.obs_properties_create()
    obspython.obs_properties_add_int(pros, "a", "初始时间-小时", 0, 24, 1)
    obspython.obs_properties_add_int(pros, "b", "初始时间-分钟", 0, 59, 1)
    obspython.obs_properties_add_int(pros, "c", "初始时间-秒", 0, 59, 1)
    obspython.obs_properties_add_int(pros, "aa", "添加时间-小时", 0, 24, 1)
    obspython.obs_properties_add_int(pros, "bb", "添加时间-分钟", 0, 59, 1)
    obspython.obs_properties_add_int(pros, "cc", "添加时间-秒", 0, 59, 1)
    text_source = obspython.obs_properties_add_list(pros, "source_name", "文字源", obspython.OBS_COMBO_TYPE_LIST,
                                                    obspython.OBS_COMBO_FORMAT_STRING)
    sources = obspython.obs_enum_sources()
    if sources:
        for source in sources:
            source_id = obspython.obs_source_get_unversioned_id(source)
            if source_id in ("text_gdiplus", "text_ft2_source"):
                name = obspython.obs_source_get_name(source)
                obspython.obs_property_list_add_string(text_source, name, name)
        obspython.source_list_release(sources)
    obspython.obs_properties_add_button(pros, "refresh", "立即刷新数据", refresh_pressed)
    return pros


def refresh_pressed(pros, prop):
    global a1
    global b1
    global c1
    global aa
    global bb
    global cc
    a1 = a1 + aa
    b1 = b1 + bb
    c1 = c1 + cc
    if c1 >= 60:
        c1 = c1 - 60
        b1 = b1 + 1
    if b1 >= 60:
        b1 = b1 - 60
        a1 = a1 + 1


def script_defaults(settings):
    obspython.obs_data_set_default_int(settings, "a", 1)
    obspython.obs_data_set_default_int(settings, "b", 0)
    obspython.obs_data_set_default_int(settings, "c", 0)
    obspython.obs_data_set_default_int(settings, "aa", 0)
    obspython.obs_data_set_default_int(settings, "bb", 0)
    obspython.obs_data_set_default_int(settings, "cc", 0)


def script_update(setting):
    global source_name
    global a
    global b
    global c
    global d
    global aa
    global bb
    global cc
    source_name = obspython.obs_data_get_string(setting, "source_name")
    global a1
    global b1
    global c1
    if d == 0:
        a = obspython.obs_data_get_int(setting, "a")
        b = obspython.obs_data_get_int(setting, "b")
        c = obspython.obs_data_get_int(setting, "c")
        d = 1
        a1 = a
        b1 = b
        c1 = c
    aa = obspython.obs_data_get_int(setting, "aa")
    bb = obspython.obs_data_get_int(setting, "bb")
    cc = obspython.obs_data_get_int(setting, "cc")
    obspython.timer_remove(update)
    obspython.timer_add(update, 1000)




def update():
    global source_name
    global a
    global b
    global c
    global a1
    global b1
    global c1
    source = obspython.obs_get_source_by_name(source_name)

    if source:
        setting = obspython.obs_data_create()
        if c1 <= -1:
            if b1 != 0:
                b1 = b1 - 1
                c1 = 59
            else:
                if a1 != 0:
                    a1 = a1 - 1
                    b1 = 59
                    c1=59
        if b1 <= -1:
            if a1 != 0:
                a1 = a1 - 1
                b1 = 59
        if a1 <= 0 and b1 <= 0 and c1 <= 0:
            mcm = "到点了"
        else:
            mcm = str(a1) + ":" + str(b1) + ":" + str(c1)
            c1 = c1 - 1

        obspython.obs_data_set_string(setting, "text", mcm)
        obspython.obs_source_update(source, setting)
        obspython.obs_data_release(setting)
    obspython.obs_source_release(source)
