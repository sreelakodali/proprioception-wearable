/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter_initialize.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 19-Aug-2024 21:04:05
 */

/* Include Files */
#include "skFilter_initialize.h"
#include "skFilter.h"
#include "skFilter_data.h"
#include "skFilter_types.h"

/* Function Definitions */
/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter_initialize(void)
{
  static const signed char iv[6] = {1, 2, 1, 1, 2, 1};
  int i;
  skFilter_init();
  /*  The following code was used to design the filter coefficients: */
  /*  */
  /*  Fpass = 0.15;  % Passband Frequency */
  /*  Fstop = 2;     % Stopband Frequency */
  /*  Apass = 1;     % Passband Ripple (dB) */
  /*  Astop = 80;    % Stopband Attenuation (dB) */
  /*  Fs    = 6.67;  % Sampling Frequency */
  /*  */
  /*  h = fdesign.lowpass('fp,fst,ap,ast', Fpass, Fstop, Apass, Astop, Fs); */
  /*  */
  /*  Hd = design(h, 'butter', ... */
  /*      'MatchExactly', 'stopband', ... */
  /*      'SystemObject', true,... */
  /*       UseLegacyBiquadFilter=true); */
  /* System object Constructor function: dsp.BiquadFilter */
  Hd.cSFunObject.P0_ICRTP = 0.0;
  for (i = 0; i < 6; i++) {
    Hd.cSFunObject.P1_RTP1COEFF[i] = iv[i];
  }
  Hd.cSFunObject.P2_RTP2COEFF[0] = -1.74549038480422;
  Hd.cSFunObject.P2_RTP2COEFF[1] = 0.81276557159165;
  Hd.cSFunObject.P2_RTP2COEFF[2] = -1.54141513767015;
  Hd.cSFunObject.P2_RTP2COEFF[3] = 0.600824798248347;
  Hd.cSFunObject.P3_RTP3COEFF[0] = 0.0168187966968575;
  Hd.cSFunObject.P4_RTP_COEFF3_BOOL[0] = true;
  Hd.cSFunObject.P3_RTP3COEFF[1] = 0.0148524151445501;
  Hd.cSFunObject.P4_RTP_COEFF3_BOOL[1] = true;
  Hd.cSFunObject.P3_RTP3COEFF[2] = 0.0;
  Hd.cSFunObject.P4_RTP_COEFF3_BOOL[2] = false;
  Hd.matlabCodegenIsDeleted = false;
  /* System object Initialization function: dsp.BiquadFilter */
  Hd.cSFunObject.W0_FILT_STATES[0] = 0.0;
  Hd.cSFunObject.W0_FILT_STATES[1] = 0.0;
  Hd.cSFunObject.W0_FILT_STATES[2] = 0.0;
  Hd.cSFunObject.W0_FILT_STATES[3] = 0.0;
  Hd.cSFunObject.W1_PreviousNumChannels = -1;
  isInitialized_skFilter = true;
}

/*
 * File trailer for skFilter_initialize.c
 *
 * [EOF]
 */
