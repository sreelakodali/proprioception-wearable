/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter_fs32_fpass04.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 28-Dec-2024 05:54:40
 */

#ifndef SKFILTER_FS32_FPASS04_H
#define SKFILTER_FS32_FPASS04_H

/* Include Files */
#include "rtwtypes.h"
#include <stddef.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
extern void skFilter_fs32_fpass04(const short x_data[], const int x_size[1],
                                  float y_data[], int y_size[2]);

void skFilter_fs32_fpass04_free(void);

void skFilter_fs32_fpass04_init(void);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for skFilter_fs32_fpass04.h
 *
 * [EOF]
 */
