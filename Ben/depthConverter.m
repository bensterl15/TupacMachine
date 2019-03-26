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

left = NaN(width,2.5*height);
right = NaN(width,2.5*height);

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

#Fill up the NaN spaces by averaging:
#has_nan = 1;
function im = filterImage(im,width,height)
	threshold = 30;
	while sum(sum(isnan(im))) > 2*width
		for i = 1:width
			for j = 2:(2.5*height - 1)
				if(isnan(im(i,j)))
					if(~isnan(im(i,j - 1)) && ~isnan(im(i,j + 1)))
						im(i,j) = (im(i,j - 1) + im(i,j + 1))/2;
					elseif(~isnan(im(i,j - 1)))
						im(i,j) = im(i,j - 1);
					elseif(~isnan(im(i,j + 1)))
						im(i,j) = im(i,j + 1);
					endif
				elseif(im(i,j) < threshold)
					im(i,j) = (im(i,j - 1) + im(i,j + 1))/2;
				endif
			endfor
		endfor
		
		for i = flip(1:width)
			for j = flip(2:(2.5*height - 1))
				if(isnan(im(i,j)))
					if(~isnan(im(i,j - 1) && ~isnan(im(i,j + 1))))
						im(i,j) = (im(i,j - 1) + im(i,j + 1))/2;
					elseif(~isnan(im(i,j - 1)))
						im(i,j) = im(i,j - 1);
					elseif(~isnan(im(i,j + 1)))
						im(i,j) = im(i,j + 1);
					endif
				endif
			endfor
		endfor
	endwhile
	im = imsmooth(im,'gaussian',2);
endfunction

left = filterImage(left,width,height);
right = filterImage(right,width,height);

left = imresize(left,[width,height]);
right = imresize(right,[width,height]);

#left = imsmooth(left,'gaussian',1.5);
#right = imsmooth(right,'gaussian',1.5);

imwrite(mat2gray(right),'right.jpg');
imwrite(mat2gray(left),'left.jpg');
