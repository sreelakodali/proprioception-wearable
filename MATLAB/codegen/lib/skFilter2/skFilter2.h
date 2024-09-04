/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter2.h
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:20:07
 */

#ifndef SKFILTER2_H
#define SKFILTER2_H

/* Include Files */
#include "rtwtypes.h"
#include <stddef.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
extern void skFilter2(const short x_data[], const int x_size[1], float y_data[],
                      int y_size[2]);

void skFilter2_free(void);

void skFilter2_init(void);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for skFilter2.h
 *
 * [EOF]
 */
