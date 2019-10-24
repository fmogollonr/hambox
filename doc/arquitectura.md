# Arquitectura propuesta
```mermaid
graph LR;
    GPS-->PI{PI};
    CAM-->PI;
    PI-->DORJI;
    DORJI-->PI;
    PI-->DAC;
    MIC-->INAMPLIFIER;
    INAMPLIFIER-->ADC;
    ADC-->PI;
    PTT-->PI;
    DORJI-->FILTER;
    FILTER-->ANTENNA;
    DAC-->OUTAMPLIFIER;
    OUTAMPLIFIER-->SPEAKER;
```