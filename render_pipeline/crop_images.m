function crop_images_modified(src_folder, dst_folder,image_size)


image_files = rdir(fullfile(src_folder,'*.png'));
image_num = length(image_files);
fprintf('%d images in total.\n', image_num);
if image_num == 0
    return;
end
rng('shuffle');

fprintf('Start croping at time %s...it takes for a while!!\n', datestr(now, 'HH:MM:SS'));
report_num = 80;
fprintf([repmat('.',1,report_num) '\n\n']);
report_step = floor((image_num+report_num-1)/report_num);
t_begin = clock;
for i = 1:image_num
    src_image_file = image_files(i).name;
    try
        [I, ~, alpha] = imread(src_image_file);  
    catch
        fprintf('Failed to read %s\n', src_image_file);
    end

    fprintf('%d before crop.\n', size(alpha));
    [alpha, top, bottom, left, right] = crop_gray(alpha, 0);
    
    I = I(top:bottom, left:right, :);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    [r, c, ~] = size(I);

    if r > c
        I_resized = imresize(I, [image_size, image_size*c / r]);
        alpha_resized = imresize(alpha, [image_size, image_size*c / r]);
        pad_left = mean(I(:, 1, :));
        pad_right = mean(I(:, c, :));
        diff_l = floor((image_size - (image_size*c / r)) / 2);
        diff_r = ceil((image_size - (image_size*c / r)) / 2);
        pad_l = repmat(pad_left, image_size, diff_l);
        pad_r = repmat(pad_left, image_size, diff_r);
        pad_a_l = zeros(image_size,diff_l)
        pad_a_r = zeros(image_size,diff_r)
        %pad_a_l = ones(image_size,diff_l)*255;
        %pad_a_r = ones(image_size,diff_r)*255;
        I_pad = cat(2, pad_l, I_resized, pad_r);
        alpha_pad = cat(2, pad_a_l, alpha_resized, pad_a_r);
    elseif c > r
        I_resized = imresize(I, [image_size*r / c, image_size]);
        alpha_resized = imresize(alpha, [image_size*r / c,image_size]);
        pad_up = mean(I(1, :, :));
        pad_down = mean(I(r, :, :));
        diff_u = floor((image_size - (image_size*r / c)) / 2);
        diff_d = ceil((image_size - (image_size*r / c)) / 2);
        pad_u = repmat(pad_up, diff_u, image_size);
        pad_d = repmat(pad_down, diff_d, image_size);
        pad_a_u = zeros(diff_u, image_size);
        pad_a_d = zeros(diff_d, image_size);
        %pad_a_u = ones(diff_u, image_size)*255;
        %pad_a_d = ones(diff_d, image_size)*255;
        I_pad = cat(1, pad_u, I_resized, pad_d);
        alpha_pad = cat(1, pad_a_u, alpha_resized, pad_a_d);
    else
        I_pad = imresize(I, [image_size,image_size]);
        alpha_pad = imresize(alpha, [image_size,image_size]);
    end
    I_pad = imresize(I_pad, [image_size,image_size]);
    alpha_pad = imresize(alpha_pad, [image_size,image_size]);
    I = I_pad;
    alpha=alpha_pad;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    if numel(I) == 0
        fprintf('Failed to crop %s (empty image after crop)\n', src_image_file);
    else
        dst_image_file = strrep(src_image_file, src_folder, dst_folder);
        fprintf('Name of file %s\n', dst_image_file)
        [dst_image_file_folder, ~, ~] = fileparts(dst_image_file);
        if ~exist(dst_image_file_folder, 'dir')
            mkdir(dst_image_file_folder);
        end
        imwrite(I, dst_image_file, 'png', 'Alpha', alpha);
    end
    
    if mod(i, report_step) == 0
        fprintf('\b|\n');
    end
end      
t_end = clock;
fprintf('%f seconds spent on cropping!\n', etime(t_end, t_begin));
end