from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_TurbineGuideBearingSwingOverLimitDiagnosis import TurbineGuideBearingSwingOverLimitDiagnosis


def main():
    """
    output:
        OK 水导摆度运行值不超限
        1st 水导摆度运行值超限一级报警
        1st 水导摆度运行值超限一级报警
        2nd 水导摆度运行值超限二级报警
        2nd 水导摆度运行值超限二级报警
    """

    obj1 = TurbineGuideBearingSwingOverLimitDiagnosis(0.18, 0.23, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = TurbineGuideBearingSwingOverLimitDiagnosis()
    sampleValues = [0.17, 0.18, 0.19, 0.23, 0.24]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()