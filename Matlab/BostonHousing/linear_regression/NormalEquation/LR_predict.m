function [y] = LR_predict(x, w)

[row, column] = size(x);

x_0 = ones(row, 1);

x_fix = [x_0, x];

y = x_fix * w;

end