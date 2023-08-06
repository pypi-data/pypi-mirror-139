from .GenericMethods import *


class UpperGuideBearingSwingOverLimitDiagnosis(TwoThresholdsGreaterEqualToAndLesserThan):
    def __init__(self, *args):
        """
        上导摆度运行值超限判断,单位均为mm

        :math:`T < 0.15, 上导摆度运行值不超限`

        :math:`0.15 \\le T < 0.20, 上导摆度运行值超限一级报警`

        :math:`T \\ge 0.20, 上导摆度运行值超限二级报警`


        [1] 参数
        ----------
        lowerThreshold:
            float,一级报警限,默认0.15
        higherThreshold:
            float,二级报警限,默认0.20
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "100": "上导摆度运行值不超限",

                    "010": "上导摆度运行值超限一级报警",

                    "001": "上导摆度运行值超限二级报警"

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
        >>> obj = UpperGuideBearingSwingOverLimitDiagnosis(0.15, 0.2, {"100": "OK", "010": "1st", "001": "2nd"})
        >>> print(obj.diagnosis(0.14))
        >>> print(obj.diagnosis(0.15))
        >>> print(obj.diagnosis(0.16))
        >>> print(obj.diagnosis(0.2))
        >>> print(obj.diagnosis(0.21))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "100": "上导摆度运行值不超限",
            "010": "上导摆度运行值超限一级报警",
            "001": "上导摆度运行值超限二级报警"
        }
        super().__init__(*args if len(args)==3 else (0.15, 0.2, truthTable))
