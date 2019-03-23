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
#depth = 5*floor(depth/5);
depth = double(depth)/(255*4) + 0.25;

#imshow(depth);
#figure;

l_depth_scaling = depth.*double(repmat([flip(0:(height - eye_displacement - 1)) 0:(eye_displacement - 1)],width,1));
r_depth_scaling = depth.*double(repmat([flip(0:(eye_displacement - 1)) 0:(height - eye_displacement - 1)],width,1));

#Let's say at most we want a pixel to displace by is 2x(distancexdepth product):
l_depth_scaling = l_depth_scaling / max(max(l_depth_scaling)) + 1;
r_depth_scaling = r_depth_scaling / max(max(r_depth_scaling)) + 1;

#{
subplot(121);
imshow(l_depth_scaling - 1);
subplot(122);
imshow(r_depth_scaling - 1);
#}

left = zeros(width,2*height);
right = zeros(width,2*height);

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

		if(j < eye_displacement - 1)
			orientation = -1;
		else
			orientation = 1;
		endif

		new_height = j + orientation*depth*abs(j - eye_displacement);
		right(i,abs(floor(new_height)) + 1) = val;
	endfor
endfor

subplot(121);
imshow(mat2gray(left));
subplot(122);
imshow(mat2gray(right));

imwrite(mat2gray(right),'right.jpg');
imwrite(mat2gray(left),'left.jpg');


#{
left_screen = zeros(width,p_density*f*tan(theta));
right_screen = zeros(width,p_density*f*tan(theta));

left_screen = [screen left_screen];
right_screen = [right_screen screen];

subplot(241);
imshow(screen);
subplot(245);
imshow(left_screen);
subplot(248);
imshow(right_screen);

imwrite(left_screen,'left.jpg');
imwrite(right_screen,'right.jpg');

width_adjusted = floor(width/cos(theta))
cols_alloc = width_adjusted - width;
#imshow(screen);

left_screen = zeros(2*width,height);

horizontalAllocation = floor(1e5*normpdf(1:width,0,200));
#horizontalAllocation = 90*horizontalAllocation/sum(horizontalAllocation);

epsilon = 0;
i = 1;
do
	epsilon = sum(nonzeros(horizontalAllocation))/(size(nonzeros(horizontalAllocation))(1));
	horizontalAllocation(horizontalAllocation < epsilon) = 0;
	horizontalAllocation = 90*horizontalAllocation/sum(horizontalAllocation);
	i = i + 1;
	if(i == 10000)
		#plot(horizontalAllocation);
		#horizontalAllocation
	endif
until(all(nonzeros(horizontalAllocation) > 1))


plot(horizontalAllocation);

ugh = screen(1:width,1:(height/3));
ugh2 = imresize(ugh,3);
imshow(ugh,[],'XData',[0 0.5],'YData',[0 .1]);
#}

while 1
endwhile
