from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_StatorWindingTemperOverLimitDiagnosis import StatorWindingTemperOverLimitDiagnosis


def main():
    """
    output:
        OK 定子绕组运行温度不超限
        1st 定子绕组运行温度超限一级报警
        1st 定子绕组运行温度超限一级报警
        2nd 定子绕组运行温度超限二级报警
        2nd 定子绕组运行温度超限二级报警
    """

    obj1 = StatorWindingTemperOverLimitDiagnosis(110, 125, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = StatorWindingTemperOverLimitDiagnosis()
    sampleValues = [100, 110, 115, 125, 126]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()