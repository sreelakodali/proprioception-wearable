/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter2_terminate.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:20:07
 */

/* Include Files */
#include "skFilter2_terminate.h"
#include "skFilter2.h"
#include "skFilter2_data.h"

/* Function Definitions */
/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter2_terminate(void)
{
  skFilter2_free();
  isInitialized_skFilter2 = false;
}

/*
 * File trailer for skFilter2_terminate.c
 *
 * [EOF]
 */
