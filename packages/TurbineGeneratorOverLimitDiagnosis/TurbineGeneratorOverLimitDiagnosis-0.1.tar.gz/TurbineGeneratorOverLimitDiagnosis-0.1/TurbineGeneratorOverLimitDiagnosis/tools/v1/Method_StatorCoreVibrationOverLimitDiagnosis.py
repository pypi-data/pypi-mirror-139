from .GenericMethods import *


class StatorCoreVibrationOverLimitDiagnosis(OneThresholdLesserEqualToAndGreaterThan):
    def __init__(self, *args):
        """
        定子铁芯振动超限判断,单位均为mm

        :math:`T \\le 0.03, 定子铁芯振动不超限`

        :math:`T > 0.03, 定子铁芯振动超限报警`


        [1] 参数
        ----------
        threshold:
            float,报警限,默认0.03
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "10": "定子铁芯振动不超限",

                    "01": "定子铁芯振动超限报警",
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
        >>> obj = StatorCoreVibrationOverLimitDiagnosis(0.03, {"10": "OK", "01": "alarm"})
        >>> print(obj.diagnosis(0.02))
        >>> print(obj.diagnosis(0.03))
        >>> print(obj.diagnosis(0.031))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "10": "定子铁芯振动不超限",
            "01": "定子铁芯振动超限报警",
        }
        super().__init__(*args if len(args)==2 else (0.03, truthTable))
