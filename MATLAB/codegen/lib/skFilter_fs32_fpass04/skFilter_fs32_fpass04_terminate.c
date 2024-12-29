/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter_fs32_fpass04_terminate.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 28-Dec-2024 05:54:40
 */

/* Include Files */
#include "skFilter_fs32_fpass04_terminate.h"
#include "skFilter_fs32_fpass04.h"
#include "skFilter_fs32_fpass04_data.h"

/* Function Definitions */
/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter_fs32_fpass04_terminate(void)
{
  skFilter_fs32_fpass04_free();
  isInitialized_skFilter_fs32_fpass04 = false;
}

/*
 * File trailer for skFilter_fs32_fpass04_terminate.c
 *
 * [EOF]
 */
