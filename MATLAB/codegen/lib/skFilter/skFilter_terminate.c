/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter_terminate.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 19-Aug-2024 21:04:05
 */

/* Include Files */
#include "skFilter_terminate.h"
#include "skFilter.h"
#include "skFilter_data.h"

/* Function Definitions */
/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter_terminate(void)
{
  skFilter_free();
  isInitialized_skFilter = false;
}

/*
 * File trailer for skFilter_terminate.c
 *
 * [EOF]
 */
