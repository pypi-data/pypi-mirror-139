from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_StatorFrameHorizontalVibrationOverLimitDiagnosis import StatorFrameHorizontalViberOverLimitDiagnosis


def main():
    """
    output:
        OK 定子机座水平振动不超限
        1st 定子机座水平振动超限一级报警
        1st 定子机座水平振动超限一级报警
        2nd 定子机座水平振动超限二级报警
        2nd 定子机座水平振动超限二级报警
    """

    obj1 = StatorFrameHorizontalViberOverLimitDiagnosis(0.03, 0.04, {"100": "OK", "010": "1st", "001": "2nd"})
    obj2 = StatorFrameHorizontalViberOverLimitDiagnosis()
    sampleValues = [0.02, 0.03, 0.035, 0.04, 0.041]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()