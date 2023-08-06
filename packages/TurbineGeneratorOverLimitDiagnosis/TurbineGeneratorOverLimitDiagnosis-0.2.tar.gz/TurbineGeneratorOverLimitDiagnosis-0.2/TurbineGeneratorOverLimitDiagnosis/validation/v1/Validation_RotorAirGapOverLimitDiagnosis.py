from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_RotorAirGapOverLimitDiagnosis import RotorAirGapOverLimitDiagnosis


def main():
    """
    output:
        OK 转子气隙运行值正常
        OK 转子气隙运行值正常
        alarm 转子气隙运行值异常
    """

    obj1 = RotorAirGapOverLimitDiagnosis(0.04, {"10": "OK", "01": "alarm"})
    obj2 = RotorAirGapOverLimitDiagnosis()
    sampleValues = [0.03, 0.04, 0.05]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()