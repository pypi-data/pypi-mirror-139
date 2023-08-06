from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_StatorCoreVibrationOverLimitDiagnosis import StatorCoreVibrationOverLimitDiagnosis


def main():
    """
    output:
        OK 定子铁芯振动超限报警
        OK 定子铁芯振动超限报警
        alarm 定子铁芯振动超限报警
    """

    obj1 = StatorCoreVibrationOverLimitDiagnosis(0.0445, {"10": "OK", "01": "alarm"})
    obj2 = StatorCoreVibrationOverLimitDiagnosis()
    sampleValues = [0.04, 0.0445, 0.05]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()