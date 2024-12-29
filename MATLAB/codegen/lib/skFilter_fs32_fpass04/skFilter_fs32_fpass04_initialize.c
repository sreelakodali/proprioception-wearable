/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: skFilter_fs32_fpass04_initialize.c
 *
 * MATLAB Coder version            : 5.5
 * C/C++ source code generated on  : 28-Dec-2024 05:54:40
 */

/* Include Files */
#include "skFilter_fs32_fpass04_initialize.h"
#include "skFilter_fs32_fpass04.h"
#include "skFilter_fs32_fpass04_data.h"
#include "skFilter_fs32_fpass04_types.h"

/* Function Definitions */
/*
 * Arguments    : void
 * Return Type  : void
 */
void skFilter_fs32_fpass04_initialize(void)
{
  static const signed char iv[6] = {1, 2, 1, 1, 2, 1};
  int i;
  skFilter_fs32_fpass04_init();
  /*  The following code was used to design the filter coefficients: */
  /*  */
  /*  Fpass = 0.4;      % Passband Frequency */
  /*  Fstop = 6;        % Stopband Frequency */
  /*  Apass = 1;        % Passband Ripple (dB) */
  /*  Astop = 80;       % Stopband Attenuation (dB) */
  /*  Fs    = 32.1761;  % Sampling Frequency */
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
  Hd.cSFunObject.P2_RTP2COEFF[0] = -1.92349207F;
  Hd.cSFunObject.P2_RTP2COEFF[1] = 0.931744F;
  Hd.cSFunObject.P2_RTP2COEFF[2] = -1.83493042F;
  Hd.cSFunObject.P2_RTP2COEFF[3] = 0.842802346F;
  Hd.cSFunObject.P3_RTP3COEFF[0] = 0.00206296565F;
  Hd.cSFunObject.P4_RTP_COEFF3_BOOL[0] = true;
  Hd.cSFunObject.P3_RTP3COEFF[1] = 0.00196798239F;
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
  isInitialized_skFilter_fs32_fpass04 = true;
}

/*
 * File trailer for skFilter_fs32_fpass04_initialize.c
 *
 * [EOF]
 */
