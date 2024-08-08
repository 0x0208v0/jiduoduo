from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Host(_message.Message):
    __slots__ = ("platform", "platform_version", "cpu", "mem_total", "disk_total", "swap_total", "arch", "virtualization", "boot_time", "ip", "country_code", "version", "gpu")
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEM_TOTAL_FIELD_NUMBER: _ClassVar[int]
    DISK_TOTAL_FIELD_NUMBER: _ClassVar[int]
    SWAP_TOTAL_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    VIRTUALIZATION_FIELD_NUMBER: _ClassVar[int]
    BOOT_TIME_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    platform: str
    platform_version: str
    cpu: _containers.RepeatedScalarFieldContainer[str]
    mem_total: int
    disk_total: int
    swap_total: int
    arch: str
    virtualization: str
    boot_time: int
    ip: str
    country_code: str
    version: str
    gpu: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, platform: _Optional[str] = ..., platform_version: _Optional[str] = ..., cpu: _Optional[_Iterable[str]] = ..., mem_total: _Optional[int] = ..., disk_total: _Optional[int] = ..., swap_total: _Optional[int] = ..., arch: _Optional[str] = ..., virtualization: _Optional[str] = ..., boot_time: _Optional[int] = ..., ip: _Optional[str] = ..., country_code: _Optional[str] = ..., version: _Optional[str] = ..., gpu: _Optional[_Iterable[str]] = ...) -> None: ...

class State(_message.Message):
    __slots__ = ("cpu", "mem_used", "swap_used", "disk_used", "net_in_transfer", "net_out_transfer", "net_in_speed", "net_out_speed", "uptime", "load1", "load5", "load15", "tcp_conn_count", "udp_conn_count", "process_count", "temperatures", "gpu")
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEM_USED_FIELD_NUMBER: _ClassVar[int]
    SWAP_USED_FIELD_NUMBER: _ClassVar[int]
    DISK_USED_FIELD_NUMBER: _ClassVar[int]
    NET_IN_TRANSFER_FIELD_NUMBER: _ClassVar[int]
    NET_OUT_TRANSFER_FIELD_NUMBER: _ClassVar[int]
    NET_IN_SPEED_FIELD_NUMBER: _ClassVar[int]
    NET_OUT_SPEED_FIELD_NUMBER: _ClassVar[int]
    UPTIME_FIELD_NUMBER: _ClassVar[int]
    LOAD1_FIELD_NUMBER: _ClassVar[int]
    LOAD5_FIELD_NUMBER: _ClassVar[int]
    LOAD15_FIELD_NUMBER: _ClassVar[int]
    TCP_CONN_COUNT_FIELD_NUMBER: _ClassVar[int]
    UDP_CONN_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROCESS_COUNT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURES_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    cpu: float
    mem_used: int
    swap_used: int
    disk_used: int
    net_in_transfer: int
    net_out_transfer: int
    net_in_speed: int
    net_out_speed: int
    uptime: int
    load1: float
    load5: float
    load15: float
    tcp_conn_count: int
    udp_conn_count: int
    process_count: int
    temperatures: _containers.RepeatedCompositeFieldContainer[State_SensorTemperature]
    gpu: float
    def __init__(self, cpu: _Optional[float] = ..., mem_used: _Optional[int] = ..., swap_used: _Optional[int] = ..., disk_used: _Optional[int] = ..., net_in_transfer: _Optional[int] = ..., net_out_transfer: _Optional[int] = ..., net_in_speed: _Optional[int] = ..., net_out_speed: _Optional[int] = ..., uptime: _Optional[int] = ..., load1: _Optional[float] = ..., load5: _Optional[float] = ..., load15: _Optional[float] = ..., tcp_conn_count: _Optional[int] = ..., udp_conn_count: _Optional[int] = ..., process_count: _Optional[int] = ..., temperatures: _Optional[_Iterable[_Union[State_SensorTemperature, _Mapping]]] = ..., gpu: _Optional[float] = ...) -> None: ...

class State_SensorTemperature(_message.Message):
    __slots__ = ("name", "temperature")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    name: str
    temperature: float
    def __init__(self, name: _Optional[str] = ..., temperature: _Optional[float] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ("id", "type", "data")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: int
    data: str
    def __init__(self, id: _Optional[int] = ..., type: _Optional[int] = ..., data: _Optional[str] = ...) -> None: ...

class TaskResult(_message.Message):
    __slots__ = ("id", "type", "delay", "data", "successful")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: int
    delay: float
    data: str
    successful: bool
    def __init__(self, id: _Optional[int] = ..., type: _Optional[int] = ..., delay: _Optional[float] = ..., data: _Optional[str] = ..., successful: bool = ...) -> None: ...

class Receipt(_message.Message):
    __slots__ = ("proced",)
    PROCED_FIELD_NUMBER: _ClassVar[int]
    proced: bool
    def __init__(self, proced: bool = ...) -> None: ...

class IOStreamData(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class GeoIP(_message.Message):
    __slots__ = ("ip", "country_code")
    IP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    ip: str
    country_code: str
    def __init__(self, ip: _Optional[str] = ..., country_code: _Optional[str] = ...) -> None: ...
