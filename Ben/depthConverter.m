pkg load optim;
pkg load image;

screen = rgb2gray(imread('Cubic_Structure.jpg'));
screen = imresize(screen,0.1);
#To adjust "correctly" we need two parameters, thetha (the angle apart from eyes)
#and the focal distance (how far back the eyes are)
theta = pi/6;
f = 2;

#We need a pixel density parameter, I don't know this for sure, but let's assume:
p_density = 75;

width = size(screen)(1);
height = size(screen)(2);

eye_displacement = floor(p_density*f*tan(theta));

depth = imread('Cubic_Depth.jpg');
depth = imresize(depth,0.1);
#Quantize the depth information:
depth = double(depth)/(255*4) + 0.25;

l_depth_scaling = depth.*double(repmat([flip(0:(height - eye_displacement - 1)) 0:(eye_displacement - 1)],width,1));
r_depth_scaling = depth.*double(repmat([flip(0:(eye_displacement - 1)) 0:(height - eye_displacement - 1)],width,1));

#Let's say at most we want a pixel to displace by is 2x(distancexdepth product):
l_depth_scaling = l_depth_scaling / max(max(l_depth_scaling)) + 1;
r_depth_scaling = r_depth_scaling / max(max(r_depth_scaling)) + 1;

left = zeros(width,2.5*height);
right = zeros(width,2.5*height);

size(left)

orientation = 0;

for i = 1:width
	for j = 1:height
		#Left Image Loop:
		val = screen(i,j);
		depth = l_depth_scaling(i,j);

		if(j < height - eye_displacement - 1)
			orientation = -1;
		else
			orientation = 1;
		endif
		
		new_height = j + height + orientation*depth*abs(height - eye_displacement - j);
		left(i,abs(floor(new_height)) + 1) = val;
		
		#Right Image Loop:
		depth = r_depth_scaling(i,j);

		if(j < eye_displacement + 1)
			orientation = -1;
		else
			orientation = 1;
		endif

		new_height = j + orientation*depth*abs(j - eye_displacement);
		right(i,abs(floor(new_height)) + 1) = val;
	endfor
endfor

abs(floor(new_height)) + 1

threshold = 40;
for k = 1:2
for i = 1:width
	for j = 2:(2.5*height - 1)
		if(right(i,j) < threshold)
			right(i,j) = (right(i,j - 1) + right(i,j + 1))/2;
		endif

		if(left(i,j) < threshold)
			left(i,j) = (left(i,j - 1) + left(i,j + 1))/2;
		endif
	endfor
endfor
endfor

#size(left)
#height
#{
subplot(121);
imshow(mat2gray(left));
subplot(122);
imshow(mat2gray(right));
#}
imwrite(mat2gray(right),'right.jpg');
imwrite(mat2gray(left),'left.jpg');

while 1
endwhile
