/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: main.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 28-Dec-2024 05:54:40
 */

/*************************************************************************/
/* This automatically generated example C main file shows how to call    */
/* entry-point functions that MATLAB Coder generated. You must customize */
/* this file for your application. Do not modify this file directly.     */
/* Instead, make a copy of this file, modify it, and integrate it into   */
/* your development environment.                                         */
/*                                                                       */
/* This file initializes entry-point function arguments to a default     */
/* size and value before calling the entry-point functions. It does      */
/* not store or use any values returned from the entry-point functions.  */
/* If necessary, it does pre-allocate memory for returned values.        */
/* You can use this file as a starting point for a main function that    */
/* you can deploy in your application.                                   */
/*                                                                       */
/* After you copy the file, and before you deploy it, you must make the  */
/* following changes:                                                    */
/* * For variable-size function arguments, change the example sizes to   */
/* the sizes that your application requires.                             */
/* * Change the example values of function arguments to the values that  */
/* your application requires.                                            */
/* * If the entry-point functions return values, store these values or   */
/* otherwise use them as required by your application.                   */
/*                                                                       */
/*************************************************************************/

/* Include Files */
#include "main.h"
#include "skFilter_fs32_fpass04.h"
#include "skFilter_fs32_fpass04_terminate.h"

/* Function Declarations */
static void argInit_d10000x1_int16_T(short result_data[], int *result_size);

static short argInit_int16_T(void);

/* Function Definitions */
/*
 * Arguments    : short result_data[]
 *                int *result_size
 * Return Type  : void
 */
static void argInit_d10000x1_int16_T(short result_data[], int *result_size)
{
  int idx0;
  /* Set the size of the array.
Change this size to the value that the application requires. */
  *result_size = 2;
  /* Loop over the array to initialize each element. */
  for (idx0 = 0; idx0 < 2; idx0++) {
    /* Set the value of the array element.
Change this value to the value that the application requires. */
    result_data[idx0] = argInit_int16_T();
  }
}

/*
 * Arguments    : void
 * Return Type  : short
 */
static short argInit_int16_T(void)
{
  return 0;
}

/*
 * Arguments    : int argc
 *                char **argv
 * Return Type  : int
 */
int main(int argc, char **argv)
{
  (void)argc;
  (void)argv;
  /* The initialize function is being called automatically from your entry-point
   * function. So, a call to initialize is not included here. */
  /* Invoke the entry-point functions.
You can call entry-point functions multiple times. */
  main_skFilter_fs32_fpass04();
  /* Terminate the application.
You do not need to do this more than one time. */
  skFilter_fs32_fpass04_terminate();
  return 0;
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void main_skFilter_fs32_fpass04(void)
{
  float y_data[10000];
  int y_size[2];
  int x_size;
  short x_data[10000];
  /* Initialize function 'skFilter_fs32_fpass04' input arguments. */
  /* Initialize function input argument 'x'. */
  argInit_d10000x1_int16_T(x_data, &x_size);
  /* Call the entry-point 'skFilter_fs32_fpass04'. */
  skFilter_fs32_fpass04(x_data, &x_size, y_data, y_size);
}

/*
 * File trailer for main.c
 *
 * [EOF]
 */
