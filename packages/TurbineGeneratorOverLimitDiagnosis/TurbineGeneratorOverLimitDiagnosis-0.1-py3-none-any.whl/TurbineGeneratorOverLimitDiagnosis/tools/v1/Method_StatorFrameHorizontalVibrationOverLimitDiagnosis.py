from .GenericMethods import *


class StatorFrameHorizontalViberOverLimitDiagnosis(TwoThresholdsGreaterEqualToAndLesserThan):
    def __init__(self, *args):
        """
        定子机座水平振动超限判断,单位均为mm

        :math:`T < 0.03, 定子机座水平振动不超限`

        :math:`0.03 \\le T < 0.04, 定子机座水平振动超限一级报警`

        :math:`T \\ge 0.04, 定子机座水平振动超限二级报警`


        [1] 参数
        ----------
        lowerThreshold:
            float,一级报警限,默认0.03
        higherThreshold:
            float,二级报警限,默认0.04
        truthTable:
            dict[str],报警真值表,默认:
                {
                    "100": "定子机座水平振动不超限",

                    "010": "定子机座水平振动超限一级报警",

                    "001": "定子机座水平振动超限二级报警"

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
        >>> obj = StatorFrameHorizontalViberOverLimitDiagnosis(0.03, 0.04, {"100": "OK", "010": "1st", "001": "2nd"})
        >>> print(obj.diagnosis(0.02))
        >>> print(obj.diagnosis(0.03))
        >>> print(obj.diagnosis(0.035))
        >>> print(obj.diagnosis(0.04))
        >>> print(obj.diagnosis(0.041))

        [5]备注
        --------
        * 实例化时,参数可以全部还用缺省值，但不允许有个别缺省参数
        """
        truthTable = {
            "100": "定子机座水平振动不超限",
            "010": "定子机座水平振动超限一级报警",
            "001": "定子机座水平振动超限二级报警"
        }
        super().__init__(*args if len(args)==3 else (0.03, 0.04, truthTable))
