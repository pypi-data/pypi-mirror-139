from dataclasses import dataclass, field 
import datetime


@dataclass
class PrivateProductionFlowback:
    api_10: str
    _api_10: str = field(init=False, repr=False)

    @property
    def api_10(self) -> str:
        return self.api_10

    @api_10.setter
    def api_10(self, api_10:str) -> None:
        self._api_10 = api_10
    
    api_12: str
    _api_12: str = field(init=False, repr=False)

    @property
    def api_12(self) -> str:
        return self.api_12

    @api_12.setter
    def api_12(self, api_12:str) -> None:
        self._api_12 = api_12
    
    api_14: str
    _api_14: str = field(init=False, repr=False)

    @property
    def api_14(self) -> str:
        return self.api_14

    @api_14.setter
    def api_14(self, api_14:str) -> None:
        self._api_14 = api_14

    basin: str
    _basin: str = field(init=False, repr=False)

    @property
    def basin(self) -> str:
        return self.basin

    @basin.setter
    def basin(self, basin:str) -> None:
        self._basin = basin

    bottom_hole_pressure_psi: float
    _bottom_hole_pressure_psi: float = field(init=False, repr=False)

    @property
    def bottom_hole_pressure_psi(self) -> float:
        return self.bottom_hole_pressure_psi

    @bottom_hole_pressure_psi.setter
    def bottom_hole_pressure_psi(self, bottom_hole_pressure_psi:float) -> None:
        self._bottom_hole_pressure_psi = bottom_hole_pressure_psi


    casing_pressure_psi: float
    _casing_pressure_psi: float = field(init=False, repr=False)

    @property
    def casing_pressure_psi(self) -> float:
        return self.casing_pressure_psi

    @casing_pressure_psi.setter
    def casing_pressure_psi(self, casing_pressure_psi:float) -> None:
        self._casing_pressure_psi = casing_pressure_psi
    

    line_pressure_psi: float
    _line_pressure_psi: float = field(init=False, repr=False)

    @property
    def line_pressure_psi(self) -> float:
        return self.line_pressure_psi

    @line_pressure_psi.setter
    def line_pressure_psi(self, line_pressure_psi:float) -> None:
        self._line_pressure_psi = line_pressure_psi

    tubing_pressure_psi: float
    _tubing_pressure_psi: float = field(init=False, repr=False)

    @property
    def tubing_pressure_psi(self) -> float:
        return self.tubing_pressure_psi

    @tubing_pressure_psi.setter
    def tubing_pressure_psi(self, tubing_pressure_psi:float) -> None:
        self._tubing_pressure_psi = tubing_pressure_psi

    choke_xx64: float
    _choke_xx64: float = field(init=False, repr=False)

    @property
    def choke_xx64(self) -> float:
        return self.choke_xx64

    @choke_xx64.setter
    def choke_xx64(self, choke_xx64:float) -> None:
        self._choke_xx64 = choke_xx64

    date: datetime.datetime
    _date: datetime.datetime = field(init=False, repr=False)

    @property
    def date(self) -> datetime.datetime:
        return self.date

    @date.setter
    def date(self, date:datetime.datetime) -> None:
        self._date = date

    flow_path: str
    _flow_path: str = field(init=False, repr=False)

    @property
    def flow_path(self) -> str:
        return self.flow_path

    @flow_path.setter
    def flow_path(self, flow_path:str) -> None:
        self._flow_path = flow_path

    gaslift_mcfd: float
    _gaslift_mcfd: float = field(init=False, repr=False)

    @property
    def gaslift_mcfd(self) -> float:
        return self.gaslift_mcfd

    @gaslift_mcfd.setter
    def gaslift_mcfd(self, gaslift_mcfd:float) -> None:
        self._gaslift_mcfd = gaslift_mcfd
    

    hour_of_day: float
    _hour_of_day: float = field(init=False, repr=False)

    @property
    def hour_of_day(self) -> float:
        return self.hour_of_day

    @hour_of_day.setter
    def hour_of_day(self, hour_of_day:float) -> None:
        self._hour_of_day = hour_of_day

    notes: str
    _notes: str = field(init=False, repr=False)

    @property
    def notes(self) -> str:
        return self.notes

    @notes.setter
    def notes(self, notes:str) -> None:
        self._notes = notes

    points_in_zone: float
    _points_in_zone: float = field(init=False, repr=False)

    @property
    def points_in_zone(self) -> float:
        return self.points_in_zone

    @points_in_zone.setter
    def points_in_zone(self, points_in_zone:float) -> None:
        self._points_in_zone = points_in_zone
    
    oil_bopd: float
    _oil_bopd: float = field(init=False, repr=False)

    @property
    def oil_bopd(self) -> float:
        return self.oil_bopd

    @oil_bopd.setter
    def oil_bopd(self, oil_bopd:float) -> None:
        self._oil_bopd = oil_bopd
    
    process: str
    _process: str = field(init=False, repr=False)

    @property
    def process(self) -> str:
        return self.process

    @process.setter
    def process(self, process:str) -> None:
        self._process = process

    
    produced_sand_gals: float
    _produced_sand_gals: float = field(init=False, repr=False)

    @property
    def produced_sand_gals(self) -> float:
        return self.produced_sand_gals

    @produced_sand_gals.setter
    def produced_sand_gals(self, produced_sand_gals:float) -> None:
        self._produced_sand_gals = produced_sand_gals
    
    pump_pressure_psi: float
    _pump_pressure_psi: float = field(init=False, repr=False)

    @property
    def pump_pressure_psi(self) -> float:
        return self.pump_pressure_psi

    @pump_pressure_psi.setter
    def pump_pressure_psi(self, pump_pressure_psi:float) -> None:
        self._pump_pressure_psi = pump_pressure_psi

    pump_type: str
    _pump_type: str = field(init=False, repr=False)

    @property
    def pump_type(self) -> str:
        return self.pump_type

    @pump_type.setter
    def pump_type(self, pump_type:str) -> None:
        self._pump_type = pump_type

    source: str
    _source: str = field(init=False, repr=False)

    @property
    def source(self) -> str:
        return self.source

    @source.setter
    def source(self, source:str) -> None:
        self._source = source
    
    water_bwpd: float
    _water_bwpd: float = field(init=False, repr=False)

    @property
    def water_bwpd(self) -> float:
        return self.water_bwpd

    @water_bwpd.setter
    def water_bwpd(self, water_bwpd:float) -> None:
        self._water_bwpd = water_bwpd

    date_updated: datetime.datetime
    _date_updated: datetime.datetime = field(init=False, repr=False)

    @property
    def date_updated(self) -> datetime.datetime:
        return self.date_updated

    @date_updated.setter
    def date_updated(self, date_updated:datetime.datetime) -> None:
        self._date_updated = date_updated
 
    
    load_timestamp: datetime.datetime
    _load_timestamp: datetime.datetime = field(init=False, repr=False)

    @property
    def load_timestamp(self) -> datetime.datetime:
        return self.load_timestamp

    @load_timestamp.setter
    def load_timestamp(self, load_timestamp:datetime.datetime) -> None:
        self._load_timestamp = load_timestamp





