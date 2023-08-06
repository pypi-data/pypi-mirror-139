from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_RotorExcitingCurrentOverLimitDiagnosis import RotorExcitingCurrentOverLimitDiagnosis


def main():
    """
    output:
        OK 励磁电流运行值正常
        OK 励磁电流运行值正常
        abnormal 励磁电流运行值异常
    """

    obj1 = RotorExcitingCurrentOverLimitDiagnosis(0.15, {"10": "OK", "01": "abnormal"})
    obj2 = RotorExcitingCurrentOverLimitDiagnosis()
    sampleValues = [0.1, 0.15, 0.2]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()