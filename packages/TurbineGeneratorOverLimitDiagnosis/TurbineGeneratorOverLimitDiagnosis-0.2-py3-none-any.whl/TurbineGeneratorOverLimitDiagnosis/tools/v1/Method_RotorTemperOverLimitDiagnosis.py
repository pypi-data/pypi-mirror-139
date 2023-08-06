from .GenericMethods import *


class RotorTemperOverLimitDiagnosis(TwoThresholdsGreaterEqualToAndLesserThan):
    def __init__(self, *args):
        """
        转子运行温度超限判断,单位均为℃

        :math:`T < 110, 转子运行温度不超限`

        :math:`110 \\le T < 125, 转子运行温度超限一级报警`

        :math:`T \\ge 125, 转子运行温度超限二级报警`


        [1] 参数
        ----------
        lowerThreshold:
            float,一级报警限,默认110
        higherThreshold:
            float,二级报警限,默认125
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "100": "转子运行温度不超限",

                    "010": "转子运行温度超限一级报警",

                    "001": "转子运行温度超限二级报警"

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
        >>> obj = RotorTemperOverLimitDiagnosis(110, 125, {"100": "OK", "010": "1st", "001": "2nd"})
        >>> print(obj.diagnosis(14))
        >>> print(obj.diagnosis(110))
        >>> print(obj.diagnosis(115))
        >>> print(obj.diagnosis(125))
        >>> print(obj.diagnosis(130))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "100": "转子运行温度不超限",
            "010": "转子运行温度超限一级报警",
            "001": "转子运行温度超限二级报警"
        }
        super().__init__(*args if len(args)==3 else (110, 125, truthTable))
