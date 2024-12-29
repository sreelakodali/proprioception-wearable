/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_skFilter_fs32_fpass04_api.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 28-Dec-2024 05:54:40
 */

#ifndef _CODER_SKFILTER_FS32_FPASS04_API_H
#define _CODER_SKFILTER_FS32_FPASS04_API_H

/* Include Files */
#include "emlrt.h"
#include "tmwtypes.h"
#include <string.h>

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
void skFilter_fs32_fpass04(int16_T x_data[], int32_T x_size[1],
                           real32_T y_data[], int32_T y_size[2]);

void skFilter_fs32_fpass04_api(const mxArray *prhs, const mxArray **plhs);

void skFilter_fs32_fpass04_atexit(void);

void skFilter_fs32_fpass04_initialize(void);

void skFilter_fs32_fpass04_terminate(void);

void skFilter_fs32_fpass04_xil_shutdown(void);

void skFilter_fs32_fpass04_xil_terminate(void);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for _coder_skFilter_fs32_fpass04_api.h
 *
 * [EOF]
 */
