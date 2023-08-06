from .GenericMethods import *


class RotorExcitingCurrentOverLimitDiagnosis(OneThresholdLesserEqualToAndGreaterThan):
    def __init__(self, *args):
        """
        转子励磁电流实测值与预测值比率超限判断

        :math:`T \\le 0.15, 励磁电流运行值正常`

        :math:`T > 0.15, 励磁电流运行值异常`

        [1] 参数
        ----------
        threshold:
            float,报警限,默认0.15
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "10": "励磁电流运行值正常",

                    "01": "励磁电流运行值异常",
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
        >>> obj = RotorExcitingCurrentOverLimitDiagnosis(0.15, {"10": "OK", "01": "Abnormal"})
        >>> print(obj.diagnosis(0.14))
        >>> print(obj.diagnosis(0.15))
        >>> print(obj.diagnosis(0.16))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "10": "励磁电流运行值正常",
            "01": "励磁电流运行值异常",
        }
        super().__init__(*args if len(args)==2 else (0.15, truthTable))
