class TwoThresholdsGreaterEqualToAndLesserThan:
    def __init__(self, lowerThreshold, higherThreshold, truthTable):
        """
        计算针对下式的判断结果

        :math:`T < T_lowerThreshold`

        :math:`T_lowerThreshold \\le T < T_higherThreshold`

        :math:`T_higherThreshold \\le T`

        真值表
        ------
        形如 {
            "100": "定子绕组运行温度不超限",

            "010": "定子绕组运行温度超限一级报警",

            "001": "定子绕组运行温度超限二级报警"
        }

        其中“100”表示针对上式的判断结果

        :param lowerThreshold: 判断高限
        :param higherThreshold: 判断高限
        :param truthTable: 真值表
        """
        self.lowerThreshold, self.higherThreshold = lowerThreshold, higherThreshold
        self.truthTable = truthTable

        def greaterEqualTo(x, x0):
            return x >= x0

        def lesserThan(x, x0):
            return x < x0

        self.diagDict = {
            "greaterEqualTo": greaterEqualTo,
            "lesserThan": lesserThan
        }


    def diagnosis(self, x):
        res =  [self.diagDict["lesserThan"](x, self.lowerThreshold),
        all([not self.diagDict["lesserThan"](x, self.lowerThreshold), not self.diagDict["greaterEqualTo"](x, self.higherThreshold)]),
        self.diagDict["greaterEqualTo"](x, self.higherThreshold)]
        return self.truthTable["".join(list(map(lambda x: str(int(x)), res)))]


class OneThresholdLesserEqualToAndGreaterThan:
    def __init__(self, threshold, truthTable):
        """
        计算针对下式的判断结果

        :math:`T \\le T_threshold

        :math:`T > T_threshold

        真值表
        ------
        形如 {
            "10": "定子绕组运行温度不超限",

            "01": "定子绕组运行温度超限一级报警",
        }

        其中“10”表示针对上式的判断结果

        :param threshold: 判断阈值
        :param truthTable: 真值表
        """
        self.threshold = threshold
        self.truthTable = truthTable

        def greaterThan(x, x0):
            return x > x0

        def lesserEqualTo(x, x0):
            return x <= x0

        self.diagDict = {
            "lesserEqualTo": lesserEqualTo,
            "greaterThan": greaterThan
        }


    def diagnosis(self, x):
        res =  [self.diagDict["lesserEqualTo"](x, self.threshold), self.diagDict["greaterThan"](x, self.threshold)]
        return self.truthTable["".join(list(map(lambda x: str(int(x)), res)))]

