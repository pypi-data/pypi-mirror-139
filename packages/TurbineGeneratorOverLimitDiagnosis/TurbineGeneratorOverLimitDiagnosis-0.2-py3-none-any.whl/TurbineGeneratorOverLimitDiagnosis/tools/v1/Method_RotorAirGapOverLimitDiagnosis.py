from .GenericMethods import *


class RotorAirGapOverLimitDiagnosis(OneThresholdLesserEqualToAndGreaterThan):
    def __init__(self, *args):
        """
        转子气隙（不均匀度）超限判断

        :math:`T \\le 0.04, 转子气隙运行值正常`

        :math:`T > 0.04, 转子气隙运行值异常`


        [1] 参数
        ----------
        threshold:
            float,报警限,默认0.04
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "10": "转子气隙运行值正常",

                    "01": "转子气隙运行值异常",
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
        >>> obj = RotorAirGapOverLimitDiagnosis(0.04, {"10": "OK", "01": "alarm"})
        >>> print(obj.diagnosis(0.03))
        >>> print(obj.diagnosis(0.04))
        >>> print(obj.diagnosis(0.05))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "10": "转子气隙运行值正常",
            "01": "转子气隙运行值异常",
        }
        super().__init__(*args if len(args)==2 else (0.04, truthTable))
