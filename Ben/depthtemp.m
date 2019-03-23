pkg load optim;
pkg load image;

depth = imread('Cubic_Depth.jpg');
#Quantize the depth information:
depth = 5*floor(depth/5);



imshow(depth);
#plot(range(depth))

while 1
endwhile
