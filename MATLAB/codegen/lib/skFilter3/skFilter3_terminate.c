/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter3_terminate.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:33:14
 */

/* Include Files */
#include "skFilter3_terminate.h"
#include "skFilter3.h"
#include "skFilter3_data.h"

/* Function Definitions */
/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter3_terminate(void)
{
  skFilter3_free();
  isInitialized_skFilter3 = false;
}

/*
 * File trailer for skFilter3_terminate.c
 *
 * [EOF]
 */
