/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter2_types.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:20:07
 */

#ifndef SKFILTER2_TYPES_H
#define SKFILTER2_TYPES_H

/* Include Files */
#include "rtwtypes.h"

/* Type Definitions */
#ifndef typedef_dsp_BiquadFilter_0
#define typedef_dsp_BiquadFilter_0
typedef struct {
  int S0_isInitialized;
  float W0_FILT_STATES[4];
  int W1_PreviousNumChannels;
  float P0_ICRTP;
  float P1_RTP1COEFF[6];
  float P2_RTP2COEFF[4];
  float P3_RTP3COEFF[3];
  bool P4_RTP_COEFF3_BOOL[3];
} dsp_BiquadFilter_0;
#endif /* typedef_dsp_BiquadFilter_0 */

#ifndef typedef_dspcodegen_BiquadFilter
#define typedef_dspcodegen_BiquadFilter
typedef struct {
  bool matlabCodegenIsDeleted;
  bool isSetupComplete;
  dsp_BiquadFilter_0 cSFunObject;
} dspcodegen_BiquadFilter;
#endif /* typedef_dspcodegen_BiquadFilter */

#endif
/*
 * File trailer for skFilter2_types.h
 *
 * [EOF]
 */
