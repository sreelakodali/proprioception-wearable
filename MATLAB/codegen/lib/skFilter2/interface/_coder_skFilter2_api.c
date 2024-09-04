/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_skFilter2_api.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:20:07
 */

/* Include Files */
#include "_coder_skFilter2_api.h"
#include "_coder_skFilter2_mex.h"

/* Variable Definitions */
emlrtCTX emlrtRootTLSGlobal = NULL;

emlrtContext emlrtContextGlobal = {
    true,                                                 /* bFirstTime */
    false,                                                /* bInitialized */
    131627U,                                              /* fVersionInfo */
    NULL,                                                 /* fErrorFunction */
    "skFilter2",                                          /* fFunctionName */
    NULL,                                                 /* fRTCallStack */
    false,                                                /* bDebugMode */
    {2045744189U, 2170104910U, 2743257031U, 4284093946U}, /* fSigWrd */
    NULL                                                  /* fSigMem */
};

/* Function Declarations */
static void b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
                               const emlrtMsgIdentifier *parentId,
                               int16_T **y_data, int32_T *y_size);

static void c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
                               const emlrtMsgIdentifier *msgId,
                               int16_T **ret_data, int32_T *ret_size);

static void emlrt_marshallIn(const emlrtStack *sp, const mxArray *x,
                             const char_T *identifier, int16_T **y_data,
                             int32_T *y_size);

static const mxArray *emlrt_marshallOut(const real32_T u_data[],
                                        const int32_T u_size[2]);

/* Function Definitions */
/*
 * Arguments    : const emlrtStack *sp
 *                const mxArray *u
 *                const emlrtMsgIdentifier *parentId
 *                int16_T **y_data
 *                int32_T *y_size
 * Return Type  : void
 */
static void b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
                               const emlrtMsgIdentifier *parentId,
                               int16_T **y_data, int32_T *y_size)
{
  int32_T i;
  int16_T *r;
  c_emlrt_marshallIn(sp, emlrtAlias(u), parentId, &r, &i);
  *y_size = i;
  *y_data = r;
  emlrtDestroyArray(&u);
}

/*
 * Arguments    : const emlrtStack *sp
 *                const mxArray *src
 *                const emlrtMsgIdentifier *msgId
 *                int16_T **ret_data
 *                int32_T *ret_size
 * Return Type  : void
 */
static void c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
                               const emlrtMsgIdentifier *msgId,
                               int16_T **ret_data, int32_T *ret_size)
{
  static const int32_T dims = 10000;
  const boolean_T b = true;
  emlrtCheckVsBuiltInR2012b((emlrtConstCTX)sp, msgId, src, "int16", false, 1U,
                            (const void *)&dims, &b, ret_size);
  *ret_data = (int16_T *)emlrtMxGetData(src);
  emlrtDestroyArray(&src);
}

/*
 * Arguments    : const emlrtStack *sp
 *                const mxArray *x
 *                const char_T *identifier
 *                int16_T **y_data
 *                int32_T *y_size
 * Return Type  : void
 */
static void emlrt_marshallIn(const emlrtStack *sp, const mxArray *x,
                             const char_T *identifier, int16_T **y_data,
                             int32_T *y_size)
{
  emlrtMsgIdentifier thisId;
  int32_T i;
  int16_T *r;
  thisId.fIdentifier = (const char_T *)identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  b_emlrt_marshallIn(sp, emlrtAlias(x), &thisId, &r, &i);
  *y_size = i;
  *y_data = r;
  emlrtDestroyArray(&x);
}

/*
 * Arguments    : const real32_T u_data[]
 *                const int32_T u_size[2]
 * Return Type  : const mxArray *
 */
static const mxArray *emlrt_marshallOut(const real32_T u_data[],
                                        const int32_T u_size[2])
{
  static const int32_T iv[2] = {0, 0};
  const mxArray *m;
  const mxArray *y;
  y = NULL;
  m = emlrtCreateNumericArray(2, (const void *)&iv[0], mxSINGLE_CLASS, mxREAL);
  emlrtMxSetData((mxArray *)m, (void *)&u_data[0]);
  emlrtSetDimensions((mxArray *)m, &u_size[0], 2);
  emlrtAssign(&y, m);
  return y;
}

/*
 * Arguments    : const mxArray *prhs
 *                const mxArray **plhs
 * Return Type  : void
 */
void skFilter2_api(const mxArray *prhs, const mxArray **plhs)
{
  emlrtStack st = {
      NULL, /* site */
      NULL, /* tls */
      NULL  /* prev */
  };
  int32_T y_size[2];
  int32_T x_size;
  real32_T(*y_data)[10000];
  int16_T(*x_data)[10000];
  st.tls = emlrtRootTLSGlobal;
  y_data = (real32_T(*)[10000])mxMalloc(sizeof(real32_T[10000]));
  /* Marshall function inputs */
  emlrt_marshallIn(&st, emlrtAlias(prhs), "x", (int16_T **)&x_data, &x_size);
  /* Invoke the target function */
  skFilter2(*x_data, *(int32_T(*)[1]) & x_size, *y_data, y_size);
  /* Marshall function outputs */
  *plhs = emlrt_marshallOut(*y_data, y_size);
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter2_atexit(void)
{
  emlrtStack st = {
      NULL, /* site */
      NULL, /* tls */
      NULL  /* prev */
  };
  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtEnterRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
  skFilter2_xil_terminate();
  skFilter2_xil_shutdown();
  emlrtExitTimeCleanup(&emlrtContextGlobal);
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter2_initialize(void)
{
  emlrtStack st = {
      NULL, /* site */
      NULL, /* tls */
      NULL  /* prev */
  };
  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, NULL);
  emlrtEnterRtStackR2012b(&st);
  emlrtFirstTimeR2012b(emlrtRootTLSGlobal);
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter2_terminate(void)
{
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/*
 * File trailer for _coder_skFilter2_api.c
 *
 * [EOF]
 */
