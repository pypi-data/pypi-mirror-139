from .GenericMethods import *


class TurbineGuideBearingSwingOverLimitDiagnosis(TwoThresholdsGreaterEqualToAndLesserThan):
    def __init__(self, *args):
        """
        水导摆度运行值超限判断,单位均为mm

        :math:`T < 0.18, 水导摆度运行值不超限`

        :math:`0.18 \\le T < 0.23, 水导摆度运行值超限一级报警`

        :math:`T \\ge 0.23, 水导摆度运行值超限二级报警`


        [1] 参数
        ----------
        lowerThreshold:
            float,一级报警限,默认0.18
        higherThreshold:
            float,二级报警限,默认0.23
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "100": "水导摆度运行值不超限",

                    "010": "水导摆度运行值超限一级报警",

                    "001": "水导摆度运行值超限二级报警"

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
        >>> obj = TurbineGuideBearingSwingOverLimitDiagnosis(0.18, 0.23, {"100": "OK", "010": "1st", "001": "2nd"})
        >>> print(obj.diagnosis(0.14))
        >>> print(obj.diagnosis(0.18))
        >>> print(obj.diagnosis(0.22))
        >>> print(obj.diagnosis(0.23))
        >>> print(obj.diagnosis(0.24))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "100": "水导摆度运行值不超限",
            "010": "水导摆度运行值超限一级报警",
            "001": "水导摆度运行值超限二级报警"
        }
        super().__init__(*args if len(args)==3 else (0.18, 0.23, truthTable))
