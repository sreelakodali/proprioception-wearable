/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter_fs32_fpass04_types.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 28-Dec-2024 05:54:40
 */

#ifndef SKFILTER_FS32_FPASS04_TYPES_H
#define SKFILTER_FS32_FPASS04_TYPES_H

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
 * File trailer for skFilter_fs32_fpass04_types.h
 *
 * [EOF]
 */
