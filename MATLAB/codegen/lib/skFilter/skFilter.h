/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 19-Aug-2024 21:04:05
 */

#ifndef SKFILTER_H
#define SKFILTER_H

/* Include Files */
#include "rtwtypes.h"
#include <stddef.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
extern void skFilter(const short x_data[], const int x_size[1], short y_data[],
                     int y_size[2]);

void skFilter_free(void);

void skFilter_init(void);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for skFilter.h
 *
 * [EOF]
 */
