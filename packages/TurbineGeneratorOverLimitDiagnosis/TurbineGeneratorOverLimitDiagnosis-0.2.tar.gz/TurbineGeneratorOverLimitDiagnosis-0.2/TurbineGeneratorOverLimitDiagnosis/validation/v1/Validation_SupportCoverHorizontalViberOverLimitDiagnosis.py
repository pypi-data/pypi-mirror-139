from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_SupportCoverHorizontalVibrationOverLimitDiagnosis import SupportCoverHorizontalViberOverLimitDiagnosis


def main():
    """
    output:
        OK 支持盖水平振动不超限
        1st 支持盖水平振动超限一级报警
        1st 支持盖水平振动超限一级报警
        2nd 支持盖水平振动超限二级报警
        2nd 支持盖水平振动超限二级报警
    """

    obj1 = SupportCoverHorizontalViberOverLimitDiagnosis(0.07, 0.09, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = SupportCoverHorizontalViberOverLimitDiagnosis()
    sampleValues = [0.06, 0.07, 0.08, 0.09, 0.091]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()