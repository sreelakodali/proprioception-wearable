/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter2_initialize.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 29-Aug-2024 20:20:07
 */

/* Include Files */
#include "skFilter2_initialize.h"
#include "skFilter2.h"
#include "skFilter2_data.h"
#include "skFilter2_types.h"

/* Function Definitions */
/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter2_initialize(void)
{
  static const signed char iv[6] = {1, 2, 1, 1, 1, 0};
  int i;
  skFilter2_init();
  /*  The following code was used to design the filter coefficients: */
  /*  */
  /*  Fpass = 0.08;    % Passband Frequency */
  /*  Fstop = 1.5;     % Stopband Frequency */
  /*  Apass = 1;       % Passband Ripple (dB) */
  /*  Astop = 80;      % Stopband Attenuation (dB) */
  /*  Fs    = 4.9261;  % Sampling Frequency */
  /*  */
  /*  h = fdesign.lowpass('fp,fst,ap,ast', Fpass, Fstop, Apass, Astop, Fs); */
  /*  */
  /*  Hd = design(h, 'butter', ... */
  /*      'MatchExactly', 'passband', ... */
  /*      'SystemObject', true,... */
  /*       UseLegacyBiquadFilter=true); */
  /* System object Constructor function: dsp.BiquadFilter */
  Hd.cSFunObject.P0_ICRTP = 0.0F;
  for (i = 0; i < 6; i++) {
    Hd.cSFunObject.P1_RTP1COEFF[i] = iv[i];
  }
  Hd.cSFunObject.P2_RTP2COEFF[0] = -1.86490643F;
  Hd.cSFunObject.P2_RTP2COEFF[1] = 0.880228F;
  Hd.cSFunObject.P2_RTP2COEFF[2] = -0.879767478F;
  Hd.cSFunObject.P2_RTP2COEFF[3] = 0.0F;
  Hd.cSFunObject.P3_RTP3COEFF[0] = 0.00383039215F;
  Hd.cSFunObject.P4_RTP_COEFF3_BOOL[0] = true;
  Hd.cSFunObject.P3_RTP3COEFF[1] = 0.0601162724F;
  Hd.cSFunObject.P4_RTP_COEFF3_BOOL[1] = true;
  Hd.cSFunObject.P3_RTP3COEFF[2] = 0.0F;
  Hd.cSFunObject.P4_RTP_COEFF3_BOOL[2] = false;
  Hd.matlabCodegenIsDeleted = false;
  /* System object Initialization function: dsp.BiquadFilter */
  Hd.cSFunObject.W0_FILT_STATES[0] = 0.0F;
  Hd.cSFunObject.W0_FILT_STATES[1] = 0.0F;
  Hd.cSFunObject.W0_FILT_STATES[2] = 0.0F;
  Hd.cSFunObject.W0_FILT_STATES[3] = 0.0F;
  Hd.cSFunObject.W1_PreviousNumChannels = -1;
  isInitialized_skFilter2 = true;
}

/*
 * File trailer for skFilter2_initialize.c
 *
 * [EOF]
 */
