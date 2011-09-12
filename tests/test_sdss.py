import pyspeckit

# Rest wavelengths of the lines we are fitting - use as initial guesses
NIIa = 6549.86
NIIb = 6585.27
Halpha = 6564.614
SIIa = 6718.29
SIIb = 6732.68

# Initialize spectrum object and plot region surrounding Halpha-[NII] complex
spec = pyspeckit.Spectrum('sample_sdss.txt', errorcol=2)
spec.plotter(xmin = 6450, xmax = 6775, ymin = 0, ymax = 150)

# Use [SII] lines to model narrow lines, then force [NII] lines and narrow H-alpha to have same width as [SII].  
# Will fit 1 additional broad component to H-alpha (standard for AGN spectra)
# Wavelengths are all tied together
guesses = [50, NIIa, 5, 100, Halpha, 5, 50, Halpha, 50, 50, NIIb, 5, 20, SIIa, 5, 20, SIIb, 5]
tied = ['', '', 'p[17]', '', '', 'p[17]', '', 'p[4]', '', '3 * p[0]', '', 'p[17]', '', '', 'p[17]', '', '', '']

# Actually do the fit.
spec.specfit(guesses = guesses, tied = tied, annotate = False)
spec.plotter.refresh()

# Let's use the measurements class to derive information about the emission lines.
spec.measure(z = 0.05, fluxnorm = 1e-17)

# Now overplot positions of lines and annotate
y = spec.plotter.ymax * 0.85
for i, line in enumerate(spec.measurements.lines.keys()):
    x = spec.measurements.lines[line]['modelpars'][1]
    spec.plotter.axis.plot([x]*2, [spec.plotter.ymin, spec.plotter.ymax], ls = '--', color = 'k')
    try: spec.plotter.axis.annotate(spec.speclines.optical.lines[line][-1], 
        (x, y), rotation = 90, ha = 'right', va = 'center')
    except KeyError: pass

# Make some nice axis labels
spec.plotter.axis.set_xlabel(r'Wavelength $(\AA)$')
spec.plotter.axis.set_ylabel(r'Flux $(10^{-17} \mathrm{erg/s/cm^2/\AA})$')
spec.plotter.refresh()

# Print out spectral line information
print "Line   Flux (erg/s/cm^2)     Amplitude (erg/s/cm^2)    FWHM (Angstrom)   Luminosity (erg/s)"
for line in spec.measurements.lines.keys():
    print line, spec.measurements.lines[line]['flux'], spec.measurements.lines[line]['amp'], spec.measurements.lines[line]['fwhm'], \
        spec.measurements.lines[line]['lum']
        
# Notice that because we supplied the objects redshift and flux normalization, the measurements class
# automatically calculated line luminosities.  Also, it separates the broad and narrow H-alpha components, and identifies which lines are which. How nice!

raw_input("Done.")

spec.specfit.plot_fit()

raw_input("Done (again).")

# Save the figure
spec.plotter.figure.savefig("sdss_fit_example.png")
