function [I, top, bottom, left, right] = crop_gray(I, bgColor)

% get boundaries of object
[nr, nc] = size(I);
colsum = sum(I == bgColor, 1) ~= nr;
rowsum = sum(I == bgColor, 2) ~= nc;

left = find(colsum, 1, 'first');
left = max([0,left-3])
if left == 0
    left = 1;
end
right = find(colsum, 1, 'last');
right = min([nc,right+3])
if right == 0
    right = length(colsum);
end
top = find(rowsum, 1, 'first');
top = max([0,top-3])
if top == 0
    top = 1;
end
bottom = find(rowsum, 1, 'last');
bottom = min([nc,bottom+3])
if bottom == 0
    bottom = length(rowsum);
end
width = right - left + 1;
height = bottom - top + 1;

% strecth
dx1 = 0.80+rand()*0.4
dx2 = 0.80+rand()*0.4
dy1 = 0.80+rand()*0.4
dy2 = 0.80+rand()*0.4

leftnew = max([1, left + dx1]);
leftnew = min([leftnew, nc]);
rightnew = max([1, right + dx2]);
rightnew = min([rightnew, nc]);
if leftnew > rightnew
    leftnew = left;
    rightnew = right;
end

topnew = max([1, top + dy1]);
topnew = min([topnew, nr]);
bottomnew = max([1, bottom + dy2]);
bottomnew = min([bottomnew, nr]);
if topnew > bottomnew
    topnew = top;
    bottomnew = bottom;
end

left = round(leftnew); right = round(rightnew);
top = round(topnew); bottom = round(bottomnew);
I = I(top:bottom, left:right, :);