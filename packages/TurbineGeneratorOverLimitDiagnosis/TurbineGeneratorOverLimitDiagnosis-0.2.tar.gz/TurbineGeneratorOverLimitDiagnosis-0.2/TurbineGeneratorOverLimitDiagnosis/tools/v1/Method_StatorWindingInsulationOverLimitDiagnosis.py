from .GenericMethods import *


class StatorWindingInsulationOverLimitDiagnosis(TwoThresholdsGreaterEqualToAndLesserThan):
    def __init__(self, *args):
        """
        定子绕组绝缘超限判断

        :math:`T < 0.6, 定子绕组绝缘超限二级报警`

        :math:`0.6 \\le T < 0.8, 定子绕组绝缘超限一级报警`

        :math:`T \\ge 0.8, 定子绕组绝缘不超限`


        [1] 参数
        ----------
        lowerThreshold:
            float,一级报警限,默认0.6
        higherThreshold:
            float,二级报警限,默认0.8
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "100": "定子绕组绝缘超限二级报警",

                    "010": "定子绕组绝缘超限一级报警",

                    "001": "定子绕组绝缘不超限"

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
        >>> obj = StatorWindingInsulationOverLimitDiagnosis(0.6， 0.8, {"100": "2nd", "010": "1st", "001": "OK"})
        >>> print(obj.diagnosis(0.5))
        >>> print(obj.diagnosis(0.6))
        >>> print(obj.diagnosis(0.7))
        >>> print(obj.diagnosis(0.8))
        >>> print(obj.diagnosis(0.81))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "100": "定子绕组绝缘超限二级报警",
            "010": "定子绕组绝缘超限一级报警",
            "001": "定子绕组绝缘不超限"
        }
        super().__init__(*args if len(args)==3 else (0.6, 0.8, truthTable))
