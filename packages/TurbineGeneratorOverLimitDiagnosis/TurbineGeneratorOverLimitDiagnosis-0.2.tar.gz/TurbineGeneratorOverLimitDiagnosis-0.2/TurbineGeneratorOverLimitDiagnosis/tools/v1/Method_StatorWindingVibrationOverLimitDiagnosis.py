from .GenericMethods import *


class StatorWindingVibrationOverLimitDiagnosis(OneThresholdLesserEqualToAndGreaterThan):
    def __init__(self, *args):
        """
        定子绕组振动超限判断,单位均为mm

        :math:`T \\le 0.045, 定子绕组振动不超限`

        :math:`T > 0.045, 定子绕组振动超限报警`



        [1] 参数
        ----------
        threshold:
            float,报警限,默认0.045
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "10": "定子绕组振动不超限",

                    "01": "定子绕组振动超限报警",
                }

        [2] 方法
        ----------
        diagnosis:
            判断当前输入对判断逻辑的满足情况

        [3] 返回
        -------
        -/-:
            超限判断结论

        [4] 示例1
        --------
        >>> obj = StatorWindingVibrationOverLimitDiagnosis(0.045, {"10": "OK", "01": "alarm"})
        >>> print(obj.diagnosis(0.04))
        >>> print(obj.diagnosis(0.045))
        >>> print(obj.diagnosis(0.05))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "10": "定子绕组运行温度不超限",
            "01": "定子绕组运行温度超限一级报警",
        }
        super().__init__(*args if len(args)==2 else (0.045, truthTable))
