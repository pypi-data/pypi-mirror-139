"""
Classes
-------
1.StatorWindingTemperOverLimitDiagnosis:定子绕组温度超限评估
2.BusRingTemperOverLimitDiagnosis:定子汇流环温度超限评估
3.StatorCoreTemperOverLimitDiagnosis:定子铁芯温度超限评估
4.RotorTemperOverLimitDiagnosis:转子温度超限评估
5.UpperGuideBearingSwingOverLimitDiagnosis:上导轴承摆度超限评估
6.TurbineGuideBearingSwingOverLimitDiagnosis:水导轴承摆度超限评估
7.StatorFrameHorizontalVibrationOverLimitDiagnosis:定子机座水平振动超限评估
8.StatorUpperFrameHorizontalVibrationOverLimitDiagnosis:定子上机架水平振动超限评估
9.SupportCoverHorizontalVibrationOverLimitDiagnosis:支持盖水平振动超限评估
10.StatorWindingInsulationOverLimitDiagnosis:定子绕组绝缘超限评估
11.StatorCoreVibrationOverLimitDiagnosis:定子铁芯振动超限评估
12.StatorWindingVibrationOverLimitDiagnosis:定子绕组振动超限评估
13.RotorExcitingCurrentOverLimitDiagnosis:转子励磁电流实测值与预测值比率超限评估
14.RotorAirGapOverLimitDiagnosis:转子气隙（不均匀度）超限判断


GenericMethods
---------
1. TwoThresholdsGreaterEqualToAndLesserThan: 如 T<T_min, T_min<=T<T_max, T_max<T的判断,输出是上述公式的真值表编码
2. OneThresholdLesserEqualToAndGreaterThan: 如 T<=T_0, T_0<T的判断,输出是上述公式的真值表编码

"""

from . import *
