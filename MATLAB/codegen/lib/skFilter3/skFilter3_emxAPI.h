/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter3_emxAPI.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:33:14
 */

#ifndef SKFILTER3_EMXAPI_H
#define SKFILTER3_EMXAPI_H

/* Include Files */
#include "rtwtypes.h"
#include "skFilter3_types.h"
#include <stddef.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
extern emxArray_real_T *emxCreateND_real_T(int numDimensions, const int *size);

extern emxArray_real_T *
emxCreateWrapperND_real_T(double *data, int numDimensions, const int *size);

extern emxArray_real_T *emxCreateWrapper_real_T(double *data, int rows,
                                                int cols);

extern emxArray_real_T *emxCreate_real_T(int rows, int cols);

extern void emxDestroyArray_real_T(emxArray_real_T *emxArray);

extern void emxInitArray_real_T(emxArray_real_T **pEmxArray, int numDimensions);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for skFilter3_emxAPI.h
 *
 * [EOF]
 */
