/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter3_types.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:33:14
 */

#ifndef SKFILTER3_TYPES_H
#define SKFILTER3_TYPES_H

/* Include Files */
#include "rtwtypes.h"

/* Type Definitions */
#ifndef typedef_dsp_BiquadFilter_0
#define typedef_dsp_BiquadFilter_0
typedef struct {
  int S0_isInitialized;
  double W0_FILT_STATES[4];
  int W1_PreviousNumChannels;
  double P0_ICRTP;
  double P1_RTP1COEFF[6];
  double P2_RTP2COEFF[4];
  double P3_RTP3COEFF[3];
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

#ifndef struct_emxArray_real_T
#define struct_emxArray_real_T
struct emxArray_real_T {
  double *data;
  int *size;
  int allocatedSize;
  int numDimensions;
  bool canFreeData;
};
#endif /* struct_emxArray_real_T */
#ifndef typedef_emxArray_real_T
#define typedef_emxArray_real_T
typedef struct emxArray_real_T emxArray_real_T;
#endif /* typedef_emxArray_real_T */

#endif
/*
 * File trailer for skFilter3_types.h
 *
 * [EOF]
 */
