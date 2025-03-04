"""
This module contains definitions for string constants used to communicate with Rigol100z series oscilloscopes.
"""


class ScopeModel:
    DS1104Z_S_Plus = "DS1104Z-S Plus"
    DS1074Z_S_Plus = "DS1074Z-S Plus"
    DS1104Z_Plus = "DS1104Z Plus"
    DS1104Z = "DS1104Z"  # Hacked model
    DS1074Z_Plus = "DS1074Z Plus"
    DS1054Z = "DS1054Z"


class EAcquireMode:
    Normal = "NORM"
    Averages = "AVER"
    Peak = "PEAK"
    HighResolution = "HRES"


class EDisplayMode:
    Vectors = "VEC"
    Dots = "DOTS"


class EDisplayGrid:
    Full = "FULL"
    Half = "HALF"
    NoGrid = "NONE"


class EEventtableFormat:
    Hex = "HEX"
    Ascii = "ASC"
    Decimal = "DEC"


class EEventtableViewFormat:
    Package = "PACK"
    Detail = "DET"
    Payload = "PAYL"


class EEventtableColumn:
    Data = "DATA"
    Tx = "TX"
    Rx = "RX"
    MISO = "MISO"
    MOSI = "MOSI"


class EMeasureStatisticMode:
    Difference = "DIFF"
    Extremum = "EXTR"


class EMeasureItem:
    VoltageMax = "VMAX"
    VoltageMin = "VMIN"
    VoltagePeakToPeak = "VPP"
    VoltageTop = "VTOP"
    VoltageBase = "VBASe"
    VoltageAmplitude = "VAMP"

    VoltageUpper = "VUP"
    VoltageMid = "VMID"
    VoltageLower = "VLOW"
    VoltageAverage = "VAVG"

    VoltageRMS = "VRMS"
    VRmsPeriod = "PVRMS"

    VoltageOvershoot = "OVER"
    VoltagePreshoot = "PRES"

    Area = "MAR"
    AreaPeriod = "MPAR"

    Period = "PER"

    Frequency = "FREQ"

    RiseTime = "RTIM"
    FallTime = "FTIM"

    WidthPositive = "PWID"
    WidthNegative = "NWID"

    DutyPositive = "PDUT"
    DutyNegative = "NDUT"

    DelayRise = "RDEL"
    DelayFall = "FDEL"

    PhaseRise = "RPH"
    PhaseFall = "FPH"

    TVMax = "TVMAX"  # time to voltage max?
    TVMin = "TVMIN"  # time to voltage min?

    SlewRatePositive = "PSLEW"
    SlewRateNegative = "NSLEW"

    Variance = "VARI"

    PulsesPositive = "PPUL"
    PulsesNegative = "NPUL"
    EdgesPositive = "PEDG"
    EdgesNegative = "NEDG"


class EMeasurementStatisticItemType:
    Maximum = "MAX"
    Minimum = "MIN"
    Current = "CURR"
    Average = "AVER"
    Deviation = "DEV"


class ETimebaseMode:
    Main = 'main'
    XY = 'xy'
    Roll = 'roll'


class ESource:
    D0 = "D0"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"
    D5 = "D5"
    D6 = "D6"
    D7 = "D7"
    D8 = "D8"
    D9 = "D9"
    D10 = "D10"
    D11 = "D11"
    D12 = "D12"
    D13 = "D13"
    D14 = "D14"
    D15 = "D15"

    Ch1 = "CHAN1"
    Ch2 = "CHAN2"
    Ch3 = "CHAN3"
    Ch4 = "CHAN4"

    Math = "MATH"


sources_digital = {
    ESource.D0,
    ESource.D1,
    ESource.D2,
    ESource.D3,
    ESource.D4,
    ESource.D5,
    ESource.D6,
    ESource.D7,
    ESource.D8,
    ESource.D9,
    ESource.D10,
    ESource.D11,
    ESource.D12,
    ESource.D13,
    ESource.D14,
    ESource.D15,
}

sources_analog = {
    ESource.Ch1,
    ESource.Ch2,
    ESource.Ch3,
    ESource.Ch4,
}

sources_math = {"MATH"}


class EWaveformMode:
    Normal = "NORM"
    Max = "MAX"
    Raw = "RAW"


waveform_modes = {EWaveformMode.Normal, EWaveformMode.Max, EWaveformMode.Raw}


class EWaveformReadFormat:
    Word = "WORD"
    Byte = "BYTE"
    Ascii = "ASC"


waveform_read_formats = {EWaveformReadFormat.Word, EWaveformReadFormat.Byte, EWaveformReadFormat.Ascii}
