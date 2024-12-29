/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_skFilter_fs32_fpass04_mex.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 28-Dec-2024 05:54:40
 */

/* Include Files */
#include "_coder_skFilter_fs32_fpass04_mex.h"
#include "_coder_skFilter_fs32_fpass04_api.h"

/* Function Definitions */
/*
 * Arguments    : int32_T nlhs
 *                mxArray *plhs[]
 *                int32_T nrhs
 *                const mxArray *prhs[]
 * Return Type  : void
 */
void mexFunction(int32_T nlhs, mxArray *plhs[], int32_T nrhs,
                 const mxArray *prhs[])
{
  mexAtExit(&skFilter_fs32_fpass04_atexit);
  /* Module initialization. */
  skFilter_fs32_fpass04_initialize();
  /* Dispatch the entry-point. */
  unsafe_skFilter_fs32_fpass04_mexFunction(nlhs, plhs, nrhs, prhs);
  /* Module termination. */
  skFilter_fs32_fpass04_terminate();
}

/*
 * Arguments    : void
 * Return Type  : emlrtCTX
 */
emlrtCTX mexFunctionCreateRootTLS(void)
{
  emlrtCreateRootTLSR2022a(&emlrtRootTLSGlobal, &emlrtContextGlobal, NULL, 1,
                           NULL, "UTF-8", true);
  return emlrtRootTLSGlobal;
}

/*
 * Arguments    : int32_T nlhs
 *                mxArray *plhs[1]
 *                int32_T nrhs
 *                const mxArray *prhs[1]
 * Return Type  : void
 */
void unsafe_skFilter_fs32_fpass04_mexFunction(int32_T nlhs, mxArray *plhs[1],
                                              int32_T nrhs,
                                              const mxArray *prhs[1])
{
  emlrtStack st = {
      NULL, /* site */
      NULL, /* tls */
      NULL  /* prev */
  };
  const mxArray *outputs;
  st.tls = emlrtRootTLSGlobal;
  /* Check for proper number of arguments. */
  if (nrhs != 1) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:WrongNumberOfInputs", 5, 12, 1, 4,
                        21, "skFilter_fs32_fpass04");
  }
  if (nlhs > 1) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:TooManyOutputArguments", 3, 4, 21,
                        "skFilter_fs32_fpass04");
  }
  /* Call the function. */
  skFilter_fs32_fpass04_api(prhs[0], &outputs);
  /* Copy over outputs to the caller. */
  emlrtReturnArrays(1, &plhs[0], &outputs);
}

/*
 * File trailer for _coder_skFilter_fs32_fpass04_mex.c
 *
 * [EOF]
 */
