import requests
import os
import platform


def send_usage_event_jitsu(payload: dict = None):
    jitsu_api_key = 's2s.f4gygbral3fiy5z2nry05.wupt3w889kd08xbaspe2b4r'  # Your Jitsu server API key here
    if os.environ.get('TELEMETRY_DISABLED', 'false') == 'true':
        return

    if payload is None:
        payload = {}

    payload['parsed_ua'] = {'os_version': platform.release(), 'os_family': platform.system(), 'os_machine': platform.machine()}
    try:
        requests.post("https://t.jitsu.com/api/v1/s2s/event", params={'token': jitsu_api_key}, json=payload, timeout=2)
    except:
        pass


