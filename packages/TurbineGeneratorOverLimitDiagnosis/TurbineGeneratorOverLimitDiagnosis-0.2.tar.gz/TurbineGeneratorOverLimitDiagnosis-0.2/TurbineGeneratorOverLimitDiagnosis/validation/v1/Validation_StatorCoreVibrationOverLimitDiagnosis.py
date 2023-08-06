from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_StatorCoreVibrationOverLimitDiagnosis import StatorCoreVibrationOverLimitDiagnosis


def main():
    """
    output:
        OK 定子铁芯振动不超限
        OK 定子铁芯振动不超限
        alarm 定子铁芯振动超限报警
    """
    obj1 = StatorCoreVibrationOverLimitDiagnosis(0.03, {"10": "OK", "01": "alarm"})
    obj2 = StatorCoreVibrationOverLimitDiagnosis()
    sampleValues = [0.02, 0.03, 0.031]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()