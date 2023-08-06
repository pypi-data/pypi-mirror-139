from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_UpperGuideBearingSwingOverLimitDiagnosis import UpperGuideBearingSwingOverLimitDiagnosis


def main():
    """
    output:
        OK 上导摆度运行值不超限
        1st 上导摆度运行值超限一级报警
        1st 上导摆度运行值超限一级报警
        2nd 上导摆度运行值超限二级报警
        2nd 上导摆度运行值超限二级报警
    """

    obj1 = UpperGuideBearingSwingOverLimitDiagnosis(0.15, 0.20, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = UpperGuideBearingSwingOverLimitDiagnosis()
    sampleValues = [0.14, 0.15, 0.16, 0.20, 0.24]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()