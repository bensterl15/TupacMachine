pkg load optim;

lambda = 0.633*10^-6; % wavelength, unit: m
delta = 10*lambda; % sampling period, unit: m
z = 0.06; % propagation distance; m
M0 = 512; % object size
c = 1:M0;
r = 1:M0;

[C, R] = meshgrid(c, r);
THOR = ((R-M0/2-1).^2 + (C-M0/2-1).^2).^0.5;
A = THOR.*delta;
OB = zeros(M0); % object pattern
OB(193:321,53:181) = 1;
Q1 = exp(-1i*pi/lambda/z.*(A.^2));
FTS = fftshift(ifft2(fftshift(OB.*Q1)));	#Fresnel diffraction
AFD = abs(FTS);
AFD = AFD/max(max(AFD));
figure; imshow(OB);
title('Rectangular aperture');
figure; imshow(AFD);
title('Modulus of the Fresnel diffraction pattern');

while 1
endwhile
