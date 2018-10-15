pkg load optim;
pkg load image;

original = imread("SampleText.png");
#Take the green information:
original = original(:,:,2);

#Zero pad to get to 256x256:
original = [original;zeros(256 - size(original)(1),size(original)(2))];
original = [original zeros(size(original)(1),256 - size(original)(2))];

imshow(original);

M = 256;

original = double(original);
PH = rand([256,256]);
I = original.*exp(2i*pi*PH); # add a random phase on the object

z = 5; #Units in cm
w = 6500*10^-8;
delta = 0.005;
r = 1:M;
c = 1:M;
[C,R] = meshgrid(c,r);

# Forward propagation (650nm)
p = exp(-2i*pi*z.*((1/w)^2-(1/M/delta)^2.*(C-M/2-1).^2-(1/M/delta)^2.*(R-M/2-1).^2).^0.5);
A0 = fftshift(ifft2(fftshift(I)));
Az = A0.*p;
E = fftshift(fft2(fftshift(Az))); % 1st order of the hologram

# Reconstruction (650nm)
p = exp(-2i*pi*(-z).*((1/w)^2-(1/M/delta)^2.*(C-M/2-1).^2-(1/M/delta)^2.*(R-M/2-1).^2).^0.5);
A1 = fftshift(ifft2(fftshift(E)));
Az1 = A1.*p;
R1 = fftshift(fft2(fftshift(Az1)));
R1 = (abs(R1)).^2;
figure;

#imshow(R1/max(max(R1)));

# Reconstruction (450nm~650nm)
dw = 50;
IMA = zeros(256,256);

for g = 0:40;
	w2 = (6500-dw*g)*10^-8; # reconstruction wavelength
	E2 = E.*exp(2i*pi*sind(10)*(w-w2)/w/w2.*R*delta);
	# phase mismatch due to the wavelength shift
	p = exp(-2i*pi*(-z).*((1/w2)^2-(1/M/delta)^2.*(C-M/2-1).^2-(1/M/delta)^2.*(R-M/2-1).^2).^0.5);

	Az2 = ifft2(fftshift(E2)).*(fftshift(p));
	R2 = fftshift(fft2(Az2));
	R2 = (abs(R2)).^2; # summation of all wavelengths
	IMA = IMA + R2;
endfor

IMA = IMA/max(max(IMA));
imshow(IMA);
imwrite(IMA,"5cm.png");

while 1
endwhile
