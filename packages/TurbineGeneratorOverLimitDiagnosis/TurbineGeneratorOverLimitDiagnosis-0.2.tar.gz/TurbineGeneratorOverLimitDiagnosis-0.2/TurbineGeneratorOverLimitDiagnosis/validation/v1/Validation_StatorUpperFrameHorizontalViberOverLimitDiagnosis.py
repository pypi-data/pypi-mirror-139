from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_StatorUpperFrameHorizontalVibrationOverLimitDiagnosis import StatorUpperFrameHorizontalViberOverLimitDiagnosis


def main():
    """
    output:
        OK 定子上机架水平振动不超限
        1st 定子上机架水平振动超限一级报警
        1st 定子上机架水平振动超限一级报警
        2nd 定子上机架水平振动超限二级报警
        2nd 定子上机架水平振动超限二级报警
    """

    obj1 = StatorUpperFrameHorizontalViberOverLimitDiagnosis(0.07, 0.08, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = StatorUpperFrameHorizontalViberOverLimitDiagnosis()
    sampleValues = [0.06, 0.07, 0.075, 0.08, 0.081]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()