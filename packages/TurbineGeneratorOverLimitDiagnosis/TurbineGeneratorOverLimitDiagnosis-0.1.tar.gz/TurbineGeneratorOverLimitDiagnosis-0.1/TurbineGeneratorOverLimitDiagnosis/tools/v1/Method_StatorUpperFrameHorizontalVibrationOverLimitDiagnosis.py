from .GenericMethods import *


class StatorUpperFrameHorizontalViberOverLimitDiagnosis(TwoThresholdsGreaterEqualToAndLesserThan):
    def __init__(self, *args):
        """
        定子上机架水平振动超限判断,单位均为mm

        :math:`T < 0.07, 定子上机架水平振动不超限`

        :math:`0.07 \\le T < 0.08, 定子上机架水平振动超限一级报警`

        :math:`T \\ge 0.08, 定子上机架水平振动超限二级报警`


        [1] 参数
        ----------
        lowerThreshold:
            float,一级报警限,默认0.07
        higherThreshold:
            float,二级报警限,默认0.08
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "100": "定子上机架水平振动不超限",

                    "010": "定子上机架水平振动超限一级报警",

                    "001": "定子上机架水平振动超限二级报警"

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
        >>> obj = StatorUpperFrameHorizontalViberOverLimitDiagnosis(0.07, 0.08, {"100": "OK", "010": "1st", "001": "2nd"})
        >>> print(obj.diagnosis(0.06))
        >>> print(obj.diagnosis(0.07))
        >>> print(obj.diagnosis(0.075))
        >>> print(obj.diagnosis(0.08))
        >>> print(obj.diagnosis(0.081))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "100": "定子上机架水平振动不超限",
            "010": "定子上机架水平振动超限一级报警",
            "001": "定子上机架水平振动超限二级报警"
        }
        super().__init__(*args if len(args)==3 else (0.07, 0.08, truthTable))
