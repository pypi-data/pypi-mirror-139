from TurbineGeneratorOverLimitDiagnosis.tools.v1.Method_StatorWindingInsulationOverLimitDiagnosis import StatorWindingInsulationOverLimitDiagnosis


def main():
    """
    output:
        2nd 定子绕组绝缘超限二级报警
        1st 定子绕组绝缘超限一级报警
        1st 定子绕组绝缘超限一级报警
        OK 定子绕组绝缘不超限
        OK 定子绕组绝缘不超限
    """
    obj1 = StatorWindingInsulationOverLimitDiagnosis(0.6, 0.8, {"100": "2nd", "010": "1st", "001": "OK"})
    obj2 = StatorWindingInsulationOverLimitDiagnosis()
    sampleValues = [0.5, 0.6, 0.7, 0.8, 0.9]
    [print(obj1.diagnosis(item), obj2.diagnosis(item), ) for item in sampleValues]

if __name__ == '__main__':
    main()