from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_RotorTemperOverLimitDiagnosis import RotorTemperOverLimitDiagnosis


def main():
    """
    output:
        OK 转子运行温度不超限
        1st 转子运行温度超限一级报警
        1st 转子运行温度超限一级报警
        2nd 转子运行温度超限二级报警
        2nd 转子运行温度超限二级报警
    """

    obj1 = RotorTemperOverLimitDiagnosis(110, 125, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = RotorTemperOverLimitDiagnosis()
    sampleValues = [100, 110, 115, 125, 126]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()