from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_BusRingTemperOverLimitDiagnosis import BusRingTemperOverLimitDiagnosis


def main():
    """
    output:
        OK 定子汇流环运行温度不超限
        1st 定子汇流环运行温度超限一级报警
        1st 定子汇流环运行温度超限一级报警
        2nd 定子汇流环运行温度超限二级报警
        2nd 定子汇流环运行温度超限二级报警
    """

    obj1 = BusRingTemperOverLimitDiagnosis(110, 125, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = BusRingTemperOverLimitDiagnosis()
    sampleValues = [100, 110, 115, 125, 126]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()