// nanoKONTROL2 -> ETC Eos : potards en mode relatif (comme des encodeurs).
// Charge dans le module MIDI de Chataigne. Le reste (faders, boutons, banque de faders) est dans les States.
// Multiplicateur = crans de roue Eos par cran de potard (negatif = sens inverse).
var INTENS = 1;                      // CC16 - potard 1
var PAN_WIDE = 10, PAN_FINE = 1;     // CC17, CC18 - potards 2 et 3
var TILT_WIDE = 5, TILT_FINE = 1;    // CC19, CC20 - potards 4 et 5
var ZOOM = 3;                        // CC21 - potard 6

var lastIntens = -1, lastPanWide = -1, lastPanFine = -1;
var lastTiltWide = -1, lastTiltFine = -1, lastZoom = -1;

function step(last, value) {
  return (last >= 0) ? value - last : 0;   // premier mouvement = reference, rien n'est envoye
}

function wheel(address, ticks) {
  if (ticks != 0) root.modules.osc.send(address, ticks);
}

function ccEvent(channel, number, value) {
  if (number == 16) {
    wheel("/eos/wheel/level", step(lastIntens, value) * INTENS);
    lastIntens = value;
  } else if (number == 17) {
    wheel("/eos/wheel/coarse/pan", step(lastPanWide, value) * PAN_WIDE);
    lastPanWide = value;
  } else if (number == 18) {
    wheel("/eos/wheel/coarse/pan", step(lastPanFine, value) * PAN_FINE);
    lastPanFine = value;
  } else if (number == 19) {
    wheel("/eos/wheel/coarse/tilt", step(lastTiltWide, value) * TILT_WIDE);
    lastTiltWide = value;
  } else if (number == 20) {
    wheel("/eos/wheel/coarse/tilt", step(lastTiltFine, value) * TILT_FINE);
    lastTiltFine = value;
  } else if (number == 21) {
    wheel("/eos/wheel/coarse/zoom", step(lastZoom, value) * ZOOM);
    lastZoom = value;
  }
}
