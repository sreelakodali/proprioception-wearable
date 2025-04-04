/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter3.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:33:14
 */

/* Include Files */
#include "skFilter3.h"
#include "skFilter3_data.h"
#include "skFilter3_emxutil.h"
#include "skFilter3_initialize.h"
#include "skFilter3_types.h"

/* Function Definitions */
/*
 * DOFILTER Filters input x and returns output y.
 *
 * Arguments    : const short x_data[]
 *                const int x_size[1]
 *                emxArray_real_T *y
 * Return Type  : void
 */
void skFilter3(const short x_data[], const int x_size[1], emxArray_real_T *y)
{
  dsp_BiquadFilter_0 *obj;
  double *y_data;
  int i;
  int ioIdx;
  if (!isInitialized_skFilter3) {
    skFilter3_initialize();
  }
  /*  MATLAB Code */
  /*  Generated by MATLAB(R) 9.13 and DSP System Toolbox 9.15. */
  /*  Generated on: 29-Aug-2024 20:28:23 */
  /*  To generate C/C++ code from this function use the codegen command. */
  /*  Type 'help codegen' for more information. */
  obj = &Hd.cSFunObject;
  /* System object Outputs function: dsp.BiquadFilter */
  ioIdx = y->size[0] * y->size[1];
  y->size[0] = x_size[0];
  y->size[1] = 1;
  emxEnsureCapacity_real_T(y, ioIdx);
  y_data = y->data;
  ioIdx = 0;
  if (Hd.cSFunObject.W1_PreviousNumChannels == -1) {
    Hd.cSFunObject.W1_PreviousNumChannels = 1;
  }
  for (i = 0; i < x_size[0]; i++) {
    double denAccum;
    double tmpState;
    denAccum = obj->P3_RTP3COEFF[0] * (double)x_data[ioIdx];
    denAccum -= obj->P2_RTP2COEFF[0] * obj->W0_FILT_STATES[0];
    tmpState = denAccum - obj->P2_RTP2COEFF[1] * obj->W0_FILT_STATES[1];
    denAccum = obj->P1_RTP1COEFF[0] * tmpState;
    denAccum += obj->W0_FILT_STATES[0] * obj->P1_RTP1COEFF[1];
    denAccum += obj->W0_FILT_STATES[1] * obj->P1_RTP1COEFF[2];
    obj->W0_FILT_STATES[1] = obj->W0_FILT_STATES[0];
    obj->W0_FILT_STATES[0] = tmpState;
    denAccum *= obj->P3_RTP3COEFF[1];
    denAccum -= obj->P2_RTP2COEFF[2] * obj->W0_FILT_STATES[2];
    tmpState = denAccum - obj->P2_RTP2COEFF[3] * obj->W0_FILT_STATES[3];
    denAccum = obj->P1_RTP1COEFF[3] * tmpState;
    denAccum += obj->W0_FILT_STATES[2] * obj->P1_RTP1COEFF[4];
    y_data[ioIdx] = denAccum + obj->W0_FILT_STATES[3] * obj->P1_RTP1COEFF[5];
    obj->W0_FILT_STATES[3] = obj->W0_FILT_STATES[2];
    obj->W0_FILT_STATES[2] = tmpState;
    ioIdx++;
  }
}

/*
 * DOFILTER Filters input x and returns output y.
 *
 * Arguments    : void
 * Return Type  : void
 */
void skFilter3_free(void)
{
  if (!Hd.matlabCodegenIsDeleted) {
    Hd.matlabCodegenIsDeleted = true;
  }
}

/*
 * DOFILTER Filters input x and returns output y.
 *
 * Arguments    : void
 * Return Type  : void
 */
void skFilter3_init(void)
{
  Hd.matlabCodegenIsDeleted = true;
}

/*
 * File trailer for skFilter3.c
 *
 * [EOF]
 */
