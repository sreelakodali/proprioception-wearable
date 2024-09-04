/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter3.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:33:14
 */

#ifndef SKFILTER3_H
#define SKFILTER3_H

/* Include Files */
#include "rtwtypes.h"
#include "skFilter3_types.h"
#include <stddef.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
extern void skFilter3(const short x_data[], const int x_size[1],
                      emxArray_real_T *y);

void skFilter3_free(void);

void skFilter3_init(void);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for skFilter3.h
 *
 * [EOF]
 */
